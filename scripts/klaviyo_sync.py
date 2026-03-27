"""
Klaviyo → Skullette Workspace Sync Script
==========================================
Pulls email campaign content and performance metrics from Klaviyo API
and saves them as organized knowledge files in the workspace.

Usage:
    python scripts/klaviyo_sync.py              # Full sync (all campaigns)
    python scripts/klaviyo_sync.py --since 2025-01-01   # Only campaigns after date
    python scripts/klaviyo_sync.py --incremental        # Only new since last sync

Requires:
    pip install requests python-dotenv
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
SYNC_LOG_FILE = OUTPUT_DIR / "sync_log.json"
SUMMARY_FILE = OUTPUT_DIR / "summary.md"

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


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Sync Klaviyo email campaigns to workspace")
    parser.add_argument("--since", type=str, help="Only fetch campaigns sent after this date (YYYY-MM-DD)")
    parser.add_argument("--incremental", action="store_true", help="Only fetch campaigns since last sync")
    parser.add_argument("--skip-metrics", action="store_true", help="Skip fetching performance metrics")
    parser.add_argument("--limit", type=int, help="Max number of campaigns to process")
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
