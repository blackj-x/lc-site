import { entities, dataUpdatedAt as entitiesUpdatedAt } from '../data/entities';
import { moons, dataUpdatedAt as moonsUpdatedAt } from '../data/moons';
import { dataUpdatedAt as itemsUpdatedAt } from '../data/items';
import { dataUpdatedAt as weatherUpdatedAt } from '../data/weather';
import { dataUpdatedAt as terminalUpdatedAt } from '../data/terminal';

export function GET({ site }) {
  const base = (site?.href ?? 'https://lethalcompany.metaup.pro/').replace(/\/$/, '');
  // 全站最新日期 —— 首页/指南/版本解读页这类聚合页用它
  const siteUpdatedAt = [entitiesUpdatedAt, moonsUpdatedAt, itemsUpdatedAt, weatherUpdatedAt, terminalUpdatedAt]
    .sort()
    .at(-1);

  // 每条 [路径, lastmod]
  const staticPaths = [
    ['', siteUpdatedAt],
    ['/monsters', entitiesUpdatedAt],
    ['/moons', moonsUpdatedAt],
    ['/items', itemsUpdatedAt],
    ['/terminal', terminalUpdatedAt],
    ['/weather', weatherUpdatedAt],
    ['/guide', siteUpdatedAt],
    ['/updates/v80', siteUpdatedAt],
    ['/updates/v81', siteUpdatedAt],
  ];
  const entityPaths = entities.map((e) => [`/monsters/${e.slug}`, e.updatedAt ?? entitiesUpdatedAt]);
  const moonPaths = moons.map((m) => [`/moons/${m.slug}`, m.updatedAt ?? moonsUpdatedAt]);

  const urls = [...staticPaths, ...entityPaths, ...moonPaths]
    .map(([p, lastmod]) => `  <url><loc>${base}${p}</loc><lastmod>${lastmod}</lastmod></url>`)
    .join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
