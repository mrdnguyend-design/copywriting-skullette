---
description: Finalize SMS — archive and log all approved SMS messages
---

# /finalize-sms — SMS Finalize

> **Chạy sau khi SMS draft đã được approve.**
> Output: Archived SMS file + send log entry

---

## Step 1: CONFIRM APPROVED SMS

Ask if no draft provided: "Paste the final approved SMS messages."

Confirm:
- Campaign context?
- Audience tier(s)?
- Send date/time?

---

## Step 2: ARCHIVE

File naming: `sms_[DDMMYY]_[tier]_[campaign-short-name].md`

Save to `campaigns/_active/[campaign-name]/sms/` if campaign SMS,
OR `klaviyo/campaigns/2026-Q2/` for standalone.

File content format:
```markdown
# SMS — [Campaign Name] — [Date]

**Tier:** [REG / HIGH / MASS]
**SMS Pillar:** [1-4 — name]
**Campaign context:** [standalone / day X of campaign]
**Sent:** [date + time]

---

## [TIER] Messages

[timestamp if live-event]
[full SMS text]

---
[repeat for each tier]
```

---

## Step 3: LOG ENTRY

Add to `learnings/post-mortems.md` (same entry as email if same campaign, or new entry):

```markdown
**SMS:** [campaign-sms-filename]
**Tier:** [REG/HIGH/MASS]
**SMS Pillar:** [1-4]
**Sent:** [date]

**What Worked:**
- [specific line or technique]

**What to Improve:**
- [revision pattern]
```

---

## Step 4: COMPLETE

Output:

```
✅ SMS FINALIZED

File saved: [path]

Tiers archived: [list]
Kaizen log: Updated

Next: /sync-klaviyo to push to Postscript
```

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
