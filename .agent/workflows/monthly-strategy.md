---
description: Create monthly content strategy with campaign schedule + P&L for Skullette
---

# /monthly-strategy — Monthly Content Strategy

> **Chạy vào cuối tháng trước** hoặc đầu tháng mới.
> Output: Campaign calendar + P&L + Story Source plan + Character arc

---

## Step 1: LOAD CONTEXT

Read:
1. `knowledge/core/revenue-config.md` — List sizes, RPS rates, revenue targets
2. `planning/monthly/` — Last month's strategy (performance, lessons)
3. `learnings/monthly-insights.md` — Last month's learnings (patterns that worked/failed)
3b. `learnings/style-rules.md` — Current writing rules
4. `campaigns/_active/` — Any ongoing campaigns carrying over
5. `knowledge/core/content-taxonomy.md` — Campaign Types + Story Sources

---

## Step 2: ASK FOR CAMPAIGN PLAN

If user hasn't provided campaign plan, ask:

> "Tháng này có campaigns nào? (Ví dụ: Friday 13th, new launch, clearance, BOGO...)"
> "Revenue target cho tháng này?"
> "Có special events không? (holidays, anniversaries, seasonal moments)"

---

## Step 3: BUILD CAMPAIGN CALENDAR

Map all planned campaigns to dates:

| Week | Dates | Campaign | Type | Job Sequence |
|------|-------|---------|------|-------------|
| W1 | [dates] | [name or "Regular"] | [type] | [ANNOUNCE→CLOSE] |
| W2 | [dates] | [name] | | |
| W3 | [dates] | [name] | | |
| W4 | [dates] | [name] | | |

**Campaign Email Sequence by Type:**

| Type | Sequence |
|------|---------|
| Gamified (3-5 days) | ANNOUNCE → PREPARE → LIVE → LIVE → CLOSE → THANK |
| Flash/Themed (1-2 days) | ANNOUNCE → LIVE → CLOSE |
| Mission (7+ days) | ANNOUNCE → TEACH → PROVE → JUSTIFY → PREPARE → CLOSE → THANK |
| Regular weeks | Daily Story Sources — see taxonomy Part 7 |

---

## Step 4: STORY SOURCE PLAN

For non-campaign days, plan Story Source distribution across the month:

- Identify which Story Sources are low in the Story Bank → prioritize in idea-research
- Identify seasonal/cultural moments this month → assign to Cultural Darkness source
- Map customer voice opportunities → schedule Witch Victory emails
- Plan Basic Brenda appearances (max 2/week — track across month)

---

## Step 5: REVENUE PROJECTION (P&L)

For each week:

```
Campaign emails: [count] × [RPS campaign] × [list size] = $X
Daily emails: [count] × [RPS daily] × [list size] = $X
SMS (REG): [count] × [RPS REG] × [REG list] = $X
SMS (HIGH): [count] × [RPS HIGH] × [HIGH list] = $X
SMS (MASS): [count] × [RPS MASS] × [MASS list] = $X
Week subtotal: $X
```

Monthly total projection vs. target:
- Target: $[X] (from revenue-config.md)
- Projected: $[Y]
- Gap: $[Z] → adjust campaign intensity or add sends

---

## Step 6: CHARACTER ARC PLAN

Map character appearances across the month:

- **Julie:** Every send (non-negotiable)
- **Alice:** Which weeks? (operations, logistics stories)
- **Jade:** Which product launches need design story?
- **Basic Brenda:** Which weeks? (max 2x/week)
- **Witch Victory (customer):** At least 1x/week — which customer stories are READY?

---

## Step 7: PRESENT STRATEGY

Output:

```
📅 [MONTH YEAR] STRATEGY

REVENUE TARGET: $[X]
PROJECTED: $[Y]

CAMPAIGNS:
[List all campaigns with dates + type]

WEEK-BY-WEEK:
[Week summaries with campaign focus or daily theme]

STORY BANK NEEDS:
[Which sources are low? What ideas to research?]

CHARACTER PLAN:
[Jade appears W2 for new launch, Alice W1 ops story, etc.]

P&L SUMMARY:
[Week-by-week revenue projection table]

ALERTS:
[Any risks, Story Bank gaps, calendar conflicts]
```

---

## Step 8: SAVE

After user approval, save to `planning/monthly/[YYYY-MM]-strategy.md`.

Confirm: "Strategy saved. Run `/weekly-planning` to build Week 1 calendar."

---

## FIRST-RUN GUIDE (New Month, No History)

If this is the first time running monthly-strategy:

1. Ask user for: list sizes, revenue targets, planned campaigns
2. Revenue-config.md likely has placeholders → ask user to fill from Excel first
3. Start with 1 campaign + majority regular weeks → don't over-commit
4. Build Story Bank BEFORE committing to Story Source-heavy weeks

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
