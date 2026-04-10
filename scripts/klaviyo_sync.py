"""
Klaviyo → Skullette Workspace Sync Script
==========================================
Pulls email campaign content and performance metrics from Klaviyo API
and saves them as organized knowledge files in the workspace.

Usage:
    python scripts/klaviyo_sync.py              # Full sync (all campaigns)
    python scripts/klaviyo_sync.py --since 2025-01-01   # Only campaigns after date
    python scripts/klaviyo_sync.py --incremental        # Only new since last sync
    python scripts/klaviyo_sync.py --enrich             # Enrich metadata with subject lines
    python scripts/klaviyo_sync.py --extract-content    # Extract campaigns to .md files

Requires:
    pip install requests python-dotenv beautifulsoup4
    .env file with KLAVIYO_API_KEY=pk_xxxxx
"""

import os
import sys
import json
import re
import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package not installed. Run: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: 'python-dotenv' package not installed. Run: pip install python-dotenv")
    sys.exit(1)

# ─── Configuration ───────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "klaviyo"
CAMPAIGNS_DIR = OUTPUT_DIR / "campaigns"
CONTENT_DIR = OUTPUT_DIR / "content"
SYNC_LOG_FILE = OUTPUT_DIR / "sync_log.json"
SUMMARY_FILE = OUTPUT_DIR / "summary.md"
ANALYSIS_FILE = OUTPUT_DIR / "content-analysis.json"

BASE_URL = "https://a.klaviyo.com/api"
API_REVISION = "2024-10-15"

# Load .env from project root
load_dotenv(PROJECT_ROOT / ".env")
API_KEY = os.getenv("KLAVIYO_API_KEY", "")


def get_headers():
    """Build request headers for Klaviyo API."""
    return {
        "Authorization": f"Klaviyo-API-Key {API_KEY}",
        "revision": API_REVISION,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def sanitize_filename(name: str) -> str:
    """Convert a campaign name into a safe folder name."""
    # Remove or replace unsafe characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', '-', name.strip())
    name = re.sub(r'-+', '-', name)
    return name[:80]  # Limit length


# ─── API Helpers ─────────────────────────────────────────────────────────────

def api_get(endpoint: str, params: dict = None) -> dict:
    """Make a GET request to Klaviyo API."""
    url = f"{BASE_URL}/{endpoint}" if not endpoint.startswith("http") else endpoint
    resp = requests.get(url, headers=get_headers(), params=params)
    resp.raise_for_status()
    return resp.json()


def api_post(endpoint: str, payload: dict) -> dict:
    """Make a POST request to Klaviyo API."""
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, headers=get_headers(), json=payload)
    if not resp.ok:
        print(f"  API POST Error {resp.status_code}: {resp.text[:500]}")
    resp.raise_for_status()
    return resp.json()


def fetch_all_pages(endpoint: str, params: dict = None) -> list:
    """Fetch all pages of a paginated Klaviyo API response."""
    all_data = []
    url = f"{BASE_URL}/{endpoint}"
    
    while url:
        resp = requests.get(url, headers=get_headers(), params=params)
        if not resp.ok:
            print(f"  API Error {resp.status_code}: {resp.text[:500]}")
            resp.raise_for_status()
        body = resp.json()
        all_data.extend(body.get("data", []))
        
        # After first request, params are included in the next URL
        params = None
        url = body.get("links", {}).get("next", None)
        
        print(f"  Fetched {len(all_data)} campaigns so far...")
    
    return all_data


# ─── Core Functions ──────────────────────────────────────────────────────────

def fetch_campaigns(since_date: str = None) -> list:
    """Fetch all sent email campaigns, optionally filtered by date."""
    print("\n[*] Fetching email campaigns from Klaviyo...")
    
    filter_parts = ["equals(messages.channel,'email')"]
    if since_date:
        filter_parts.append(f"greater-or-equal(send_time,{since_date}T00:00:00+00:00)")
    
    filter_str = filter_parts[0] if len(filter_parts) == 1 else f"and({','.join(filter_parts)})"
    
    params = {
        "filter": filter_str,
        "include": "campaign-messages",
    }
    
    campaigns = fetch_all_pages("campaigns", params)
    
    # Filter to only sent campaigns
    sent_campaigns = [c for c in campaigns if c.get("attributes", {}).get("status") == "Sent"]
    print(f"  Found {len(sent_campaigns)} sent email campaigns (of {len(campaigns)} total)")
    
    return sent_campaigns


def fetch_campaign_messages(campaign: dict) -> list:
    """Get message IDs from a campaign's relationships."""
    messages = campaign.get("relationships", {}).get("campaign-messages", {}).get("data", [])
    return [m["id"] for m in messages]


def fetch_template_html(message_id: str) -> str | None:
    """Fetch the HTML content of a campaign message's template."""
    try:
        resp = api_get(f"campaign-messages/{message_id}/template")
        html = resp.get("data", {}).get("attributes", {}).get("html", "")
        return html if html else None
    except requests.HTTPError as e:
        print(f"    [!] Could not fetch template for message {message_id}: {e}")
        return None


def fetch_conversion_metric_id() -> str:
    """Auto-detect the 'Placed Order' metric ID from Klaviyo."""
    try:
        resp = api_get("metrics")
        for metric in resp.get("data", []):
            name = metric.get("attributes", {}).get("name", "")
            if "placed order" in name.lower():
                metric_id = metric.get("id", "")
                print(f"  Found conversion metric: '{name}' ({metric_id})")
                return metric_id
        # Fallback: just use the first metric
        first = resp.get("data", [{}])[0]
        metric_id = first.get("id", "")
        print(f"  Using fallback metric: '{first.get('attributes', {}).get('name', '?')}' ({metric_id})")
        return metric_id
    except Exception as e:
        print(f"  [!] Could not fetch metrics: {e}")
        return ""


def api_post_with_retry(endpoint: str, payload: dict, max_retries: int = 3) -> dict:
    """POST with automatic retry on 429 rate limit errors."""
    for attempt in range(max_retries):
        url = f"{BASE_URL}/{endpoint}"
        resp = requests.post(url, headers=get_headers(), json=payload)
        if resp.status_code == 429:
            # Rate limited — parse retry-after or default backoff
            retry_after = int(resp.headers.get("Retry-After", 2 * (attempt + 1)))
            print(f"  Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
            continue
        if not resp.ok:
            print(f"  API POST Error {resp.status_code}: {resp.text[:500]}")
        resp.raise_for_status()
        return resp.json()
    # Final attempt without retry
    resp.raise_for_status()
    return resp.json()


def fetch_campaign_metrics(campaign_ids: list) -> dict:
    """Fetch performance metrics for a batch of campaigns via Reporting API."""
    if not campaign_ids:
        return {}
    
    print(f"\n[*] Fetching metrics for {len(campaign_ids)} campaigns...")
    
    # Get conversion metric ID (required by API)
    conversion_metric_id = fetch_conversion_metric_id()
    if not conversion_metric_id:
        print("  [!] Skipping metrics — no conversion metric found")
        return {}
    
    all_results = {}
    
    # Process in batches of 100
    for i in range(0, len(campaign_ids), 100):
        batch = campaign_ids[i:i + 100]
        
        # Build filter string
        if len(batch) > 1:
            ids_joined = "','".join(batch)
            filter_str = f"in(campaign_id,['{ids_joined}'])"
        else:
            filter_str = f"equals(campaign_id,'{batch[0]}')"
        
        payload = {
            "data": {
                "type": "campaign-values-report",
                "attributes": {
                    "timeframe": {
                        "key": "last_365_days"
                    },
                    "conversion_metric_id": conversion_metric_id,
                    "filter": filter_str,
                    "statistics": [
                        "recipients",
                        "opens",
                        "open_rate",
                        "clicks",
                        "click_rate",
                        "unsubscribes",
                        "unsubscribe_rate",
                        "bounce_rate",
                    ],
                }
            }
        }
        
        try:
            resp = api_post_with_retry("campaign-values-reports", payload)
            results = resp.get("data", {}).get("attributes", {}).get("results", [])
            for result in results:
                cid = result.get("groupings", {}).get("campaign_id", "")
                if cid:
                    stats = result.get("statistics", {})
                    all_results[cid] = stats
        except requests.HTTPError as e:
            print(f"  [!] Metrics batch error: {e}")
            # Try individual fallback with delay
            for cid in batch:
                try:
                    time.sleep(1)  # Rate limit safety
                    single_payload = {
                        "data": {
                            "type": "campaign-values-report",
                            "attributes": {
                                "timeframe": {"key": "last_365_days"},
                                "conversion_metric_id": conversion_metric_id,
                                "filter": f"equals(campaign_id,'{cid}')",
                                "statistics": [
                                    "recipients", "opens", "open_rate",
                                    "clicks", "click_rate",
                                    "bounce_rate",
                                ],
                            }
                        }
                    }
                    resp = api_post_with_retry("campaign-values-reports", single_payload)
                    results = resp.get("data", {}).get("attributes", {}).get("results", [])
                    if results:
                        all_results[cid] = results[0].get("statistics", {})
                except Exception:
                    pass
    
    print(f"  Got metrics for {len(all_results)} campaigns")
    return all_results


def save_campaign(campaign: dict, html_content: str | None, metrics: dict, folder: Path):
    """Save a single campaign's data to disk."""
    folder.mkdir(parents=True, exist_ok=True)
    
    attrs = campaign.get("attributes", {})
    
    # Save metadata
    metadata = {
        "id": campaign.get("id"),
        "name": attrs.get("name"),
        "status": attrs.get("status"),
        "send_time": attrs.get("send_time"),
        "created_at": attrs.get("created_at"),
        "updated_at": attrs.get("updated_at"),
        "archived": attrs.get("archived"),
        "send_strategy": attrs.get("send_strategy"),
    }
    
    with open(folder / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Save HTML
    if html_content:
        with open(folder / "email.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    # Save metrics
    if metrics:
        with open(folder / "metrics.json", "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)


def generate_summary(campaigns_data: list):
    """Generate a human-readable markdown summary of all campaigns."""
    print("\n[*] Generating summary.md...")
    
    lines = [
        "# Skullette Email Campaigns — Klaviyo Data",
        "",
        f"*Last synced: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        f"**Total campaigns:** {len(campaigns_data)}",
        "",
        "---",
        "",
        "## Campaign Performance Overview",
        "",
        "| Date | Campaign Name | Recipients | Opens | Open Rate | Clicks | Click Rate |",
        "|------|--------------|-----------|-------|-----------|--------|------------|",
    ]
    
    for item in campaigns_data:
        name = item.get("name", "Unknown")
        send_time = item.get("send_time", "")
        date_str = send_time[:10] if send_time else "N/A"
        m = item.get("metrics", {})
        
        recipients = m.get("recipients", "-")
        opens = m.get("opens", "-")
        open_rate = f"{m['open_rate']:.1%}" if isinstance(m.get("open_rate"), (int, float)) else "-"
        clicks = m.get("clicks", "-")
        click_rate = f"{m['click_rate']:.1%}" if isinstance(m.get("click_rate"), (int, float)) else "-"
        
        lines.append(f"| {date_str} | {name} | {recipients} | {opens} | {open_rate} | {clicks} | {click_rate} |")
    
    lines.extend([
        "",
        "---",
        "",
        "## Top Performers by Open Rate",
        "",
    ])
    
    # Sort by open rate for top performers
    with_rates = [c for c in campaigns_data if isinstance(c.get("metrics", {}).get("open_rate"), (int, float))]
    top_opens = sorted(with_rates, key=lambda x: x["metrics"]["open_rate"], reverse=True)[:10]
    
    for i, item in enumerate(top_opens, 1):
        m = item["metrics"]
        lines.append(f"{i}. **{item['name']}** - {m['open_rate']:.1%} open rate ({m.get('recipients', '?')} recipients)")
    
    lines.extend(["", "## Top Performers by Click Rate", ""])
    
    top_clicks = sorted(with_rates, key=lambda x: x["metrics"].get("click_rate", 0), reverse=True)[:10]
    
    for i, item in enumerate(top_clicks, 1):
        m = item["metrics"]
        lines.append(f"{i}. **{item['name']}** - {m.get('click_rate', 0):.1%} click rate ({m.get('clicks', '?')} clicks)")
    
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"  Saved to {SUMMARY_FILE}")


def save_sync_log(campaign_count: int, since_date: str = None):
    """Save a sync log for incremental updates."""
    log = {
        "last_sync": datetime.now(timezone.utc).isoformat(),
        "campaigns_synced": campaign_count,
        "since_date": since_date,
    }
    
    # Merge with existing log
    if SYNC_LOG_FILE.exists():
        with open(SYNC_LOG_FILE, "r") as f:
            existing = json.load(f)
        log["sync_history"] = existing.get("sync_history", [])
        log["sync_history"].append({
            "date": log["last_sync"],
            "count": campaign_count,
        })
    else:
        log["sync_history"] = [{"date": log["last_sync"], "count": campaign_count}]
    
    with open(SYNC_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


# ─── Enrich & Extract ───────────────────────────────────────────────────────

def enrich_metadata(limit: int = None):
    """Enrich existing metadata.json files with subject lines and preview text."""
    print("\n[*] Enriching metadata with subject lines...")

    quarter_dirs = sorted(CAMPAIGNS_DIR.iterdir())
    count = 0
    enriched = 0

    for qdir in quarter_dirs:
        if not qdir.is_dir():
            continue
        for campaign_dir in sorted(qdir.iterdir()):
            if not campaign_dir.is_dir():
                continue
            meta_file = campaign_dir / "metadata.json"
            if not meta_file.exists():
                continue

            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)

            # Skip if already enriched
            if meta.get("subject") is not None:
                count += 1
                continue

            campaign_id = meta.get("id", "")
            if not campaign_id:
                count += 1
                continue

            # Fetch campaign messages to get subject/preview
            try:
                resp = api_get(f"campaigns/{campaign_id}/campaign-messages")
                messages = resp.get("data", [])
                if messages:
                    msg_id = messages[0].get("id", "")
                    if msg_id:
                        msg_resp = api_get(f"campaign-messages/{msg_id}")
                        msg_attrs = msg_resp.get("data", {}).get("attributes", {}).get("content", {})
                        meta["subject"] = msg_attrs.get("subject", "")
                        meta["preview_text"] = msg_attrs.get("preview_text", "")

                        with open(meta_file, "w", encoding="utf-8") as f:
                            json.dump(meta, f, indent=2, ensure_ascii=False)
                        enriched += 1
                        print(f"  [{enriched}] {meta.get('name', '?')}: \"{meta['subject'][:60]}\"")
                time.sleep(0.4)  # Rate limiting
            except Exception as e:
                print(f"  [!] Error enriching {meta.get('name', '?')}: {e}")

            count += 1
            if limit and enriched >= limit:
                print(f"  Reached limit of {limit}")
                break
        if limit and enriched >= limit:
            break

    print(f"\n  [OK] Enriched {enriched} campaigns (of {count} total)")


# ─── Content Classification ─────────────────────────────────────────────────

# Phase detection keywords
PHASE_KEYWORDS = {
    "teaser": ["teaser", "coming soon", "register", "tease", "get ready", "announcement"],
    "sale": ["sale", "clearance", "% off", "day 1", "day 2", "day 3", "flash",
             "final 300", "weekend specials", "live now", "last call", "gamified"],
    "post": ["thank", "recap", "wrap-up", "results"],
}

# Story source detection — keywords in subject + body
STORY_SOURCE_KEYWORDS = {
    "Gothic Mundane": ["morning", "coffee", "kroger", "walmart", "grocery", "uber",
                       "kitchen", "routine", "midnight", "3 am", "everyday",
                       "parking lot", "checkout line"],
    "Witch Victory": ["review", "customer", "testimonial", "she said", "her words",
                      "5-star", "five star", "trust pilot", "ordered", "unboxing"],
    "Basic Brenda Encounter": ["brenda", "basic", "beige", "boring", "normie",
                               "coach bag", "michael kors", "they said", "concerned aunt"],
    "Product Origin": ["designed", "leather", "handmade", "crafted", "new collection",
                       "jade", "designer", "workshop", "buckle", "hardware", "material"],
    "Cultural Darkness": ["halloween", "friday the 13th", "full moon", "mercury retrograde",
                          "solstice", "samhain", "día de los muertos", "goth", "dark romance",
                          "witchy", "pagan", "equinox", "bat", "skull"],
    "Julie Personal": ["my daughter", "my husband", "my mom", "family", "growing up",
                       "when i was", "confession", "personal", "i remember",
                       "childhood", "my life"],
    "Industry Commentary": ["fast fashion", "shein", "amazon", "industry", "sustainability",
                            "mass-produced", "disposable", "trend", "fashion week"],
}

# Hook type detection — first 5 lines of body
HOOK_KEYWORDS = {
    "quote_open": ['"', "'", "she said", "her exact words", "i quote"],
    "question": ["?"],
    "scene_setting": ["am", "pm", "o'clock", "morning", "night", "sitting", "standing",
                      "walking", "looking", "scrolling"],
    "direct_offer": ["% off", "sale", "deal", "save", "discount", "free shipping"],
    "mystery_statement": ["here's the thing", "confession", "i wasn't going to",
                          "don't tell", "secret"],
    "urgency": ["last chance", "ending", "final", "only", "hours left", "midnight"],
}

# Character detection
CHARACTER_KEYWORDS = {
    "Julie": ["julie", "i ", "my ", "love,"],  # Julie is always present as narrator
    "Alice": ["alice"],
    "Jade": ["jade"],
    "Basic Brenda": ["brenda", "basic brenda"],
    "The Witch": ["the witch", "witches", "coven"],
}

# Campaign series detection
SERIES_KEYWORDS = {
    "Skull-a-palooza": ["skull-a-palooza", "skullapalooza", "palooza"],
    "Small Bag Clearance": ["small bag clearance"],
    "Weekend Specials": ["weekend specials", "weekend special"],
    "Friday 13th": ["friday the 13th", "friday 13"],
    "Mothers Day": ["mother's day", "mothers day", "mom"],
    "Final 300": ["final 300"],
}

EMAIL_PILLAR_MAP = {
    "Gothic Mundane": ("1", "Gothic Infotainment"),
    "Witch Victory": ("3", "Coven Chronicles"),
    "Basic Brenda Encounter": ("4", "Darkness vs Beige"),
    "Product Origin": ("2", "Witch's Arsenal"),
    "Cultural Darkness": ("1", "Gothic Infotainment"),
    "Julie Personal": ("1", "Gothic Infotainment"),
    "Industry Commentary": ("4", "Darkness vs Beige"),
}


def html_to_text(html_content: str) -> tuple[str, list[str]]:
    """Convert HTML email to plain text, preserving paragraph structure. Returns (text, links)."""
    from bs4 import BeautifulSoup, NavigableString

    # Pre-clean: remove Klaviyo template tags
    cleaned = re.sub(r'\{%.*?%\}', '', html_content, flags=re.DOTALL)
    cleaned = re.sub(r'\{\{.*?\}\}', '', cleaned)

    soup = BeautifulSoup(cleaned, "html.parser")

    # Remove non-content tags
    for tag in soup(["style", "script", "head", "meta", "title", "noscript"]):
        tag.decompose()

    # Extract links before converting
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        text = a_tag.get_text(strip=True)
        if href and not href.startswith("#") and not href.startswith("mailto:"):
            if text and len(text) > 2 and text.lower() not in ("unsubscribe", "view in browser"):
                links.append(f"[{text}]({href})")

    # Find the main content area — look for kl-text divs (Klaviyo content blocks)
    content_divs = soup.find_all(class_=re.compile(r'kl-text'))

    if content_divs:
        # Use only kl-text content blocks (the actual email body)
        paragraphs = []
        for div in content_divs:
            for element in div.find_all(["p", "h1", "h2", "h3", "li"]):
                text = element.get_text(strip=True)
                if text and len(text) > 1:
                    paragraphs.append(text)
    else:
        # Fallback: extract from all p/div tags but skip navigation/footer
        paragraphs = []
        for element in soup.find_all(["p", "h1", "h2", "h3"]):
            text = element.get_text(strip=True)
            if text and len(text) > 1:
                paragraphs.append(text)

    # Deduplicate — remove exact duplicates while preserving order
    seen = set()
    deduped = []
    for p in paragraphs:
        if p not in seen:
            seen.add(p)
            deduped.append(p)

    # Remove footer/menu content (anything after sign-off patterns)
    body_parts = []
    for p in deduped:
        # Stop at footer markers
        p_lower = p.lower()
        if any(marker in p_lower for marker in [
            "post-email menu", "no longer want to receive",
            "need help?", "❓ need help", "unsubscribe",
            "organization.name", "leather handbags-",
        ]):
            break
        body_parts.append(p)

    body_text = "\n\n".join(body_parts)

    # Clean up artifacts
    body_text = re.sub(r'\n{3,}', '\n\n', body_text)
    body_text = body_text.strip()

    # Deduplicate links
    seen_links = set()
    unique_links = []
    for link in links:
        if link not in seen_links:
            seen_links.add(link)
            unique_links.append(link)

    return body_text, unique_links


def classify_phase(name: str, body_lower: str) -> str:
    """Classify campaign phase from name and body text."""
    name_lower = name.lower()
    # Check name first (more reliable)
    for phase, keywords in PHASE_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                return phase
    # Check body text
    for phase, keywords in PHASE_KEYWORDS.items():
        for kw in keywords:
            if kw in body_lower[:500]:  # First 500 chars
                return phase
    return "daily"


def classify_story_source(name: str, subject: str, body_lower: str) -> str:
    """Classify story source from campaign text."""
    combined = f"{name.lower()} {subject.lower()} {body_lower[:2000]}"
    scores = {}
    for source, keywords in STORY_SOURCE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > 0:
            scores[source] = score
    if scores:
        return max(scores, key=scores.get)
    return "Gothic Mundane"  # Default


def classify_hook_type(body_text: str) -> str:
    """Classify hook type from first 5 lines of body."""
    first_lines = "\n".join(body_text.split("\n")[:5]).lower()
    scores = {}
    for hook_type, keywords in HOOK_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in first_lines)
        if score > 0:
            scores[hook_type] = score
    if scores:
        return max(scores, key=scores.get)
    return "scene_setting"  # Default


def detect_characters(body_lower: str) -> list[str]:
    """Detect which characters appear in the email body."""
    found = []
    for char, keywords in CHARACTER_KEYWORDS.items():
        if char == "Julie":
            found.append("Julie")  # Julie is always narrator
            continue
        for kw in keywords:
            if kw in body_lower:
                found.append(char)
                break
    return found


def detect_series(name: str, body_lower: str) -> str:
    """Detect which campaign series this belongs to."""
    combined = f"{name.lower()} {body_lower[:500]}"
    for series, keywords in SERIES_KEYWORDS.items():
        for kw in keywords:
            if kw in combined:
                return series
    return ""


def extract_content(limit: int = None):
    """Extract all campaigns to .md files with classification."""
    print("\n[*] Extracting campaign content to .md files...")

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    all_campaigns = []
    count = 0
    errors = 0

    quarter_dirs = sorted(CAMPAIGNS_DIR.iterdir())

    for qdir in quarter_dirs:
        if not qdir.is_dir():
            continue
        for campaign_dir in sorted(qdir.iterdir()):
            if not campaign_dir.is_dir():
                continue

            meta_file = campaign_dir / "metadata.json"
            html_file = campaign_dir / "email.html"
            metrics_file = campaign_dir / "metrics.json"

            if not meta_file.exists():
                continue

            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)

            # Load metrics
            metrics = {}
            if metrics_file.exists():
                with open(metrics_file, "r", encoding="utf-8") as f:
                    metrics = json.load(f)

            # Extract HTML to text
            body_text = ""
            links = []
            if html_file.exists():
                with open(html_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
                try:
                    body_text, links = html_to_text(html_content)
                except Exception as e:
                    print(f"  [!] HTML parse error for {meta.get('name', '?')}: {e}")
                    errors += 1

            body_lower = body_text.lower()
            name = meta.get("name", "Untitled")
            subject = meta.get("subject", "")
            preview = meta.get("preview_text", "")
            send_time = meta.get("send_time", "")
            date_str = send_time[:10] if send_time else "no-date"

            # Classify
            phase = classify_phase(name, body_lower)
            story_source = classify_story_source(name, subject, body_lower)
            hook_type = classify_hook_type(body_text)
            characters = detect_characters(body_lower)
            series = detect_series(name, body_lower)
            pillar_num, pillar_name = EMAIL_PILLAR_MAP.get(story_source, ("1", "Gothic Infotainment"))

            # Build classification record
            record = {
                "id": meta.get("id", ""),
                "name": name,
                "date": date_str,
                "send_time": send_time,
                "subject": subject,
                "preview_text": preview,
                "phase": phase,
                "series": series,
                "story_source": story_source,
                "pillar": pillar_num,
                "pillar_name": pillar_name,
                "hook_type": hook_type,
                "characters": characters,
                "metrics": {
                    "recipients": metrics.get("recipients", 0),
                    "opens": metrics.get("opens", 0),
                    "open_rate": metrics.get("open_rate", 0),
                    "clicks": metrics.get("clicks", 0),
                    "click_rate": metrics.get("click_rate", 0),
                    "bounce_rate": metrics.get("bounce_rate", 0),
                },
                "channel": "email",
                "word_count": len(body_text.split()) if body_text else 0,
            }

            # Generate .md file
            safe_name = sanitize_filename(name)
            md_filename = f"{date_str}_{safe_name}.md"
            md_path = CONTENT_DIR / md_filename

            open_rate_str = f"{record['metrics']['open_rate']:.1%}" if record['metrics']['open_rate'] else "N/A"
            click_rate_str = f"{record['metrics']['click_rate']:.1%}" if record['metrics']['click_rate'] else "N/A"
            recipients_str = f"{int(record['metrics']['recipients']):,}" if record['metrics']['recipients'] else "N/A"

            series_str = f" | **Series:** {series}" if series else ""
            chars_str = ", ".join(characters) if characters else "Julie"

            md_content = f"""# {name}
- **Date:** {date_str}
- **Phase:** {phase}{series_str}
- **Pillar:** {pillar_num} ({pillar_name}) | **Story Source:** {story_source}
- **Characters:** {chars_str}
- **Hook Type:** {hook_type}
- **Open Rate:** {open_rate_str} | **Click Rate:** {click_rate_str} | **Recipients:** {recipients_str}

## Subject Line
{subject if subject else "(not enriched — run --enrich first)"}

## Preview Text
{preview if preview else "(not enriched — run --enrich first)"}

## Body
{body_text if body_text else "(no HTML content available)"}

## Links
{chr(10).join("- " + l for l in links) if links else "(none)"}
"""

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            all_campaigns.append(record)
            count += 1

            if count % 25 == 0:
                print(f"  Extracted {count} campaigns...")

            if limit and count >= limit:
                print(f"  Reached limit of {limit}")
                break
        if limit and count >= limit:
            break

    # Save analysis JSON
    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_campaigns, f, indent=2, ensure_ascii=False)

    print(f"\n  [OK] Extracted {count} campaigns to {CONTENT_DIR}")
    print(f"  [OK] Analysis data saved to {ANALYSIS_FILE}")
    if errors:
        print(f"  [!] {errors} HTML parse errors")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Sync Klaviyo email campaigns to workspace")
    parser.add_argument("--since", type=str, help="Only fetch campaigns sent after this date (YYYY-MM-DD)")
    parser.add_argument("--incremental", action="store_true", help="Only fetch campaigns since last sync")
    parser.add_argument("--skip-metrics", action="store_true", help="Skip fetching performance metrics")
    parser.add_argument("--limit", type=int, help="Max number of campaigns to process")
    parser.add_argument("--enrich", action="store_true", help="Enrich metadata with subject lines and preview text")
    parser.add_argument("--extract-content", action="store_true", help="Extract campaigns to .md files with classification")
    args = parser.parse_args()
    
    # Validate API key
    if not API_KEY:
        print("[ERROR] KLAVIYO_API_KEY not set.")
        print("   Create a .env file in the project root with:")
        print("   KLAVIYO_API_KEY=pk_your_private_api_key_here")
        sys.exit(1)

    print("=" * 60)
    print("  Klaviyo -> Skullette Workspace Sync")
    print("=" * 60)

    # Handle --enrich mode
    if args.enrich:
        enrich_metadata(limit=args.limit)
        return

    # Handle --extract-content mode
    if args.extract_content:
        extract_content(limit=args.limit)
        return

    # Determine since_date
    since_date = args.since
    if args.incremental and SYNC_LOG_FILE.exists():
        with open(SYNC_LOG_FILE, "r") as f:
            log = json.load(f)
        since_date = log.get("last_sync", "")[:10]
        print(f"  Incremental mode: fetching since {since_date}")
    
    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CAMPAIGNS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Fetch campaigns
    campaigns = fetch_campaigns(since_date)
    
    if args.limit:
        campaigns = campaigns[:args.limit]
        print(f"  Limited to {args.limit} campaigns")
    
    if not campaigns:
        print("\n[OK] No new campaigns to sync.")
        return
    
    # Step 2: Collect campaign IDs for batch metrics
    campaign_ids = [c["id"] for c in campaigns]
    
    # Step 3: Fetch metrics
    metrics_map = {}
    if not args.skip_metrics:
        metrics_map = fetch_campaign_metrics(campaign_ids)
    
    # Step 4: Process each campaign
    print(f"\n[*] Saving {len(campaigns)} campaigns to disk...")
    
    campaigns_data = []
    
    for i, campaign in enumerate(campaigns):
        attrs = campaign.get("attributes", {})
        name = attrs.get("name", "Untitled")
        send_time = attrs.get("send_time", "")
        date_prefix = send_time[:10] if send_time else "no-date"
        
        folder_name = f"{date_prefix}_{sanitize_filename(name)}"
        folder_path = CAMPAIGNS_DIR / folder_name
        
        print(f"  [{i+1}/{len(campaigns)}] {name}")
        
        # Fetch template HTML
        message_ids = fetch_campaign_messages(campaign)
        html_content = None
        for msg_id in message_ids:
            html_content = fetch_template_html(msg_id)
            if html_content:
                break
        
        # Get metrics for this campaign
        campaign_metrics = metrics_map.get(campaign["id"], {})
        
        # Save to disk
        save_campaign(campaign, html_content, campaign_metrics, folder_path)
        
        # Collect for summary
        campaigns_data.append({
            "name": name,
            "send_time": send_time,
            "id": campaign["id"],
            "metrics": campaign_metrics,
            "has_html": html_content is not None,
        })
    
    # Step 5: Generate summary
    generate_summary(campaigns_data)
    
    # Step 6: Save sync log
    save_sync_log(len(campaigns), since_date)
    
    # Done
    print("\n" + "=" * 60)
    print(f"  [OK] Sync complete!")
    print(f"  [>] {len(campaigns)} campaigns saved to: {CAMPAIGNS_DIR}")
    print(f"  [>] Summary at: {SUMMARY_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
