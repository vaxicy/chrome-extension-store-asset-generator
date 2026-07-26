import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "store-assets" / "screenshots"
BASE.mkdir(parents=True, exist_ok=True)

W, H = 1280, 800

COLORS = {
    "ink": "#332d36",
    "soft": "#716676",
    "pink": "#ff5f9c",
    "mint": "#67d6bd",
    "cream": "#fff0a8",
    "paper": "#fff9fc",
    "panel": "#fffdf7",
    "white": "#ffffff",
    "purple": "#8c6cff",
    "blue": "#75bfe8",
    "green": "#12c96f",
}

# ── Per-language copy (screenshots are split by language, never mixed) ──
STRINGS = {
    "zh": {
        "tool": "PIXEL TOOL",
        "popup_title": "像素吸色器",
        "quick_pick": "快速取色",
        "palettes": "我的色卡组",
        "pal_names": ["默认色卡", "品牌灵感", "网页主题"],
        "pal_count": lambda i: f"{4 + i}/20 色",
        "bottom_bar": "历史 · 设置 · Pro",
        "copy": "复制颜色",
        "save": "保存到色卡",
        "default_pal": "默认色卡",
        "pal_meta": "12 个颜色 · 支持备注、搜索、排序",
        "roles": ["主按钮", "标题", "背景", "强调"],
        "history": "取色历史",
        "theme_presets": "主题预设",
        "theme_label": "主题",
        "lang_line": "简体中文",
        "export_labels": ["CSS", "SCSS", "JSON", "Tailwind", "PNG", "备份"],
        "export_details": ["变量格式", "$ 变量", "可再次导入", "配置片段", "色卡图片", "备份恢复"],
        "hist_labels": ["刚刚 · 主按钮", "3 分钟前 · 提示色", "昨天 · 标题", "昨天 · 高亮"],
        "theme_names": ["莓果像素", "森绿软糖", "月夜霓虹", "海盐气泡", "绿屏掌机", "雾粉灰调"],
    },
    "en": {
        "tool": "PIXEL TOOL",
        "popup_title": "Pixel Picker",
        "quick_pick": "Quick Pick",
        "palettes": "My Palettes",
        "pal_names": ["Default", "Brand", "Web"],
        "pal_count": lambda self: f"{4 + self}/20 colors",
        "bottom_bar": "History · Settings · Pro",
        "copy": "Copy Color",
        "save": "Save to Palette",
        "default_pal": "Default",
        "pal_meta": "12 colors · notes, search, sort",
        "roles": ["Primary", "Heading", "Background", "Accent"],
        "history": "Color History",
        "theme_presets": "Theme Presets",
        "theme_label": "Theme",
        "lang_line": "English",
        "export_labels": ["CSS", "SCSS", "JSON", "Tailwind", "PNG", "Backup"],
        "export_details": ["Variables", "$ var", "Re-import", "Config", "PNG image", "Backup & restore"],
        "hist_labels": ["Just now · Primary", "3 min ago · Hint", "Yesterday · Heading", "Yesterday · Highlight"],
        "theme_names": ["Berry Pixel", "Forest Gummy", "Neon Night", "Sea Salt", "Green Handheld", "Misty Pink"],
    },
}

# Screenshot-specific headlines / paragraphs per language.
SHOTS = {
    "zh": {
        "s1_title": "Pixel Color Picker",
        "s1_sub": "像素风网页取色、色卡管理和导出工具",
        "s1_h1": "一键吸取网页颜色",
        "s1_desc": "从网页中快速获取颜色，自动保存到色卡和历史记录。适合设计师、前端开发者和内容创作者整理灵感配色。",
        "s2_title": "Palettes & History",
        "s2_sub": "多色卡、历史记录、备注与搜索",
        "s3_title": "Export For Developers",
        "s3_sub": "CSS、SCSS、JSON、Tailwind 和 PNG 色卡导出",
        "s3_h1": "把灵感颜色变成可用代码",
        "s3_desc": "一键导出常用格式，方便放进设计系统、前端项目或团队文档。",
        "s4_title": "Pixel Pro",
        "s4_sub": "免费可用，Pro 解锁更多主题和无限色卡",
        "s4_free": "免费版",
        "s4_free_desc": "基础取色、历史记录、导出功能和最多 5 个色卡。",
        "s4_try": "适合先体验",
        "s4_pro": "Pro 版",
        "s4_pro_desc": "解锁无限色卡、Pro 主题、自定义主题和后续高级工具。提供 14 天免费试用，支持 PayPal 付款，付款后用邮箱在扩展内解锁。",
        "s4_trial": "14 天免费试用",
        "s5_title": "Themes & Languages",
        "s5_sub": "中英文界面、多套像素主题、可自定义颜色",
    },
    "en": {
        "s1_title": "Pixel Color Picker",
        "s1_sub": "Pixel-style eyedrop, palette manager & exporter",
        "s1_h1": "Pick colors in one click",
        "s1_desc": "Grab colors from any page and auto-save to palettes and history. Great for designers, developers and creators curating palettes.",
        "s2_title": "Palettes & History",
        "s2_sub": "Multiple palettes, history, notes & search",
        "s3_title": "Export For Developers",
        "s3_sub": "CSS, SCSS, JSON, Tailwind & PNG palette export",
        "s3_h1": "Turn inspiration into code",
        "s3_desc": "Export common formats in one click for design systems, frontend projects or team docs.",
        "s4_title": "Pixel Pro",
        "s4_sub": "Free to use; Pro unlocks themes & unlimited palettes",
        "s4_free": "Free",
        "s4_free_desc": "Basic eyedrop, history, export and up to 5 palettes.",
        "s4_try": "Try it first",
        "s4_pro": "Pro",
        "s4_pro_desc": "Unlock unlimited palettes, Pro themes, custom themes and advanced tools. 14-day free trial, PayPal payment, unlock in-extension by email after purchase.",
        "s4_trial": "14-Day Free Trial",
        "s5_title": "Themes & Languages",
        "s5_sub": "Bilingual UI, pixel themes & custom colors",
    },
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
    "h1": font(48, bold=True),
    "h2": font(34, bold=True),
    "h3": font(24, bold=True),
    "body": font(21),
    "small": font(16),
    "tiny": font(13),
    "pixel": font(22, pixel=True),
    "pixel_small": font(12, pixel=True),
}


def rect(draw, xy, fill, outline=COLORS["ink"], width=4):
    draw.rectangle(xy, fill=fill, outline=outline, width=width)


def text(draw, xy, value, fill=COLORS["ink"], f=None, anchor=None):
    draw.text(xy, value, fill=fill, font=f or F["body"], anchor=anchor)


def wrap(draw, value, max_width, f):
    """Word-aware wrap: keep Latin words intact, split CJK text by character."""
    def is_cjk(ch):
        return "\u4e00" <= ch <= "\u9fff"

    tokens = []
    for part in re.split(r"(\s+)", value):
        if part.isspace():
            if tokens:
                tokens[-1] += part
            else:
                tokens.append(part)
        elif any(is_cjk(c) for c in part):
            tokens.extend(list(part))
        else:
            tokens.append(part)

    lines = []
    current = ""
    for tok in tokens:
        test = current + tok
        if draw.textlength(test, font=f) <= max_width or not current:
            current = test
        else:
            lines.append(current.rstrip())
            current = tok
    if current:
        lines.append(current.rstrip())
    return lines


def paragraph(draw, xy, value, max_width, f=None, fill=COLORS["soft"], leading=10):
    f = f or F["body"]
    x, y = xy
    for line in wrap(draw, value, max_width, f):
        text(draw, (x, y), line, fill=fill, f=f)
        y += f.size + leading
    return y


def base():
    img = Image.new("RGB", (W, H), COLORS["paper"])
    draw = ImageDraw.Draw(img)
    for x in range(0, W, 24):
        draw.line([(x, 0), (x, H)], fill="#f1e4ec", width=1)
    for y in range(0, H, 24):
        draw.line([(0, y), (W, y)], fill="#f1e4ec", width=1)
    for x in range(12, W, 24):
        for y in range(12, H, 24):
            draw.rectangle((x, y, x + 2, y + 2), fill="#ffd9ea")
    return img, draw


def hero(draw, title, subtitle):
    rect(draw, (56, 52, 1224, 184), COLORS["pink"], width=5)
    text(draw, (94, 87), title, fill="white", f=F["h1"])
    text(draw, (96, 146), subtitle, fill="white", f=F["body"])


def popup_mock(draw, x, y, scale=1, lang="zh"):
    S = STRINGS[lang]
    w, h = int(360 * scale), int(520 * scale)
    rect(draw, (x + 8, y + 8, x + w + 8, y + h + 8), "#d8d1d8", outline="#d8d1d8", width=0)
    rect(draw, (x, y, x + w, y + h), COLORS["white"], width=5)
    rect(draw, (x + 14, y + 14, x + w - 18, y + 80), COLORS["pink"], width=4)
    text(draw, (x + 38, y + 28), S["tool"], fill="white", f=F["pixel_small"])
    text(draw, (x + 38, y + 48), S["popup_title"], fill="white", f=font(17, bold=True))
    rect(draw, (x + 28, y + 100, x + w - 28, y + 154), COLORS["mint"], width=4)
    text(draw, (x + w // 2, y + 117), S["quick_pick"], f=font(20, bold=True), anchor="ma")
    text(draw, (x + 28, y + 186), S["palettes"], f=font(20, bold=True))
    swatches = ["#ff6b9d", "#8c6cff", "#69d9bf", "#fff0a8", "#75bfe8", "#f05f7d"]
    for i in range(3):
        yy = y + 222 + i * 78
        rect(draw, (x + 28, yy, x + w - 28, yy + 56), COLORS["panel"], width=3)
        for j in range(4):
            color = swatches[(i + j) % len(swatches)]
            draw.rectangle((x + 46 + j * 22, yy + 14, x + 66 + j * 22, yy + 38), fill=color, outline=COLORS["ink"], width=2)
        text(draw, (x + 150, yy + 12), S["pal_names"][i], f=font(16, bold=True))
        text(draw, (x + 150, yy + 34), S["pal_count"](i), fill=COLORS["soft"], f=F["small"])
    rect(draw, (x + 28, y + h - 82, x + w - 28, y + h - 28), COLORS["cream"], width=3)
    text(draw, (x + w // 2, y + h - 66), S["bottom_bar"], f=F["small"], anchor="ma")


def palette_board(draw, x, y, w, h, lang="zh"):
    S = STRINGS[lang]
    rect(draw, (x, y, x + w, y + h), COLORS["white"], width=5)
    text(draw, (x + 32, y + 30), S["default_pal"], f=F["h3"])
    text(draw, (x + 32, y + 65), S["pal_meta"], fill=COLORS["soft"], f=F["body"])
    colors = ["#ff6b9d", "#8c6cff", "#69d9bf", "#fff0a8", "#75bfe8", "#f05f7d", "#b58af0", "#6f8f55", "#f6c65b", "#c7834f", "#76d9bd", "#d7a4b8"]
    cols = 6
    cell = 86
    sx, sy = x + 34, y + 116
    for i, c in enumerate(colors):
        cx = sx + (i % cols) * (cell + 16)
        cy = sy + (i // cols) * (cell + 52)
        rect(draw, (cx, cy, cx + cell, cy + cell), c, width=4)
        text(draw, (cx, cy + cell + 12), c, f=F["tiny"])
        text(draw, (cx, cy + cell + 32), S["roles"][i % 4], fill=COLORS["soft"], f=F["tiny"])


def export_card(draw, x, y, label, detail, color):
    rect(draw, (x, y, x + 178, y + 126), COLORS["panel"], width=4)
    rect(draw, (x + 18, y + 18, x + 68, y + 68), color, width=3)
    text(draw, (x + 88, y + 24), label, f=font(18, bold=True))
    paragraph(draw, (x + 88, y + 56), detail, 70, f=F["tiny"], fill=COLORS["soft"], leading=4)


def screenshot_1(lang="zh"):
    S, H_ = STRINGS[lang], SHOTS[lang]
    img, draw = base()
    hero(draw, H_["s1_title"], H_["s1_sub"])
    popup_mock(draw, 82, 230, lang=lang)
    text(draw, (520, 268), H_["s1_h1"], f=F["h2"])
    paragraph(draw, (522, 322), H_["s1_desc"], 610, f=F["body"])
    rect(draw, (520, 452, 1138, 532), COLORS["panel"], width=4)
    text(draw, (548, 480), "HEX", f=font(24, pixel=True))
    text(draw, (630, 476), "#FF6B9D", f=font(28, bold=True))
    rect(draw, (548, 586, 748, 654), COLORS["mint"], width=4)
    text(draw, (680, 620), S["copy"], f=font(22, bold=True), anchor="mm")
    rect(draw, (780, 586, 1016, 654), COLORS["cream"], width=4)
    text(draw, (898, 620), S["save"], f=font(22, bold=True), anchor="mm")
    img.save(BASE / lang / "screenshot-01-picker.png")


def screenshot_2(lang="zh"):
    S, H_ = STRINGS[lang], SHOTS[lang]
    img, draw = base()
    hero(draw, H_["s2_title"], H_["s2_sub"])
    palette_board(draw, 74, 234, 710, 486, lang=lang)
    rect(draw, (836, 234, 1190, 720), COLORS["white"], width=5)
    text(draw, (868, 270), S["history"], f=F["h3"])
    items = [("#ff6b9d", S["hist_labels"][0]), ("#69d9bf", S["hist_labels"][1]),
             ("#8c6cff", S["hist_labels"][2]), ("#fff0a8", S["hist_labels"][3])]
    for i, (c, label) in enumerate(items):
        yy = 330 + i * 82
        rect(draw, (868, yy, 1158, yy + 56), COLORS["panel"], width=3)
        draw.rectangle((888, yy + 13, 918, yy + 43), fill=c, outline=COLORS["ink"], width=2)
        text(draw, (940, yy + 10), c, f=F["small"])
        text(draw, (940, yy + 32), label, fill=COLORS["soft"], f=F["tiny"])
    img.save(BASE / lang / "screenshot-02-palettes-history.png")


def screenshot_3(lang="zh"):
    S, H_ = STRINGS[lang], SHOTS[lang]
    img, draw = base()
    hero(draw, H_["s3_title"], H_["s3_sub"])
    text(draw, (82, 242), H_["s3_h1"], f=F["h2"])
    paragraph(draw, (84, 300), H_["s3_desc"], 560, f=F["body"])
    exports = list(zip(
        S["export_labels"],
        S["export_details"],
        ["#ff6b9d", "#8c6cff", "#69d9bf", "#fff0a8", "#75bfe8", "#f05f7d"]))
    card_w, card_h = 178, 126
    gap_x, gap_y = 44, 30
    start_x, start_y = 84, 430
    for i, (label, detail, color) in enumerate(exports):
        col = i % 3
        row = i // 3
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)
        export_card(draw, cx, cy, label, detail, color)
    rect(draw, (740, 230, 1160, 360), "#201c2b", outline=COLORS["ink"], width=5)
    text(draw, (770, 258), ":root {", fill="#f8edf7", f=F["body"])
    text(draw, (798, 290), "--primary: #FF6B9D;", fill="#69d9bf", f=F["small"])
    text(draw, (798, 318), "--accent:  #8C6CFF;", fill="#fff0a8", f=F["small"])
    img.save(BASE / lang / "screenshot-03-export.png")


def screenshot_4(lang="zh"):
    S, H_ = STRINGS[lang], SHOTS[lang]
    img, draw = base()
    hero(draw, H_["s4_title"], H_["s4_sub"])
    rect(draw, (80, 240, 580, 650), COLORS["white"], width=5)
    text(draw, (116, 282), H_["s4_free"], f=F["h2"])
    paragraph(draw, (120, 340), H_["s4_free_desc"], 390, f=F["body"])
    rect(draw, (120, 506, 432, 574), COLORS["cream"], width=4)
    text(draw, (276, 540), H_["s4_try"], f=font(22, bold=True), anchor="mm")
    rect(draw, (700, 240, 1200, 650), COLORS["white"], width=5)
    text(draw, (736, 282), H_["s4_pro"], f=F["h2"])
    paragraph(draw, (740, 340), H_["s4_pro_desc"], 390, f=F["body"])
    rect(draw, (740, 506, 1060, 574), COLORS["mint"], width=4)
    text(draw, (900, 540), H_["s4_trial"], f=font(22, bold=True), anchor="mm")
    img.save(BASE / lang / "screenshot-04-pro.png")


def screenshot_5(lang="zh"):
    S, H_ = STRINGS[lang], SHOTS[lang]
    img, draw = base()
    hero(draw, H_["s5_title"], H_["s5_sub"])
    rect(draw, (82, 238, 1198, 690), COLORS["white"], width=5)
    text(draw, (124, 286), S["theme_presets"], f=F["h2"])
    cols = ["#ff6b9d", "#70c59b", "#6f5bd8", "#75bfe8", "#6f8f55", "#c78ca0"]
    for i, (name, color) in enumerate(zip(S["theme_names"], cols)):
        x = 124 + (i % 3) * 330
        y = 370 + (i // 3) * 116
        rect(draw, (x, y, x + 280, y + 78), COLORS["panel"], width=3)
        draw.rectangle((x + 18, y + 18, x + 58, y + 58), fill=color, outline=COLORS["ink"], width=3)
        text(draw, (x + 78, y + 18), name, f=font(18, bold=True))
        text(draw, (x + 78, y + 44), S["theme_label"], fill=COLORS["soft"], f=F["tiny"])
    rect(draw, (882, 286, 1128, 338), COLORS["cream"], width=3)
    text(draw, (912, 300), S["lang_line"], f=F["small"])
    img.save(BASE / lang / "screenshot-05-themes-language.png")


def generate(lang):
    (BASE / lang).mkdir(parents=True, exist_ok=True)
    screenshot_1(lang)
    screenshot_2(lang)
    screenshot_3(lang)
    screenshot_4(lang)
    screenshot_5(lang)
    print(f"Generated {lang} screenshots in {BASE / lang}")


if __name__ == "__main__":
    for lang in ("zh", "en"):
        generate(lang)
