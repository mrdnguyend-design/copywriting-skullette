---
description: Process customer emails/reviews into organized voice library for Skullette content
---

# /process-customer-voices — Process Customer Voices

> **Mục tiêu:** Biến email/feedback khách hàng thành kho nguyên liệu có tổ chức cho content
> **Trigger:** User paste emails, reviews, hoặc cung cấp feedback khách hàng

---

## Bước 1: Nhận Input

User cung cấp customer feedback qua: paste trực tiếp, mô tả tóm tắt, hoặc screenshot.

Cần xác định cho mỗi entry:
1. **Tên khách** (first name only) + **Thành phố/State**
2. **Ngày nhận**
3. **Nguồn:** Email reply / DM / Review / Survey
4. **Sản phẩm** được đề cập (nếu có)

> **Privacy first:** Chỉ lưu first name + city. KHÔNG lưu email, phone, hoặc last name.

---

## Bước 2: Phân loại vào 4 Categories

| Category | Dấu hiệu | Folder |
|----------|-----------|--------|
| **Story** | Kể câu chuyện, trải nghiệm cụ thể, có timeline, có dialogue | `customer-voices/stories/` |
| **Compliment** | Ai đó khen bag, brand, Julie — phản ứng tích cực | `customer-voices/compliments/` |
| **Product Feedback** | Nhận xét chất lượng, chi tiết kỹ thuật (leather, zippers, lining) | `customer-voices/product-feedback/` |
| **Suggestion** | Gợi ý sản phẩm mới, charm designs, feature requests | `customer-voices/suggestions/` |

> Nếu entry thuộc 2 categories → ưu tiên category có potential hook cao hơn, ghi cross-ref.

---

## Bước 3: Extract & Format

Lưu mỗi entry theo format:

```markdown
## [ID] Tên khách, Thành phố
- **Date:** YYYY-MM-DD
- **Source:** Email reply / DM / Review / Survey
- **Product:** [Tên sản phẩm] ([Variant]) hoặc "General"
- **Story Source:** [Gothic Mundane / Witch Victory / Basic Brenda Encounter / Product Origin / Cultural Darkness / Julie Personal / Industry Commentary]
- **Quote:** "Giữ nguyên lời gốc, chỉ lược bỏ phần không liên quan..."
- **Context:** [1 dòng bối cảnh — ví dụ: "Cashier at Kroger complimented her Lunacat"]
- **Tags:** #customer-story #lunacat #kroger #age-empowerment
- **Potential Hook:** ⭐⭐⭐⭐⭐ (1-5)
- **Used:** ❌
```

---

## Bước 4: Chấm điểm Potential Hook

| Score | Tiêu chí |
|-------|----------|
| ⭐ | Feedback đơn giản ("I love my bag!"), khó viết thành story |
| ⭐⭐ | Có chi tiết hay nhưng không đủ dramatic |
| ⭐⭐⭐ | Có thể dùng làm supporting detail trong email khác |
| ⭐⭐⭐⭐ | Có scene/moment cụ thể, dễ build thành story (Marianne at Kroger level) |
| ⭐⭐⭐⭐⭐ | Có drama, cảm xúc mạnh, chi tiết vivid, dialogue — SẴN SÀNG viết email (Sharon's bat drawing level) |

### Skullette-Specific Hook Indicators
- Stranger complimenting the bag → ⭐⭐⭐⭐+
- Basic Brenda moment (normie confusion) → ⭐⭐⭐⭐+
- Multigenerational story (mom/daughter/grandma) → ⭐⭐⭐⭐⭐
- Age empowerment ("I'm 57 and...") → ⭐⭐⭐⭐⭐
- Customer drew/created something inspired by Skullette → ⭐⭐⭐⭐⭐
- Partner/husband reaction → ⭐⭐⭐⭐

---

## Bước 5: Lưu & Báo cáo

- Lưu vào `customer-voices/[category]/YYYY-MM.md` (gộp theo tháng)
- Output summary table:

| ID | Tên | Product | Category | Hook ⭐ | Tags |
|----|-----|---------|----------|---------|------|
| CV001 | Marianne, TX | Lunacat Crossbody | Story | ⭐⭐⭐⭐⭐ | #kroger #age #compliment |
| CV002 | Gina, FL | Nyxrose Handbag | Compliment | ⭐⭐⭐⭐ | #valentine #husband |

- Highlight entries ⭐⭐⭐⭐+ và đề xuất dùng cho email tiếp theo

---

## Platform Notes

- **Claude Code (Duc):** Run via `/command` directly in terminal. Full automation.
- **Cowork (team):** Copy workflow steps into conversation. Paste draft into Google Doc for review/comment.
- **Antigravity (team):** Assign as agent task with workspace path `D:\Skullette - Copywriting`.
