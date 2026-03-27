# 💀 SKULL-A-PALOOZA — Collection Sale Page Content Outline

> **Dùng cho:** Dev handoff → build HTML for Shopify collection page
> **Page type:** Shopify Collection Page (live sale page — customers use this to SHOP)
> **Go-live:** Mar 17, 10:00 AM ET (hidden until then)
> **URL:** skullette.com/collections/skull-a-palooza

---

## 📌 PAGE CONCEPT

Đây là **trang sale chính** — nơi khách hàng browse và mua sản phẩm. Khác với Landing Page (signup/registration), trang này cần:

- Product grid hiển thị sản phẩm theo ngày drop
- Urgency elements (countdown, sold-out badges, stock alerts)
- Rotatable content theo từng ngày (Day 1 → Day 2 → Day 3)
- Dark carnival aesthetic nhất quán với brand

---

## 🎨 DESIGN SPECS

| Element | Spec |
|---|---|
| **Background** | Black (#0D0D0D) |
| **CTA Buttons** | Hot Pink (#FF2D7B) |
| **Accent** | Electric Purple (#9B59FF) |
| **Text** | Off-white (#F5F0E8) |
| **Alerts/Sold Out** | Neon Green (#39FF14) |
| **Price Tags** | Handwritten/stamp feel (font: Permanent Marker hoặc tương đương) |
| **Headlines** | Bold condensed all-caps, festival poster style (font: Oswald hoặc tương đương) |
| **Body** | Clean readable (font: Inter / Helvetica) |
| **Texture** | Gritty noise overlay, không smooth/corporate |
| **❌ Tránh** | Pastels, clean minimalism, generic red SALE banners, department store vibes |

---

## 📐 PAGE STRUCTURE

```
┌─────────────────────────────────────────┐
│  S1: HERO BANNER                         │
│  (full-width, badge + headline + CTA)    │
├─────────────────────────────────────────┤
│  S2: TODAY'S HEADLINER                   │
│  (featured $9.95 product category)       │
├─────────────────────────────────────────┤
│  S3: TODAY'S PRODUCT GRID                │
│  (all products for today's drop)         │
├─────────────────────────────────────────┤
│  S4: BAGS — THE SIDE STAGE              │
│  (bags $9.95 — $29.95)                   │
├─────────────────────────────────────────┤
│  S5: SOLD OUT HALL OF FAME              │
│  (social proof — what's already gone)    │
├─────────────────────────────────────────┤
│  S6: BOTTOM CTA + COUNTDOWN             │
│  (urgency close)                         │
└─────────────────────────────────────────┘
```

---

## S1: HERO BANNER

> Full-width. Dark bg. Festival poster energy. Changes each day.

### Day 1 (Mar 17)

```
[Badge]         💀 SKULL-A-PALOOZA · DAY 1 OF 3 · THE GATES ARE OPEN
[H1]            WALLETS FROM $9.95.
[Sub]           normally $49.95. today they're not.
[Body]          72 hours. 3 days. New drops daily.
                When it's gone, it's gone.
[Countdown]     SKULL-A-PALOOZA ENDS IN __:__:__:__
```

### Day 2 (Mar 18)

```
[Badge]         💀 SKULL-A-PALOOZA · DAY 2 OF 3 · THE FESTIVAL CONTINUES
[H1]            MINI WALLETS FROM $9.95.
[Sub]           normally $39.95. don't tell our accountant.
[Body]          Day 2 = fresh drops. Yesterday's favorites? GONE.
                New skulls just hit the stage.
[Countdown]     SKULL-A-PALOOZA ENDS IN __:__:__:__
```

### Day 3 (Mar 19)

```
[Badge]         💀 SKULL-A-PALOOZA · FINAL DAY · LAST CALL AT THE DARK CARNIVAL
[H1]            MAKEUP BAGS FROM $9.95.
[Sub]           normally $49.95. last day. last chance.
[Body]          After midnight, SKULL-A-PALOOZA is over.
                No extensions. No "one more day."
[Countdown]     SKULL-A-PALOOZA ENDS IN __:__:__:__
```

### Dev Notes — S1
- Countdown timer: JavaScript, tính đến **Mar 19, 11:59 PM ET**
- Badge + H1 + Sub cần dynamic (thay đổi theo ngày) — có thể dùng Shopify metafields hoặc hardcode swap mỗi sáng
- Mobile: H1 nên 2 dòng max, body text scan-friendly

---

## S2: TODAY'S HEADLINER

> Highlight danh mục sản phẩm chính của ngày. Full-width section, 2-column layout (image trái, copy phải).

### Day 1: WALLETS

```
[Layout]        2 cột: Product Image (trái) | Copy (phải)
[Tag]           🎪 TODAY'S HEADLINER
[H2]            SKULL WALLETS — $9.95
[Price]         $49.95  →  $9.95
                (80% OFF)
[Body]          Premium leather. Skull hardware.
                Wine-dark linings.
                The wallet that makes your
                credit cards feel fancy.

                Every design we carry.
                All at $9.95.
                Until they're gone.
[CTA]           GRAB A WALLET → (links to wallet section in grid)
```

### Day 2: MINI WALLETS

```
[Tag]           🎪 TODAY'S HEADLINER
[H2]            SKULL MINI WALLETS — $9.95
[Price]         $39.95  →  $9.95
                (75% OFF)
[Body]          Compact. Fierce. Fits in your
                back pocket and still turns heads.

                Every skull mini wallet design.
                All at $9.95.
                One day only.
[CTA]           GRAB A MINI WALLET →
```

### Day 3: MAKEUP BAGS

```
[Tag]           🎪 TODAY'S HEADLINER
[H2]            SKULL MAKEUP BAGS — $9.95
[Price]         $49.95  →  $9.95
                (80% OFF)
[Body]          Your makeup deserves better
                than a plastic bag from Target.

                Skull leather. Dark linings.
                The makeup bag that's prettier
                than what's inside it.

                Last day. Last drop.
[CTA]           GRAB A MAKEUP BAG →
```

### Dev Notes — S2
- Price hiển thị kiểu "vintage price tag" — gạch ngang giá cũ, giá mới to + neon green
- Image: product photo của danh mục headliner
- Mobile: stack thành 1 cột (image trên, copy dưới)

---

## S3: TODAY'S PRODUCT GRID

> Shopify product grid — sản phẩm headliner + các SP khác hôm nay

### Grid layout

```
[Section Header]  TODAY'S DROPS 💀

[Filter bar]      All | $9.95 | $11.95 | $13.95 | $14.95 | Bags

[Product Card Layout — mỗi card:]
┌──────────────────────┐
│  [Product Image]      │
│                       │
│  [SOLD OUT overlay    │
│   nếu hết hàng]      │
├──────────────────────┤
│  Product Name         │
│  $49.95  →  $9.95    │  ← giá cũ gạch, giá mới nổi bật
│  [ADD TO CART]        │  ← Hot Pink button
│  💀 Only X left       │  ← nếu stock thấp (≤5)
└──────────────────────┘
```

### Sorting logic (đề xuất)

1. **$9.95 items first** — giá thấp nhất lên đầu
2. Trong mỗi mức giá: **headliner category trước** (Day 1 = wallets đầu, Day 2 = mini wallets đầu)
3. **Sold out items cuối** (hoặc hide, tùy chiến lược)

### Dev Notes — S3
- Product cards: cần hiển thị `compare_at_price` gạch ngang + `price` nổi bật
- Sold Out: overlay neon green (#39FF14), text "SOLD OUT 💀", item không click được
- Low stock badge: "💀 Only X left" khi inventory ≤ 5 — màu Hot Pink, nhấp nháy nhẹ
- Mobile: 2 cột product grid
- Desktop: 3-4 cột
- Filter bar: optional nhưng hữu ích nếu số lượng SP nhiều

---

## S4: BAGS — THE SIDE STAGE

> Section riêng cho bags ($9.95 — $29.95). Số lượng giới hạn → urgency cao.

```
[Section Header]

[H2]            THE SIDE STAGE: SKULL BAGS 🎪
[Sub]           Limited drops. When it sells out, it's NOT restocking.

[Body]          These are the bags. The real deal.
                Normally $100+. Today?
                Starting from $9.95.

                We only have a handful left.
                Once they're gone, the stage goes dark.
```

### Bag Grid

```
┌──────────────────────┐
│  [Product Image]      │
│  [🔥 BAIT badge       │   ← cho SP $9.95 (2-3 items, 1-3 units)
│   nếu $9.95]         │
├──────────────────────┤
│  Noctaflora Small     │
│  Leather Bag          │
│  $XXX  →  $9.95      │
│  [ADD TO CART]        │
│  ⚡ Only 2 left       │   ← ultra-low stock warning
└──────────────────────┘
```

### Tier display rules

| Tier | Giá | Badge | Stock display |
|---|---|---|---|
| 🔥 Bait | $9.95 | "🔥 INSANE DEAL" (neon green bg) | "⚡ Only X left" (luôn hiển thị) |
| 💰 Deal | $29.95 | Không badge, nhưng giá gạch nổi bật | "💀 Only X left" khi ≤ 10 |
| 📦 Regular | TBD | — | Standard stock display |

### Dev Notes — S4
- Section này giữ nguyên cả 3 ngày (bags available xuyên suốt sale)
- Bag $9.95 (bait) cần visual treatment đặc biệt — border neon green, pulse animation
- Real-time inventory hiển thị rất quan trọng ở section này

---

## S5: SOLD OUT HALL OF FAME

> Social proof section — hiển thị sản phẩm đã sold out. Tạo FOMO cho items còn lại.

```
[H2]            SOLD OUT HALL OF FAME 💀
[Sub]           These skulls left the building. Gone forever.

[Sold Out Card Layout:]
┌──────────────────────┐
│  [Product Image]      │
│  [B&W filter /        │   ← greyscale + "SOLD OUT" stamp overlay
│   desaturated]        │
├──────────────────────┤
│  Gothic Rose Wallet   │
│  $9.95                │
│  SOLD OUT in 23 min   │   ← neon green text
└──────────────────────┘
```

### Dev Notes — S5
- Section ẩn khi chưa có SP nào sold out
- Auto-populate khi item inventory = 0
- Sold-out time: nếu có thể track → hiển thị "SOLD OUT in X min/hours"
- Nếu không track được → chỉ hiển thị "SOLD OUT 💀"
- Sắp xếp: mới sold out nhất lên đầu
- Image: desaturate / B&W filter + "SOLD OUT" stamp đỏ hoặc neon green

---

## S6: BOTTOM CTA + COUNTDOWN

> Final urgency section. Hard close.

### Day 1-2

```
[H2]            $9.95 SKULLS WON'T LAST.
[Body]          New drops daily. But once it sells out?
                Gone. No restocks. No extensions.
                The dark carnival doesn't do reruns.
[CTA]           SHOP NOW → (Hot Pink)
[Countdown]     SKULL-A-PALOOZA ENDS IN __:__:__:__
```

### Day 3

```
[H2]            LAST CALL AT THE DARK CARNIVAL. 💀
[Body]          After midnight, these prices die.
                Everything goes back to full price.
                No exceptions. No "one more day."
[CTA]           SHOP NOW — FINAL HOURS → (Gold button #FFD700)
[Countdown]     SKULL-A-PALOOZA ENDS IN __:__:__:__
```

### Dev Notes — S6
- Countdown: same timer as S1, synced to **Mar 19, 11:59 PM ET**
- Day 3 CTA switches to gold (#FFD700) for visual urgency break
- Sticky CTA bar ở bottom mobile (optional nhưng recommended)

---

## 🔧 TECHNICAL REQUIREMENTS

### Dynamic Content (thay đổi theo ngày)

| Section | Day 1 (Mar 17) | Day 2 (Mar 18) | Day 3 (Mar 19) |
|---|---|---|---|
| S1 Hero | Wallets headline | Mini Wallets headline | Makeup Bags headline |
| S1 Badge | "DAY 1 OF 3" | "DAY 2 OF 3" | "FINAL DAY" |
| S2 Headliner | Wallets $9.95 | Mini Wallets $9.95 | Makeup Bags $9.95 |
| S3 Grid sort | Wallets first | Mini Wallets first | Makeup Bags first |
| S5 Hall of Fame | Grows as items sell out | Grows | Grows |
| S6 CTA | Pink button | Pink button | **Gold button** |

### Implementation options

1. **Simplest:** 3 versions of the page, swap manually mỗi sáng
2. **Medium:** Shopify metafields cho dynamic content, swap via admin
3. **Best:** JavaScript date-check → auto-swap content based on EST timezone

### Real-time Inventory

- Shopify AJAX API: `/products/[handle].json` → check `inventory_quantity`
- Low stock badge trigger: inventory ≤ 5
- Sold Out: inventory = 0 → overlay + move to Hall of Fame

### Countdown Timer

- Target: **Mar 19, 2026 11:59:59 PM ET (UTC-4)**
- Format: `DD : HH : MM : SS`
- When expired: show "SKULL-A-PALOOZA IS OVER 💀" static text

### Mobile Responsive

| Element | Desktop | Mobile |
|---|---|---|
| Product grid | 3-4 cột | 2 cột |
| Hero text | Large headline | Smaller, 2 lines max |
| S2 Headliner | 2 cột side-by-side | 1 cột stacked |
| Sticky CTA | Không cần | Sticky bottom bar |

---

## 📋 DAILY DROP SCHEDULE — TỔNG KẾT

| Ngày | 🎪 Headliner ($9.95) | 🎸 Side Stage (bags) | Giá range |
|---|---|---|---|
| **Day 1** (Mar 17) | **Wallets** (normally $49.95) | Small Leather Bags | $9.95 — $29.95 |
| **Day 2** (Mar 18) | **Mini Wallets** (normally $39.95) | Small Leather Bags | $9.95 — $29.95 |
| **Day 3** (Mar 19) | **Makeup Bags** (normally $49.95) | Small Leather Bags + leftover wallets | $9.95 — $29.95 |

---

## ⚡ QUICK REFERENCE — COPY BANK

### Microcopy cho UI elements

| Element | Copy |
|---|---|
| Add to Cart button | ADD TO CART 💀 |
| Sold Out overlay | SOLD OUT 💀 |
| Low stock badge | ⚡ Only X left |
| Ultra-low stock (≤2) | 🔥 Almost gone — X left |
| Price tag | ~~$49.95~~ **$9.95** |
| Empty cart | Your cart is empty. The skulls are waiting. |
| Countdown expired | SKULL-A-PALOOZA IS OVER 💀 See you next time. |
| Collection empty (pre-sale) | 🔒 The gates open March 17 at 10AM ET. |
| Filter: All | ALL DROPS |
| Filter: $9.95 | $9.95 STEALS |

### Page title & meta

```
Title:    SKULL-A-PALOOZA 💀 Skull Bags & Wallets From $9.95 | Skullette
Meta:     72-hour flash sale. Premium skull leather wallets, makeup bags & accessories from $9.95. March 17-19 only. When it's gone, it's gone.
```
