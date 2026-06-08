import { defineConfig } from 'astro/config';

// 全站域名唯一配置处 —— sitemap/canonical/OG/robots 全部由 site 字段生成
export default defineConfig({
  site: 'https://lethalcompany.metaup.pro',
  // 强制绑 127.0.0.1:本机代理工具的 fake-ip DNS 会把 localhost 解析到
  // 198.18.x.x 不可绑定段,导致 astro dev 报 EADDRNOTAVAIL
  server: { host: '127.0.0.1' },
});
