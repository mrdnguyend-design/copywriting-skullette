"""
Skullette Content Analysis — Summary Generator
================================================
Reads content-analysis.json (from klaviyo_sync.py --extract-content)
and generates a comprehensive content-analysis-summary.md.

Optionally also processes Postscript SMS data from postscript/sms-raw.json.

Usage:
    python scripts/content_analysis.py                    # Email only
    python scripts/content_analysis.py --include-sms      # Email + SMS

Requires:
    klaviyo/content-analysis.json (run klaviyo_sync.py --extract-content first)
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ANALYSIS_FILE = PROJECT_ROOT / "klaviyo" / "content-analysis.json"
SMS_FILE = PROJECT_ROOT / "postscript" / "sms-raw.json"
SUMMARY_FILE = PROJECT_ROOT / "klaviyo" / "content-analysis-summary.md"


def load_data() -> list[dict]:
    """Load the content analysis JSON."""
    if not ANALYSIS_FILE.exists():
        print(f"[ERROR] {ANALYSIS_FILE} not found.")
        print("  Run: python scripts/klaviyo_sync.py --extract-content")
        sys.exit(1)

    with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"[*] Loaded {len(data)} campaigns from {ANALYSIS_FILE}")
    return data


def load_sms_data() -> list[dict]:
    """Load SMS data if available."""
    if not SMS_FILE.exists():
        return []

    with open(SMS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"[*] Loaded {len(data)} SMS campaigns from {SMS_FILE}")
    return data


def safe_avg(values: list) -> float:
    """Calculate average, ignoring zeros and None."""
    filtered = [v for v in values if v and v > 0]
    return sum(filtered) / len(filtered) if filtered else 0


def fmt_pct(val: float) -> str:
    """Format a decimal as percentage."""
    return f"{val:.1%}" if val else "N/A"


def fmt_num(val: float) -> str:
    """Format a number with comma separators."""
    return f"{int(val):,}" if val else "0"


def generate_summary(campaigns: list[dict], sms_data: list[dict] = None):
    """Generate the content analysis summary markdown."""
    lines = []

    # ─── Header ──────────────────────────────────────────────────────────
    email_campaigns = [c for c in campaigns if c.get("channel") == "email"]
    dates = [c["date"] for c in email_campaigns if c.get("date") and c["date"] != "no-date"]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    lines.extend([
        "# Skullette Content Analysis Summary",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "---",
        "",
        "## Overview",
        "",
        f"- **Total Email Campaigns:** {len(email_campaigns)}",
        f"- **Date Range:** {date_range}",
    ])

    if sms_data:
        lines.append(f"- **Total SMS Campaigns:** {len(sms_data)}")

    # ─── Phase Breakdown ─────────────────────────────────────────────────
    phase_groups = defaultdict(list)
    for c in email_campaigns:
        phase_groups[c.get("phase", "unknown")].append(c)

    lines.extend([
        "",
        "---",
        "",
        "## By Phase",
        "",
        "| Phase | Count | Avg Open Rate | Avg Click Rate |",
        "|-------|-------|---------------|----------------|",
    ])

    for phase in ["daily", "teaser", "sale", "post"]:
        group = phase_groups.get(phase, [])
        if not group:
            continue
        avg_or = safe_avg([c["metrics"]["open_rate"] for c in group])
        avg_cr = safe_avg([c["metrics"]["click_rate"] for c in group])
        lines.append(f"| {phase.title()} | {len(group)} | {fmt_pct(avg_or)} | {fmt_pct(avg_cr)} |")

    # ─── Story Source Breakdown ──────────────────────────────────────────
    source_groups = defaultdict(list)
    for c in email_campaigns:
        source_groups[c.get("story_source", "Unknown")].append(c)

    lines.extend([
        "",
        "---",
        "",
        "## By Story Source",
        "",
        "| Story Source | Count | Avg Open Rate | Avg Click Rate | Top Performer |",
        "|-------------|-------|---------------|----------------|---------------|",
    ])

    for source in sorted(source_groups.keys()):
        group = source_groups[source]
        avg_or = safe_avg([c["metrics"]["open_rate"] for c in group])
        avg_cr = safe_avg([c["metrics"]["click_rate"] for c in group])
        # Find top performer by open rate
        with_rates = [c for c in group if c["metrics"]["open_rate"] > 0]
        top = max(with_rates, key=lambda x: x["metrics"]["open_rate"]) if with_rates else None
        top_str = f"{top['name'][:40]} ({fmt_pct(top['metrics']['open_rate'])})" if top else "N/A"
        lines.append(f"| {source} | {len(group)} | {fmt_pct(avg_or)} | {fmt_pct(avg_cr)} | {top_str} |")

    # ─── Campaign Series ─────────────────────────────────────────────────
    series_groups = defaultdict(list)
    for c in email_campaigns:
        s = c.get("series", "")
        if s:
            series_groups[s].append(c)

    if series_groups:
        lines.extend([
            "",
            "---",
            "",
            "## By Campaign Series",
            "",
            "| Series | Emails | Avg Open Rate | Avg Click Rate |",
            "|--------|--------|---------------|----------------|",
        ])
        for series in sorted(series_groups.keys()):
            group = series_groups[series]
            avg_or = safe_avg([c["metrics"]["open_rate"] for c in group])
            avg_cr = safe_avg([c["metrics"]["click_rate"] for c in group])
            lines.append(f"| {series} | {len(group)} | {fmt_pct(avg_or)} | {fmt_pct(avg_cr)} |")

    # ─── Hook Type Analysis ──────────────────────────────────────────────
    hook_groups = defaultdict(list)
    for c in email_campaigns:
        hook_groups[c.get("hook_type", "unknown")].append(c)

    lines.extend([
        "",
        "---",
        "",
        "## By Hook Type",
        "",
        "| Hook Type | Count | Avg Open Rate | Avg Click Rate |",
        "|-----------|-------|---------------|----------------|",
    ])

    for hook in sorted(hook_groups.keys()):
        group = hook_groups[hook]
        avg_or = safe_avg([c["metrics"]["open_rate"] for c in group])
        avg_cr = safe_avg([c["metrics"]["click_rate"] for c in group])
        lines.append(f"| {hook} | {len(group)} | {fmt_pct(avg_or)} | {fmt_pct(avg_cr)} |")

    # ─── Character Analysis ──────────────────────────────────────────────
    char_counter = Counter()
    char_performance = defaultdict(list)
    for c in email_campaigns:
        for char in c.get("characters", []):
            char_counter[char] += 1
            if c["metrics"]["open_rate"] > 0:
                char_performance[char].append(c["metrics"]["open_rate"])

    lines.extend([
        "",
        "---",
        "",
        "## By Character",
        "",
        "| Character | Appearances | Avg Open Rate (when present) |",
        "|-----------|-------------|----------------------------|",
    ])

    for char, count in char_counter.most_common():
        avg_or = safe_avg(char_performance[char])
        lines.append(f"| {char} | {count} | {fmt_pct(avg_or)} |")

    # ─── Top Performers ──────────────────────────────────────────────────
    # Filter for campaigns with meaningful recipient count
    meaningful = [c for c in email_campaigns
                  if c["metrics"]["recipients"] >= 20000 and c["metrics"]["open_rate"] > 0]

    lines.extend([
        "",
        "---",
        "",
        "## Top 15 Emails by Open Rate (min 20K recipients)",
        "",
        "| # | Date | Campaign | Open Rate | Click Rate | Recipients |",
        "|---|------|----------|-----------|------------|------------|",
    ])

    top_open = sorted(meaningful, key=lambda x: x["metrics"]["open_rate"], reverse=True)[:15]
    for i, c in enumerate(top_open, 1):
        m = c["metrics"]
        lines.append(f"| {i} | {c['date']} | {c['name'][:50]} | {fmt_pct(m['open_rate'])} | {fmt_pct(m['click_rate'])} | {fmt_num(m['recipients'])} |")

    lines.extend([
        "",
        "## Top 15 Emails by Click Rate (min 20K recipients)",
        "",
        "| # | Date | Campaign | Click Rate | Open Rate | Recipients |",
        "|---|------|----------|------------|-----------|------------|",
    ])

    top_click = sorted(meaningful, key=lambda x: x["metrics"]["click_rate"], reverse=True)[:15]
    for i, c in enumerate(top_click, 1):
        m = c["metrics"]
        lines.append(f"| {i} | {c['date']} | {c['name'][:50]} | {fmt_pct(m['click_rate'])} | {fmt_pct(m['open_rate'])} | {fmt_num(m['recipients'])} |")

    # ─── Bottom Performers ───────────────────────────────────────────────
    meaningful_40k = [c for c in email_campaigns
                      if c["metrics"]["recipients"] >= 40000 and c["metrics"]["open_rate"] > 0]

    lines.extend([
        "",
        "## Bottom 10 Emails by Open Rate (min 40K recipients)",
        "",
        "| # | Date | Campaign | Open Rate | Click Rate | Recipients |",
        "|---|------|----------|-----------|------------|------------|",
    ])

    bottom_open = sorted(meaningful_40k, key=lambda x: x["metrics"]["open_rate"])[:10]
    for i, c in enumerate(bottom_open, 1):
        m = c["metrics"]
        lines.append(f"| {i} | {c['date']} | {c['name'][:50]} | {fmt_pct(m['open_rate'])} | {fmt_pct(m['click_rate'])} | {fmt_num(m['recipients'])} |")

    # ─── Monthly Trends ──────────────────────────────────────────────────
    monthly = defaultdict(list)
    for c in email_campaigns:
        if c.get("date") and c["date"] != "no-date":
            month = c["date"][:7]  # YYYY-MM
            monthly[month].append(c)

    lines.extend([
        "",
        "---",
        "",
        "## Monthly Trends",
        "",
        "| Month | Sends | Avg Open Rate | Avg Click Rate | Total Recipients |",
        "|-------|-------|---------------|----------------|------------------|",
    ])

    for month in sorted(monthly.keys()):
        group = monthly[month]
        avg_or = safe_avg([c["metrics"]["open_rate"] for c in group])
        avg_cr = safe_avg([c["metrics"]["click_rate"] for c in group])
        total_recip = sum(c["metrics"]["recipients"] for c in group)
        lines.append(f"| {month} | {len(group)} | {fmt_pct(avg_or)} | {fmt_pct(avg_cr)} | {fmt_num(total_recip)} |")

    # ─── Story Source Distribution per Week ──────────────────────────────
    weekly_sources = defaultdict(lambda: Counter())
    for c in email_campaigns:
        if c.get("date") and c["date"] != "no-date":
            try:
                dt = datetime.strptime(c["date"], "%Y-%m-%d")
                week = dt.strftime("%Y-W%W")
                weekly_sources[week][c.get("story_source", "Unknown")] += 1
            except ValueError:
                pass

    lines.extend([
        "",
        "---",
        "",
        "## Weekly Story Source Distribution (last 12 weeks)",
        "",
        "| Week | Sources Used | Most Common | Distribution |",
        "|------|-------------|-------------|--------------|",
    ])

    recent_weeks = sorted(weekly_sources.keys())[-12:]
    for week in recent_weeks:
        sources = weekly_sources[week]
        most_common = sources.most_common(1)[0][0] if sources else "N/A"
        dist = ", ".join(f"{s}:{n}" for s, n in sources.most_common())
        lines.append(f"| {week} | {len(sources)} | {most_common} | {dist} |")

    # ─── SMS Analysis (if available) ─────────────────────────────────────
    if sms_data:
        lines.extend([
            "",
            "---",
            "",
            "## SMS Campaign Analysis",
            "",
            f"**Total SMS Campaigns:** {len(sms_data)}",
            "",
        ])

        # Classify SMS by Pillar
        def classify_sms_pillar(sms):
            body = (sms.get("sms_body", "") or "").lower()
            if any(w in body for w in ["update", "right now", "just sold", "live", "screaming"]):
                return "Live Chaos"
            if any(w in body for w in ["first look", "before everyone", "just between", "early access", "you're seeing"]):
                return "Insider Access"
            if any(w in body for w in ["% off", "discount", "coupon", "code ", "deal", "free", "sale"]):
                return "The Dark Offer"
            if "?" in body or len(body) < 200:
                return "Witch Check-in"
            return "The Dark Offer"

        sms_pillar_groups = defaultdict(list)
        for s in sms_data:
            s["sms_pillar"] = classify_sms_pillar(s)
            sms_pillar_groups[s["sms_pillar"]].append(s)

        lines.extend([
            "### SMS by Pillar",
            "",
            "| Pillar | Count | Avg UCTR | Avg Revenue |",
            "|--------|-------|----------|-------------|",
        ])

        for pillar in sorted(sms_pillar_groups.keys()):
            group = sms_pillar_groups[pillar]
            avg_uctr = safe_avg([s.get("uctr", 0) for s in group])
            avg_rev = safe_avg([s.get("revenue", 0) for s in group])
            lines.append(f"| {pillar} | {len(group)} | {avg_uctr:.1f}% | ${avg_rev:,.0f} |")

        # SMS by Segment
        sms_seg_groups = defaultdict(list)
        for s in sms_data:
            sms_seg_groups[s.get("segment", "Unknown")].append(s)

        lines.extend([
            "",
            "### SMS by Segment",
            "",
            "| Segment | Count | Avg Sent | Avg UCTR |",
            "|---------|-------|----------|----------|",
        ])

        for seg in sorted(sms_seg_groups.keys()):
            group = sms_seg_groups[seg]
            avg_sent = safe_avg([s.get("sent", 0) for s in group])
            avg_uctr = safe_avg([s.get("uctr", 0) for s in group])
            lines.append(f"| {seg} | {len(group)} | {fmt_num(avg_sent)} | {avg_uctr:.1f}% |")

    # ─── Footer ──────────────────────────────────────────────────────────
    lines.extend([
        "",
        "---",
        "",
        f"*Analysis based on {len(email_campaigns)} email campaigns",
    ])
    if sms_data:
        lines[-1] += f" + {len(sms_data)} SMS campaigns"
    lines[-1] += ".*"

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate content analysis summary")
    parser.add_argument("--include-sms", action="store_true", help="Include SMS data from Postscript")
    args = parser.parse_args()

    campaigns = load_data()
    sms_data = load_sms_data() if args.include_sms else []

    summary = generate_summary(campaigns, sms_data)

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"\n[OK] Summary saved to {SUMMARY_FILE}")
    print(f"  Sections: Phase, Story Source, Series, Hook Type, Character,")
    print(f"  Top/Bottom Performers, Monthly Trends, Weekly Distribution")
    if sms_data:
        print(f"  + SMS by Pillar, SMS by Segment")


if __name__ == "__main__":
    main()
