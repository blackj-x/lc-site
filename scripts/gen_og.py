#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成站点默认 OG 图 public/og-default.png(1200×630)。
- 优先用 Pillow 输出 PNG;环境无 Pillow 时降级输出同构图 og-default.svg(PNG 待转换)。
- 构图:#14161a 工业暗底 + 大字「致命公司攻略社」+ 副题 + 三个分类色装饰条。
版权说明:纯文字+几何装饰,不含任何游戏素材。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")

W, H = 1200, 630
BG = "#14161a"
BG2 = "#1c2026"
FG = "#e8e8ec"
SUB = "#8b92a0"
CATS = ["#ff5470", "#3ba9ff", "#ffd84e"]  # indoor / outdoor / daytime

TITLE = "致命公司攻略社"
SUBTITLE = "怪物图鉴 · 卫星攻略 · 物品价值表"
TAG = "LETHAL COMPANY GUIDE"

FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]


def gen_png():
    from PIL import Image, ImageDraw, ImageFont

    def load_font(size):
        for p in FONT_CANDIDATES:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    continue
        return ImageFont.load_default(size)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # 垂直渐变暗底 #14161a -> #1c2026
    c0 = (0x14, 0x16, 0x1A)
    c1 = (0x1C, 0x20, 0x26)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(c0, c1)))

    # 背景细网格(工业感)
    grid = (0x23, 0x27, 0x2E)
    for x in range(0, W, 80):
        d.line([(x, 0), (x, H)], fill=grid, width=1)
    for y in range(0, H, 80):
        d.line([(0, y), (W, y)], fill=grid, width=1)

    # 顶部三个分类色装饰条
    bar_w, bar_h, gap, x0, y0 = 120, 10, 16, 80, 84
    for i, c in enumerate(CATS):
        d.rounded_rectangle([x0 + i * (bar_w + gap), y0,
                             x0 + i * (bar_w + gap) + bar_w, y0 + bar_h],
                            radius=5, fill=c)

    # 文案
    f_tag = load_font(30)
    f_title = load_font(110)
    f_sub = load_font(44)
    d.text((82, 130), TAG, font=f_tag, fill=SUB)
    d.text((76, 196), TITLE, font=f_title, fill=FG)
    d.text((82, 356), SUBTITLE, font=f_sub, fill=SUB)

    # 左下三个分类色圆点 + 右下抽象几何角饰(纯原创)
    for i, c in enumerate(CATS):
        cx, cy, r = 96 + i * 44, 540, 11
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    d.polygon([(1040, 630), (1200, 470), (1200, 630)], fill=(0x22, 0x26, 0x2D))
    d.polygon([(1110, 630), (1200, 540), (1200, 630)], fill=(0x2A, 0x2F, 0x38))
    # 底部三色细条
    seg = W // 3
    for i, c in enumerate(CATS):
        d.rectangle([i * seg, H - 6, (i + 1) * seg if i < 2 else W, H], fill=c)

    out = os.path.join(PUB, "og-default.png")
    img.save(out, "PNG")
    return out


def gen_svg_fallback():
    bars = "".join(
        f'<rect x="{80 + i * 136}" y="84" width="120" height="10" rx="5" fill="{c}"/>'
        for i, c in enumerate(CATS))
    dots = "".join(
        f'<circle cx="{96 + i * 44}" cy="540" r="11" fill="{c}"/>'
        for i, c in enumerate(CATS))
    seg = W // 3
    bottom = "".join(
        f'<rect x="{i * seg}" y="{H - 6}" width="{seg}" height="6" fill="{c}"/>'
        for i, c in enumerate(CATS))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="PingFang SC, Hiragino Sans GB, sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG2}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {bars}
  <text x="82" y="158" fill="{SUB}" font-size="30" letter-spacing="6">{TAG}</text>
  <text x="76" y="300" fill="{FG}" font-size="110" font-weight="800">{TITLE}</text>
  <text x="82" y="400" fill="{SUB}" font-size="44">{SUBTITLE}</text>
  {dots}
  <polygon points="1040,630 1200,470 1200,630" fill="#22262d"/>
  <polygon points="1110,630 1200,540 1200,630" fill="#2a2f38"/>
  {bottom}
</svg>
'''
    out = os.path.join(PUB, "og-default.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    return out


def main():
    try:
        out = gen_png()
        print(f"OK png: {out}")
    except ImportError:
        out = gen_svg_fallback()
        print(f"no Pillow -> svg fallback: {out} (PNG 待转换)")
        sys.exit(0)


if __name__ == "__main__":
    main()
