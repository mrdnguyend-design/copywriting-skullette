---
description: Sync email campaign data from Klaviyo into the workspace
---

# Sync Klaviyo Data

Pull email campaign content and performance metrics from Klaviyo API into `klaviyo/`.

## Prerequisites
- `.env` file in project root with `KLAVIYO_API_KEY=pk_xxxxx`
- Python packages: `requests`, `python-dotenv`

## Steps

// turbo-all

1. Run the sync script (all campaigns):
```
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" "d:\Skullette - Copywriting\scripts\klaviyo_sync.py"
```

### Optional Variants

- **Incremental sync** (only new since last run):
```
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" "d:\Skullette - Copywriting\scripts\klaviyo_sync.py" --incremental
```

- **Since a specific date**:
```
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" "d:\Skullette - Copywriting\scripts\klaviyo_sync.py" --since 2025-01-01
```

- **Limit to N campaigns** (for testing):
```
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" "d:\Skullette - Copywriting\scripts\klaviyo_sync.py" --limit 5
```

## Output

After running, you'll find:
- `klaviyo/campaigns/` — Individual campaign folders with `email.html`, `metadata.json`, `metrics.json`
- `klaviyo/summary.md` — Readable overview with performance rankings
- `klaviyo/sync_log.json` — Sync history for incremental updates
