---
description: Sync Postscript SMS data — scrape campaigns, generate .md files, update analysis
---

# /sync-postscript — Postscript SMS Data Sync

> Scrapes SMS campaign data from Postscript and integrates into content analysis.
> Requires: Node.js, Playwright, Chromium browser installed.

---

## Step 1: PRE-FLIGHT CHECK

Verify dependencies:
```bash
cd scripts && npm list playwright
```

If missing: `npm install && npx playwright install chromium`

Check for existing data:
```bash
ls postscript/sms-raw.json 2>/dev/null && echo "Existing data found — will append" || echo "Fresh scrape"
```

---

## Step 2: RUN SCRAPER

### First Run (headed mode for shop switch verification)
```bash
node scripts/postscript-scrape.js --headed --limit 5
```
- Verify: correct shop (555740) selected
- Verify: login succeeds
- Verify: 5 SMS .md files created in `postscript/sms/`

### Production Run
```bash
node scripts/postscript-scrape.js --since 2026-01-01
```
- Scrapes all campaigns since the given date
- Saves incrementally every 15 campaigns (resumable)
- Creates individual .md files in `postscript/sms/`

---

## Step 3: VERIFY OUTPUT

Check output files:
1. `postscript/sms-raw.json` — raw scraped data
2. `postscript/sms/*.md` — individual SMS campaign files
3. `postscript/sms-summary.md` — aggregate summary

Spot-check 3 random .md files against Postscript UI for accuracy.

---

## Step 4: UPDATE CONTENT ANALYSIS

Run content analysis with SMS integration:
```bash
python scripts/content_analysis.py --include-sms
```

This updates:
- `klaviyo/content-analysis.json` (adds SMS data)
- `klaviyo/content-analysis-summary.md` (adds SMS sections)

---

## Step 5: COMPLETE

Output:
```
Postscript Sync Complete

SMS campaigns scraped: [N]
Date range: [earliest] to [latest]
Files created: postscript/sms/[count] .md files

Content analysis updated: Yes/No
Next: Review sms-summary.md for insights
```

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
