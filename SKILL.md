---
name: store-asset-generator
description: "Generate Chrome Web Store screenshots (1280x800, per-language zh/en) and bilingual promo tiles (440x280 / 1400x560) for browser-extension or web-app projects using a PIL-based Python pipeline, then enforce a strict visual QA + localization checklist before delivery. Use when the user asks to create, update, or fix store listing art, promo tiles, screenshots, or any marketing image produced by a generate-store-*.py script. 中文：Chrome 扩展商店素材生成器，一键生成商店截图与宣传图并做视觉 QA。"
allowed-tools: Bash, Read, Write, Edit
compatibility: Requires Python 3.10+ with Pillow. Cross-agent: works in CodeBuddy, Claude Code, and Codex (Agent Skills spec).
---

# Store Asset Generator

## Overview

This skill packages the user's established workflow for producing Chrome Web
Store screenshots and promotional images. It combines two reusable PIL scripts
with a hard visual-QA checklist so that every generated asset passes layout,
overflow, alignment, and spacing checks before delivery.

The bundled scripts are written for the "Pixel Color Picker" project as concrete
templates. Adapt the copy, colors, and layout blocks per project, but keep the
shared helpers (`base_bg` / `base`, `popup_mock`, `font`, `rect`, `text`) and
the QA rules intact.

## When To Use

Trigger this skill when the user:

- Asks to generate or update Chrome store screenshots / promo tiles /宣传图.
- Mentions `generate-store-screenshots.py` or `generate-store-promo.py`.
- Reports a visual defect in a generated asset (overflow, misalignment, overlap,
  text cut off, odd orphan row in a grid).
- Wants a new store asset for a project that should follow the same SaaS
  visual style and QA bar (the bundled examples use an optional pixel font).

## Prerequisites

- Python 3 with `Pillow` installed. **Run scripts with `python3` on macOS/Linux,
  or `py -3` on Windows** (this author's Windows has broken `python`/`python3`
  launchers → use `py -3` there). Install: `python3 -m pip install -r requirements.txt`
  (Windows: `py -3 -m pip install -r requirements.txt`).
- The pixel font `assets/PressStart2P-Regular.ttf` is **optional**. If a project
  wants the retro/pixel look, copy it to `<project>/fonts/PressStart2P-Regular.ttf`
  (the scripts look there first). For non-pixel projects, the scripts fall back to
  standard system fonts (e.g., msyh.ttc / simhei.ttf on Windows).

## Workflow (mandatory loop)

Follow this exact cycle for every asset change. Do not skip steps.

1. **Generate** — run the relevant script from the project root. On Windows use
   `py -3`, on macOS/Linux use `python3`:
   - Screenshots: `python3 scripts/generate-store-screenshots.py`
     (outputs **per-language** sets — `zh` fully Chinese, `en` fully English —
     to `<project>/store-assets/screenshots/{zh,en}/`, 1280×800 each).
   - Promo tiles: `python3 scripts/generate-store-promo.py`
     (outputs **bilingual** `promo-small-440x280.png` and
     `promo-large-1400x560.png` — both Chinese + English in one image — to
     `<project>/store-assets/promo/`).
2. **Self-preview** — open the generated PNG(s) and inspect against
   `references/qa-checklist.md`. Check overflow, alignment, spacing, even grids,
   bottom-margin safety line, and section non-overlap.
3. **Fix** — edit the offending coordinates / font sizes / widths in the script
   (the QA checklist names the exact parameters to adjust).
4. **Regenerate** — re-run the script and repeat steps 2–3 until every checklist
   item passes. Never assume "it's probably fine" — verify visually.

## Using The Bundled Scripts As Templates

- `scripts/generate-store-screenshots.py` defines `screenshot_1()` … `screenshot_5()`,
  each a full 1280×800 canvas. Copy the structure, swap the hero title/subtitle
  and content blocks for the new project.
- `scripts/generate-store-promo.py` defines `small_promo()` (440×280) and
  `large_promo()` (1400×560). The large promo uses a 3-column grid
  (popup | hero+actions | exports+Pro).
- Keep `popup_mock(draw, x, y, scale)` and its `scale < 0.6` branch — it is the
  reference implementation of scale-aware font sizing (QA rule #5 in the checklist).

## Visual Style & Hard Rules (mandatory, from global user rules)

These hard rules are enforced by `references/qa-checklist.md`. They are
non-negotiable for Chrome Web Store assets and must be followed on every
generation:

- **Visual style comes from the real project UI.** Read `css/style.css` `:root`
  vars (`--bg`, `--surface`, `--border`, `--shadow`, `--radius`, `--primary`,
  `--accent`), read `popup.html`, and use the running popup as the mockup
  reference. Match colors / fonts / radius / shadow exactly. Stay within the
  brand palette; never invent an unrelated visual language.
- **No emoji / non-standard Unicode glyphs.** PIL renders most emoji and
  decorative Unicode (✦ ✧ ▽ ➤ ◆) as **□ boxes** on Windows. Replace with
  geometric shapes (`ellipse` / `rectangle` / `polygon`). Chinese text must use
  `font_zh()` (msyh), never `font_en()`.
- **Background must be solid color.** No grid lines, dot arrays, or tiled
  patterns (triggers "密集恐惧症"). Use a soft solid color or a smooth gradient.
- **Background must NOT equal any swatch / theme color.** The canvas backdrop
  must differ from every color shown as a swatch / color block in the image
  (a card that matches the background merges into an empty frame — user pushed
  back on this twice). Pick a backdrop color not in the swatch list; when the
  only usable token *is* a swatch, derive a clearly darker/lighter version
  (e.g. `token × 0.35`) and add an `assert` so a collision fails at generation:
  `assert all(tuple(bg) != tuple(c) for c in swatches)`.
- **No extra gray.** Never use `surface2` (`#f0f2f5`) on a light page background;
  use `surface` (white). Any `card()`-style helper defaults to `shadow=True` —
  pass `shadow=False` on every outer card that is not the popup shell itself, or a
  gray halo appears (user rejects).
- **Redraw from scratch, never patch.** When the user asks to swap assets / adjust
  layout / fix a flaw, edit the composer script and regenerate from zero. Do not
  write a patch that pastes onto the old PNG. Parameterize multi-layout variants;
  derive pasted material height from aspect ratio (never hardcode). Use **relative
  output paths** so Windows never hits the intermittent `OSError 22` on Chinese
  absolute paths (both bundled scripts already resolve paths from
  `ROOT = Path(__file__).resolve()` — keep this).
- **Unified alignment baselines.** Derive all blocks from one `MARGIN` and
  `RIGHT = W − MARGIN`. Banner right edge must equal the last column's right edge.
  Column gap ≥ 20px (never 0). Add `assert` so an out-of-bounds block fails at
  generation, not at review.
- **Contrast ≥ WCAG AA 4.5:1.** Button / key text vs background must be dark-on-
  light or light-on-dark. Never pale-text-on-pale-bg. Verify every text is
  readable, including at 50% zoom.
- **440×280 small promo iron rules.** popup mock scale ≤ 0.30; features use
  plain text + colored dot (no card containers); ≤ 3 feature rows + 1 CTA only.
- **Mandatory self-preview loop.** After every change, open **every** generated
  PNG with your agent's image viewer (`read_file` in CodeBuddy, `Read` in
  Claude Code, `read` in Codex) and verify against the 10-item self-check in the
  checklist. Never
  assume "probably fine".

## Language & Localization Rules (mandatory)

These rules are non-negotiable for Chrome Web Store assets and are enforced by
the QA checklist (`references/qa-checklist.md`):

- **Screenshots are split by language.** Generate one set per language and save
  under `<project>/store-assets/screenshots/{zh,en}/`. A `zh` screenshot is
  **all Chinese**; an `en` screenshot is **all English**. Never mix both
  languages in a single screenshot.
- **Promo tiles are bilingual.** The 440×280 and 1400×560 tiles MUST contain
  both Chinese and English copy in the *same* image so the store backend
  recognizes multi-language and reuses one file. Save under
  `<project>/store-assets/promo/` (no `zh`/`en` subdirs).
- **Mockup "dynamic" copy follows the screenshot language.** Any text that looks
  like the product's live output (AI replies / option buttons, simulated emails,
  search suggestions) must match the screenshot language. Drive it from a `lang`
  dictionary — never hardcode English placeholders under a translated banner.
- **Hand-drawn cards: recompute coordinates after edits.** When you change a
  card's preview rows or copy length, recompute every downstream coordinate
  (button Y, card height, internal spacing) so elements don't overlap.
- **Promo CTA separator is a middot `·`.** Separate Chinese/English inside a CTA
  button with `·` (e.g. `立即体验 · Try It Now`), not double spaces.
- **All generated assets stay inside the project** (under `store-assets/`). Only
  the final packed `.zip` may be copied out to the user's default folder.

## Visual QA Standard

All generated assets MUST satisfy the checklist in
`references/qa-checklist.md`. It is the source of truth and now covers:

- **Visual style source** (read `css/style.css` `:root` + `popup.html`, match the
  real UI, stay in the brand palette).
- **No emoji / non-ASCII glyphs** (replace with geometric shapes; `font_zh` for
  Chinese — emoji render as □ boxes).
- **Solid-color backgrounds** (no grid/dot/dense patterns).
- **No extra gray** (`surface2` banned on light bg; `shadow=False` on outer cards).
- **Scale-aware fonts**, banner title/subtitle gaps, even 2×N/3×N grids,
  bottom-margin safety line (< canvas − 12px), inter-section non-overlap,
  section-title-to-content spacing ≥ 20px.
- **Button text** vertically centered (`anchor="mm"`) + auto-shrink, with
  **WCAG AA ≥ 4.5:1 contrast** (dark-on-light / light-on-dark only).
- **Internal breathing-space minimums** (brand area, kbd badge ≥ 10px, button
  font ≤ 0.40×height, toggle width, small-canvas strategy).
- **440×280 small-promo iron rules** (scale ≤ 0.30, no card containers for
  features, ≤ 3 feature rows + 1 CTA).
- **Unified alignment baselines** (one `MARGIN`/`RIGHT`, banner == last column
  right edge, column gap ≥ 20px, `assert` bounds).
- **Redraw-not-patch** + relative output paths (Windows `OSError 22` guard).
- The **mandatory generate → self-preview → fix → regenerate** loop, ending in the
  **10-item self-check** (§21) — all must pass before delivery.
- The **localization rules** above (per-language screenshots, bilingual promo,
  dynamic-copy switching, hand-drawn-card coordinate recomputation, middot CTA).

## Resources

- `scripts/generate-store-screenshots.py` — screenshot generator template.
- `scripts/generate-store-promo.py` — promo tile generator template.
- `references/qa-checklist.md` — the mandatory visual QA checklist.
- `assets/PressStart2P-Regular.ttf` — optional pixel font used by the bundled
  example templates.
