from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "store-assets" / "promo"
OUT.mkdir(parents=True, exist_ok=True)

COLORS = {
    "ink": "#332d36",
    "soft": "#716676",
    "pink": "#ff5f9c",
    "mint": "#67d6bd",
    "cream": "#fff0a8",
    "paper": "#fff9fc",
    "panel": "#fffdf7",
    "white": "#ffffff",
}


def font(size, bold=False, pixel=False):
    candidates = []
    if pixel:
        candidates.append(ROOT / "fonts" / "PressStart2P-Regular.ttf")
    if bold:
        candidates += [
            Path("C:/Windows/Fonts/msyhbd.ttc"),
            Path("C:/Windows/Fonts/simhei.ttf"),
        ]
    candidates += [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


F = {
    "h1": font(44, bold=True),
    "h2": font(30, bold=True),
    "h3": font(22, bold=True),
    "body": font(18),
    "small": font(14),
    "tiny": font(12),
    "pixel": font(20, pixel=True),
    "pixel_small": font(13, pixel=True),
}


def rect(draw, xy, fill, outline=COLORS["ink"], width=4):
    draw.rectangle(xy, fill=fill, outline=outline, width=width)


def text(draw, xy, value, fill=COLORS["ink"], f=None, anchor=None):
    draw.text(xy, value, fill=fill, font=f or F["body"], anchor=anchor)


def base_bg(W, H):
    img = Image.new("RGB", (W, H), COLORS["paper"])
    draw = ImageDraw.Draw(img)
    step = 16 if W <= 500 else 24
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill="#f1e4ec", width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill="#f1e4ec", width=1)
    for x in range(step // 2, W, step):
        for y in range(step // 2, H, step):
            draw.rectangle((x, y, x + 2, y + 2), fill="#ffd9ea")
    return img, draw


# ── Shared popup mock (scale-aware: small scales use smaller fonts) ──
def popup_mock(draw, x, y, scale=1.0):
    w, h = int(360 * scale), int(520 * scale)
    rect(draw, (x + 8, y + 8, x + w + 8, y + h + 8), "#d8d1d8", outline="#d8d1d8", width=0)
    rect(draw, (x, y, x + w, y + h), COLORS["white"], width=int(5 * scale))

    # header bar — compact when scaled down
    hdr_h = int(56 * scale) if scale < 0.6 else int(80 * scale)
    rect(draw, (x + 14, y + 14, x + w - 18, y + 14 + hdr_h), COLORS["pink"], width=int(4 * scale))
    if scale < 0.6:
        text(draw, (x + 36 * scale, y + 24 * scale), "PIXEL TOOL", fill="white", f=font(int(9 * scale), pixel=True))
        text(draw, (x + 36 * scale, y + 38 * scale), "像素吸色器", fill="white", f=font(int(12 * scale), bold=True))
    else:
        text(draw, (x + 38 * scale, y + 28 * scale), "PIXEL TOOL", fill="white", f=F["pixel_small"])
        text(draw, (x + 38 * scale, y + 50 * scale), "像素吸色器", fill="white", f=font(17, bold=True))

    # quick-pick
    qpk_top = int(86 * scale)
    qpk_h = int(48 * scale)
    rect(draw, (x + 28 * scale, y + qpk_top, x + w - 28 * scale, y + qpk_top + qpk_h),
         COLORS["mint"], width=int(4 * scale))
    qpk_font = int(15 * scale) if scale < 0.6 else int(19 * scale)
    text(draw, (x + w // 2, y + qpk_top + int(14 * scale)), "快速取色",
         f=font(qpk_font, bold=True), anchor="ma")

    rect(draw, (x + 28 * scale, y + qpk_top + qpk_h + int(8 * scale), x + w - 28 * scale, y + qpk_top + qpk_h + int(8 * scale) + int(20 * scale)),
         COLORS["mint"], width=int(3 * scale))
    text(draw, (x + w // 2, y + qpk_top + qpk_h + int(18 * scale)), "Quick Pick",
         f=font(int(11 * scale)), anchor="ma")

    # palettes section
    pal_y = y + int(144 if scale < 0.6 else 160) * scale
    pal_font = int(13 if scale < 0.6 else 17) * scale
    text(draw, (x + 28 * scale, pal_y), "我的色卡组", f=font(pal_font, bold=True))

    swatches = ["#ff6b9d", "#8c6cff", "#69d9bf", "#fff0a8", "#75bfe8", "#f05f7d"]
    card_start = int(162 if scale < 0.6 else 188) * scale
    card_h = int(46 if scale < 0.6 else 56) * scale
    card_gap = int(54 if scale < 0.6 else 72) * scale
    title_sz = int(11 if scale < 0.6 else 15) * scale
    sub_sz   = int(9 if scale < 0.6 else 11)
    sw_w = int(18 if scale < 0.6 else 22) * scale
    sw_gap = int(17 if scale < 0.6 else 22) * scale
    tx_off = int(125 if scale < 0.6 else 150) * scale
    ty_title = int(8 if scale < 0.6 else 12) * scale
    ty_sub   = int(24 if scale < 0.6 else 34) * scale

    for i in range(3):
        yy = card_start + i * (card_h + card_gap)
        rect(draw, (x + 28 * scale, yy, x + w - 28 * scale, yy + card_h),
             COLORS["panel"], width=int(3 * scale))
        sh = int(20 if scale < 0.6 else 24) * scale
        sy = yy + int(10 if scale < 0.6 else 14) * scale
        for j in range(4):
            c = swatches[(i + j) % len(swatches)]
            sx = x + (40 if scale < 0.6 else 46) * scale + j * sw_gap
            draw.rectangle((sx, sy, sx + sw_w, sy + sh),
                           fill=c, outline=COLORS["ink"], width=max(1, int(2 * scale)))
        text(draw, (x + tx_off, yy + ty_title),
             ["默认色卡", "品牌灵感", "网页主题"][i], f=font(title_sz, bold=True))
        text(draw, (x + tx_off, yy + ty_sub),
             f"{4 + i}/20 色", fill=COLORS["soft"], f=font(sub_sz))

    # bottom bar
    bb_top = h - int(64 if scale < 0.6 else 78) * scale
    bb_bot = h - int(22 if scale < 0.6 else 26) * scale
    rect(draw, (x + 28 * scale, y + bb_top, x + w - 28 * scale, y + bb_bot),
         COLORS["cream"], width=int(3 * scale))
    bt_font = int(10 if scale < 0.6 else 14)
    text(draw, (x + w // 2, y + h - int(52 if scale < 0.6 else 62) * scale),
         "历史 · 设置 · Pro", f=font(bt_font), anchor="ma")


# ── Small Promo Tile (440 × 280) — bilingual ──────────────────────────────
def small_promo():
    W, H = 440, 280
    img, draw = base_bg(W, H)

    # pink banner (title brand + bilingual subtitle)
    rect(draw, (16, 14, 424, 58), COLORS["pink"], width=3)
    text(draw, (28, 20), "Pixel Color Picker", fill="white", f=font(19, bold=True))
    text(draw, (28, 44), "网页取色 · Web color picker", fill="white", f=font(11))

    # compact popup mock that fully fits the 440×280 canvas with safe margins
    px, py, pw, ph = 18, 68, 150, 190
    rect(draw, (px + 6, py + 6, px + pw + 6, py + ph + 6), "#d8d1d8",
         outline="#d8d1d8", width=0)
    rect(draw, (px, py, px + pw, py + ph), COLORS["white"], width=4)

    # header
    rect(draw, (px + 10, py + 10, px + pw - 10, py + 42), COLORS["pink"], width=3)
    text(draw, (px + 18, py + 17), "PIXEL TOOL", fill="white",
         f=font(10, pixel=True))
    text(draw, (px + 18, py + 28), "像素吸色器", fill="white",
         f=font(12, bold=True))

    # bilingual quick-pick bar (single bar, both languages)
    rect(draw, (px + 14, py + 50, px + pw - 14, py + 78), COLORS["mint"], width=3)
    text(draw, (px + pw // 2, py + 58), "快速取色 · Pick", f=font(12, bold=True),
         anchor="ma")

    # two palette cards
    swatches = ["#ff6b9d", "#8c6cff", "#69d9bf", "#fff0a8"]
    pal_names = [("默认色卡", "4/20 色"), ("品牌灵感", "5/20 色")]
    for i, ((name, count), color) in enumerate(zip(pal_names, swatches)):
        cy = py + 88 + i * 50
        rect(draw, (px + 14, cy, px + pw - 14, cy + 40), COLORS["panel"], width=3)
        for j, c in enumerate(swatches):
            sx = px + 22 + j * 20
            draw.rectangle((sx, cy + 9, sx + 16, cy + 25), fill=c,
                           outline=COLORS["ink"], width=2)
        text(draw, (px + 102, cy + 8), name, f=font(11, bold=True))
        text(draw, (px + 102, cy + 24), count, fill=COLORS["soft"], f=font(9))

    # bottom bar
    rect(draw, (px + 14, py + ph - 32, px + pw - 14, py + ph - 10),
         COLORS["cream"], width=3)
    text(draw, (px + pw // 2, py + ph - 21), "历史 · History", f=font(10),
         anchor="ma")

    # right-side features — compact bilingual
    rx = 182
    features = [
        ("网页吸色", "取色 · Pick"),
        ("色卡管理", "色卡 · Palettes"),
        ("格式导出", "导出 · Export"),
        ("中英双语", "双语 · Bilingual"),
    ]
    for i, (title, desc) in enumerate(features):
        fy = 74 + i * 45
        rect(draw, (rx, fy, 420, fy + 38), COLORS["panel"], width=3)
        draw.ellipse((rx + 9, fy + 9, rx + 25, fy + 25), fill=COLORS["pink"],
                     outline=COLORS["ink"], width=2)
        text(draw, (rx + 34, fy + 5), title, f=font(13, bold=True))
        text(draw, (rx + 34, fy + 21), desc, fill=COLORS["soft"], f=font(10))

    img.save(OUT / "promo-small-440x280.png")


# ── Large Promo Tile (1400 × 560) — bilingual, middot CTA ─────────────────
# Clean 3-column grid: popup | hero-text+actions | exports+Pro
def large_promo():
    W, H = 1400, 560
    img, draw = base_bg(W, H)

    # ── Top: full-width pink hero banner ─────────────────────
    rect(draw, (36, 24, 1364, 116), COLORS["pink"], width=5)
    text(draw, (68, 40), "Pixel Color Picker", fill="white", f=font(38, bold=True))
    # bilingual subtitle: clear gap from title, well within banner bounds
    text(draw, (70, 86),
         "像素网页取色 · 色卡管理 · 多格式导出 · 双语界面 · 14-Day Trial",
         fill="white", f=font(16))

    # ── Content area: 3 logical columns ─────────────────────
    # Col 1: Popup mock (left)
    popup_mock(draw, 48, 120, scale=0.72)

    # Col 2: Feature highlight + color preview + buttons (center-left)
    cx = 330
    cy = 130

    text(draw, (cx, cy), "一键吸取网页颜色 · Pick web colors", f=font(26, bold=True))

    desc_lines = [
        "从网页快速取色，自动存入色卡与历史。",
        "Quick eyedrop, auto-saved to palettes & history.",
    ]
    dy = cy + 38
    for line in desc_lines:
        text(draw, (cx, dy), line, f=font(15))
        dy += 24

    panel_y = dy + 8
    rect(draw, (cx, panel_y, cx + 480, panel_y + 68), COLORS["panel"], width=4)
    text(draw, (cx + 20, panel_y + 16), "HEX", f=font(21, pixel=True))
    text(draw, (cx + 95, panel_y + 16), "#FF6B9D", f=font(26, bold=True))

    btn_y = panel_y + 84
    btn_h = 48
    rect(draw, (cx, btn_y, cx + 220, btn_y + btn_h), COLORS["mint"], width=4)
    text(draw, (cx + 110, btn_y + btn_h // 2), "复制颜色 · Copy",
         f=font(17, bold=True), anchor="mm")
    rect(draw, (cx + 236, btn_y, cx + 456, btn_y + btn_h), COLORS["cream"], width=4)
    text(draw, (cx + 346, btn_y + btn_h // 2), "保存到色卡 · Save",
         f=font(17, bold=True), anchor="mm")

    # ── Col 3: Export format cards + Pro CTA (right side) ───
    rx = 850

    # Section label — clear separation from cards below, bilingual
    text(draw, (rx, 120), "多格式导出 · Export", f=font(18, bold=True))

    # 6 export cards → 2 cols × 3 rows (even grid)
    exports = [
        ("CSS 变量", "#ff6b9d"),
        ("SCSS",    "#8c6cff"),
        ("JSON",    "#69d9bf"),
        ("Tailwind","#fff0a8"),
        ("PNG 色卡","#75bfe8"),
        ("备份恢复","#f05f7d"),
    ]
    ew, eh = 116, 70
    gap_x, gap_y = 18, 10
    for i, (label, color) in enumerate(exports):
        col = i % 2
        row = i // 2
        ex = rx + col * (ew + gap_x)
        ey = 146 + row * (eh + gap_y)
        rect(draw, (ex, ey, ex + ew, ey + eh), COLORS["white"], width=4)
        rect(draw, (ex + 12, ey + 9, ex + 46, ey + 43), color, width=3)
        text(draw, (ex + ew // 2, ey + 50), label, f=font(13, bold=True), anchor="ma")

    # Pro CTA block — compact, with safe bottom margin
    pro_x, pro_y = 850, 388
    rect(draw, (pro_x, pro_y, 1364, 528), COLORS["white"], width=5)

    # Pro badge + title (bilingual)
    rect(draw, (pro_x + 20, pro_y + 12, pro_x + 106, pro_y + 38), COLORS["pink"], width=3)
    text(draw, (pro_x + 63, pro_y + 15), "PRO", fill="white",
         f=font(14, bold=True), anchor="ma")
    text(draw, (pro_x + 116, pro_y + 15), "专业版 · Pro", f=font(20, bold=True))

    # Features list (bilingual)
    text(draw, (pro_x + 20, pro_y + 46),
         "无限色卡 · Pro 主题 · 自定义 · Pro tools",
         fill=COLORS["soft"], f=font(13))

    # Trial note (bilingual)
    text(draw, (pro_x + 20, pro_y + 64),
         "14 天免费试用，邮箱解锁 · 14-day free trial",
         fill=COLORS["soft"], f=font(12))

    # CTA button — mint, bilingual, middot, vertically centered
    # (bottom = 388+82+38 = 508, well within 560)
    cta_w = 260
    cta_h = 38
    cta_x = pro_x + 20
    cta_y = pro_y + 82
    rect(draw, (cta_x, cta_y, cta_x + cta_w, cta_y + cta_h), COLORS["mint"], width=4)
    text(draw, (cta_x + cta_w // 2, cta_y + cta_h // 2),
         "14 天免费试用 · 14-Day Trial",
         f=font(15, bold=True), anchor="mm")

    img.save(OUT / "promo-large-1400x560.png")


if __name__ == "__main__":
    small_promo()
    print(f"Generated {OUT / 'promo-small-440x280.png'} (440×280, bilingual)")
    large_promo()
    print(f"Generated {OUT / 'promo-large-1400x560.png'} (1400×560, bilingual)")
