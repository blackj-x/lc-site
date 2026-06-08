#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原创抽象 SVG 生成器（lc-site）
- public/monsters-art/{slug}.svg ×33 : 320x200,工业暗底+分类色边框+抽象几何剪影
- public/moons-art/{slug}.svg   ×13 : 480x320,地形剪影+着陆区/主门/防火门标记
版权说明:全部为纯几何原创示意,不描摹任何官方美术。
名称只用 entities.json / moons.json 里的 nameZh / nameEn,不自译。
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "src", "data")
MON_DIR = os.path.join(ROOT, "public", "monsters-art")
MOON_DIR = os.path.join(ROOT, "public", "moons-art")

CAT_COLOR = {"indoor": "#ff5470", "outdoor": "#3ba9ff", "daytime": "#ffd84e"}
CAT_NAME = {"indoor": "INDOOR", "outdoor": "OUTDOOR", "daytime": "DAYTIME"}

# ---------------------------------------------------------------- monsters

def power_dots(power, color, x_start, y):
    """危险度点阵(左下角):powerLevel 取整个实心点,0.5 用半透明点表示;null 不画。"""
    if power is None:
        return ""
    full = int(power)
    half = (power - full) >= 0.5
    n = full + (1 if half else 0)
    out = []
    for i in range(n):
        cx = x_start + i * 12
        op = "0.45" if (half and i == n - 1) else "1"
        out.append(f'<circle cx="{cx}" cy="{y}" r="3.6" fill="{color}" opacity="{op}"/>')
    return "".join(out)


def spiral_path(cx, cy, r0, r1, turns, steps=64):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return d


def coil_d(cx, top, bot, w, loops):
    """弹簧:上下往返折线。"""
    pts = []
    n = loops * 2
    for i in range(n + 1):
        y = top + (bot - top) * i / n
        x = cx + (w if i % 2 else -w)
        pts.append((x, y))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


# 每个 slug 一段手工几何剪影,画布中心区约 (40..210, 35..165),c=分类色
def monster_shape(slug, c):
    S = {}

    S["baboon-hawk"] = f'''
<path d="M125 100 L75 70 L95 102 L70 120 Z" fill="{c}" opacity="0.7"/>
<path d="M125 100 L175 70 L155 102 L180 120 Z" fill="{c}" opacity="0.7"/>
<ellipse cx="125" cy="108" rx="20" ry="26" fill="{c}" opacity="0.35"/>
<circle cx="125" cy="78" r="13" fill="{c}" opacity="0.9"/>
<path d="M125 84 L113 95 L125 92 Z" fill="#e8e8ec"/>
<path d="M112 70 L106 56 M138 70 L144 56" stroke="{c}" stroke-width="3" fill="none"/>'''

    S["backwater-gunkfish"] = f'''
<ellipse cx="125" cy="105" rx="48" ry="24" fill="{c}" opacity="0.45"/>
<path d="M170 105 L200 85 L200 125 Z" fill="{c}" opacity="0.7"/>
<circle cx="98" cy="98" r="5" fill="#e8e8ec" opacity="0.85"/>
<path d="M85 118 Q95 128 110 122" stroke="{c}" stroke-width="3" fill="none"/>
<circle cx="78" cy="78" r="4" fill="{c}" opacity="0.4"/>
<circle cx="68" cy="64" r="6" fill="{c}" opacity="0.3"/>
<circle cx="60" cy="48" r="8" fill="{c}" opacity="0.2"/>'''

    S["barber"] = f'''
<path d="M90 150 L160 60" stroke="{c}" stroke-width="6" stroke-linecap="round"/>
<path d="M160 150 L90 60" stroke="{c}" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
<circle cx="86" cy="156" r="11" fill="none" stroke="{c}" stroke-width="4"/>
<circle cx="164" cy="156" r="11" fill="none" stroke="{c}" stroke-width="4" opacity="0.8"/>
<path d="M160 60 L178 38 L168 64 Z" fill="{c}"/>
<path d="M90 60 L72 38 L82 64 Z" fill="{c}" opacity="0.8"/>
<circle cx="125" cy="105" r="6" fill="#e8e8ec"/>'''

    S["bracken"] = f'''
<path d="M125 165 C95 140 85 105 100 70 C110 45 125 38 125 38 C125 38 140 45 150 70 C165 105 155 140 125 165 Z" fill="{c}" opacity="0.35"/>
<path d="M125 160 L125 45" stroke="{c}" stroke-width="3"/>
<path d="M125 140 L98 122 M125 120 L103 100 M125 100 L108 82 M125 140 L152 122 M125 120 L147 100 M125 100 L142 82" stroke="{c}" stroke-width="2.5" fill="none"/>
<circle cx="116" cy="62" r="3.5" fill="#ff3344"/>
<circle cx="134" cy="62" r="3.5" fill="#ff3344"/>'''

    S["bunker-spider"] = f'''
<ellipse cx="125" cy="105" rx="26" ry="20" fill="{c}" opacity="0.55"/>
<circle cx="125" cy="80" r="12" fill="{c}" opacity="0.8"/>
<path d="M104 98 L62 72 M106 108 L55 105 M108 118 L62 142 M112 124 L80 158" stroke="{c}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<path d="M146 98 L188 72 M144 108 L195 105 M142 118 L188 142 M138 124 L170 158" stroke="{c}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<circle cx="120" cy="77" r="2.5" fill="#e8e8ec"/><circle cx="130" cy="77" r="2.5" fill="#e8e8ec"/>'''

    S["butler"] = f'''
<path d="M125 60 C150 60 158 95 152 130 L98 130 C92 95 100 60 125 60 Z" fill="{c}" opacity="0.45"/>
<circle cx="125" cy="50" r="13" fill="{c}" opacity="0.85"/>
<path d="M113 72 L125 80 L137 72 L125 64 Z" fill="#e8e8ec"/>
<rect x="98" y="130" width="54" height="28" rx="4" fill="{c}" opacity="0.3"/>
<path d="M168 50 L168 150" stroke="{c}" stroke-width="4"/>
<path d="M160 150 L176 150 L172 168 L164 168 Z" fill="{c}" opacity="0.8"/>'''

    S["cadaver-bloom"] = f'''
<path d="M125 165 L125 100" stroke="{c}" stroke-width="4"/>
<ellipse cx="125" cy="78" rx="11" ry="26" fill="{c}" opacity="0.6"/>
<ellipse cx="125" cy="78" rx="11" ry="26" fill="{c}" opacity="0.5" transform="rotate(60 125 78)"/>
<ellipse cx="125" cy="78" rx="11" ry="26" fill="{c}" opacity="0.5" transform="rotate(-60 125 78)"/>
<circle cx="125" cy="78" r="9" fill="#e8e8ec" opacity="0.85"/>
<circle cx="92" cy="150" r="4" fill="{c}" opacity="0.4"/>
<circle cx="158" cy="142" r="5" fill="{c}" opacity="0.4"/>
<circle cx="105" cy="128" r="3" fill="{c}" opacity="0.3"/>'''

    S["cadaver-growth"] = f'''
<path d="M60 160 C70 120 95 100 125 102 C158 104 182 128 190 160 Z" fill="{c}" opacity="0.45"/>
<path d="M95 112 C90 92 100 78 96 62 M125 102 C128 84 118 72 124 52 M158 116 C165 96 156 84 162 66" stroke="{c}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<circle cx="96" cy="58" r="5" fill="{c}" opacity="0.8"/>
<circle cx="124" cy="48" r="6" fill="{c}" opacity="0.8"/>
<circle cx="162" cy="62" r="5" fill="{c}" opacity="0.8"/>'''

    S["circuit-bees"] = f'''
<rect x="95" y="118" width="60" height="42" rx="5" fill="{c}" opacity="0.35"/>
<path d="M95 132 L155 132 M95 146 L155 146" stroke="{c}" stroke-width="2" opacity="0.6"/>
<path d="M118 108 L130 92 L122 92 L134 74" stroke="{c}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<circle cx="86" cy="74" r="6" fill="{c}"/><ellipse cx="86" cy="65" rx="8" ry="4" fill="{c}" opacity="0.4"/>
<circle cx="160" cy="58" r="6" fill="{c}"/><ellipse cx="160" cy="49" rx="8" ry="4" fill="{c}" opacity="0.4"/>
<circle cx="186" cy="96" r="6" fill="{c}"/><ellipse cx="186" cy="87" rx="8" ry="4" fill="{c}" opacity="0.4"/>
<circle cx="62" cy="108" r="5" fill="{c}" opacity="0.8"/>'''

    S["coil-head"] = f'''
<path d="{coil_d(125, 70, 150, 18, 5)}" stroke="{c}" stroke-width="5" fill="none" stroke-linejoin="round"/>
<rect x="103" y="36" width="44" height="38" rx="6" fill="{c}" opacity="0.85"/>
<circle cx="116" cy="52" r="4" fill="#14161a"/><circle cx="134" cy="52" r="4" fill="#14161a"/>
<path d="M112 64 L138 64" stroke="#14161a" stroke-width="3"/>
<rect x="100" y="150" width="50" height="12" rx="3" fill="{c}" opacity="0.5"/>'''

    S["earth-leviathan"] = f'''
<path d="M40 158 L210 158" stroke="{c}" stroke-width="3" opacity="0.5"/>
<path d="M70 158 C70 90 180 90 180 158" fill="none" stroke="{c}" stroke-width="14" stroke-linecap="round" opacity="0.75"/>
<path d="M70 158 C70 90 180 90 180 158" fill="none" stroke="{c}" stroke-width="5" opacity="0.35" stroke-dasharray="4 8"/>
<path d="M58 150 L48 132 L66 142 Z" fill="{c}" opacity="0.5"/>
<path d="M192 150 L204 130 L186 140 Z" fill="{c}" opacity="0.5"/>
<path d="M120 96 L114 80 L126 88 Z" fill="{c}" opacity="0.45"/>'''

    S["eyeless-dog"] = f'''
<path d="M70 140 L70 100 C70 84 92 78 112 80 L160 84 C178 86 190 96 190 110 L190 140" fill="{c}" opacity="0.45"/>
<path d="M78 140 L78 162 M100 140 L100 162 M158 140 L158 162 M180 140 L180 162" stroke="{c}" stroke-width="6" stroke-linecap="round"/>
<path d="M60 92 C48 92 42 102 46 112 L70 108 Z" fill="{c}" opacity="0.75"/>
<path d="M46 112 L70 118 L62 124 Z" fill="#e8e8ec" opacity="0.8"/>
<path d="M86 80 L80 64 L94 74 Z" fill="{c}" opacity="0.6"/>'''

    S["feiopar"] = f'''
<path d="M75 145 C70 110 95 92 125 92 C155 92 178 105 182 132 L182 145" fill="{c}" opacity="0.45"/>
<circle cx="186" cy="86" r="14" fill="{c}" opacity="0.8"/>
<path d="M178 74 L172 60 L184 68 Z" fill="{c}"/>
<path d="M196 74 L202 60 L190 68 Z" fill="{c}"/>
<path d="M75 130 C50 125 42 100 52 82" stroke="{c}" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M92 145 L92 162 M118 145 L118 162 M152 145 L152 162 M174 145 L174 162" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'''

    S["forest-keeper"] = f'''
<circle cx="125" cy="48" r="9" fill="{c}" opacity="0.85"/>
<path d="M125 57 C108 60 100 78 102 96 L148 96 C150 78 142 60 125 57 Z" fill="{c}" opacity="0.5"/>
<path d="M108 96 L92 164 M142 96 L158 164" stroke="{c}" stroke-width="8" stroke-linecap="round"/>
<path d="M104 70 L70 96 M146 70 L180 96" stroke="{c}" stroke-width="6" stroke-linecap="round"/>
<path d="M86 164 L98 164 M152 164 L164 164" stroke="{c}" stroke-width="6" stroke-linecap="round"/>
<circle cx="121" cy="46" r="2" fill="#14161a"/><circle cx="129" cy="46" r="2" fill="#14161a"/>'''

    S["ghost-girl"] = f'''
<circle cx="125" cy="62" r="14" fill="{c}" opacity="0.35"/>
<path d="M108 78 L94 150 L156 150 L142 78 Z" fill="{c}" opacity="0.25"/>
<path d="M94 150 L88 160 M110 150 L108 162 M140 150 L142 162 M156 150 L162 160" stroke="{c}" stroke-width="2.5" opacity="0.3"/>
<circle cx="119" cy="60" r="2.5" fill="{c}" opacity="0.9"/>
<circle cx="131" cy="60" r="2.5" fill="{c}" opacity="0.9"/>
<path d="M105 50 C108 38 142 38 145 50" stroke="{c}" stroke-width="2" fill="none" opacity="0.4"/>'''

    S["giant-sapsucker"] = f'''
<ellipse cx="120" cy="105" rx="34" ry="42" fill="{c}" opacity="0.45"/>
<circle cx="140" cy="58" r="15" fill="{c}" opacity="0.85"/>
<path d="M153 56 L196 48 L155 66 Z" fill="{c}"/>
<path d="M96 92 L52 70 L70 104 L48 118 L96 118 Z" fill="{c}" opacity="0.65"/>
<path d="M110 147 L104 168 M132 147 L138 168" stroke="{c}" stroke-width="4.5" stroke-linecap="round"/>
<circle cx="137" cy="53" r="3" fill="#14161a"/>'''

    S["hoarding-bug"] = f'''
<ellipse cx="118" cy="108" rx="30" ry="22" fill="{c}" opacity="0.55"/>
<circle cx="150" cy="92" r="11" fill="{c}" opacity="0.85"/>
<path d="M154 84 L166 68 M158 88 L174 78" stroke="{c}" stroke-width="2.5" fill="none"/>
<ellipse cx="100" cy="84" rx="22" ry="10" fill="{c}" opacity="0.3" transform="rotate(-28 100 84)"/>
<ellipse cx="86" cy="100" rx="20" ry="8" fill="{c}" opacity="0.25" transform="rotate(-12 86 100)"/>
<path d="M104 126 L96 142 M120 128 L118 146 M136 124 L144 140" stroke="{c}" stroke-width="3"/>
<rect x="150" y="120" width="26" height="20" rx="3" fill="#e8e8ec" opacity="0.75"/>
<path d="M144 110 L156 122" stroke="{c}" stroke-width="3"/>'''

    S["hygrodere"] = f'''
<path d="M62 150 C58 120 80 108 95 114 C98 92 130 88 140 104 C158 92 184 104 182 124 C196 130 196 146 188 150 Z" fill="{c}" opacity="0.45"/>
<circle cx="100" cy="128" r="6" fill="{c}" opacity="0.5"/>
<circle cx="135" cy="118" r="8" fill="{c}" opacity="0.4"/>
<circle cx="162" cy="132" r="5" fill="{c}" opacity="0.55"/>
<circle cx="118" cy="140" r="4" fill="#e8e8ec" opacity="0.35"/>
<path d="M62 150 L188 150" stroke="{c}" stroke-width="2" opacity="0.6"/>'''

    S["jester"] = f'''
<rect x="92" y="92" width="66" height="62" rx="6" fill="{c}" opacity="0.5"/>
<path d="M92 92 L158 92" stroke="{c}" stroke-width="3"/>
<path d="M158 118 C180 118 180 100 192 100" stroke="{c}" stroke-width="4" fill="none"/>
<circle cx="194" cy="100" r="6" fill="{c}"/>
<path d="{coil_d(125, 62, 90, 10, 3)}" stroke="{c}" stroke-width="3.5" fill="none"/>
<circle cx="125" cy="48" r="11" fill="{c}" opacity="0.85"/>
<path d="M117 40 L108 26 M133 40 L142 26" stroke="{c}" stroke-width="3" stroke-linecap="round"/>
<circle cx="108" cy="24" r="3.5" fill="{c}"/><circle cx="142" cy="24" r="3.5" fill="{c}"/>
<rect x="86" y="154" width="78" height="10" rx="3" fill="{c}" opacity="0.3"/>'''

    S["kidnapper-fox"] = f'''
<path d="M72 142 C72 112 96 100 124 102 L168 106 C184 108 192 118 192 130 L192 142" fill="{c}" opacity="0.45"/>
<path d="M196 96 C210 96 214 108 208 116 L186 112 Z" fill="{c}" opacity="0.8"/>
<path d="M192 92 L188 74 L200 86 Z" fill="{c}"/>
<path d="M206 92 L214 76 L212 92 Z" fill="{c}"/>
<path d="M208 116 C200 132 178 138 162 132" stroke="#ff3344" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<path d="M80 142 L80 162 M104 142 L104 162 M158 142 L158 162 M184 142 L184 162" stroke="{c}" stroke-width="5" stroke-linecap="round"/>
<path d="M72 122 C52 116 46 98 56 84" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>'''

    S["lasso-man"] = f'''
<circle cx="110" cy="56" r="12" fill="{c}" opacity="0.85"/>
<path d="M110 68 L110 124 M110 84 L84 108 M110 84 L140 96 M110 124 L92 162 M110 124 L128 162" stroke="{c}" stroke-width="5" stroke-linecap="round" fill="none"/>
<path d="M140 96 C168 88 184 96 186 112" stroke="{c}" stroke-width="3" fill="none"/>
<circle cx="178" cy="126" r="16" fill="none" stroke="{c}" stroke-width="3.5"/>
<circle cx="178" cy="126" r="16" fill="{c}" opacity="0.15"/>'''

    S["maneater"] = f'''
<path d="M125 52 C160 52 175 86 168 122 C162 150 145 162 125 162 C105 162 88 150 82 122 C75 86 90 52 125 52 Z" fill="{c}" opacity="0.4"/>
<path d="M92 108 L102 118 L112 106 L122 118 L132 106 L142 118 L152 106 L158 114" stroke="{c}" stroke-width="3.5" fill="none" stroke-linejoin="round"/>
<circle cx="110" cy="84" r="4" fill="{c}"/><circle cx="140" cy="84" r="4" fill="{c}"/>
<path d="M125 162 L125 174" stroke="{c}" stroke-width="3" opacity="0.5"/>'''

    S["manticoil"] = f'''
<ellipse cx="125" cy="105" rx="18" ry="26" fill="{c}" opacity="0.55"/>
<circle cx="125" cy="72" r="9" fill="{c}" opacity="0.85"/>
<path d="M110 92 L52 70 L92 104 Z" fill="{c}" opacity="0.6"/>
<path d="M140 92 L198 70 L158 104 Z" fill="{c}" opacity="0.6"/>
<path d="M112 116 L62 134 L98 124 Z" fill="{c}" opacity="0.45"/>
<path d="M138 116 L188 134 L152 124 Z" fill="{c}" opacity="0.45"/>
<path d="M125 130 L118 152 M125 130 L132 152" stroke="{c}" stroke-width="3"/>'''

    S["mask-hornets"] = f'''
<path d="M100 70 C100 56 150 56 150 70 L148 108 C148 124 102 124 102 108 Z" fill="{c}" opacity="0.4"/>
<circle cx="114" cy="80" r="4" fill="#14161a" stroke="{c}" stroke-width="2"/>
<circle cx="136" cy="80" r="4" fill="#14161a" stroke="{c}" stroke-width="2"/>
<path d="M112 100 C120 108 130 108 138 100" stroke="{c}" stroke-width="2.5" fill="none"/>
<circle cx="78" cy="132" r="4" fill="{c}"/><ellipse cx="78" cy="126" rx="6" ry="3" fill="{c}" opacity="0.4"/>
<circle cx="170" cy="124" r="4" fill="{c}"/><ellipse cx="170" cy="118" rx="6" ry="3" fill="{c}" opacity="0.4"/>
<circle cx="150" cy="150" r="4" fill="{c}"/><ellipse cx="150" cy="144" rx="6" ry="3" fill="{c}" opacity="0.4"/>
<circle cx="98" cy="152" r="3.5" fill="{c}" opacity="0.8"/>'''

    S["masked"] = f'''
<path d="M125 78 L100 162 L150 162 Z" fill="{c}" opacity="0.3"/>
<ellipse cx="125" cy="60" rx="20" ry="26" fill="{c}" opacity="0.5"/>
<ellipse cx="117" cy="54" rx="4" ry="6" fill="#14161a"/>
<ellipse cx="133" cy="54" rx="4" ry="6" fill="#14161a"/>
<path d="M114 72 C120 80 130 80 136 72" stroke="#14161a" stroke-width="3" fill="none"/>
<path d="M105 96 L82 130 M145 96 L168 130" stroke="{c}" stroke-width="4.5" stroke-linecap="round"/>'''

    S["nutcracker"] = f'''
<rect x="108" y="30" width="34" height="26" rx="3" fill="{c}" opacity="0.7"/>
<rect x="106" y="56" width="38" height="34" rx="4" fill="{c}" opacity="0.5"/>
<circle cx="125" cy="70" r="6" fill="#e8e8ec"/>
<circle cx="125" cy="70" r="2.5" fill="#14161a"/>
<rect x="102" y="90" width="46" height="36" rx="4" fill="{c}" opacity="0.4"/>
<path d="M112 126 L112 162 M138 126 L138 162" stroke="{c}" stroke-width="7" stroke-linecap="round"/>
<path d="M158 80 L158 150" stroke="{c}" stroke-width="4"/>
<path d="M154 80 L162 80 L158 64 Z" fill="{c}"/>'''

    S["old-bird"] = f'''
<rect x="100" y="56" width="50" height="44" rx="6" fill="{c}" opacity="0.6"/>
<circle cx="125" cy="74" r="9" fill="#ff3344" opacity="0.9"/>
<path d="M125 74 L196 38 L196 110 Z" fill="#ff3344" opacity="0.12"/>
<path d="M104 100 L88 162 M146 100 L162 162" stroke="{c}" stroke-width="8" stroke-linecap="round"/>
<path d="M80 162 L96 162 M154 162 L170 162" stroke="{c}" stroke-width="6" stroke-linecap="round"/>
<path d="M100 64 L82 52 M150 64 L168 52" stroke="{c}" stroke-width="4" stroke-linecap="round"/>'''

    S["red-pill"] = f'''
<g transform="rotate(-24 125 105)">
<path d="M85 105 A26 26 0 0 1 111 79 L139 79 L139 131 L111 131 A26 26 0 0 1 85 105 Z" fill="#ff3344" opacity="0.75"/>
<path d="M165 105 A26 26 0 0 0 139 79 L139 131 A26 26 0 0 0 165 105 Z" fill="#e8e8ec" opacity="0.55"/>
</g>
<path d="M70 150 L180 150" stroke="{c}" stroke-width="2" opacity="0.4"/>
<circle cx="170" cy="64" r="3" fill="{c}" opacity="0.5"/>
<circle cx="84" cy="58" r="2.5" fill="{c}" opacity="0.4"/>'''

    S["roaming-locusts"] = f'''
<g fill="{c}">
<ellipse cx="90" cy="80" rx="5" ry="3"/><ellipse cx="118" cy="64" rx="5" ry="3"/><ellipse cx="150" cy="76" rx="5" ry="3"/>
<ellipse cx="172" cy="96" rx="5" ry="3"/><ellipse cx="104" cy="102" rx="5" ry="3"/><ellipse cx="136" cy="96" rx="5" ry="3"/>
<ellipse cx="80" cy="118" rx="5" ry="3"/><ellipse cx="160" cy="120" rx="5" ry="3"/><ellipse cx="120" cy="126" rx="5" ry="3"/>
<ellipse cx="142" cy="142" rx="5" ry="3"/><ellipse cx="98" cy="142" rx="5" ry="3"/>
</g>
<g fill="{c}" opacity="0.35">
<circle cx="84" cy="74" r="2"/><circle cx="124" cy="58" r="2"/><circle cx="156" cy="70" r="2"/>
<circle cx="178" cy="90" r="2"/><circle cx="70" cy="100" r="2"/><circle cx="190" cy="118" r="2"/>
</g>'''

    S["snare-flea"] = f'''
<path d="M125 18 L125 64" stroke="{c}" stroke-width="2.5" stroke-dasharray="5 4"/>
<ellipse cx="125" cy="92" rx="28" ry="24" fill="{c}" opacity="0.55"/>
<path d="M102 104 L84 130 M112 112 L102 142 M138 112 L148 142 M148 104 L166 130" stroke="{c}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<path d="M118 114 L116 134 M132 114 L134 134" stroke="{c}" stroke-width="3" stroke-linecap="round"/>
<circle cx="118" cy="86" r="3" fill="#14161a"/><circle cx="132" cy="86" r="3" fill="#14161a"/>
<path d="M40 18 L210 18" stroke="{c}" stroke-width="4" opacity="0.5"/>'''

    S["spore-lizard"] = f'''
<ellipse cx="112" cy="118" rx="42" ry="24" fill="{c}" opacity="0.5"/>
<circle cx="68" cy="104" r="14" fill="{c}" opacity="0.8"/>
<path d="M58 110 C50 114 50 120 58 122" stroke="#e8e8ec" stroke-width="2.5" fill="none"/>
<path d="M150 110 C176 100 186 80 180 60" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
<circle cx="180" cy="52" r="9" fill="{c}" opacity="0.5"/>
<circle cx="194" cy="44" r="6" fill="{c}" opacity="0.35"/>
<circle cx="170" cy="38" r="5" fill="{c}" opacity="0.3"/>
<path d="M88 138 L84 158 M110 142 L110 160 M134 138 L140 158" stroke="{c}" stroke-width="4.5" stroke-linecap="round"/>'''

    S["thumper"] = f'''
<path d="M70 96 C70 70 110 60 140 70 L196 132 C200 142 192 152 180 150 L92 138 C76 134 70 116 70 96 Z" fill="{c}" opacity="0.45"/>
<path d="M84 86 L72 70 L94 76 Z" fill="{c}" opacity="0.7"/>
<path d="M78 108 L96 112 L84 122 L102 124 L92 134" stroke="#e8e8ec" stroke-width="3" fill="none" stroke-linejoin="round"/>
<path d="M120 138 L112 164 M150 142 L146 166" stroke="{c}" stroke-width="7" stroke-linecap="round"/>
<circle cx="92" cy="92" r="3.5" fill="#14161a"/>'''

    S["tulip-snake"] = f'''
<path d="M70 158 C100 158 100 120 130 120 C160 120 160 84 130 84 C108 84 104 100 116 106" stroke="{c}" stroke-width="7" fill="none" stroke-linecap="round"/>
<circle cx="138" cy="62" r="10" fill="{c}" opacity="0.85"/>
<path d="M130 52 C122 38 132 28 140 36 C146 26 158 32 152 44 C162 44 162 56 150 56 Z" fill="{c}" opacity="0.45"/>
<path d="M148 66 L160 70" stroke="{c}" stroke-width="2.5"/>
<circle cx="135" cy="59" r="2.5" fill="#14161a"/>'''

    return S[slug]


def monster_svg(e):
    c = CAT_COLOR[e["category"]]
    name_main = e["nameZh"] or e["nameEn"]
    name_sub = e["nameEn"] if e["nameZh"] else ""
    shape = monster_shape(e["slug"], c)
    dots = power_dots(e.get("powerLevel"), c, 22, 182)
    sub = (f'<text x="302" y="186" text-anchor="end" fill="#8b92a0" font-size="10" '
           f'font-family="sans-serif">{name_sub}</text>') if name_sub else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" font-family="sans-serif" role="img" aria-label="{name_main} 抽象示意图">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#14161a"/>
      <stop offset="1" stop-color="#1c2026"/>
    </linearGradient>
  </defs>
  <rect width="320" height="200" rx="12" fill="url(#bg)"/>
  <rect x="0" y="0" width="320" height="6" rx="3" fill="{c}" opacity="0.9"/>
  <rect x="0.75" y="0.75" width="318.5" height="198.5" rx="11" fill="none" stroke="{c}" stroke-width="1.5" opacity="0.7"/>
  <path d="M0 60 L320 60 M0 130 L320 130" stroke="{c}" stroke-width="0.5" opacity="0.08"/>
  <circle cx="20" cy="22" r="4" fill="{c}"/>
  <text x="32" y="26" fill="{c}" font-size="10" letter-spacing="2">{CAT_NAME[e["category"]]}</text>
{shape}
  {dots}
  <text x="302" y="170" text-anchor="end" fill="#e8e8ec" font-size="17" font-weight="700">{name_main}</text>
  {sub}
</svg>
'''


# ---------------------------------------------------------------- moons

# 主题:地形剪影 + 装饰(全部原创几何,抽象示意)
MOON_THEME = {
    "experimentation": "desert_industrial",
    "assurance": "desert",
    "offense": "desert",
    "vow": "forest",
    "march": "forest_swamp",
    "adamance": "forest_cliff",
    "rend": "snow",
    "dine": "snow_forest",
    "titan": "snow_tower",
    "artifice": "industrial",
    "embrion": "rocky",
    "liquidation": "flooded",
    "gordion": "company",
}

THEME_SKY = {
    "desert": ("#2a2018", "#14161a"), "desert_industrial": ("#262019", "#14161a"),
    "forest": ("#17211a", "#14161a"), "forest_swamp": ("#161f1c", "#14161a"),
    "forest_cliff": ("#1a2020", "#14161a"), "snow": ("#1b2330", "#14161a"),
    "snow_forest": ("#192230", "#14161a"), "snow_tower": ("#1a2434", "#14161a"),
    "industrial": ("#20202a", "#14161a"), "rocky": ("#211d22", "#14161a"),
    "flooded": ("#152230", "#14161a"), "company": ("#1e1e22", "#14161a"),
}

GROUND = {
    "desert": "#5a4630", "desert_industrial": "#55432e", "forest": "#28402c",
    "forest_swamp": "#27392f", "forest_cliff": "#2c3a36", "snow": "#aeb8c6",
    "snow_forest": "#a6b2c2", "snow_tower": "#9faec2", "industrial": "#3a3a46",
    "rocky": "#463c44", "flooded": "#1f4a5e", "company": "#3c3c42",
}

TIER_COLOR = {"D": "#8b92a0", "C": "#8b92a0", "B": "#3ba9ff", "A": "#3ba9ff",
              "S": "#ffd84e", "S+": "#ffd84e", "S++": "#ff5470", "Safe": "#4ade80"}


def theme_scene(theme):
    """返回 (远景层, 地面装饰层)。地平线 y≈210,地面 210..320。"""
    g = GROUND[theme]
    if theme in ("desert", "desert_industrial"):
        far = (f'<path d="M0 210 Q90 168 180 206 T480 200 L480 210 Z" fill="{g}" opacity="0.35"/>'
               f'<circle cx="396" cy="74" r="20" fill="#d8c9a8" opacity="0.25"/>')
        deco = (f'<path d="M40 262 Q110 244 190 260 T420 256" stroke="#6b5638" stroke-width="2.5" fill="none" opacity="0.5"/>'
                f'<path d="M120 292 Q200 278 300 290 T460 286" stroke="#6b5638" stroke-width="2" fill="none" opacity="0.35"/>')
        if theme == "desert_industrial":
            deco += ('<rect x="330" y="176" width="10" height="34" fill="#55524a" opacity="0.8"/>'
                     '<rect x="348" y="188" width="8" height="22" fill="#55524a" opacity="0.7"/>'
                     '<path d="M335 176 C333 164 340 160 337 150" stroke="#777" stroke-width="3" fill="none" opacity="0.4"/>')
        return far, deco
    if theme in ("forest", "forest_swamp", "forest_cliff"):
        far = f'<path d="M0 212 L70 158 L140 206 L210 150 L290 204 L370 162 L480 208 L480 212 Z" fill="{g}" opacity="0.3"/>'
        deco = ""
        for x, by, s in [(60, 250, 0.9), (95, 268, 1.1), (250, 246, 0.8), (305, 262, 1.0), (432, 252, 0.9), (458, 274, 0.7)]:
            hh = 46 * s
            deco += f'<path d="M{x} {by} L{x - hh * 0.3:.0f} {by} L{x} {by - hh:.0f} L{x + hh * 0.3:.0f} {by} Z" fill="#2f4a33" opacity="0.85"/>'
        if theme == "forest_swamp":
            deco += ('<ellipse cx="190" cy="290" rx="60" ry="10" fill="#1f4a5e" opacity="0.5"/>'
                     '<ellipse cx="360" cy="300" rx="42" ry="8" fill="#1f4a5e" opacity="0.4"/>')
        if theme == "forest_cliff":
            far += '<path d="M0 212 L40 130 L96 212 Z" fill="#36464a" opacity="0.5"/><path d="M380 210 L440 124 L480 210 Z" fill="#36464a" opacity="0.45"/>'
        return far, deco
    if theme in ("snow", "snow_forest", "snow_tower"):
        far = (f'<path d="M0 212 L90 140 L170 210 L260 132 L350 208 L420 156 L480 210 L480 212 Z" fill="#5d6b80" opacity="0.4"/>'
               f'<path d="M70 156 L90 140 L110 156 Z" fill="#dfe6f0" opacity="0.5"/>'
               f'<path d="M240 148 L260 132 L280 148 Z" fill="#dfe6f0" opacity="0.5"/>')
        deco = ('<circle cx="100" cy="120" r="1.6" fill="#dfe6f0" opacity="0.7"/><circle cx="200" cy="90" r="1.4" fill="#dfe6f0" opacity="0.6"/>'
                '<circle cx="320" cy="110" r="1.6" fill="#dfe6f0" opacity="0.7"/><circle cx="420" cy="84" r="1.3" fill="#dfe6f0" opacity="0.6"/>'
                '<circle cx="150" cy="64" r="1.3" fill="#dfe6f0" opacity="0.5"/><circle cx="260" cy="246" r="1.6" fill="#fff" opacity="0.5"/>'
                '<path d="M40 270 Q140 258 240 268 T460 264" stroke="#cdd6e4" stroke-width="2" fill="none" opacity="0.4"/>')
        if theme == "snow_forest":
            for x, by, s in [(70, 252, 0.9), (110, 268, 1.0), (390, 250, 0.9), (430, 268, 1.1)]:
                hh = 44 * s
                deco += f'<path d="M{x} {by} L{x - hh * 0.3:.0f} {by} L{x} {by - hh:.0f} L{x + hh * 0.3:.0f} {by} Z" fill="#46586a" opacity="0.85"/>'
        if theme == "snow_tower":
            deco += ('<rect x="356" y="96" width="44" height="116" fill="#46586a" opacity="0.85"/>'
                     '<path d="M356 96 L378 70 L400 96 Z" fill="#46586a" opacity="0.85"/>'
                     '<path d="M312 212 L356 150" stroke="#5d6b80" stroke-width="5" opacity="0.8"/>'
                     '<path d="M320 212 L320 200 M334 212 L334 188 M346 212 L346 172" stroke="#5d6b80" stroke-width="4" opacity="0.6"/>')
        return far, deco
    if theme == "industrial":
        far = ('<rect x="30" y="140" width="40" height="72" fill="#2c2c38" opacity="0.9"/>'
               '<rect x="84" y="120" width="30" height="92" fill="#34343f" opacity="0.9"/>'
               '<rect x="350" y="130" width="46" height="82" fill="#2c2c38" opacity="0.9"/>'
               '<rect x="410" y="150" width="34" height="62" fill="#34343f" opacity="0.9"/>'
               '<rect x="92" y="130" width="6" height="6" fill="#ffd84e" opacity="0.6"/>'
               '<rect x="360" y="142" width="6" height="6" fill="#ffd84e" opacity="0.5"/>'
               '<rect x="40" y="152" width="6" height="6" fill="#ffd84e" opacity="0.4"/>')
        deco = ('<path d="M20 250 L460 250" stroke="#4a4a58" stroke-width="2" opacity="0.5" stroke-dasharray="14 10"/>'
                '<path d="M60 296 L420 296" stroke="#4a4a58" stroke-width="2" opacity="0.3" stroke-dasharray="10 14"/>')
        return far, deco
    if theme == "rocky":
        far = ('<path d="M0 212 L60 170 L120 210 L200 158 L280 208 L360 176 L480 210 L480 212 Z" fill="#3a323c" opacity="0.6"/>')
        deco = ('<path d="M90 268 L110 244 L132 268 Z" fill="#524652" opacity="0.7"/>'
                '<path d="M330 284 L356 252 L384 284 Z" fill="#524652" opacity="0.6"/>'
                '<circle cx="230" cy="290" r="6" fill="#524652" opacity="0.5"/>'
                '<circle cx="430" cy="270" r="5" fill="#524652" opacity="0.45"/>')
        return far, deco
    if theme == "flooded":
        far = '<path d="M0 212 L80 178 L160 210 L260 172 L350 208 L480 184 L480 212 Z" fill="#2a3c4a" opacity="0.5"/>'
        deco = ('<path d="M0 268 Q60 262 120 268 T240 268 T360 268 T480 268 L480 320 L0 320 Z" fill="#1f4a5e" opacity="0.55"/>'
                '<path d="M40 282 Q80 278 120 282 T220 282" stroke="#5dc8e8" stroke-width="1.5" fill="none" opacity="0.35"/>'
                '<path d="M280 296 Q330 292 380 296 T470 294" stroke="#5dc8e8" stroke-width="1.5" fill="none" opacity="0.3"/>')
        return far, deco
    # company
    far = ('<rect x="150" y="104" width="180" height="108" rx="4" fill="#2e2e36" opacity="0.95"/>'
           '<rect x="150" y="104" width="180" height="16" fill="#3c3c46"/>'
           '<rect x="172" y="136" width="22" height="18" fill="#1a1a20"/><rect x="208" y="136" width="22" height="18" fill="#1a1a20"/>'
           '<rect x="250" y="136" width="22" height="18" fill="#1a1a20"/><rect x="286" y="136" width="22" height="18" fill="#1a1a20"/>'
           '<rect x="226" y="170" width="30" height="42" fill="#15151a"/>'
           '<rect x="166" y="170" width="44" height="26" fill="#1a1a20"/>'
           '<text x="188" y="187" fill="#4ade80" font-size="11" text-anchor="middle" font-family="sans-serif">柜台</text>')
    deco = '<path d="M60 250 L420 250" stroke="#4a4a52" stroke-width="2" opacity="0.4" stroke-dasharray="12 10"/>'
    return far, deco


# 标记点位(抽象布点,不按实际比例)
MARKER_POS = {
    "default": {"ship": (110, 236), "main": (250, 222), "fire": (398, 244)},
    "gordion": {"ship": (110, 240), "main": (241, 216), "fire": None},
}


def moon_title(m):
    if m["slug"] == "gordion":
        return "公司大楼(Gordion)"
    t = f'{m["moonId"]}-{m["nameEn"]}'
    if m.get("nameZh"):
        t += f'({m["nameZh"]})'
    return t


def moon_svg(m):
    theme = MOON_THEME[m["slug"]]
    sky0, sky1 = THEME_SKY[theme]
    g = GROUND[theme]
    far, deco = theme_scene(theme)
    title = moon_title(m)
    tier = m.get("tier") or "?"
    tc = TIER_COLOR.get(tier, "#8b92a0")
    pos = MARKER_POS["gordion" if m["slug"] == "gordion" else "default"]

    def door_icon(x, y, color, w=14, h=18):
        """门形(拱顶矩形)标记,纯几何原创。(x,y) 为门底中心。"""
        hw = w / 2
        return (f'<path d="M{x - hw} {y} L{x - hw} {y - h + hw} '
                f'Q{x - hw} {y - h} {x} {y - h} Q{x + hw} {y - h} {x + hw} {y - h + hw} '
                f'L{x + hw} {y} Z" fill="{color}" opacity="0.3" stroke="{color}" stroke-width="1.8"/>'
                f'<circle cx="{x + hw - 4.5}" cy="{y - h / 2 + 2}" r="1.4" fill="{color}"/>')

    def rocket_icon(x, y, color):
        """小火箭(三角头+矩形身+双翼),纯几何。(x,y) 为火箭中心。"""
        return (f'<path d="M{x - 3.5} {y - 2} L{x} {y - 9} L{x + 3.5} {y - 2} Z" fill="{color}"/>'
                f'<rect x="{x - 3.5}" y="{y - 2}" width="7" height="9" rx="1.5" fill="{color}"/>'
                f'<path d="M{x - 3.5} {y + 7} L{x - 7} {y + 10} L{x - 3.5} {y + 4} Z" fill="{color}" opacity="0.8"/>'
                f'<path d="M{x + 3.5} {y + 7} L{x + 7} {y + 10} L{x + 3.5} {y + 4} Z" fill="{color}" opacity="0.8"/>')

    markers = []
    legend = []
    items = [("ship", "#4ade80", "飞船着陆区"),
             ("main", "#3ba9ff", "主入口" if m["slug"] != "gordion" else "入口/柜台"),
             ("fire", "#ff5470", "防火门")]
    for key, color, label in items:
        p = pos.get(key)
        if p is None:
            continue
        x, y = p
        if key == "ship":
            markers.append(f'<rect x="{x - 26}" y="{y - 12}" width="52" height="24" rx="5" fill="{color}" opacity="0.18" stroke="{color}" stroke-width="1.5"/>')
            markers.append(f'<g filter="url(#glow)">{rocket_icon(x, y, color)}</g>')
        elif key == "main":
            markers.append(f'<g filter="url(#glow)">{door_icon(x, y + 8, color, 16, 22)}</g>')
        else:
            markers.append(f'<g filter="url(#glow)">{door_icon(x, y + 7, color, 11, 15)}</g>')
        markers.append(f'<rect x="{x - 34}" y="{y + 12}" width="68" height="16" rx="4" fill="#14161a" opacity="0.85"/>')
        markers.append(f'<text x="{x}" y="{y + 24}" text-anchor="middle" fill="#e8e8ec" font-size="10">{label}</text>')

    # 右上角图例(竖排)
    ly = 22
    for key, color, label in items:
        if pos.get(key) is None:
            continue
        if key == "ship":
            icon = f'<rect x="372" y="{ly - 5}" width="14" height="10" rx="2" fill="{color}" opacity="0.25" stroke="{color}" stroke-width="1.2"/>'
        elif key == "main":
            icon = door_icon(379, ly + 5, color, 9, 11)
        else:
            icon = door_icon(379, ly + 5, color, 7, 9)
        legend.append(f'{icon}<text x="392" y="{ly + 4}" fill="#aab1bd" font-size="10">{label}</text>')
        ly += 17
    legend.insert(0, f'<rect x="362" y="8" width="110" height="{len([k for k, _, _ in items if pos.get(k)]) * 17 + 8}" rx="6" fill="#14161a" opacity="0.72" stroke="#2c3038" stroke-width="1"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 320" font-family="sans-serif" role="img" aria-label="{title} 外部布局示意图">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{sky0}"/>
      <stop offset="1" stop-color="{sky1}"/>
    </linearGradient>
    <linearGradient id="gnd" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{g}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{g}" stop-opacity="0.18"/>
    </linearGradient>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="480" height="320" rx="10" fill="url(#sky)"/>
  {far}
  <path d="M0 212 L480 212 L480 320 L0 320 Z" fill="url(#gnd)"/>
  {deco}
  {''.join(markers)}
  <text x="20" y="34" fill="#e8e8ec" font-size="18" font-weight="800">{title}</text>
  <rect x="20" y="44" width="{16 + 9 * len(tier)}" height="18" rx="9" fill="{tc}" opacity="0.18" stroke="{tc}" stroke-width="1"/>
  <text x="{28 + 4.5 * len(tier)}" y="57" text-anchor="middle" fill="{tc}" font-size="11" font-weight="700">{tier}</text>
  {''.join(legend)}
  <text x="460" y="299" text-anchor="end" fill="#8b92a0" font-size="10" font-weight="600">{m["moonId"]}-{m["nameEn"]}</text>
  <text x="460" y="313" text-anchor="end" fill="#6b7280" font-size="10">示意图,非实际比例</text>
  <rect x="1" y="1" width="478" height="318" rx="9" fill="none" stroke="#2c3038" stroke-width="2"/>
</svg>
'''


def main():
    os.makedirs(MON_DIR, exist_ok=True)
    os.makedirs(MOON_DIR, exist_ok=True)

    ents = json.load(open(os.path.join(DATA, "entities.json"), encoding="utf-8"))["entities"]
    for e in ents:
        path = os.path.join(MON_DIR, f'{e["slug"]}.svg')
        with open(path, "w", encoding="utf-8") as f:
            f.write(monster_svg(e))
    print(f"monsters-art: {len(ents)} svg")

    moons = json.load(open(os.path.join(DATA, "moons.json"), encoding="utf-8"))["moons"]
    for m in moons:
        path = os.path.join(MOON_DIR, f'{m["slug"]}.svg')
        with open(path, "w", encoding="utf-8") as f:
            f.write(moon_svg(m))
    print(f"moons-art: {len(moons)} svg")


if __name__ == "__main__":
    main()
