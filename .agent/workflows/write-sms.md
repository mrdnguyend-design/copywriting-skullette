---
description: Write SMS campaign messages for Skullette — pillar-based, 3 audience tiers
---

# /write-sms — SMS Campaign Writer

> **Pillar-based approach.** 4 SMS Pillars × 3 Tiers = clear combination logic.
> Reference: `knowledge/core/content-taxonomy.md` Part 2B

---

## Step 1: BRIEF

Ask:
- **Campaign context:** What event/sale/moment? Is there an email going out same day?
- **SMS Pillar:** Which pillar fits this send? (See taxonomy Part 2B)
  - Pillar 1: Live Chaos (active sale, price shuffles)
  - Pillar 2: Insider Access (pre-launch, exclusive info)
  - Pillar 3: Witch Check-in (non-sale, relationship)
  - Pillar 4: Dark Offer (direct deal, flash)
- **Tiers to write for:** REG / HIGH / MASS (which tiers today?)
- **Offer details:** Discount, product, link, deadline, specific numbers
- **Timing:** Send time? Live-event timestamps needed?

---

## Step 2: LOAD KNOWLEDGE

// turbo
Read: `knowledge/brand/examples/SMS - Friday 13th Sale - Registered Customers.md`
Read: `knowledge/brand/THE SKULLETTE UNIVERSE CAST.txt` — team characters
Read: `learnings/style-rules.md` — SMS checklist at bottom
Read: `knowledge/core/sms-templates.md` — 10 rotating SMS angles (if file exists)

Check `knowledge/core/story-bank.md` — any SMS-relevant ideas?

If email was written today: cross-reference tone and offer details.

---

## Step 3: DRAFT BY TIER + PILLAR

### Pillar 1: Live Chaos
**REG (150-300 words)**
- Timestamp every message: "2:13 PM UPDATE"
- Real-time stats: specific numbers ("16 bags gone in 8 minutes")
- Team chaos: Alice screaming, Jade commentary
- Gothic metaphors for sale mechanics
- Multiple CTAs, countdown to next shuffle
- Sign-off: "Julie (eating popcorn watching this unfold)"

**HIGH (80-150 words)**
- Key update up front (first 2 lines)
- 1 team character reaction
- Specific scarcity number
- One clear CTA link

**MASS (40-80 words)**
- Deal in line 1
- One urgency signal (time or quantity)
- CTA link
- 1 personality touch

---

### Pillar 2: Insider Access
**REG (100-200 words)**
- "You're in the coven" energy — exclusive info, early access
- Conspiratorial tone: "We're not supposed to say this yet..."
- Specific advantage: "You get first pick before we announce tomorrow"
- CTA to private link

**HIGH (60-100 words)**
- Early access angle
- What they get that others don't
- CTA link

**MASS — Pillar 2 not recommended for MASS. Use Pillar 4 instead.**

---

### Pillar 3: Witch Check-in
**HIGH only (40-80 words)**
- Casual, personal, relationship-first
- No hard sell — product mention optional, not required
- Dark humor, Julie's daily life
- Soft CTA: "checking in" not "buy now"

**REG (50-100 words)**
- Slightly more personal than HIGH
- Inside reference to previous campaign or shared moment

---

### Pillar 4: Dark Offer
**MASS (30-60 words)**
- Offer in LINE 1 — no exceptions
- One hook or curiosity line
- CTA link immediately
- Minimal context
- Just enough Julie to not sound automated

**HIGH (50-80 words)**
- Same as MASS but add 1 personality line

**REG — Use Pillar 1 or 2 for REG when possible. Pillar 4 for REG = last resort.**

---

## Step 4: CROSS-REFERENCE WITH EMAIL

If email is going out same day:
- SMS should NOT repeat email story
- SMS = separate angle or live update, not summary of email
- Different hook, different tone, complementary (not duplicate)

---

## Step 5: VARIETY CHECK

Before finalizing, check last 3 SMS sends (from `knowledge/brand/examples/` or archive):
- Same pillar two days in a row? → Adjust
- Same tier always gets same format? → Vary structure
- Any tier getting too many sends this week?

---

## Step 6: CHECKLIST

- [ ] Offer/update in first 2 lines for all tiers
- [ ] Correct length for each tier
- [ ] Specific numbers (not "limited stock" / "selling fast")
- [ ] CTA link present in every message
- [ ] Sounds like Julie (not a text alert)
- [ ] Timestamps present for live-event messages
- [ ] No "VIP" / "EXCLUSIVE" language
- [ ] CAPSLOCK used sparingly (2-3 max per message)
- [ ] Not duplicating today's email story

---

## Step 7: OUTPUT

Present all messages grouped by tier:

```
📱 SMS CAMPAIGN — [Campaign/Event Name] — [Date]
Pillar: [#] — [Pillar Name]

--- REG TIER ---
[full SMS text]

--- HIGH TIER ---
[full SMS text]

--- MASS TIER ---
[full SMS text]
```

⛔ **STOP — Wait for user review.**

After approval: run `/review-craft` for SMS, then `/finalize-sms`.

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
