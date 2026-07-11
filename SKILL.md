---
name: chrome-extension-store-asset-generator
description: "Generate Chrome Web Store screenshots and promotional images (PNG/JPG) for browser-extension or web-app projects using a PIL-based Python pipeline, then enforce a strict visual QA checklist before delivery. Use this skill whenever the user asks to create, update, or fix store listing art, promo tiles, screenshots, or any marketing image produced by a generate-store-*.py script. 中文：Chrome 扩展商店素材生成器，一键生成商店截图与宣传图并做视觉 QA。"
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
- Wants a new store asset for a project that should follow the same pixel/SaaS
  visual style and QA bar.

## Prerequisites

- Python 3 with `Pillow` installed (`pip install Pillow`).
- The pixel font `assets/PressStart2P-Regular.ttf` must be available at
  `<project>/fonts/PressStart2P-Regular.ttf` (the scripts look there first).
  Copy it from this skill's `assets/` folder into the target project before
  running. Chinese/Windows system fonts (msyh.ttc, simhei.ttf) are also used and
  resolve automatically on Windows.

## Workflow (mandatory loop)

Follow this exact cycle for every asset change. Do not skip steps.

1. **Generate** — run the relevant script from the project root:
   - Screenshots: `python scripts/generate-store-screenshots.py`
     (outputs to `<project>/store-assets/screenshots/`, 1280×800 each).
   - Promo tiles: `python scripts/generate-store-promo.py`
     (outputs `promo-small-440x280.png` and `promo-large-1400x560.png` to
     `<project>/store-assets/`).
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
  reference implementation of scale-aware font sizing (QA rule #1).

## Visual QA Standard

All generated assets MUST satisfy the checklist in
`references/qa-checklist.md`. The checklist is the source of truth for:
font scaling, banner title/subtitle gaps, even card grids, bottom-margin safety
line, inter-section non-overlap, section-title-to-content spacing, and the
generate→preview→fix→regenerate delivery loop.

## Resources

- `scripts/generate-store-screenshots.py` — screenshot generator template.
- `scripts/generate-store-promo.py` — promo tile generator template.
- `references/qa-checklist.md` — the mandatory visual QA checklist.
- `assets/PressStart2P-Regular.ttf` — pixel font required by the scripts.
