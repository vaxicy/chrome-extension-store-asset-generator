# store-asset-generator

A reusable **user-level** CodeBuddy skill that generates Chrome Web Store screenshots and promotional images (PNG/JPG) for browser-extension / web-app projects with a PIL-based Python pipeline, then enforces a strict visual QA checklist before delivery.

## What it does

- Generates store **screenshots** (1280×800) and **promo images** (440×280 small tile + 1400×560 large) from a `popup_mock` component.
- Pixel-art font (`PressStart2P-Regular.ttf`) for the retro look.
- Forces a **generate → self-preview → fix → regenerate** loop so every asset passes 7 visual QA rules (scale-aware font sizing, banner spacing, even grid, bottom safety margin, no block overlap, section-title spacing, self-preview flow).

## Folder structure

```
store-asset-generator/
├── SKILL.md                              # skill trigger + workflow (required at root)
├── scripts/
│   ├── generate-store-screenshots.py    # 1280×800 screenshot generator
│   └── generate-store-promo.py          # 440×280 + 1400×560 promo generator
├── references/
│   └── qa-checklist.md                   # 7 visual QA hard rules
└── assets/
    └── PressStart2P-Regular.ttf          # pixel font
```

## Prerequisites

- Python 3.10+
- `Pillow` (`pip install Pillow`)

## Usage

The skill auto-triggers when you ask CodeBuddy to "generate store screenshots / promo images" or mention a `generate-store-*.py` script. It copies the templates into your project, adapts the copy/text, runs the generator, self-previews, and iterates until QA passes.

## Install (user-level, cross-project)

Copy the folder to your CodeBuddy user skills directory:

```powershell
Copy-Item . "C:\Users\<user>\.codebuddy\skills\store-asset-generator" -Recurse -Force
```
