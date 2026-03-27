---
description: Write SMS campaign messages for Skullette (sale updates, promos, engagement)
---

# /write-sms — SMS Campaign

> **Mục tiêu:** Viết SMS cho Skullette campaigns — sale updates, promos, engagement
> **Đặc thù:** SMS có format khác email (ngắn hơn, urgent hơn, personality-dense)

---

## Bước 1: Nhận Brief

Hỏi user:
- **Campaign context:** Event gì? (Friday 13th, BOGO, flash sale, new launch, engagement)
- **Audience tier:** Segment nào?
  - 🔴 **Registered participants** — Insider tier. Longer messages OK. Full chaos mode.
  - 🟡 **High-engaged customers** — Warm audience. Medium length. Exciting but focused.
  - 🟢 **Mass subscribers** — Ngắn nhất. Clear offer. Minimal context needed.
- **Number of messages:** Bao nhiêu SMS trong sequence này?
- **Offer details:** Discount, products, links, deadlines
- **Tone:** Chaos/live-event vs. casual update vs. urgent last-chance
- **Timing:** Timestamps cho mỗi message (nếu live-event style)

---

## Bước 2: Load Knowledge

// turbo
1. Read `knowledge/brand/examples/SMS - Friday 13th Sale - Registered Customers.md`
// turbo
2. Read `knowledge/brand/THE SKULLETTE UNIVERSE CAST.txt` — Team characters (Alice, Jade)

---

## Bước 3: Draft Messages Per Tier

### 🔴 Registered Participants (Insider Tier)
- **Length:** 150-300 words per message
- **Tone:** Julie texting her inner circle. CAPSLOCK chaos. (Parenthetical asides).
- **Must include:**
  - Real-time updates with timestamps ("10:13 AM UPDATE")
  - Team character moments ("ALICE just screamed across the building")
  - Specific customer wins ("Some WITCH in Texas scored a $9.95 Roselace in 6 MINUTES")
  - Gothic humor throughout ("Russian roulette but make it GOTH")
  - Countdown to next event (price shuffle, new drop)
  - Exact numbers ("284 bags left," not "limited stock")
- **Sign-off:** Short + personality ("Julie (eating popcorn watching this chaos unfold)")
- **CTA:** Link embedded in context ("Hunt here before someone else does → [LINK]")

### 🟡 High-Engaged Customers
- **Length:** 80-150 words
- **Tone:** Excited but focused. "Here's what you need to know" energy.
- **Must include:**
  - Key offer details up front (first 2 lines)
  - 1-2 personality touches (not full chaos mode)
  - Clear CTA link
  - Scarcity/urgency element (specific number or deadline)
- **Sign-off:** "Julie" + one-liner
- **CTA:** Direct with link

### 🟢 Mass Subscribers
- **Length:** 40-80 words
- **Tone:** Direct, clear, benefit-first
- **Must include:**
  - Offer in the FIRST LINE
  - One hook or curiosity element
  - CTA link immediately after
  - Just enough personality to not sound corporate
- **Sign-off:** "Julie" or "— Skullette"
- **CTA:** Single clear link

---

## Bước 4: Live-Event Elements (nếu applicable)

For live sale campaigns (Friday 13th style):
- **Timestamp** mỗi message ("10:13 AM UPDATE," "2:45 PM — ROUND 3")
- **Real-time stats** ("SIXTEEN BAGS ARE GONE," "284 left")
- **Narrative escalation** across messages (calm → excited → chaos → "I've lost control")
- **Team reactions** as proof of excitement (Alice screaming, Jade's commentary)
- **Tease next round** — "Prices shuffle again at 1:13 PM. Set your witch alarms."
- **Gothic metaphors** for sale mechanics ("death ring," "danger zone," "extinction")

---

## Bước 5: Checklist

- [ ] Does each message have a clear CTA link?
- [ ] Is the offer/update obvious within the first 2 lines?
- [ ] Does it sound like Julie (not a corporate SMS)?
- [ ] Is the length appropriate for the audience tier?
- [ ] For live-event: does each message escalate energy?
- [ ] Is there a reason to check back? (next shuffle time, new drop tease)
- [ ] Are numbers specific? ("16 bags gone" not "selling fast")
- [ ] Are team characters in-character? (Alice = energetic, Jade = designer focus)

---

## Bước 6: Present All Messages

Show all SMS messages in sequence.
- Label each with: **audience tier + timestamp** (if applicable)
- Group by tier if writing for multiple segments

**DỪNG — Chờ user review.**

---

## Bước 7: Revise & Finalize

Apply user feedback and present revised versions.
Save final SMS set to `knowledge/brand/examples/SMS - [Campaign Name].md` for future reference.
