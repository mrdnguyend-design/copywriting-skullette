---
description: Critique a Skullette email/SMS draft as Ben Settle and Daniel Throssell
---

# /critique — Standalone Brainstorm & Critique

> **Dùng độc lập** — Không cần chạy full `/write-email` workflow
> **Trigger:** User có draft và muốn review/improve

---

## Bước 1: Nhận Draft

Ask user for the draft to critique:
- Paste trực tiếp trong chat
- Reference last draft from current conversation
- File path to an existing draft

---

## Bước 2: Load Knowledge

// turbo
1. Read `knowledge/frameworks/infotainment-jackpot/INFOTAINMENT JACKPOT - THE PLAYBOOK.txt` — Ben Settle's 21 Laws
// turbo
2. Read `knowledge/frameworks/gameshow/GAMESHOW.txt` — Daniel Throssell's framework
// turbo
3. Read `knowledge/brand/BRAND CONTEXT & MEMORY.md` — Key learnings on what works/fails

---

## Bước 3: Ben's Review (Marketing & Hook)

Adopt Ben Settle's voice. Direct, blunt, opinionated. No corporate politeness.

| Tiêu chí | Score ⭐/5 | Nhận xét |
|----------|-----------|----------|
| **Hook Power** | | Dòng đầu có stop the scroll? |
| **Personality** | | Julie có hiện diện mạnh mẽ? CAPSLOCK, (parentheses), dark humor? |
| **Status Positioning** | | Reader cảm thấy là insider? Julie là The Prize, không phải kẻ cầu xin? |
| **Sales Psychology** | | CTA có irresistible? Urgency tự nhiên hay gượng ép? |
| **Polarization** | | Đủ mạnh để repel Basic Brendas? Hay đang please everyone? |

**Line-by-line improvements:**
- Quote exact lines + suggest rewrites
- Focus on: hook strength, personality injection, selling mechanics

---

## Bước 4: Daniel's Review (Story & Craft)

Adopt Daniel Throssell's voice. Thoughtful, craft-focused, specific.

| Tiêu chí | Score ⭐/5 | Nhận xét |
|----------|-----------|----------|
| **Scene Construction** | | Đọc lên có thấy, nghe, ngửi được? Hay chỉ là tóm tắt? |
| **Dialogue** | | Conversations có real, natural? Hay manufactured? |
| **Show vs Tell** | | Show emotion qua action? Hay just state "I was happy"? |
| **Emotional Pacing** | | Tension build và release đúng nhịp? |
| **Specificity** | | Chi tiết cụ thể ("third coffee at 9AM," "6 minutes") hay chung chung? |

**Line-by-line improvements:**
- Quote exact lines + suggest rewrites
- Focus on: scene stacking, sensory details, emotional arc

---

## Bước 5: Logic Check

- [ ] **Character consistency** — Julie/Alice/Jade/customers in-character?
- [ ] **Timeline logic** — Timestamps/events make sense? (Không viết "sáng nay" nhưng email gửi buổi tối)
- [ ] **Emotional arc** — vulnerability → revelation → pride → action?
- [ ] **Scene believability** — Tình huống có thể xảy ra ngoài đời? Không quá scripted?
- [ ] **Voice check** — Nghe như witchy best friend, hay corporate copywriter?
- [ ] **Cultural sensitivity** — Bold mà không alienate target audience (women 30+)?

---

## Bước 6: Joint Assessment

### Overall Score: ⭐/5

### Top 3 Strengths
1. ...
2. ...
3. ...

### Top 3 Improvements Needed
1. (Highest impact)
2. ...
3. ...

### Priority Revision Table

| Priority | Issue | Exact Line | Suggested Rewrite |
|----------|-------|-----------|-------------------|
| 1 | [Most impactful] | "original line..." | "improved version..." |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |

---

## Bước 7: Revise (nếu cần)

- Nếu Overall Score < ⭐⭐⭐⭐: Tự động tạo revised draft kèm theo
- Nếu Overall Score ≥ ⭐⭐⭐⭐: Hỏi user muốn revise không

Present revised version side-by-side với original cho easy comparison.

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
