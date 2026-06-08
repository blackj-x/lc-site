// 怪物数据模块 —— 唯一数据源 entities.json(parse_data.py 生成,只读)
import data from './entities.json';

export interface EntityEvidence {
  source: string;
  page: string;
  revid: number;
  timestamp: string;
}

export interface EntityCategory {
  name: string;
  nameEn: string;
  color: string;
  icon: string;
}

export interface Entity {
  slug: string;
  nameEn: string;
  /** terminology recommended 译名,空字符串=暂无中文,显示 nameEn */
  nameZh: string;
  officialZh: string;
  aliases: string[];
  category: 'indoor' | 'outdoor' | 'daytime';
  powerLevel: number | null;
  maxCount: number | null;
  hp: string | null;
  immortal: boolean | null;
  stunnable: boolean | null;
  doorSpeedMultiplier: number | null;
  attackDamage: string | null;
  sciName: string | null;
  behavior: string;
  counter: string[];
  tips: string[];
  image: string | null;
  updatedAt: string;
  evidence: EntityEvidence[];
}

export const categories = data.categories as Record<string, EntityCategory>;
export const entities = data.entities as Entity[];
export const version = data.version as string;
export const dataUpdatedAt = data.updatedAt as string;

/** 分类中文名速查(与 categories[cat].name 一致) */
export const categoryName: Record<string, string> = Object.fromEntries(
  Object.entries(categories).map(([k, v]) => [k, v.name])
);

export const getEntity = (slug: string) => entities.find((e) => e.slug === slug);
export const entitiesByCategory = (cat: string) => entities.filter((e) => e.category === cat);

/** 显示名:nameZh 为空降级 nameEn,禁止自译 */
export const entityName = (e: Entity) => e.nameZh || e.nameEn;
