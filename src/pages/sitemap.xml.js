import { entities } from '../data/entities';
import { moons } from '../data/moons';

export function GET({ site }) {
  const base = (site?.href ?? 'https://lethalcompany.metaup.pro/').replace(/\/$/, '');
  const staticPaths = [
    '',
    '/monsters',
    '/moons',
    '/items',
    '/terminal',
    '/weather',
    '/guide',
    '/updates/v80',
    '/updates/v81',
  ];
  const entityPaths = entities.map((e) => `/monsters/${e.slug}`);
  const moonPaths = moons.map((m) => `/moons/${m.slug}`);
  const urls = [...staticPaths, ...entityPaths, ...moonPaths]
    .map((p) => `  <url><loc>${base}${p}</loc></url>`)
    .join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
