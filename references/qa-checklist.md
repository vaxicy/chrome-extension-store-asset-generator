# Store Asset Visual QA Checklist

Apply this checklist to **every** PNG/JPG produced by the
`generate-store-*.py` scripts, after generation and before delivery. The
generate → self-preview → fix → regenerate loop is mandatory; never assume an
asset "is probably fine" without visually verifying each item.

## 1. Font sizes must scale with the canvas (scale-aware)

- When the same `popup_mock` / component is used at two sizes, the smaller size
  must recompute font sizes proportionally. Do **not** reuse the large font
  sizes — that caused the "像素吸色器" and "4/20 色" labels to overflow in the
  small promo tile.
- Implementation: in `popup_mock`, the `scale < 0.6` branch sets smaller font
  sizes for the title and numbers (one step down each).
- Verify: no text exceeds its container at any scale.

## 2. Banner title vs subtitle spacing

- The gap between the title baseline-bottom and the subtitle top must be
  **≥ 8px** — they must not touch.
- The subtitle bottom (baseline + font descent) must be **< pink-box bottom −
  14px**, so the whole line stays inside the box. (A subtitle once exceeded the
  pink box and was judged "not inside the box".)
- Verify on both the 1280×800 hero and the 1400×560 promo banner.

## 3. Card grids must be even and tidy

- Multiple cards prefer a **2×N or 3×N even grid**. Never leave an "orphan" row
  like 2+2+1. (5 export cards were padded to 6 → 2×3 to stay tidy.)
- Card gap **≥ 10px**; text inside a card must be **≥ 8px** from the card border.
- Verify: row counts divide evenly; no lone card on its own row.

## 4. Bottom-margin safety line

- The bottom edge of any CTA button / white block = start-y + height must be
  **< canvas-height − 12px**.
- Example: 1400×560 canvas → Pro box bottom ≤ 548 (12px reserved). A value of
  570 overflowed the canvas.
- Verify every anchored bottom element against the canvas height.

## 5. Sections must not overlap

- Adjacent sections (e.g. last row of export cards vs the Pro section) must have
  non-intersecting y-ranges. Fix any overlap, even 2px, by moving up or
  compressing.
- Verify by computing the y-intervals of neighboring blocks.

## 6. Section title vs content spacing

- A section title (e.g. "多格式导出") must be **≥ 20px** above the first element
  below it. Do not let it hug the content. (A label once sat almost on top of a
  card.)
- Verify spacing for every section heading.

## 7. Delivery loop: generate → preview → fix → regenerate

- After every change, re-run the script and **self-preview** for overflow /
  alignment / spacing.
- Do not deliver until all of the above pass. Communicate to the user which
  parameters were changed and confirm the regenerate verified them.

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
