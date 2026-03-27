# 📧 Skullette Email HTML Format

> **Usage:** Phase 6 (FINALIZE) of `/write-email` workflow
> **Rule:** Mỗi paragraph wrap trong `<p><span>` tag. Dùng `<strong>` cho câu cần bold.

## Paragraph Format

Mỗi paragraph/dòng trong email → wrap trong:

```html
<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">
  Content here
</span></p>
```

## Bold Text

Thêm `<strong>` khi câu cần được nhấn mạnh:

```html
<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">
  <strong>They're GONE. EXTINCT. FOREVER.</strong>
</span></p>
```

## Khi nào dùng `<strong>`:
- CAPSLOCK sentences (emphasis moments)
- CTA lines ("Shop now", "Grab yours", "Click here")
- Key offer details ("50% OFF", "FREE matching wallet")
- Dramatic one-liners
- Sign-off line ("Stay spooky,")

## Khi KHÔNG dùng `<strong>`:
- Storytelling paragraphs (để flow tự nhiên)
- Parenthetical asides
- P.S. content (trừ khi có offer/scarcity)

## Example: Full Email Conversion

### Plain Text:
```
I'm sitting at my desk right now with my third coffee.

(The first two clearly didn't work.)

And then I open this email from Marianne in Texas.

She took her Lunacat to Kroger. KROGER.

The cashier stopped scanning her groceries mid-beep and said: "Ma'am, where did you get THAT bag?"

Here's the thing.

Nobody stops you at Kroger for a beige tote.

Shop the Lunacat Crossbody → [LINK]

Stay spooky,
Julie
Founder, Skullette.com
```

### HTML:
```html
<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">I'm sitting at my desk right now with my third coffee.</span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">(The first two clearly didn't work.)</span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">And then I open this email from Marianne in Texas.</span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;"><strong>She took her Lunacat to Kroger. KROGER.</strong></span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">The cashier stopped scanning her groceries mid-beep and said: "Ma'am, where did you get THAT bag?"</span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">Here's the thing.</span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;"><strong>Nobody stops you at Kroger for a beige tote.</strong></span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;"><strong><a href="{{LINK}}">Shop the Lunacat Crossbody →</a></strong></span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;"><strong>Stay spooky,</strong></span></p>

<p><span style="font-size: 16px; font-family: Helvetica, Arial, sans-serif; font-weight: 400;">Julie<br>Founder, Skullette.com</span></p>
```
