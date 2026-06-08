# 🦢 鹅鸭攻略社

> 《鹅鸭杀》(Goose Goose Duck) 中文攻略站 —— 角色图鉴 · 地图攻略 · 新手入门

🔗 **在线访问:[gooseduck.metaup.pro](https://gooseduck.metaup.pro)**

## 这是什么

为多人社交推理游戏《鹅鸭杀》打造的中文攻略站,数据驱动的纯静态站点:

- 🪿 **角色图鉴** — 53 个角色(鹅 24 / 鸭 22 / 中立 7),技能、胜利条件、实战技巧、克制关系,支持阵营筛选与搜索
- 🗺️ **地图攻略** — 12 张地图的机制特性与分阵营打法,热门图配原创 SVG 示意图 + 可交互标注(任务点 / 刀人点 / 通风口 / 视野盲区…)
- 📖 **新手入门** — 核心规则、三阵营玩法、对局流程、黑话术语表、新手避坑

## 技术栈

| | |
|---|---|
| 框架 | [Astro](https://astro.build) 静态生成(SSG),零 JS 框架依赖 |
| 数据 | JSON 数据驱动 —— 角色/地图都是数据文件,加内容不碰页面代码 |
| 部署 | Cloudflare Pages,push 即自动构建发布 |
| SEO | 每页独立 canonical / OG / 结构化数据,动态生成 sitemap 与 robots |

## 本地开发

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # 构建到 dist/
npm run preview  # 预览构建产物
```

## 项目结构

```
src/
├─ data/            # ★ 数据源:roles.json / maps.json + 类型定义 + 字段文档
├─ layouts/         # 全局布局(SEO 头部、导航、页脚)
├─ components/      # 角色卡、地图卡
├─ pages/           # 页面 + [slug] 动态详情页 + sitemap/robots 端点
└─ styles/          # 设计系统(CSS 变量:暗紫底 + 阵营色)
```

加一个角色或地图 = 往 JSON 加一条记录,详情页、列表页、sitemap 全部自动生成。

## 说明

- 本站为玩家自制的非官方攻略站,与 Gaggle Studios 无关联
- 地图示意图均为原创抽象绘制,不使用游戏素材
- 角色数据基于游戏当前版本整理,游戏更新后会持续核对修订
# lc-site
