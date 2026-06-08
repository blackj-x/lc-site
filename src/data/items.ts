// 物品数据模块 —— 唯一数据源 items.json(parse_data.py 生成,只读)
import data from './items.json';

export interface ItemEvidence {
  source: string;
  page: string;
  revid: number;
  timestamp: string;
}

export interface Item {
  slug: string;
  nameEn: string;
  /** 降级链 terminology > I18n > ''(空显示 nameEn) */
  nameZh: string;
  aliases: string[];
  type: 'tool' | 'store' | 'scrap';
  value: { min: number; max: number } | null;
  /** >1 部分 ×100 = 磅 */
  weight: number | null;
  /** 雷暴天气导电 */
  conductive: boolean | null;
  twoHanded: boolean | null;
  storePrice: number | null;
  updatedAt: string;
  evidence: ItemEvidence[];
}

export const items = data.items as Item[];
export const version = data.version as string;
export const dataUpdatedAt = data.updatedAt as string;
