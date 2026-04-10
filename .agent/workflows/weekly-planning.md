---
description: Create 7-day content calendar + revenue projection for Skullette
---

# /weekly-planning — Weekly Content Calendar

> **Chạy vào cuối tuần** (Thứ 6 hoặc Chủ nhật) cho tuần tới.
> Output: 7-day content calendar + revenue projection

---

## Step 1: LOAD CONTEXT

Read:
1. `planning/monthly/[current month]-strategy.md` — Monthly campaign schedule + goals
2. `knowledge/core/content-taxonomy.md` — Story Sources, Pillars, Weekly View (Part 7)
3. `knowledge/core/story-bank.md` — READY items available
4. `knowledge/core/revenue-config.md` — RPS rates + targets
5. `learnings/post-mortems.md` — Last 5 entries for patterns
6. `learnings/monthly-insights.md` — Current month's performance trends

---

## Step 2: DETERMINE WEEK TYPE

**What kind of week is this?**

| Type | Definition | Email Strategy |
|------|-----------|----------------|
| **Campaign Week** | Active sale event running | Campaign Jobs take priority, daily emails fill gaps |
| **Mixed Week** | Campaign launches or ends mid-week | Campaign emails + daily story builds |
| **Regular Week** | No active campaign | Pure Story Source rotation, relationship-building |
| **Pre-Launch Week** | Campaign starting next week | Tease + prepare, build anticipation |

---

## Step 3: MAP 7 DAYS

For each day, assign:
- Email type (Daily / Campaign — which Job)
- Story Source (if daily)
- Email Pillar (1-4)
- Product to feature (if any)
- Character rotation
- SMS tier(s) + SMS Pillar

Use the Weekly View from `content-taxonomy.md` Part 7 as starting template.

### Campaign Days Override:
- Campaign Job determines structure
- Story Source can be used in hook/opening, but Campaign Job drives the content

---

## Step 4: VALIDATE DISTRIBUTION

Check before finalizing:

**Story Source variety:**
- [ ] No same Story Source two consecutive days
- [ ] Basic Brenda max 2x/week
- [ ] At least 1 Coven Chronicles (Pillar 3) this week
- [ ] At least 1 customer voice/testimonial this week

**Revenue projection:**
For each day: [RPS for email type] × [list size for segment] = projected revenue
Sum all days → Compare to weekly target from revenue-config.md

**Story Bank readiness:**
- [ ] READY items available for at least 3 days
- [ ] If < 3 READY items: flag and suggest /idea-research this week

**Character rotation:**
- [ ] Alice + Jade combined: ≤ 3x this week
- [ ] Basic Brenda: ≤ 2x this week

---

## Step 5: PRESENT WEEKLY PLAN

Output format:

```
📅 WEEK [YYYY-WW] CONTENT CALENDAR
[Date range]

WEEK TYPE: [Campaign / Mixed / Regular / Pre-Launch]
WEEKLY REVENUE TARGET: $[X] | PROJECTED: $[Y]

---

[DAY], [DATE]
📧 EMAIL: [Type] — [Campaign Job or Story Source]
   Pillar: [#] — [Name]
   Story: [2-sentence seed]
   Product: [Product name + offer if any]
   Character: [Who features]
   Segment: [MASS/HIGH/REG]
   RPS: $[X] × [list size] = $[projected]

📱 SMS: [Tier] — [SMS Pillar]
   Angle: [1 sentence]

---
[repeat for each day]

STORY BANK STATUS: [X] READY items
ALERTS: [any flags from validation]
```

---

## Step 6: USER REVIEW

Present plan → Wait for feedback:
- **"oke"** → Save to `planning/weekly/week-[YYYY-WW].md`
- **Swap a day** → Adjust that day's entry
- **Missing a campaign** → Add campaign context and re-map

---

## Step 7: SAVE PLAN

Save to `planning/weekly/week-[YYYY-WW].md` in the output format above.

Confirm: "Week [WW] plan saved. Start each day with `/daily-brief`."

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
