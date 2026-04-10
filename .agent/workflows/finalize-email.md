---
description: Finalize email — HTML output, archive, kaizen log entry, story bank update
---

# /finalize-email — Email Finalize

> **Chạy sau khi draft đã qua 3 review agents và user đã approve.**
> Output: HTML ready for Klaviyo + archived files + kaizen log entry

---

## Step 1: CONFIRM APPROVED DRAFT

Ask if no draft provided: "Paste the final approved email draft."

Confirm: "Is this the final approved version? Have all 3 review agents been run?"

---

## Step 2: FINAL PROOFREAD PASS (Throssell-Style Audit)

Before generating HTML, run a final quality gate based on Daniel Throssell's "Adventures in Copyland" methodology.

### 2A. Diagnose — Check for 6 Patterns of Failure

Scan the approved draft for:

1. **Stunted Pacing:** Rushes through events without visual detail or tension?
2. **Missing the Point:** Fails to identify the true humor or core tension of the story?
3. **Lead Failure (Rule #28):** Is the opening Relevant, Entertaining, AND Brief? (Must hit at least two.)
4. **Muddled Argument:** "Word slop" of conflicting sales ideas instead of a single "Greased Slide"?
5. **Weak Insight (Rule #42):** Is the "tip" too obvious or generic? Fails to expand the reader's mind?
6. **No Sales Desire:** Pitch feels "bolted on" without making the reader *want* the product?

### 2B. Check AI Tells

- **Em Dash Count:** Count em dashes (—). More than 2-3 per email = AI fingerprint. Replace with periods, commas, parentheses, or ellipses. ONE dramatic pause per email max.
- **Anti-Staccato:** Check for AI trap of every sentence being 3 words long. Ensure natural, conversational flow with varied sentence lengths.
- **Triple-And Anaphora:** "And she... And she... And she..." = AI pattern. Cut or restructure.

### 2C. Decision

- **If 0 issues found:** Proceed to Step 3 (HTML).
- **If minor issues (1-2):** Fix inline, note in output, proceed.
- **If major issues (3+):** Flag to user: "Draft has [N] quality issues. Recommend running `/review-craft` again before finalizing." List issues. Wait for user decision.

---

## Step 3: GENERATE HTML

Read `knowledge/templates/` for HTML template if available.

Convert the plain text draft to HTML using these rules:

**Each paragraph:**
```html
<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">
  Content here
</span></p>
```

**Bold / CAPSLOCK sentences:**
```html
<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">
  <strong>SHE BOUGHT SEVENTEEN. IN ONE SESSION.</strong>
</span></p>
```

**Rules:**
- Each short punchy line = its own `<p><span>` block
- CAPSLOCK sentences → wrap in `<strong>`
- CTA lines → wrap in `<strong>`
- (Parenthetical asides) → keep inside `<span>`, no italic
- Links: `<a href="{{URL}}">Link Text</a>` inside `<span>`

---

## Step 4: GENERATE SUBJECT LINE OPTIONS

Provide 5 subject line options:

| # | Type | Subject Line |
|---|------|-------------|
| 1 | Curiosity/Dark | |
| 2 | Confession/Personal | |
| 3 | Story-driven | |
| 4 | Weird/Specific | |
| 5 | Direct (for sale emails) | |

Ask user to select one (or provide their own).

---

## Step 5: ARCHIVE

Determine file naming:
- Type prefix: `daily_` / `sale_` / `teaser_`
- Date: `[DDMMYY]`
- Short name: 2-3 word description

Save to `campaigns/_active/[campaign-name]/emails/` if part of campaign,
OR `klaviyo/campaigns/2026-Q2/` for standalone emails.

Files to save:
1. `[type]_[DDMMYY]_[name].md` — Plain text final draft
2. `[type]_[DDMMYY]_[name].html` — HTML ready for Klaviyo

---

## Step 6: KAIZEN LOG ENTRY

Add entry to `learnings/post-mortems.md`:

```markdown
### Entry #[next number] — [YYYY-MM-DD]
**Email:** [file name]
**Type:** [Daily / Sale / Teaser]
**Story Source:** [from taxonomy]
**Email Pillar:** [1-4]
**Product:** [product featured]
**Rating:** [⭐ to ⭐⭐⭐⭐⭐ — ask user]

**What Worked:**
- [specific technique or line that was strong]
- [scene/hook that landed]
- [structure choice that worked]

**What Needed Revision:**
- [corrections made during review]
- [patterns to avoid next time]

**Notes:**
[Any unusual context, campaign position, test element]
```

---

## Step 7: STORY BANK UPDATE

1. Find the story used in `knowledge/core/story-bank.md`
2. Move from READY → USED:
```
**[Title]** — USED [date]
- Email: [filename]
- Story Source: [source]
- Notes: [brief note]
```
3. Update Story Source Coverage table (date + count)

4. Check if any UNUSED elements from brainstorm can become new SEEDs:
   - Any rejected approaches from write-email Phase 2 with potential? → Add as SEED
   - Any customer detail mentioned but not developed? → Add as SEED

---

## Step 8: COMPLETE

Output:

```
✅ FINALIZED

Files saved:
- [path to .md]
- [path to .html]

Subject line selected: "[chosen subject]"
Preview text: "[preview text]"

Kaizen log: Entry #[X] added
Story Bank: [story name] → USED | [X] new seeds added

Story Bank health: [X] READY items remaining
[If < 3: "Run /idea-research soon"]

Next: /finalize-sms (if SMS was written) or /sync-klaviyo to push to platform
```

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
