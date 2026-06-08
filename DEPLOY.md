# 部署到 Cloudflare(Workers 静态资产模式)

本项目是 Astro 纯静态站,构建产物在 `dist/`。部署采用 **Cloudflare Workers 静态资产**模式(非 Pages),配置在 `wrangler.jsonc`:用 `wrangler deploy` 把 `dist/` 整目录作为静态站发布。

正式域名:**lethalcompany.metaup.pro**(主域 `metaup.pro` 托管在同一 Cloudflare 账号)。

## 一、域名只在一处配置

全站域名只在 `astro.config.mjs` 的 `site` 字段:

```js
export default defineConfig({
  site: 'https://lethalcompany.metaup.pro',  // ← sitemap/canonical/OG/robots 全部由此生成
  ...
});
```

robots.txt、sitemap.xml、所有页面的 canonical 和 OG 标签都从这个值生成,改完重新部署即可。

## 二、首次/日常部署步骤

```bash
npx wrangler login     # 首次需人工 OAuth 授权(浏览器点 Allow)
npm run build          # 构建到 dist/(应产出 56 页)
npx wrangler deploy    # 把 dist/ 作为静态资产发布
```

`wrangler.jsonc` 关键配置:

```jsonc
{
  "name": "lc-site",
  "assets": {
    "directory": "./dist",
    "not_found_handling": "404-page"   // 404 时返回构建出的 /404.html
  },
  "routes": [
    // metaup.pro 在本账号,custom_domain 会自动建 DNS 记录 + 签 TLS 证书
    { "pattern": "lethalcompany.metaup.pro", "custom_domain": true }
  ]
}
```

部署成功后,正式域名几十秒内由 Cloudflare 自动签发证书并生效。
> 注:配置里未设 `workers_dev`,故 `*.workers.dev` 临时地址默认关闭(避免与正式域名重复内容被搜索引擎判重)。需要临时地址做测试时,可在 `wrangler.jsonc` 加 `"workers_dev": true`。

## 三、自定义域名的 DNS 处理

因为 `metaup.pro` 已托管在本 Cloudflare 账号,`routes` 里的 `custom_domain: true` 会自动:
1. 在 metaup.pro 这个 zone 下创建 `lethalcompany` 的 DNS 记录
2. 签发并绑定 TLS 证书
3. 把流量路由到本 Worker 的静态资产

无需手动建 DNS 记录。若主域日后迁出 Cloudflare,则需改为手动 CNAME 并自行处理证书。

## 四、验证上线(注意本机代理坑)

```bash
curl -sL -o /dev/null -w "%{http_code}\n" https://lethalcompany.metaup.pro/
```

⚠️ **本机若开了代理工具(fake-ip 模式)**,会把域名劫持解析到 `198.18.x.x`,导致本机直接访问报 522 —— 这是本机环境问题,不是站点故障。验证真实状态可:
- 用手机流量访问,或临时关闭代理;
- 或用 DoH 查真实解析:`curl -s -H "accept: application/dns-json" "https://1.1.1.1/dns-query?name=lethalcompany.metaup.pro&type=A"`(应返回 Cloudflare IP);
- 或用真实 CF IP 直连:`curl --resolve lethalcompany.metaup.pro:443:<CF_IP> https://lethalcompany.metaup.pro/`。

## 五、上线后必做(需外部凭证,填入 src/data/site.ts 后重新 deploy)

`src/data/site.ts` 里以下字段留空待填(⚠ 均须本站新建,不得沿用站群其他站的值):

- `googleSiteVerification` —— Google Search Console 注册 `lethalcompany.metaup.pro` 拿到的验证码,填入后提交 `/sitemap.xml`
- `cfBeaconToken` —— Cloudflare Web Analytics 新建 beacon 的 token
- `adSlots.top` / `adSlots.side` —— AdSense 本站新建广告单元的 slot ID(内容/流量起来后再申请)

`adsenseClient`(账号级发布商 ID)已填,与站群同主体沿用。

### SEO 提交
1. **Google Search Console**:添加站点 → 提交 `https://lethalcompany.metaup.pro/sitemap.xml`
2. **Bing Webmaster Tools**:同样提交 sitemap
3. 国内搜索引擎:百度资源平台(无 ICP 备案的海外站收录较慢,这是放海外的已知代价)
