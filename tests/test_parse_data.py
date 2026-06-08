# -*- coding: utf-8 -*-
"""parse_data 测试 —— fixture 全部为真实收割数据(data/raw/),expected 值人工核自原始 wikitext/Lua,
禁止由 parser 输出反填(CLAUDE.md Fixture-Based 测试铁律)。
数据基线:miraheze v81(Module:*/Data/v81),收割日 2026-06-07。
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import parse_data as pd  # noqa: E402

RAW = json.load(open(ROOT / "data/raw/miraheze-raw.json"))
MODS = json.load(open(ROOT / "data/raw/miraheze-modules.json"))
CSV_PATH = ROOT / "data/raw/terminology-map.csv"
OFFICIAL = json.load(open(ROOT / "data/raw/terminology-official.json"))


def entities_lua():
    return pd.parse_lua_data(MODS["pages"]["Module:Entities/Data/v81"]["lua"])


def moons_lua():
    return pd.parse_lua_data(MODS["pages"]["Module:Moons/Data/v81"]["lua"])


class TestLuaParser(unittest.TestCase):
    """单元:Lua 数据表解析(机器生成的扁平表)"""

    def test_entity_jester(self):
        # 人工核自 Module:Entities/Data/v81 原文
        j = entities_lua()["Jester"]
        self.assertEqual(j["powerLevel"], 3)
        self.assertEqual(j["maxCount"], 1)
        self.assertIs(j["canDie"], False)
        self.assertEqual(j["enemyHP"], "3")
        self.assertEqual(j["doorSpeedMultiplier"], 0.5)
        self.assertIs(j["isOutside"], False)

    def test_moon_assurance_nested_structures(self):
        a = moons_lua()["AssuranceLevel"]
        self.assertEqual(a["name"], "220 Assurance")
        self.assertEqual(a["riskLevel"], "C")
        self.assertEqual(a["weatherTypes"], [1, 2, 4, 5, 3])     # 顺序保留
        self.assertEqual(a["dungeonRarities"], {1: 300, 2: 3, 5: 40})
        self.assertEqual(a["minScrap"], 13)
        self.assertEqual(a["maxScrap"], 16)
        self.assertEqual(a["minTotalScrapValue"], 100)
        self.assertEqual(a["maxTotalScrapValue"], 250)

    def test_moon_gordion_nil_and_empty(self):
        g = moons_lua()["CompanyBuildingLevel"]
        self.assertEqual(g["name"], "71 Gordion")
        self.assertEqual(g["riskLevel"], "Safe")
        self.assertEqual(g["weatherTypes"], [])                  # 空表
        self.assertIsNone(g["dungeonRarities"])                  # nil

    def test_scrap_gold_bar(self):
        s = pd.parse_lua_data(MODS["pages"]["Module:Scraps/Data/v81"]["lua"])
        g = s["GoldBar"]
        self.assertEqual(g["minValue"], 255)
        self.assertEqual(g["maxValue"], 525)
        self.assertEqual(g["weight"], 1.73)
        self.assertIs(g["conductive"], True)
        self.assertIs(g["twoHanded"], False)


class TestTerminology(unittest.TestCase):
    """单元:术语表读取"""

    def test_bracken(self):
        t = pd.load_terminology(CSV_PATH)
        self.assertEqual(t["Bracken"]["recommended"], "蕨影")
        self.assertIn("小黑", t["Bracken"]["aliases"])
        self.assertIn("花人", t["Bracken"]["aliases"])

    def test_gap_egg_stays_empty(self):
        t = pd.load_terminology(CSV_PATH)
        self.assertEqual(t["Egg"]["recommended"], "")            # 全缺项,禁止自译


class TestEntityBuild(unittest.TestCase):
    """集成:实体轴(wiki 页 + module 数据 + 术语三源合流)"""

    @classmethod
    def setUpClass(cls):
        cls.out = pd.build_entities(RAW, MODS, pd.load_terminology(CSV_PATH), OFFICIAL)
        cls.by_en = {e["nameEn"]: e for e in cls.out["entities"]}

    def test_match_by_infobox_id_case_insensitive(self):
        # Hygrodere infobox id=Blob;Thumper infobox id=crawler(小写)—— 大小写不敏感匹配
        self.assertEqual(self.by_en["Hygrodere"]["maxCount"], 2)     # Blob 条目核实值
        self.assertEqual(self.by_en["Thumper"]["maxCount"], 4)       # Crawler 条目核实值
        self.assertEqual(self.by_en["Manticoil"]["maxCount"], 16)    # Doublewing 条目核实值

    def test_category_from_module_flags(self):
        self.assertEqual(self.by_en["Jester"]["category"], "indoor")          # isOutside=false
        self.assertEqual(self.by_en["Earth Leviathan"]["category"], "outdoor")  # SandWorm isOutside=true, isDaytime=false
        self.assertEqual(self.by_en["Manticoil"]["category"], "daytime")      # Doublewing isDaytime=true

    def test_name_zh_from_terminology(self):
        self.assertEqual(self.by_en["Bracken"]["nameZh"], "蕨影")
        self.assertIn("史莱姆", self.by_en["Hygrodere"]["aliases"])

    def test_count_excludes_employee(self):
        self.assertEqual(len(self.out["entities"]), 33)              # 34 官方分类 − Employee
        self.assertNotIn("Employee", self.by_en)

    def test_slugs_unique(self):
        slugs = [e["slug"] for e in self.out["entities"]]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_every_entity_has_revid_evidence(self):
        for e in self.out["entities"]:
            self.assertTrue(any("revid" in ev for ev in e["evidence"]),
                            f"{e['nameEn']} 缺 revid 证据锚点")

    def test_power_level_from_module(self):
        self.assertEqual(self.by_en["Bracken"]["powerLevel"], 3)     # Flowerman 条目核实值


class TestOrderDependency(unittest.TestCase):
    """顺序依赖:术语表必须先于实体构建加载(CLAUDE.md 管线顺序测试铁律)"""

    def test_build_entities_without_terminology_raises(self):
        with self.assertRaises(ValueError):
            pd.build_entities(RAW, MODS, None, OFFICIAL)


class TestMoonBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = pd.build_moons(RAW, MODS, pd.load_terminology(CSV_PATH), OFFICIAL)
        cls.by_en = {m["nameEn"]: m for m in cls.out["moons"]}

    def test_assurance(self):
        a = self.by_en["Assurance"]
        self.assertEqual(a["moonId"], "220")
        self.assertEqual(a["slug"], "assurance")
        self.assertEqual(a["tier"], "C")                             # riskLevel 照抄不自造
        self.assertEqual(a["weatherPool"], ["Rainy", "Stormy", "Flooded", "Eclipsed", "Foggy"])
        self.assertEqual(a["interiorTypes"], {"Factory": 300, "Mansion": 3, "Mineshaft": 40})
        self.assertEqual(a["scrapValue"], {"min": 100, "max": 250})
        self.assertEqual(a["cost"], 0)                               # wiki infobox routecost=0 核实

    def test_gordion(self):
        g = self.by_en["Gordion"]
        self.assertEqual(g["moonId"], "71")
        self.assertEqual(g["tier"], "Safe")
        self.assertEqual(g["weatherPool"], [])

    def test_titan_name_zh(self):
        self.assertEqual(self.by_en["Titan"]["nameZh"], "泰坦")      # 唯一跨源一致中文名

    def test_count_13(self):
        self.assertEqual(len(self.out["moons"]), 13)


class TestItemBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = pd.build_items(RAW, MODS, pd.load_terminology(CSV_PATH), OFFICIAL)
        cls.by_en = {i["nameEn"]: i for i in cls.out["items"]}

    def test_gold_bar_scrap(self):
        g = self.by_en["Gold bar"]
        self.assertEqual(g["value"], {"min": 255, "max": 525})
        self.assertEqual(g["type"], "scrap")
        self.assertEqual(g["weight"], 1.73)
        self.assertIs(g["conductive"], True)

    def test_store_item_price(self):
        b = self.by_en["Belt bag"]
        self.assertEqual(b["storePrice"], 45)                        # Items/Data purchasePrice 核实
        self.assertEqual(b["type"], "store")

    def test_name_zh_chain_terminology_beats_i18n(self):
        """降级链竞争测试:terminology(专业手电筒) 与 I18n(Pro手电筒) 同时存在 → 选 terminology"""
        p = self.by_en["Pro-flashlight"]
        self.assertEqual(p["nameZh"], "专业手电筒")
        self.assertNotEqual(p["nameZh"], "Pro手电筒")

    def test_gap_item_stays_english(self):
        self.assertEqual(self.by_en["Egg"]["nameZh"], "")            # 全缺,禁止自译

    def test_count_91_union_minus_maneater(self):
        # Items 91 ∪ Tools 9(全包含) − Maneater(归实体)= 90
        self.assertEqual(len(self.out["items"]), 90)
        self.assertNotIn("Maneater", self.by_en)

    def test_tool_type(self):
        self.assertEqual(self.by_en["Kitchen knife"]["type"], "tool")


class TestWeatherBuild(unittest.TestCase):
    def test_six_weathers_from_enum(self):
        out = pd.build_weather(RAW, MODS, pd.load_terminology(CSV_PATH))
        names = [w["nameEn"] for w in out["weathers"]]
        # WEATHER_TYPE_NAMES 核自 Module:WikiAutomated:0=Clear,1=Rainy,2=Stormy,3=Foggy,4=Flooded,5=Eclipsed
        self.assertEqual(names, ["Clear", "Rainy", "Stormy", "Foggy", "Flooded", "Eclipsed"])
        self.assertEqual(out["weathers"][5]["slug"], "eclipsed")


class TestFullPipeline(unittest.TestCase):
    """集成:端到端管线落盘"""

    def test_main_writes_five_json(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            pd.main(out_dir=td)
            outs = {p.name for p in Path(td).iterdir()}
            for f in ["entities.json", "moons.json", "items.json", "weather.json"]:
                self.assertIn(f, outs)
            ents = json.load(open(Path(td) / "entities.json"))
            self.assertIn("v81", ents["version"])
            self.assertEqual(len(ents["entities"]), 33)
            moons = json.load(open(Path(td) / "moons.json"))
            self.assertEqual(len(moons["moons"]), 13)


if __name__ == "__main__":
    unittest.main()
