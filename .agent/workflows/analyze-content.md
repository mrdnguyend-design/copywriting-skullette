---
description: Analyze Content — run extraction pipeline, classify campaigns, generate summary report
---

# /analyze-content — Content Analysis Pipeline

> Extracts campaign content from Klaviyo HTML, classifies by taxonomy, generates performance summary.
> Run after new campaigns are synced or when refreshing analysis data.

---

## Step 1: ENRICH METADATA

Add subject lines and preview text to campaign metadata:
```bash
python scripts/klaviyo_sync.py --enrich
```
- Fetches `/campaigns/{id}/campaign-messages` for each campaign
- Updates `metadata.json` files with `subject` + `preview_text` fields

Use `--limit N` to test on a subset first.

---

## Step 2: EXTRACT CONTENT TO MARKDOWN

Convert HTML campaigns to classified .md files:
```bash
python scripts/klaviyo_sync.py --extract-content
```

This:
1. Strips HTML → plain text (via BeautifulSoup)
2. Classifies each campaign: phase, story source, pillar, characters, hook type, series
3. Outputs one `.md` per campaign to `klaviyo/content/`
4. Generates `klaviyo/content-analysis.json` with all structured data

---

## Step 3: GENERATE SUMMARY REPORT

```bash
python scripts/content_analysis.py
```

Generates `klaviyo/content-analysis-summary.md` with sections:
- Overview (total campaigns, date range, breakdown by phase)
- By Story Source (count + avg open/click per source)
- By Campaign Series (which series performs best)
- By Hook Type (which hooks get highest open rates)
- By Character (appearance frequency + performance correlation)
- Top 15 by open rate (min 20K recipients)
- Top 15 by click rate
- Bottom 10 by open rate (min 40K recipients)
- Monthly trends
- Weekly Story Source distribution (rotation compliance)

To include SMS data (if Postscript has been scraped):
```bash
python scripts/content_analysis.py --include-sms
```

---

## Step 4: REVIEW INSIGHTS

Read the summary and flag actionable findings:
1. **Under-used themes** with high performance → recommend increasing
2. **Over-used themes** with declining performance → recommend reducing
3. **Character appearances** vs open rate correlation → recommend more Alice/Jade
4. **Anti-patterns** from bottom performers → add to `learnings/style-rules.md`

---

## Step 5: UPDATE KNOWLEDGE FILES (if significant changes)

If the analysis reveals new patterns, update:
- `knowledge/core/writing-patterns.md` — new voice/structural patterns
- `knowledge/core/theme-rotation-matrix.md` — adjusted frequencies
- `knowledge/core/swipe-file-best-emails.md` — new top performers
- `knowledge/core/performance-tracking.md` — updated benchmarks
- `learnings/monthly-insights.md` — new monthly entry

---

## Step 6: COMPLETE

Output:
```
Content Analysis Complete

Campaigns analyzed: [N]
Date range: [earliest] to [latest]
Content files: klaviyo/content/[count] .md files
Summary: klaviyo/content-analysis-summary.md

Key findings:
- [Top insight 1]
- [Top insight 2]
- [Top insight 3]

Next: Review summary, then /weekly-planning or /monthly-strategy
```

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
