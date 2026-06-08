# entities.json schema
顶层:`{ version, updatedAt, sources[], categories, entities[] }`
- categories: `indoor|outdoor|daytime → {name, nameEn, color, icon}`(分类色驱动 UI,沿用 ggd camps 模式)
- entity 字段:
  - `slug` nameEn 小写连字符化,发布后不可改
  - `nameEn` miraheze 页面标题(主键);`nameZh` = terminology recommended(gap 留空显示英文);`officialZh` miraheze zh-cn displaytitle;`aliases[]` 社区别名(SEO)
  - `category` 由 module isDaytime/isOutside 推导
  - `powerLevel/maxCount/hp/immortal/stunnable/doorSpeedMultiplier` ← Module:Entities/Data/v81(无匹配条目则 null,不编造)
  - `attackDamage/sciName` ← 页面 infobox
  - `behavior/counter[]/tips[]` 内容工序填充,**必须过四道事实校验闸**
  - `evidence[]` 每条含 miraheze 页 revid + 数据模块 revid
生成:`python3 scripts/parse_data.py`(测试:tests/test_parse_data.py)
