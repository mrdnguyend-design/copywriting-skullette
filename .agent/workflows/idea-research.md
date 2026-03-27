---
description: Research and brainstorm daily email ideas from reviews, news, and cultural calendar for Skullette
---

# /idea-research — Daily Idea Research

> **Mục tiêu:** Tìm và brainstorm ý tưởng câu chuyện mới từ nhiều nguồn
> **Output:** 3-5 ý tưởng email với Hook + Bridge + Product

---

## Bước 1: Scan Customer Voices (Stored Stories)

// turbo
1. Scan `customer-voices/` cho entries chưa dùng (`Used: ❌`) có Potential ⭐⭐⭐⭐+
2. Read `knowledge/brand/examples/` để tránh lặp lại angles đã dùng
3. **Tìm kiếm:** Entries có câu chuyện cá nhân, chi tiết cảm xúc, dialogue, drama

---

## Bước 2: Scan Reviews Online

// turbo
Scan reviews mới từ 3 nguồn:
1. **TrustPilot:** https://www.trustpilot.com/review/skullette.com
2. **Store Reviews:** https://skullette.com/pages/skullette-reviews
3. **Facebook Fanpage:** https://www.facebook.com/skullette.official/ (posts, comments, tagged photos)

**Tìm kiếm:**
- Reviews có câu chuyện cá nhân (stranger compliments, partner reactions)
- Reviews đề cập specific moments/scenes
- Reviews có emotional language mạnh
- Reviews từ recurring customers (collectors, "I have 8 Skullettes now")
- Facebook comments/posts có UGC (photos, drawings, unboxing reactions)

---

## Bước 2B: Scan Reddit (5-Phase Idea & Language Mining)

Reddit là nguồn idea VÀ ngôn ngữ audience quan trọng nhất. Thực hiện đủ 5 phases dưới đây.

---

### Phase 1: Reddit Search — Keyword Clusters 🔍

// turbo
Dùng `search_web` với các search queries dưới đây. Chạy **ít nhất 3/5 clusters** mỗi session.

| Cluster | Search Query |
|---------|-------------|
| **"Too Much" Identity** | `site:reddit.com "too much" OR "extra" OR "over the top" (goth OR alternative OR dark)` |
| **Goth in Mainstream** | `site:reddit.com "people stare" OR "judged for" OR "weird looks" (fashion OR style OR outfit)` |
| **Age & Style Rebellion** | `site:reddit.com "too old to wear" OR "dress your age" OR "age appropriate" (fashion OR style)` |
| **Bag as Identity** | `reddit "my bag" OR "purse" OR "daily carry" gothic OR skull OR dark OR alternative accessory` |
| **Dark Feminine Energy** | `site:reddit.com "dark feminine" OR "witch energy" OR "don't mess with me" OR "witchy"` |

**Nếu cluster không trả kết quả tốt** → thêm subreddit cụ thể vào query, ví dụ: `site:reddit.com/r/GothFashion "too much"`

> ⚠️ **KHÔNG dùng year filter** (e.g. "2025", "2026") — Reddit content là evergreen, year filter sẽ trả 0 kết quả.

---

### Phase 2: Browse Subreddits — Tier Priority & Rate Limit 📖

// turbo
Chọn **3-4 subreddits** dựa trên context ngày hôm nay (event, product push, emotion target). Đọc top/hot posts từ tuần gần nhất.

**Search Strategy (PRIMARY = search_web):**
- **Cách 1 (Primary):** `search_web` query: `reddit r/{subreddit} {topic keyword}` — ví dụ `reddit r/GothStyle strangers compliment goth outfit`
- **Cách 2 (Backup):** `read_url_content` trên Reddit URL — thường bị rate-limit, dùng khi Cách 1 không đủ
- Mỗi subreddit **tối đa 2 searches**. Ưu tiên Tier 1-2 trước. Chỉ xuống Tier 3-5 nếu Tier 1-2 không đủ material.

#### 🔴 Tier 1: Đúng tệp khách — Gothic/Alternative Women
| Subreddit | What to look for |
|-----------|-------------------|
| r/GothFashion | OOTDs, bag/accessory posts, "where to find..." |
| r/GothStyle | Compliment stories, "people stare at me" moments |
| r/AltFashion | Alt accessory finds, confidence stories |
| r/DarklyInclined | Gothic lifestyle conversations, dark aesthetic appreciation |
| r/WitchesVsPatriarchy | "Too much" celebrations, empowerment stories, witchy humor |

#### 🟡 Tier 2: Women 30+ & Empowerment
| Subreddit | What to look for |
|-----------|-------------------|
| r/AskWomenOver30 | "I stopped caring what people think" moments, self-expression |
| r/oldhagfashion | Age-defying fashion, bold style choices |
| r/femalefashionadvice | Bag threads, "not like basic" conversations |
| r/TwoXChromosomes | Personal victories, gender dynamics |

#### 🟢 Tier 3: Dark Culture
| Subreddit | What to look for |
|-----------|-------------------|
| r/DarkRomance | Dark emotional language, metaphors |
| r/horror | Pop culture tie-ins, skull aesthetics, horror as lifestyle |
| r/witchcraft | Dark feminine energy, rituals, moon phases |
| r/tarot | Self-discovery stories, spiritual moments |

#### 🔵 Tier 4: Product-Adjacent
| Subreddit | What to look for |
|-----------|-------------------|
| r/handbags | "Why I love my bag" stories, alt bag requests |
| r/BuyItForLife | Leather quality discussions, longevity stories |

#### ⚪ Tier 5: Seasonal/Event-Based (chọn khi phù hợp)
| Subreddit | When to use |
|-----------|-------------|
| r/halloween | Halloween countdown, spooky season nostalgia |
| r/crystals | Moon events, spiritual aesthetic moments |
| r/childfree | "Unapologetic lifestyle" angles |
| r/antiwork | "I don't owe anyone" rebellion energy |

---

### Phase 3: Đào sâu Comments — High-Engagement Posts 💬

// turbo
Với mỗi post tìm được ở Phase 1-2 mà có **≥20 comments VÀ ≥50 upvotes**:

1. Đọc **top 25 comments** (sort by Best)
2. Tìm kiếm trong comments:
   - **Câu chuyện cá nhân** có chi tiết cụ thể (tên, nơi chốn, dialogue)
   - **Cảm xúc mạnh** — frustration, pride, defiance, belonging
   - **Recurring phrases** — cách audience nói về vấn đề (không phải cách brand nói)
   - **Unpopular opinions** — góc nhìn controversial = email hooks tốt
   - **"Me too" replies** — nhiều upvotes = shared pain/desire = big email angle

**Nếu không tìm post đủ engagement** → hạ threshold xuống ≥10 comments, ≥25 upvotes

---

### Phase 4: Extract Ngôn ngữ Audience — Mini-Glossary 🗣️

// turbo
Từ tất cả content đã đọc ở Phase 1-3, trích xuất và ghi lại:

```
### 🗣️ REDDIT LANGUAGE CAPTURE — [Ngày]

#### Exact Quotes (giữ nguyên ngôn ngữ gốc)
| Quote | Subreddit | Post Context | Emotion | Dùng cho |
|-------|-----------|-------------|---------|----------|
| "I wear skulls because they scare boring people away" | r/GothFashion | OOTD thread | rebellion/pride | Subject line, CTA |
| "my husband calls it my 'don't talk to me' bag" | r/handbags | daily carry | humor/identity | Seinfeld Email hook |

#### Slang & Phrases hay
| Phrase | Meaning in context | Dùng cho |
|--------|--------------------|---------| 
| "normie repellent" | Thứ gì đó đuổi người bình thường | Product description, email hook |
| "giving main character energy" | Tự tin không cần approval | Subject line |

#### Pain Points & Desires
| Pain/Desire | Example Quote | Frequency | Email Angle |
|-------------|--------------|-----------|-------------|
| Bị judge vì style dark sau 30 | "my coworkers think I'm going through a phase... I'm 42" | Rất phổ biến | Age rebellion email |
| Muốn tìm accessories dark nhưng chất lượng | "everything goth is cheap costume quality" | Phổ biến | Quality positioning email |
```

**Lưu ý:** Mỗi session cần **ít nhất 5 quotes, 3 phrases, 3 pain points** — nếu chưa đủ, quay lại Phase 2-3 đọc thêm.

---

### Phase 5: Ghi lại Findings — Structured Template 📋

// turbo
Cho mỗi Reddit finding có tiềm năng thành email idea, ghi theo template:

```
### 🔖 REDDIT FINDING [#]
- **Source:** [Subreddit] — [Link/Post title nếu có]
- **Post Summary:** [1-2 câu tóm tắt]
- **Best Quote:** "[exact quote từ post hoặc comment]"
- **Why It's Good:** [Giải thích tại sao finding này có hook potential]
- **Hook Potential:** [Cách biến thành email hook — 1 câu]
- **Bridge to Product:** [Sản phẩm Skullette nào phù hợp nhất]
- **Brand Tension:** ["Too much" / Age rebellion / Dark feminine / Goth mainstream / Bag identity]
- **Potential:** ⭐⭐⭐⭐⭐ (1-5)
```

**Minimum output:** 2-3 Reddit Findings có ≥⭐⭐⭐. Nếu không tìm đủ → mở rộng sang Tier 3-5 hoặc chạy thêm keyword clusters.

---

## Bước 3: Scan Tin tức & Văn hóa

// turbo
1. Search web cho tin tức liên quan đến gothic culture, dark aesthetics, female empowerment
2. Check ngày hôm nay — có gì đặc biệt?
   - Full moon? Mercury retrograde?
   - Gothic/horror pop culture events (movie releases, anniversaries)
   - Seasonal moments (Halloween countdown, Friday the 13th, Valentine's, etc.)
   - Women's empowerment dates
3. Tìm viral moments, memes, or cultural conversations liên quan đến "being too much"

---

## Bước 4: Brainstorm & Chọn lọc

// turbo
Cho mỗi ý tưởng, read `knowledge/frameworks/infotainment-jackpot/INFOTAINMENT JACKPOT - THE PLAYBOOK.txt` và xác định:

| Element | Câu hỏi |
|---------|---------|
| **Hot Dog (Hook)** | Câu chuyện gì khiến người đọc PHẢI đọc tiếp? |
| **Broccoli (Product)** | Sản phẩm/feature nào cần push? Bag nào phù hợp? |
| **Law (Vehicle)** | Dùng Law nào từ Playbook? (#1 Personality, #5 Mocking, #9 Pop Culture, #15 Intimate, #18 Polarization...) |
| **Mechanism** | Seinfeld Email, Simplicio Dialogue, Upstairs Troll, Pop Culture Analogy? |
| **Dark Emotion** | Mystery, rebellion, power, belonging, indifference, "too much"? |

---

## Bước 5: Output Format

Trình bày 3-5 ý tưởng:

```
## IDEA [#]: [Tên ngắn]
- **Source:** [Customer Voice / Review / News / History / Cultural Calendar]
- **Hot Dog:** [Hook story 1-2 câu — vivid, specific]
- **Broccoli:** [Product/feature to sell]
- **Law:** [Từ Playbook — e.g., Law #1 Personality + #15 Intimate Details]
- **Mechanism:** [Từ Glossary — e.g., Seinfeld Email]
- **Dark Emotion:** [e.g., "Age empowerment + rebellion against 'act your age'"]
- **Subject Line Ideas:** [2-3 options]
- **Potential Rating:** ⭐⭐⭐⭐⭐ (1-5)
```

---

## Bước 6: Chờ User Chọn

Sắp xếp ideas theo Potential Rating (cao nhất trước).

**DỪNG — Chờ user chọn idea.**

Khi user chọn → chuyển sang `/write-email` workflow với idea đã chọn làm brief.
