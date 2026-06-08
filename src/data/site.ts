// 站点级配置 —— 域名在 astro.config.mjs 的 site 字段统一配置，这里放其余站点信息
export const SITE = {
  name: '致命公司攻略社',
  shortName: '致命攻略社',
  // 默认社交分享图（public/og-default.png），各页可覆盖
  defaultOgImage: '/og-default.png',
  locale: 'zh_CN',
  // 主题色（移动端浏览器地址栏）—— 工业暗色系
  themeColor: '#14161a',
  // Cloudflare Web Analytics (RUM) beacon token（留空则不输出统计脚本）
  // ⚠ 新站必须新建 beacon，不沿用 ggd-site 的 token
  cfBeaconToken: '',
  // Google Search Console HTML 标签验证码（meta content 值，留空则不输出标签）
  // ⚠ 上线后在 GSC 注册 lethalcompany.metaup.pro 拿到后填入
  googleSiteVerification: 'UR0RG5nmu-tPhRNul1s70PYqPo8LveYuHDFw8qLPkjk',
  // AdSense 发布商 ID（账号级，与站群同主体沿用）
  // public/ads.txt：google.com, pub-1501729431443241, DIRECT, f08c47fec0942fa0
  adsenseClient: 'ca-pub-1501729431443241',
  // AdSense 广告单元 slot ID —— ⚠ 必须为本站新建单元，留空时显示占位块
  adSlots: {
    top: '2560256325',
    side: '7521928644',
  },
};
