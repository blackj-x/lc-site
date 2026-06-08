# items.json schema
顶层:`{ version, updatedAt, sources[], items[] }`
- 口径:官方 Items 91 ∪ Tools 9 − Maneater(归实体)= 90;type = tool(Tools 分类)| store(有 purchasePrice)| scrap
- `value{min,max}` ← Module:Scraps/Data/v81;`storePrice` ← Module:Items/Data purchasePrice
- `weight`(>1 部分 ×100=磅)/ `conductive`(雷暴导电)/ `twoHanded`
- `nameZh` 降级链:terminology recommended > Module:I18n/Items zh-cn > ''(竞争测试见 tests)
