---
description: Write a Skullette infotainment email in Julie's voice — Full or Quick mode
---

# /write-email — Infotainment Copywriter

> **Email types:** daily (daily_), sale (sale_), teaser (teaser_)
> **2 modes:** Full (important dailies + campaign emails) | Quick (simple dailies)

---

## Mode Selection

**Full Mode** (5 phases: Brief → Brainstorm → Draft → Self-Check → Output)
- Campaign emails (any Job)
- High-stakes daily emails
- New product launches
- Any email where you need strong story development

**Quick Mode** (3 phases: Brief → Draft → Output)
- Simple daily emails with clear story seed already from /daily-brief
- CLOSE / LIVE / THANK emails in a campaign (structure-driven, not story-driven)
- When user provides complete brief with story seed

---

## FULL MODE

### Phase 1: BRIEF

Load from `/daily-brief` if already run today. Otherwise ask:

- **Email type:** Daily / Sale / Teaser?
- **Campaign Job** (if campaign): Which job in the sequence?
- **Story Source** (if daily): Which Story Source? (from taxonomy)
- **Story seed:** Any specific scene or hook in mind?
- **Product/Broccoli:** Which bag or offer to feature?
- **Audience segment:** MASS / HIGH / REG?
- **Tone:** Gothic Mundane / Live Chaos / Coven Chronicles / Dark vs Beige?
- **Campaign context:** Standalone / day X of Y?

// turbo
Read: `knowledge/core/content-taxonomy.md`, `knowledge/core/content-standards.md`, `knowledge/brand/THE SKULLETTE UNIVERSE CAST.txt`, `learnings/style-rules.md`

---

### Phase 2: BRAINSTORM

// turbo
Read 1-2 relevant examples from `knowledge/brand/examples/`
Read: `knowledge/frameworks/infotainment-jackpot/INFOTAINMENT JACKPOT - THE PLAYBOOK.txt`

Roleplay 2 expert personas → Output **3-5 diverse approaches**, each using a different angle.

For each approach:

1. **Name** — e.g., "The Kroger Stare"
2. **Story Source + Pillar** — e.g., Gothic Mundane → Pillar 1
3. **Hook draft** — 3-5 sentence opening blockquote showing entry into the scene
4. **Pivot strategy** — How does the story connect to product?
5. **Why it works** — Ben's OR Daniel's perspective (1 sentence)

**Scoring table:**

| # | Approach | Entertainment | Pivot | Voice | Risk | Pick |
|---|----------|--------------|-------|-------|------|------|
| 1 | | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Low | ✅ |

⛔ **STOP — Wait for user to choose approach.**

---

### Phase 3: DRAFT

Write the complete email based on chosen approach.

#### Structure:

**Subject Line** (from /finalize-email — but draft 1 working version now)

**Preview Text** (1 line, complements subject, doesn't repeat)

**The Hook**
- Drops into action or specific scene
- ❌ Never: "Hey witch!" / "Happy [holiday]!" / "I hope..."
- ✅ Always: dialogue, action, or a specific moment
- Sensory details: leather, old books, rain, extinguished candles, coffee, incense
- Inner thoughts: (parenthetical asides)

**The Narrative Arc**
- Build the scene. Real dialogue. Show don't tell.
- "Her face went through three emotions in half a second" > "She was surprised"
- CAPSLOCK for drama. (Parentheses for inner thoughts.)
- 5th-grade reading level. Punchy. Lots of line spacing.

**The Turn**
- Expectation vs. reality gap
- Julie's reaction — internal or external

**The Pivot**
- Bridge: story → Big Idea → product
- Earned, not bolted on
- Options: "It made me realize something..." / "Here's the thing." / Lead with customer quote

**The Offer/Product**
- Product as weapon, armor, warning — not spec sheet
- "The Moonreaver isn't a bag. It's a declaration of intent."
- For sale emails: OFFER IN FIRST THIRD, multiple CTAs, specific scarcity numbers

**The CTA**
- Command voice: "Go claim your armor." / "Hunt it here." / "Wield this."
- Optional indifference: "Or don't. I won't beg."

**Sign-off**
- "Stay spooky," / "Stay wicked," / "Stay weird," / "Stay in control,"
- Julie, Founder, Skullette.com

**P.S.**
- Scarcity reminder / secondary CTA / witty close / future tease
- Must work as standalone

---

### Phase 4: SELF-CHECK

Run before presenting draft:

- [ ] Julie IN the scene (not narrating from outside)?
- [ ] Scene has: location + 2 sensory details + Turn + Julie's inner life?
- [ ] Voice passes the Julie Test?
- [ ] No anti-patterns triggered? (check taxonomy Part 5)
- [ ] For sale: offer in first third? Specific scarcity? Multiple CTAs?
- [ ] Pivot earned (not bolted on)?
- [ ] No AI-isms (em dash overuse, triple-And anaphora, purple prose)?

If anything fails: fix before presenting.

---

### Phase 5: OUTPUT

Present clean draft. Note:
> "Draft complete. Run `/review-craft` → `/review-strategy` → `/review-brand` before publishing."
> "After all reviews approved: run `/finalize-email`"

⛔ **STOP — Wait for user to review or run review agents.**

---

## QUICK MODE

### Phase 1: BRIEF (condensed)

Take brief from `/daily-brief` or ask:
- Story seed? Product? Email type? Segment?

### Phase 2: DRAFT

Write the email. Same structure as Full Mode Phase 3.
No brainstorm — go straight to draft based on brief.
Run Phase 4 Self-Check internally before presenting.

### Phase 3: OUTPUT

Present draft with note to run review agents.

---

## Phase Gate Rules

| Transition | Action |
|------------|--------|
| Phase 1 → 2 | Automatic (after brief complete) |
| Phase 2 → 3 | ⛔ STOP — Wait for user to choose approach |
| Phase 3 → 4 | Automatic (self-check before presenting) |
| Phase 4 → 5 | Automatic |
| After Output | ⛔ STOP — User runs review agents independently |

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
