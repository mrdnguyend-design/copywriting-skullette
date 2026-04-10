---
description: View, add, develop, and manage Story Bank items for Skullette
---

# /story-bank — Story Bank Manager

> Quản lý pipeline: SEED → CONCEPT → READY → USED
> File: `knowledge/core/story-bank.md`

---

## Actions Available

When user runs `/story-bank`, ask what they want to do:

1. **VIEW** — Show current Story Bank status
2. **ADD** — Add a new seed or idea
3. **DEVELOP** — Develop a SEED into CONCEPT or READY
4. **AUDIT** — Check coverage + health of Story Bank

---

## Action 1: VIEW

Read `knowledge/core/story-bank.md`. Present:

```
📚 STORY BANK STATUS

READY: [count] items
CONCEPTS: [count] items
SEEDS: [count] items

READY ITEMS:
[List each READY item — title + product fit + Story Source]

STORY SOURCE COVERAGE:
[Table showing Last Used + Times This Month for each source]

RECOMMENDATION:
[If READY < 3: suggest /idea-research]
[If any source unused for 5+ days: flag it]
```

---

## Action 2: ADD

User provides raw idea. Format it as SEED:

```
What's the story? (1-2 sentences)
What's the Story Source? (Gothic Mundane / Witch Victory / etc.)
Any product connection in mind?
```

Add to SEEDS section of `knowledge/core/story-bank.md`.

---

## Action 3: DEVELOP

Select a SEED or CONCEPT to develop. For each item, ask:

**SEED → CONCEPT:**
1. What's the Turn? (expectation vs reality gap)
2. Which Email Pillar fits? (1-4)
3. What's the hook direction? (possible first line)
4. What product could this connect to?

**CONCEPT → READY:**
1. What's the exact (or near-exact) first line?
2. Is there a specific customer quote to anchor it?
3. Which pivot method? (from taxonomy Part 3B)
4. What specific product + offer details?
5. Any timing constraints? (seasonal, campaign-dependent)

Update the item's status and move it to the correct section in `knowledge/core/story-bank.md`.

---

## Action 4: AUDIT

Read `knowledge/core/story-bank.md` and `planning/weekly/` (last 2 weeks).

Report:

```
🔍 STORY BANK AUDIT

HEALTH: [Green / Yellow / Red]
- Green: 5+ READY items, all 7 sources covered in last 2 weeks
- Yellow: 3-4 READY items, or 2+ sources unused for 5+ days
- Red: < 3 READY items, or 3+ sources unused

GAPS:
[Which Story Sources are underrepresented?]

AGING CONCEPTS:
[Items in CONCEPT for 7+ days — should develop or archive]

RECOMMENDATION:
[Specific actions: run /idea-research for X source, develop Y concept]
```

---

## Updating After Publishing

When an email has been sent, mark the story as USED:

1. Find the item in READY section
2. Move to USED section with format:
```
**[Title]** — USED [date]
- Email: [email filename]
- Story Source: [source]
- Notes: [brief note on what worked or changed from plan]
```
3. Update Story Source Coverage table (last used date + count)

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
