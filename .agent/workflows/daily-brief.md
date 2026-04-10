---
description: Daily entry point — create today's email + SMS brief from weekly plan
---

# /daily-brief — Daily Content Brief

> **Bắt đầu mỗi ngày từ đây.** Tạo brief cho email + SMS hôm nay.

---

## Step 1: GATHER CONTEXT

Read in this order:
1. `planning/weekly/` — Find this week's plan (current ISO week)
2. `knowledge/core/story-bank.md` — Check READY items
3. `knowledge/core/content-taxonomy.md` — Refresh Story Sources + Pillars
4. `planning/monthly/` — Current month's strategy + campaign schedule
5. `learnings/post-mortems.md` — Last 3 entries (what worked recently)
6. `learnings/style-rules.md` — Skim rules relevant to today's content type

---

## Step 2: DETERMINE TODAY'S CONTENT

### If weekly plan exists:
Pull today's entry from the plan. Extract:
- Email type + Campaign Job (if campaign week) or Story Source (if daily)
- Product/offer to feature
- Any notes or constraints

### If no weekly plan (Freestyle Mode):
Use the Decision Tree from `content-taxonomy.md` Part 4:

```
1. Check story-bank.md — Any READY items?
   → Yes: Use the READY item → skip to Step 3
   → No: Continue below

2. What's the campaign status?
   → Active campaign → determine Campaign Job for today
   → No campaign → pick Story Source (what hasn't been used in 2 days?)

3. Story Source → Email Pillar (from taxonomy Part 7 weekly view)
```

---

## Step 3: CREATE BRIEF

Present brief to user in this format:

```
📋 TODAY'S BRIEF — [DATE, DAY OF WEEK]

📧 EMAIL
- Type: [Daily / Sale / Teaser]
- Campaign Job: [if applicable] or Story Source: [source type]
- Pillar: [1-4] — [Pillar name]
- Story seed: [What's the story? 2-3 sentences]
- Product/Broccoli: [Which product? What offer?]
- Character: [Julie alone / Julie + Alice / Julie + Jade / customer story]
- Emotional driver: [What feeling should the reader leave with?]
- Hook direction: [Suggested first line or scene entry point]
- Audience: [MASS / HIGH / REG — who gets this?]

📱 SMS
- Tier(s): [REG / HIGH / MASS — which tiers today?]
- SMS Pillar: [1-4] — [Pillar name]
- Timing: [Standalone / same event as email / different angle]
- Key message: [1 sentence]

⚠️ ALERTS
[See Step 4]
```

---

## Step 4: ALERTS

Check and flag if any of these are true:

**Story Bank:**
- [ ] READY items count < 3 → "Story Bank low — run /idea-research soon"
- [ ] No READY items → "Story Bank empty — run /idea-research before writing"

**Character fatigue:**
- [ ] Basic Brenda used 2+ days this week → "Brenda limit approaching"
- [ ] Alice or Jade used 3+ days combined this week → "Supporting character overuse"

**Story Source:**
- [ ] Same Story Source as yesterday → flag and suggest alternative

**Campaign:**
- [ ] Active campaign — is today's email the right Campaign Job in sequence?
- [ ] Is tomorrow a campaign milestone (launch, close)? → prep note

---

## Step 5: STYLE REMINDERS

Pull 3 most relevant style rules from `learnings/style-rules.md` for today's content type.

Example for Gothic Mundane daily:
> 1. Julie must be IN the scene physically
> 2. Every scene needs a Turn (expectation gap)
> 3. (Parenthetical asides) to show inner life

---

## Step 6: USER CONFIRMATION

Present brief → Wait for user response:

- **"oke"** / approve → Proceed to hand-off
- **"đổi story"** / swap → Show 2 alternative story seeds
- **Specific adjustment** → Update brief accordingly, re-present

---

## Step 7: HAND-OFF

After approval:

> "Brief confirmed. Run `/write-email` to start — brief is pre-loaded."
> "After email draft: `/review-craft` → `/review-strategy` → `/review-brand`"
> "Then: `/write-sms` → `/finalize-email` → `/finalize-sms`"

---

## Step 8: END-OF-DAY (optional)

If user runs this at end of day or after publishing:

1. Update `knowledge/core/story-bank.md`:
   - Mark used READY item as USED (add date)
   - Update Story Source Coverage table

2. Tomorrow preview:
   - What's next in the weekly plan?
   - Any READY items that fit?
   - Story Bank health check

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
