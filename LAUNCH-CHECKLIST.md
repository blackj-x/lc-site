# 发布检查清单(Launch Checklist)

正式域名:**lethalcompany.metaup.pro** · 构建产物:56 页(33 怪物 + 13 卫星 + 物品/终端/天气/指南/v80/v81 解读等)

---

## A. 部署(已完成)

- [x] 域名已配置:`astro.config.mjs` 的 `site` = `https://lethalcompany.metaup.pro`
- [x] `npm run build` 产出 56 页,零构建错误
- [x] `npx wrangler deploy` 发布 `dist/`(Workers 静态资产模式)
- [x] 绑定自定义域名 `lethalcompany.metaup.pro`(`wrangler.jsonc` routes,custom_domain 自动建 DNS + 签证书)
- [x] 公网验证 HTTPS 200 + 证书有效 + 各类页面出页正常

详细流程见 `DEPLOY.md`。

---

## B. 上线后必做(需外部凭证 → 填入 `src/data/site.ts` → 重新 `wrangler deploy`)

### 1. 搜索引擎验证与收录
- [ ] **Google Search Console**:注册 `lethalcompany.metaup.pro` → 验证码填 `site.ts` 的 `googleSiteVerification` → 提交 `/sitemap.xml`
- [ ] **Bing Webmaster Tools**:添加站点 → 提交 `/sitemap.xml`
- [ ] (可选)百度资源平台 —— 无 ICP 备案的海外站收录慢,已知代价
- [ ] 用 Google「富媒体结果测试」验证怪物页(FAQPage)/卫星页(Article)结构化数据

### 2. 统计
- [ ] **Cloudflare Web Analytics**:新建 beacon(⚠ 本站新建,不沿用站群其他站)→ token 填 `site.ts` 的 `cfBeaconToken`

### 3. 广告(内容/流量起来后)
- [ ] AdSense 本站新建广告单元 → slot ID 填 `site.ts` 的 `adSlots.top` / `adSlots.side`(留空时显示固定尺寸占位块,已防 CLS)
- [ ] `adsenseClient`(账号级)已填,无需改

> 上述凭证均为占位待填,任一拿到后改 `site.ts` 并重新 `wrangler deploy` 即可生效。

---

## C. 已完成(无需操作)

- ✅ 数据驱动:33 怪物 + 13 卫星 + 90 物品 + 6 天气 + 19 终端命令,改 JSON 即全站更新
- ✅ 每个怪物/卫星独立静态 URL,getStaticPaths 自动生成
- ✅ SEO:title / description / canonical / OG + Twitter 卡 / 默认社交分享图(PNG)
- ✅ 结构化数据:WebSite(首页)、FAQPage + BreadcrumbList(怪物)、Article + BreadcrumbList(卫星)
- ✅ sitemap.xml + robots.txt(构建时按 `site` 域名自动生成)
- ✅ 404 页面、theme-color、图片 lazy-load
- ✅ 响应式:移动端无横向溢出
- ✅ 全原创 SVG 素材(33 怪物 + 13 卫星 = 46 张),无游戏截图/描摹/位图
- ✅ 广告位预留:固定尺寸防 CLS(728×90 / 300×600)

---

## D. 上线后可持续补充(不阻塞发布)

- [ ] 新手指南页 `/guide` 内容深化
- [ ] 怪物强度/优先级梯队(数据字段已留,按实战填)
- [ ] 怪物/卫星数据随游戏版本复查(每条有 `updatedAt`,留意带数值的字段)
- [ ] 新版本解读页:`src/pages/updates/vXX.astro`(v81 起 Zeekerss 在 Discord 发 patch notes,miraheze Version_XX 页是存档源)

---

## E. 内容准确性铁律(继承站群红线)

- 术语只用 JSON 的 `nameZh` / `aliases`(源头是指挥部 terminology-map.csv);nameZh 空 = 显示英文,**禁止自译**
- 页面渲染的数值必须来自 JSON 字段;wiki 上游异常数据按「待核」处理(案例见 `moons.json` dataNotes 的 Dine scrapCount)
- 不整段搬运 wiki;数值断言要能在 evidence 的 revid 里找到依据
- 全部原创 SVG,无截图、无描摹、无位图嵌入
- 动 `scripts/parse_data.py` 必须走测试先行(`tests/test_parse_data.py`)
