# Store Asset Visual QA Checklist

Apply this checklist to **every** PNG/JPG produced by the
`generate-store-*.py` scripts, after generation and before delivery. The
generate → self-preview → fix → regenerate loop is mandatory; never assume an
asset "is probably fine" without visually verifying each item.

All assets must also satisfy the **Localization Rules** at the bottom of this
file (per-language screenshots, bilingual promo, dynamic-copy switching,
hand-drawn-card coordinate recomputation, middot CTA).

## Visual QA Rules (9 items)

### 1. Font sizes must scale with the canvas (scale-aware)

- When the same `popup_mock` / component is used at two sizes, the smaller size
  must recompute font sizes proportionally. Do **not** reuse the large font
  sizes — that caused the "像素吸色器" and "4/20 色" labels to overflow in the
  small promo tile.
- Implementation: in `popup_mock`, the `scale < 0.6` branch sets smaller font
  sizes for the title and numbers (one step down each).
- Verify: no text exceeds its container at any scale.

### 2. Banner title vs subtitle spacing

- The gap between the title baseline-bottom and the subtitle top must be
  **≥ 8px** — they must not touch.
- The subtitle bottom (baseline + font descent) must be **< pink-box bottom −
  14px**, so the whole line stays inside the box. (A subtitle once exceeded the
  pink box and was judged "not inside the box".)
- Verify on both the 1280×800 hero and the 1400×560 promo banner.

### 3. Card grids must be even and tidy

- Multiple cards prefer a **2×N or 3×N even grid**. Never leave an "orphan" row
  like 2+2+1. (5 export cards were padded to 6 → 2×3 to stay tidy.)
- Card gap **≥ 10px**; text inside a card must be **≥ 8px** from the card border.
- Verify: row counts divide evenly; no lone card on its own row.

### 4. Bottom-margin safety line

- The bottom edge of any CTA button / white block = start-y + height must be
  **< canvas-height − 12px**.
- Example: 1400×560 canvas → Pro box bottom ≤ 548 (12px reserved). A value of
  570 overflowed the canvas.
- Verify every anchored bottom element against the canvas height.

### 5. Sections must not overlap

- Adjacent sections (e.g. last row of export cards vs the Pro section) must have
  non-intersecting y-ranges. Fix any overlap, even 2px, by moving up or
  compressing.
- Verify by computing the y-intervals of neighboring blocks.

### 6. Section title vs content spacing

- A section title (e.g. "多格式导出") must be **≥ 20px** above the first element
  below it. Do not let it hug the content. (A label once sat almost on top of a
  card.)
- Verify spacing for every section heading.

### 7. Delivery loop: generate → preview → fix → regenerate

- After every change, re-run the script and **self-preview** for overflow /
  alignment / spacing.
- Do not deliver until all of the above pass. Communicate to the user which
  parameters were changed and confirm the regenerate verified them.

### 8. Button text must be vertically centered + auto-shrink

- In promo tiles (and any CTA button), bilingual text inside the button must be
  **vertically centered against the button's own height**, not pinned to a top-Y
  that drags text to the button's bottom edge (or off the canvas).
- When the font is too large and hugs the edge, **shrink it** (e.g. 中文 17 /
  英文 13 two-line layout). Compute `btn_center_y = btn_y + btn_h // 2` and split
  the two lines around that midline, using anchor `"mm"` for true vertical center.
- Anti-example: the marquee 1400×560 button text once used font 20/14 with a
  high top-Y, dragging the whole line to the bottom edge.
- Verify: button text is centered within the button and never touches the canvas
  bottom.

### 9. Long copy must wrap / condense to avoid truncation

- Detail / description copy (especially **English, which runs longer**) that
  exceeds its container width must be **wrapped or condensed** — never left to be
  clipped into a fragment like "gradient roll b...".
- Implementation: drop redundant words + shrink the font slightly (e.g. 24→22),
  and wrap manually into multiple lines when needed. The `paragraph()` helper in
  `generate-store-screenshots.py` already wraps by `max_width`; use it for long
  blocks.
- Anti-example: an English screenshot detail was once truncated on the right by
  the canvas because the copy was too long and the font too large.
- Verify: no English/Chinese detail line is cut off at the canvas or card edge.

## Localization Rules (store-asset specific)

### A. Screenshots are split by language; promo is bilingual

- **Screenshots**: one set per language, saved under
  `store-assets/screenshots/{zh,en}/`. A `zh` screenshot is **all Chinese**; an
  `en` screenshot is **all English**. Never mix both languages in one screenshot.
- **Promo tiles** (440×280 and 1400×560): MUST be **bilingual** — the same image
  contains both Chinese and English copy so the store backend recognizes
  multi-language and reuses one file. Save under `store-assets/promo/` (no
  `zh`/`en` subdirs).

### B. Mockup "dynamic" copy must switch with the screenshot language

- Any text that looks like the product's **live-generated output** (AI replies /
  recommended options, option-select buttons, simulated emails / senders /
  signatures, search suggestions) must match the screenshot language.
- Do **not** hardcode English placeholders while the banner is translated. Drive
  it from a dictionary keyed by `lang`:
  ```python
  options = {
      "zh": [("积极支持", "中文预览..."), ...],
      "en": [("Positive", "English preview..."), ...],
  }[lang]
  ```
- General rule: any "simulated product output" copy is dynamic and MUST follow
  the language; apply this to **every** per-language screenshot.

### C. Hand-drawn cards: recompute coordinates after edits

- When you change a hand-drawn card's preview rows (e.g. 2→3) or copy length, you
  **MUST recompute** every downstream coordinate: button Y, card height, internal
  spacing. Otherwise elements overlap.
- Preferred: make card height and button position a **function of row count**
  (`card_h = header + rows*line_gap + button_area + pad`); or manually push the
  button Y to (last-row text bottom + safe gap) and grow `card_h`.
- Self-check: open the image; confirm card text and button don't overlap and the
  button fully sits inside the card.

### D. Promo CTA separator is a middot `·`

- Inside a promo CTA button, separate Chinese and English with a **middot `·`**
  (e.g. `立即体验 · Try It Now`) — more elegant and compact than double spaces.

## Cross-cutting checks (apply throughout)

- **Overflow**: all text, color blocks, and cards stay within their container or
  canvas. Watch Chinese/English labels truncated in narrow cards, title-bar text
  hugging edges, and rects with `width=N` stroke that expand outward beyond the
  parent.
- **Alignment**: elements in the same row/group (label + value, icon + text)
  share a vertical center / baseline. When a pixel font mixes with a bold
  regular font, align by visual midline, not just top Y.
- **Spacing**: enough breathing room between cards and between text and margins;
  do not cram content until elements touch edges.
