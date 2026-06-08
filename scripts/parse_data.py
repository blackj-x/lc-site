# -*- coding: utf-8 -*-
"""miraheze raw(wikitext + Lua 数据模块)→ 五 JSON 数据源。

数据链路(site-plan §4):
  data/raw/miraheze-raw.json      151 页 wikitext(含 revid 锚点)
  data/raw/miraheze-modules.json  Module:*/Data/v81 等 Lua 数据表
  data/raw/terminology-map.csv    术语对照表(唯一术语数据源,闸①产物)
  data/raw/terminology-official.json  官方 en→zh-cn + 实体分类
→ src/data/{entities,moons,items,weather}.json

铁律:术语只取 terminology-map.csv(recommended/aliases),gap 项保持英文;
     每条记录带 evidence(revid 锚点);数值不编造,模块里没有就留 None。
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"

# 枚举映射 —— 核自 Module:WikiAutomated(WEATHER_TYPE_NAMES)与 Module:Moons/AutoSingleInteriorRarities
WEATHER_TYPE_NAMES = {0: "Clear", 1: "Rainy", 2: "Stormy", 3: "Foggy", 4: "Flooded", 5: "Eclipsed"}
INTERIOR_NAMES = {1: "Factory", 2: "Mansion", 5: "Mineshaft"}
DATA_VERSION = "miraheze v81 (harvested 2026-06-07)"


# ---------------- Lua 数据表解析 ----------------
# 目标格式为机器生成的扁平表:data["data"]["Key"] = { k = v, arr = { 1, 2 }, map = { [1] = 300 } }

def _parse_lua_value(s, i):
    """从位置 i 解析一个 Lua 值,返回 (value, next_i)。"""
    while i < len(s) and s[i] in " \t\n":
        i += 1
    c = s[i]
    if c == '"':
        j = i + 1
        buf = []
        while s[j] != '"':
            if s[j] == "\\":
                j += 1
            buf.append(s[j])
            j += 1
        return "".join(buf), j + 1
    if c == "{":
        return _parse_lua_table(s, i)
    m = re.match(r"(true|false|nil)\b", s[i:])
    if m:
        word = m.group(1)
        val = {"true": True, "false": False, "nil": None}[word]
        return val, i + len(word)
    m = re.match(r"-?\d+\.?\d*(?:[eE][+-]?\d+)?", s[i:])
    if m:
        txt = m.group(0)
        return (float(txt) if ("." in txt or "e" in txt or "E" in txt) else int(txt)), i + len(txt)
    raise ValueError(f"无法解析 Lua 值: ...{s[i:i+40]!r}")


def _parse_lua_table(s, i):
    """解析 { ... },数组形式返回 list,键值形式返回 dict,空表返回 []。"""
    assert s[i] == "{"
    i += 1
    arr, mapping = [], {}
    while True:
        while i < len(s) and s[i] in " \t\n,":
            i += 1
        if s[i] == "}":
            i += 1
            break
        m = re.match(r"\[(\d+)\]\s*=\s*", s[i:])
        if m:  # [1] = v
            key = int(m.group(1))
            val, i = _parse_lua_value(s, i + m.end())
            mapping[key] = val
            continue
        m = re.match(r"([A-Za-z_]\w*)\s*=\s*", s[i:])
        if m:  # k = v
            key = m.group(1)
            val, i = _parse_lua_value(s, i + m.end())
            mapping[key] = val
            continue
        val, i = _parse_lua_value(s, i)  # 数组元素
        arr.append(val)
    if mapping and arr:
        mapping.update({idx + 1: v for idx, v in enumerate(arr)})
        return mapping, i
    if mapping:
        return mapping, i
    return arr, i


def parse_lua_data(lua_src):
    """提取 data["data"]["X"] = {...} 全部条目。"""
    out = {}
    for m in re.finditer(r'data\["data"\]\["([^"]+)"\]\s*=\s*', lua_src):
        key = m.group(1)
        val, _ = _parse_lua_value(lua_src, m.end())
        out[key] = val
    return out


# ---------------- 术语表 ----------------

def load_terminology(csv_path):
    """en_key → {recommended, aliases[], type, conflict}。术语唯一数据源(闸①)。"""
    out = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            aliases = [a.strip() for a in (row.get("aliases") or "").split(";") if a.strip()]
            out[row["en_key"]] = {
                "recommended": (row.get("recommended_zh") or "").strip(),
                "aliases": aliases,
                "type": row.get("type", ""),
                "conflict": row.get("conflict", ""),
            }
    return out


def _name_zh(en_key, term, fallback=""):
    """nameZh 降级链:terminology recommended > fallback(如 I18n)> ''。
    recommended 等于英文主键本身(官方未翻占位)视为空。"""
    rec = term.get(en_key, {}).get("recommended", "")
    if rec and rec.lower() != en_key.lower():
        return rec
    if fallback:
        return fallback
    return ""


def _aliases(en_key, term, extra=None):
    out = list(term.get(en_key, {}).get("aliases", []))
    for x in extra or []:
        if x and x not in out:
            out.append(x)
    return out


def slugify(name_en):
    return re.sub(r"[^a-z0-9]+", "-", name_en.lower()).strip("-")


# ---------------- 通用取数 ----------------

def _infobox_field(wikitext, field):
    m = re.search(r"\|\s*" + re.escape(field) + r"\s*=\s*([^\n|]+)", wikitext)
    if not m:
        return None
    val = re.sub(r"<[^>]+>", "", m.group(1))  # 去 <translate> 等标签
    val = re.sub(r"<!--.*?-->", "", val)
    return val.strip() or None


def _evidence(raw, mods, page_title, module_title=None):
    ev = []
    pg = raw["pages"].get(page_title)
    if pg:
        ev.append({"source": "miraheze", "page": page_title, "revid": pg["revid"], "timestamp": pg["timestamp"]})
    if module_title and module_title in mods["pages"]:
        mp = mods["pages"][module_title]
        ev.append({"source": "miraheze", "page": module_title, "revid": mp["revid"], "timestamp": mp["timestamp"]})
    return ev


def _require_term(term):
    if not term:
        raise ValueError("terminology 必须先加载(术语表是 nameZh/aliases 的唯一来源,顺序依赖)")


# ---------------- 实体轴 ----------------

def build_entities(raw, mods, term, official):
    _require_term(term)
    lua = parse_lua_data(mods["pages"]["Module:Entities/Data/v81"]["lua"])
    by_mname = {k.lower(): v for k, v in lua.items()}
    by_display = {v["name"].lower(): v for v in lua.values()}

    entities = []
    for title in official["cats"]["Entities"]:
        if title == "Employee":
            continue  # 玩家本体,不建怪物页
        pg = raw["pages"].get(title)
        wikitext = pg["wikitext"] if pg else ""
        # 匹配链:infobox id(大小写不敏感)→ module name 字段 == 页面标题
        info_id = _infobox_field(wikitext, "id")
        mod = None
        if info_id:
            mod = by_mname.get(info_id.lower())
        if mod is None:
            mod = by_display.get(title.lower())

        if mod and mod.get("isDaytime"):
            category = "daytime"
        elif mod and mod.get("isOutside"):
            category = "outdoor"
        else:
            category = "indoor"

        official_zh = official["map"].get(title, "")
        if official_zh.lower() == title.lower() or official_zh.endswith("/zh-cn"):
            official_zh = ""

        entities.append({
            "slug": slugify(title),
            "nameEn": title,
            "nameZh": _name_zh(title, term),
            "officialZh": official_zh,
            "aliases": _aliases(title, term),
            "category": category,
            "powerLevel": mod.get("powerLevel") if mod else None,
            "maxCount": mod.get("maxCount") if mod else None,
            "hp": mod.get("enemyHP") if mod else None,
            "immortal": (not mod["canDie"]) if mod and mod.get("canDie") is not None else None,
            "stunnable": mod.get("stunnable") if mod else None,
            "doorSpeedMultiplier": mod.get("doorSpeedMultiplier") if mod else None,
            "attackDamage": _infobox_field(wikitext, "attack_damage"),
            "sciName": _infobox_field(wikitext, "sciname"),
            "behavior": "",      # 内容工序填充(过事实校验闸)
            "counter": [],       # 内容工序填充
            "tips": [],
            "image": None,        # SVG 工序填充
            "updatedAt": "2026-06-07",
            "evidence": _evidence(raw, mods, title, "Module:Entities/Data/v81"),
        })

    categories = {
        "indoor": {"name": "室内怪物", "nameEn": "Indoor", "color": "#ff5470", "icon": "🏭"},
        "outdoor": {"name": "室外怪物", "nameEn": "Outdoor", "color": "#3ba9ff", "icon": "🌑"},
        "daytime": {"name": "日间生物", "nameEn": "Daytime", "color": "#ffd84e", "icon": "🌤"},
    }
    return {"version": DATA_VERSION, "updatedAt": "2026-06-07",
            "sources": ["lethal.miraheze.org(浏览器/带UA curl 抓取,revid 见各条 evidence)"],
            "categories": categories, "entities": entities}


# ---------------- 卫星轴 ----------------

def build_moons(raw, mods, term, official):
    _require_term(term)
    lua = parse_lua_data(mods["pages"]["Module:Moons/Data/v81"]["lua"])
    moons = []
    for key, mod in lua.items():
        m = re.match(r"(\d+)\s+(.+)", mod["name"])  # "220 Assurance"
        moon_id, name_en = (m.group(1), m.group(2)) if m else ("", mod["name"])
        wikitext = raw["pages"].get(name_en, {}).get("wikitext", "")
        cost_raw = _infobox_field(wikitext, "routecost")
        try:
            cost = int(cost_raw) if cost_raw is not None else None
        except ValueError:
            cost = None
        rarities = mod.get("dungeonRarities") or {}
        moons.append({
            "slug": slugify(name_en),
            "moonId": moon_id,
            "nameEn": name_en,
            "nameZh": _name_zh(name_en, term),
            "aliases": _aliases(name_en, term),
            "tier": mod.get("riskLevel"),
            "cost": cost,
            "weatherPool": [WEATHER_TYPE_NAMES[i] for i in (mod.get("weatherTypes") or [])],
            "interiorTypes": {INTERIOR_NAMES[k]: v for k, v in rarities.items() if k in INTERIOR_NAMES},
            "scrapCount": {"min": mod.get("minScrap"), "max": mod.get("maxScrap")},
            "scrapValue": {"min": mod.get("minTotalScrapValue"), "max": mod.get("maxTotalScrapValue")},
            "sizeMultiplier": mod.get("sizeMultiplier"),
            "hasTime": mod.get("hasTime"),
            "layoutNotes": "",
            "image": None, "imageW": None, "imageH": None,
            "annotations": [],
            "strategy": {},
            "tips": [],
            "updatedAt": "2026-06-07",
            "evidence": _evidence(raw, mods, name_en, "Module:Moons/Data/v81"),
        })
    moons.sort(key=lambda x: (len(x["moonId"]), x["moonId"]))
    annotation_types = {
        "entrance": {"name": "主入口", "color": "#3ba9ff", "icon": "🚪"},
        "fire-exit": {"name": "防火门", "color": "#ff5470", "icon": "🧯"},
        "ship": {"name": "飞船着陆点", "color": "#4ade80", "icon": "🚀"},
        "machine": {"name": "发电装置", "color": "#ffd84e", "icon": "⚙️"},
        "hazard": {"name": "环境危害", "color": "#fb923c", "icon": "⚠️"},
        "spawn": {"name": "怪物高发区", "color": "#b06bff", "icon": "👁"},
        "item": {"name": "高价值废料区", "color": "#facc15", "icon": "💰"},
        "terrain": {"name": "地形要点", "color": "#94a3b8", "icon": "⛰"},
    }
    return {"version": DATA_VERSION, "updatedAt": "2026-06-07",
            "sources": ["lethal.miraheze.org Module:Moons/Data/v81 + 各卫星页 infobox"],
            "annotationTypes": annotation_types, "moons": moons}


# ---------------- 物品轴 ----------------

def build_items(raw, mods, term, official):
    _require_term(term)
    scraps = parse_lua_data(mods["pages"]["Module:Scraps/Data/v81"]["lua"])
    scraps_by_name = {v["name"].lower(): v for v in scraps.values()}
    store_lua = mods["pages"]["Module:Items/Data"]["lua"]
    store = _parse_items_data(store_lua)
    i18n = _parse_i18n(mods["pages"]["Module:I18n/Items"]["lua"])
    tools = set(official["cats"]["Tools"])

    titles = list(dict.fromkeys(official["cats"]["Items"] + official["cats"]["Tools"]))
    items = []
    for title in titles:
        if title == "Maneater":
            continue  # 实体+蛋双形态,归实体轴(terminology-notes §②D)
        s = scraps_by_name.get(title.lower())
        st = store.get(title) or store.get(title.replace(" (Item)", ""))
        i18n_zh = i18n.get(title) or i18n.get(title.title()) or i18n.get(title.replace("-", "-").title())
        if title in tools:
            typ = "tool"
        elif st and st.get("purchasePrice") is not None:
            typ = "store"
        else:
            typ = "scrap"
        src = s or st or {}
        value = None
        if src.get("minValue") is not None:
            value = {"min": src["minValue"], "max": src["maxValue"]}
        items.append({
            "slug": slugify(title),
            "nameEn": title,
            "nameZh": _name_zh(title, term, fallback=i18n_zh or ""),
            "aliases": _aliases(title, term, extra=[i18n_zh] if i18n_zh else []),
            "type": typ,
            "value": value,
            "weight": src.get("weight"),
            "conductive": src.get("conductive"),
            "twoHanded": src.get("twoHanded"),
            "storePrice": st.get("purchasePrice") if st else None,
            "updatedAt": "2026-06-07",
            "evidence": _evidence(raw, mods, title, "Module:Scraps/Data/v81" if s else "Module:Items/Data"),
        })
    return {"version": DATA_VERSION, "updatedAt": "2026-06-07",
            "sources": ["lethal.miraheze.org Module:Scraps/Data/v81 + Module:Items/Data + Module:I18n/Items"],
            "items": items}


def _parse_items_data(lua_src):
    """Module:Items/Data:return { ["Name"] = { ... }, ... }"""
    out = {}
    for m in re.finditer(r'\["([^"]+)"\]\s*=\s*\{', lua_src):
        val, _ = _parse_lua_value(lua_src, m.end() - 1)
        out[m.group(1)] = val
    return out


def _parse_i18n(lua_src):
    """Module:I18n/Items 的 zh-cn 段:p['zh-cn']['Boombox'] = '音响'"""
    out = {}
    for m in re.finditer(r"p\['zh-cn'\]\['([^']+)'\]\s*=\s*'([^']*)'", lua_src):
        out[m.group(1)] = m.group(2)
    return out


# ---------------- 天气轴 ----------------

def build_weather(raw, mods, term):
    _require_term(term)
    weathers = []
    for idx in sorted(WEATHER_TYPE_NAMES):
        name_en = WEATHER_TYPE_NAMES[idx]
        weathers.append({
            "slug": slugify(name_en),
            "nameEn": name_en,
            "nameZh": _name_zh(name_en, term),
            "aliases": _aliases(name_en, term),
            "enumIndex": idx,
            "effect": "",    # 内容工序填充(Weather 页 prose,过校验闸)
            "danger": None,
            "affectedItems": [],
            "counter": [],
            "updatedAt": "2026-06-07",
            "evidence": _evidence(raw, mods, "Weather", "Module:WikiAutomated"),
        })
    return {"version": DATA_VERSION, "updatedAt": "2026-06-07",
            "sources": ["Module:WikiAutomated WEATHER_TYPE_NAMES + Weather 页"],
            "weathers": weathers}


# ---------------- 入口 ----------------

def main(out_dir=None):
    out_dir = Path(out_dir) if out_dir else ROOT / "src" / "data"
    raw = json.load(open(RAW_DIR / "miraheze-raw.json"))
    mods = json.load(open(RAW_DIR / "miraheze-modules.json"))
    official = json.load(open(RAW_DIR / "terminology-official.json"))
    term = load_terminology(RAW_DIR / "terminology-map.csv")  # 顺序依赖:必须先于各 build

    outputs = {
        "entities.json": build_entities(raw, mods, term, official),
        "moons.json": build_moons(raw, mods, term, official),
        "items.json": build_items(raw, mods, term, official),
        "weather.json": build_weather(raw, mods, term),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    for fname, data in outputs.items():
        with open(out_dir / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"{fname}: {len(data.get('entities') or data.get('moons') or data.get('items') or data.get('weathers'))} 条")


if __name__ == "__main__":
    main()
