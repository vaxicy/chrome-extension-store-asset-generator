# Store Asset Visual QA Checklist (Comprehensive)

Apply this checklist to **every** PNG/JPG produced by the `generate-store-*.py`
scripts, after generation and before delivery. The
**generate → self-preview → fix → regenerate** loop is mandatory; never assume
an asset "is probably fine" without visually verifying each item via `read_file`
on **every** PNG (not just a sample).

All assets must also satisfy the **Localization Rules** (§20) and the **10-item
self-check** (§21) at the bottom.

---

## 0. Mandatory delivery loop (highest priority)

```
1. edit script → 2. run generate → 3. self-preview (read_file every PNG) →
4. find issue → edit script → 5. regenerate → 6. re-check
                  ↑________________________________ until ALL items pass ______↓
```

- Step 3 is **mandatory**: actually open every PNG and look. Do not judge
  "should be fine" from script logic alone.
- Fix by editing the script and regenerating. Never "mentally patch" a fix.
- The 10-item self-check (§21) must all pass before delivery.

---

## 1. Visual style source priority

Base the asset on the **real project UI**, never an unrelated visual language
(pixel / cyberpunk / retro unless the project itself is pixel/hand-drawn).

1. Read `css/style.css` `:root` vars → extract palette, radius, shadow, font.
2. Read `popup.html` → understand layout (header / search / tabs / content).
3. Run / screenshot the actual popup UI → use as the mockup reference.

Must match: background (`--bg`), card/surface (`--surface` + `--border` thin +
`--shadow` soft + `--radius`), primary (`--primary` / `--primary-grad`), accent
(`--accent` only), kbd-badge style, font-family. Stay within the brand palette
(indigo / purple / violet / amber families); no blue-green / magenta outside it.

---

## 2. Absolutely no emoji / non-standard Unicode glyphs

PIL cannot render most emoji (💠⌨️📋🎬🌐…) or decorative Unicode (✦ ✧ ▽ ➤ ◆ ◇)
on Windows → they become **□ boxes**.

- **Never** put emoji characters in drawn text. Replace with **geometric
  shapes** (`ellipse` / `rectangle` / `polygon` / `line`) — colored bar, rounded
  square, circle indicator.
- Replace decorative Unicode with ASCII or PIL-drawn shapes (`★`/`*` for stars,
  `→`/`>` for arrows, `...` for ellipsis).
- Only ASCII keyboard symbols (Ctrl / Cmd / ⌘ / Shift / Alt / Win) are safe in
  monospace.
- **Chinese text must use `font_zh()`** (msyh), never `font_en()` → English-only
  fonts render Chinese as □.
- `font_zh(10)` is too small and fails to render; minimum ~11 for feature
  descriptions.
- Self-check: `grep` the script for any emoji/non-ASCII symbol; `read_file`
  every PNG to confirm no □ boxes (including ✦/▽/➤).

---

## 3. Background must be solid color (no dense patterns)

- Background must be **solid** (e.g. `#fef7f8`, `#f8f9fa`, `#ffffff`). **No**
  grid lines, dot arrays, or regularly-tiled small squares/circles — these
  trigger "密集恐惧症" and look unprofessional.
- Gradients OK only if smooth (no hard repeating edges).
- Texture noise permitted only at opacity ≤ 0.03 (barely visible).
- Self-check: `read_file` confirm solid background; no stray grid/dots;
  foreground UI has enough contrast on it.

---

## 3.1 Background must NOT equal any swatch / theme color

(alwaysApply rule `store-asset-bg-must-differ-from-swatches-RULE`) The canvas
backdrop must **differ from every color shown as a swatch / color block** in the
image. If the backdrop equals one of the swatches, that card merges into the
background and looks like an empty frame (user pushed back on this twice,
cross-project).

- Before choosing a backdrop, list every color that appears as a swatch/block in
  that image, then pick a backdrop **not in that list**.
- Prefer taking the backdrop from the real source (Chrome theme:
  `manifest.json` `theme.colors`; web/extension: CSS vars) — choose a token that
  is *not* itself a swatch (e.g. a near-white `tab_text` / `omnibox_background`).
- When the only usable token *is* a swatch, derive a clearly separated version
  (deepen or lighten, e.g. `token × 0.35`) — derived still counts as "from the
  real source" — never reuse the raw swatch value.
- Keep a thin derived stroke on cards so the boundary stays visible in the worst
  case.
- **Add a hard `assert`** so a collision fails at generation, not at review:
  ```python
  assert all(tuple(bg) != tuple(c) for c in swatches), \
      "backdrop must not equal a swatch colour"
  ```
- Affects window-preview promos too: if the page backdrop equals the NTP color
  inside the mocked window, switch the backdrop to a derived color.
- Self-check: `read_file` every PNG; confirm each card's border is visibly
  distinct from the backdrop; no card "disappears".

---

## 4. Gray-background / shadow protection

The user is highly sensitive to "extra gray".

- **Do not** use `surface2` (`#f0f2f5`) on a light page background (`#f5f6f8`)
  — it still looks gray. Use `surface` (white) instead.
- `card()` defaults to `shadow=True`. On **any outer card that is not the popup
  shell itself**, pass `shadow=False` explicitly — otherwise a gray halo appears.
- Only the popup shell may keep a shadow (for float feel); remove even that if
  the user reports "gray".
- Search the script for `surface2` / default `shadow=True`; replace.

---

## 5. Font sizes scale with canvas (scale-aware)

(formerly rule #1) When the same `popup_mock` / component is used at two sizes,
the smaller size must recompute font sizes proportionally. Do **not** reuse the
large font sizes — that caused the "像素吸色器" and "4/20 色" labels to overflow
in the small promo tile. Implementation: in `popup_mock`, the `scale < 0.6`
branch sets smaller font sizes for title and numbers. Verify no text exceeds its
container at any scale.

---

## 6. Banner title vs subtitle spacing

(formerly #2) The gap between the title baseline-bottom and the subtitle top must
be **≥ 8px** — they must not touch. The subtitle bottom (baseline + font
descent) must be **< box bottom − 14px**, so the whole line stays inside the
box. (A subtitle once exceeded the pink box and was judged "not inside the box".)
Verify on both the 1280×800 hero and the 1400×560 promo banner.

---

## 7. Card grids must be even and tidy

(formerly #3) Multiple cards prefer a **2×N or 3×N even grid**. Never leave an
"orphan" row like 2+2+1. (5 export cards were padded to 6 → 2×3 to stay tidy.)
Card gap **≥ 10px**; text inside a card must be **≥ 8px** from the card border.
Verify: row counts divide evenly; no lone card on its own row.

---

## 8. Bottom-margin safety line

(formerly #4) The bottom edge of any CTA button / white block = start-y + height
must be **< canvas-height − 12px**. Example: 1400×560 canvas → Pro box bottom ≤
548 (12px reserved). A value of 570 overflowed the canvas. Verify every anchored
bottom element against the canvas height.

---

## 9. Sections must not overlap

(formerly #5) Adjacent sections (e.g. last row of export cards vs the Pro
section) must have non-intersecting y-ranges. Fix any overlap, even 2px, by
moving up or compressing. Verify by computing the y-intervals of neighboring
blocks.

---

## 10. Section title vs content spacing

(formerly #6) A section title (e.g. "多格式导出") must be **≥ 20px** above the
first element below it. Do not let it hug the content. (A label once sat almost
on top of a card.) Verify spacing for every section heading.

---

## 11. Button text vertically centered + auto-shrink + high contrast

(formerly #8) In promo tiles (and any CTA button), bilingual text inside the
button must be **vertically centered against the button's own height**, not
pinned to a top-Y that drags text to the button's bottom edge (or off the
canvas). When the font is too large and hugs the edge, **shrink it** (e.g. 中文
17 / 英文 13 two-line layout). Compute `btn_center_y = btn_y + btn_h // 2` and
split the two lines around that midline, using `anchor="mm"` for true vertical
center.

**Contrast**: button text vs button background must be **WCAG AA ≥ 4.5:1** — use
**dark bg + white text** or **white bg + dark text**; never pale-text-on-pale-bg
or dark-text-on-dark-bg. Verify at 50% zoom.

---

## 12. Long copy must wrap / condense to avoid truncation

(formerly #9) Detail / description copy (especially **English, which runs
longer**) that exceeds its container width must be **wrapped or condensed** —
never left to be clipped into a fragment like "gradient roll b…". Implementation:
drop redundant words + shrink the font slightly (e.g. 24→22), and wrap manually
into multiple lines when needed. The `paragraph()` helper in
`generate-store-screenshots.py` already wraps by `max_width`; use it for long
blocks. Verify: no English/Chinese detail line is cut off at the canvas or card
edge.

---

## 13. Internal breathing-space minimums (experience floor)

Below these values → crowding / overlap / overflow.

- **Brand area**: brand-name baseline ↔ tagline top **≥ brand_font_size + 6px**.
  Logo ↔ brand name **≥ 12px** horizontally.
- **Category tile / card**: colored bar right edge ↔ name left edge **≥ 14px**
  (bar at cx+8~14, text from cx+28). Name ↔ count gap per card height.
- **kbd badge row**: badge right edge ↔ action name **≥ 10px** (not 4px).
  Action ↔ source separated by y.
- **Button / pill**: font size **≤ button_height × 0.40** (46px→≤18; 34px→≤13).
  **Always `anchor="mm"`**. Text↔edge **≥ 8px**. Toggle min width **≥ text_width
  + 24px** ("EN / 中文 Toggle" ~144px; "当前：简体中文" ~130px).
- **Status bar / narrow strip**: shorten EN long text or −1~2pt; side padding
  **≥ 14px** (scale=1).
- **Small canvas (≤440px wide)**: reduce element count before shrinking
  elements (4 cards → 3 taller). popup mock scale ≤ 0.38. Feature card height
  **≥ 52px** for CN+EN two-line. Card gap **≥ 8px**.
- **popup_mock rhythm**: logo → (+16) → search → (+12) → tabs → (+14) →
  category → (+8) → shortcut card → (+8) → status bar; inter-section **≥ 8px**,
  intra **≥ 6px**.

---

## 14. Small promo (440×280) iron rules

440×280 is the extreme size for Chrome small marquee — space is extremely tight.

- **Space budget**: Banner 38–44px; popup mock scale **≤ 0.30** (0.38 too big;
  0.30 = 114×162); feature rows 32–38px each (no card containers!); bottom CTA
  28–34px; global margin **≥ 10px**.
- **Features: NO card containers** — use plain text line + colored dot
  (`ellipse` 12px + text). Card borders+shadows waste ~20px/row.
  - `● 即时搜索` (bold 11pt) / `  Instant Search` (sub 9pt); dot 12px;
    CN bold 10–11pt, EN regular 9–10pt; line height 32–36px, row gap 6px.
- **Element count cap**: 440×280 → 1 popup(0.30) + **≤ 3** feature rows + 1 CTA
  only. Never popup(>0.32) + 3+ cards + CTA + stats simultaneously.
- **Font table (440×280 only)**: banner title 14–15pt bold (max 16); subtitle
  8–9pt (max 10); popup brand `max(9, int(16*scale))`; feature CN 10–11pt bold
  (max 12); feature EN 9pt (max 10); CTA 10–11pt bold (max 12).

---

## 15. Alignment baselines (unified margins)

- Fix `MARGIN` and `RIGHT = W − MARGIN` first; derive all blocks from them.
  Don't hand-fit each block.
- **Banner right edge == last column card right edge == RIGHT.** Banner must not
  be narrower than cards.
- Multi-column: derive from `RIGHT` backward with explicit `GAP` (≥ 20px; never
  0). `assert col2_x + card_w == RIGHT`.
- **Right safety line**: last column x + card_w ≤ W − MARGIN (add `assert`).
- Pasted mockup left x == `MARGIN` (same line as banner left). ≥ 40px breathing
  space to right content column.
- Self-check: `assert` right edge ≤ RIGHT, bottom ≤ H−12, adjacent y-ranges
  non-intersecting; `read_file` every PNG to confirm edges align to one line.

---

## 16. CTA button vs text-above spacing

- Between a CTA box (label list / feature list above it) and the button, reserve
  **≥ 12px** using the **worst-case line height including descender**, not just
  baseline alignment.
- On overlap, **grow the whole CTA container** (e.g. +8px) and shift the text
  group up / tighten — do **not** just push the button down (that can hit canvas
  bottom).
- Re-generate and self-preview to confirm clear gap.
- Self-check: last feature line bottom → button top **≥ 12px**; button fully
  inside box; bottom ≥ canvas−12px.

---

## 17. Contrast — WCAG AA ≥ 4.5:1

- Key text vs background **≥ 4.5:1**. Watch: pale text (sub/hint) with opacity
  on pale surface → invisible; text color == bg color → gone.
- Safe combos: dark `(26,26,26)` + white `(255,255,255)` ~15:1; white
  `(255,255,255)` + dark `(26,26,26)` ~15:1; mid-gray `(120,120,120)` + white
  ~7:1.
- Avoid: pale `(240+)` + white `(255,255,255)` CR<1.5; dark `(40-)` + black
  `(0,0,0)` CR<2; near-identical colors.
- After generation, visually confirm every button/text is readable, including at
  different display brightness.

---

## 18. Redraw from scratch, never patch + Windows path

- When the user says "swap asset / adjust layout / fix flaw", **edit the composer
  script and regenerate from zero** — never write a patch script that pastes onto
  the old PNG.
- **Parameterize multi-layout**: each layout variant gets its own geometry
  constants (e.g. `CARD_GEOM_SINGLE` / `CARD_GEOM_DUAL`); don't share one global
  constant.
- **Material size adaptive**: derive pasted height from width by aspect ratio
  (`ph = round(cap.height * scale)`), never hardcode `POPUP_H`; verify
  `paste_y + ph < H − margin`.
- **Windows PIL `img.save()` with a Chinese absolute path → intermittent
  `OSError 22`**. Fix: use **relative paths**
  (`store-assets/screenshots/zh/x.png`); run via a launcher with ASCII `cwd`.
  (Both bundled scripts already resolve paths from
  `ROOT = Path(__file__).resolve()` — keep this pattern.)
- Nested literal (2 lang × 5 images × 4 cards) → after writing,
  `assert src.count('{') - src.count('}') == 0` before running.

---

## 19. Window / IDE mockup text spacing (if applicable)

For editor/IDE-style window mockups: tab-to-tab **≥ 50px**; title-bar hints
(TypeScript / UTF-8 / LF) each **≥ 70px**; status-bar right items each
**≥ 110px**, placed right→left with ≥30px safe gaps. Never hardcode
W−170/W−120/W−70 decreasing — actual widths differ. Self-check both light &
dark sets.

---

## 20. Localization rules (store-asset specific, mandatory)

### A. Screenshots split by language; promo is bilingual

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

### D. Promo CTA separator is a middot `·`

- Inside a promo CTA button, separate Chinese and English with a **middot `·`**
  (e.g. `立即体验 · Try It Now`) — more elegant and compact than double spaces.

### E. Language detection priority (for the product itself, when relevant)

- URL param > localStorage > browser language. (For generated assets, simply
  produce both zh & en sets.)

---

## 21. 10-item self-check (all must pass before delivery)

| # | Dimension | Fail sign |
|---|-----------|-----------|
| 1 | Gray/shadow | outer cards `shadow=False`? no stray `surface2`? |
| 2 | Overflow | text/block exits container or canvas? stroked rect expands out? |
| 3 | Overlap | adjacent y-ranges intersect (even 2px)? baselines aligned? |
| 4 | Spacing | inter-section ≥8px, intra ≥6px? small-card gap ≥10px? |
| 5 | Font scale | small canvas uses smaller fonts? no reuse of large fonts? |
| 6 | Grid | even 2×N/3×N? no orphan row? |
| 7 | Bottom margin | CTA/white-box bottom < canvas−12px? |
| 8 | Bilingual | zh & en both checked? dynamic text switched per language? |
| 9 | Noise | small popup over-detailed → noise? simplify. |
| 10 | Contrast | main/secondary text vs bg ≥ WCAG AA 4.5:1? |

**High-frequency pitfalls (always recheck):**
1. `card()` default `shadow=True` → forgot `shadow=False` on outer card = gray
   halo (user rejects).
2. `surface2` misuse on light bg → still gray (user sensitive) → use `surface`
   white.
3. Small popup overload: 440×280 popup drawing category grid + shortcut cards =
   noise → draw shell+logo+search+tabs+status only.
4. Bilingual leak: EN set's toggle pill used `surface2` while ZH set already
   fixed → check both.
5. Emoji/□ boxes from non-ASCII glyphs → replace with shapes.
6. Dense grid/dot background → replace with solid color.
