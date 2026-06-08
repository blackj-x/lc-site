# moons.json schema
顶层:`{ version, updatedAt, sources[], annotationTypes, moons[] }`
- annotationTypes:8 类(entrance/fire-exit/ship/machine/hazard/spawn/item/terrain),百分比坐标标注层沿用 ggd 机制
- moon 字段:
  - `moonId` 编号字符串(如 '220',title/H1 渲染用,slug 不带编号)
  - `tier` = module riskLevel 照抄(D/C/B/A/S/S+/S++/Safe),不自造
  - `cost` ← 页面 infobox routecost(null=未核到)
  - `weatherPool[]` module weatherTypes 数字 → 名称(枚举核自 Module:WikiAutomated)
  - `interiorTypes` dungeonRarities → {Factory|Mansion|Mineshaft: 权重}
  - `scrapCount/scrapValue` min/max ← module
  - `annotations[]` `{type,x,y,label,note?}` 百分比坐标 0-100(SVG 工序填充)
  - `strategy{landing/scavenging/evac}` 按阶段分组(内容工序)
