# 🛰️ 致命公司攻略社

> 《致命公司》(Lethal Company) 中文攻略站 —— 怪物图鉴 · 卫星攻略 · 物品价值表 · 终端指令

🔗 **在线访问:[lethalcompany.metaup.pro](https://lethalcompany.metaup.pro)**

## 这是什么

为合作生存恐怖游戏《致命公司》打造的中文攻略站,数据驱动的纯静态站点,共 56 页:

- 👾 **怪物图鉴** — 33 种实体(室内 / 室外 / 日间),行为模式、危险等级、应对策略与实战技巧
- 🛰️ **卫星攻略** — 13 颗卫星(含 Gordion 公司大楼、泰坦等),难度、地形、天气池、刷怪与路线建议
- 💰 **物品价值表** — 90 件废料/装备的价格、重量、导电性等数值
- 🖥️ **终端指令** — 19 条终端命令速查
- 🌦️ **天气机制** — 6 种天气的影响与对策
- 📖 **新手指南 + 版本解读** — v80 / v81 改动解读

## 技术栈

| | |
|---|---|
| 框架 | [Astro](https://astro.build) 静态生成(SSG),零 JS 框架依赖 |
| 数据 | JSON 数据驱动 —— 怪物/卫星/物品都是数据文件,加内容不碰页面代码 |
| 数据管线 | Python 脚本从 miraheze 收割原料解析为结构化 JSON,内容字段独立合并 |
| 部署 | Cloudflare(Workers 静态资产模式),`wrangler deploy` 发布 `dist/` |
| SEO | 每页独立 canonical / OG / 结构化数据,动态生成 sitemap 与 robots |

## 本地开发

```bash
npm install
npm run dev      # 开发服务器 http://localhost:4321
npm run build    # 构建到 dist/(应产出 56 页)
npm run preview  # 预览构建产物

python3 -m pytest tests/ -q    # 数据管线测试(改 parse/数据前后必跑)
```

## 项目结构

```
src/
├─ data/            # ★ 唯一数据源:五个 JSON + 同名 *.schema.md 字段文档
│                   #   + *.ts 类型与访问函数 + site.ts 站点配置
├─ layouts/         # Base.astro 全局布局(SEO 头部、导航、页脚)
├─ components/      # EntityCard / MoonCard / AdSlot
├─ pages/           # 页面 + monsters|moons/[slug].astro 动态详情页
│                   #   + sitemap.xml / robots.txt 端点 + updates/vXX 版本解读
└─ styles/          # global.css 设计系统(工业暗色系)

scripts/            # parse_data.py(raw→JSON) / gen_art.py / gen_og.py
data/raw/           # miraheze 收割原料(wikitext + Lua 模块,基线 v81)
public/
├─ monsters-art/    # 33 张原创怪物 SVG
└─ moons-art/       # 13 张原创卫星 SVG
```

**加一个怪物或卫星 = 往对应 JSON 加一条记录**,详情页、列表页、sitemap 全部自动生成。
数值字段由 `scripts/parse_data.py` 从 `data/raw/` 解析生成;行为/应对/技巧等内容字段由内容工序独立合并(重跑解析脚本会覆盖内容字段,需谨慎)。

## 部署

域名在 `astro.config.mjs` 的 `site` 字段统一配置(已设为正式域名),sitemap / canonical / OG / robots 全部由它生成。
部署流程见 [`DEPLOY.md`](./DEPLOY.md),上线检查清单见 [`LAUNCH-CHECKLIST.md`](./LAUNCH-CHECKLIST.md)。

## 说明

- 本站为玩家自制的非官方攻略站,与 Zeekerss / 致命公司开发方无关联
- 所有怪物/卫星示意图均为原创 SVG 抽象绘制,不使用任何游戏截图或素材
- 数据基于 miraheze wiki 快照(基线 v81)整理,游戏更新后持续核对修订
- 术语统一采用攻略站术语表,空译名处显示英文原名,不做自译
