// 卫星数据模块 —— 唯一数据源 moons.json(parse_data.py 生成,只读)
import data from './moons.json';

export interface MoonEvidence {
  source: string;
  page: string;
  revid: number;
  timestamp: string;
}

export interface AnnotationType {
  name: string;
  color: string;
  icon: string;
}

export interface MoonAnnotation {
  type: string;
  x: number;
  y: number;
  label: string;
  note?: string;
}

export interface MoonStrategy {
  landing?: string;
  scavenging?: string;
  evac?: string;
}

export interface Moon {
  slug: string;
  /** 编号字符串(如 '220'),title/H1 渲染用 */
  moonId: string;
  nameEn: string;
  nameZh: string;
  aliases: string[];
  /** module riskLevel 照抄 */
  tier: 'D' | 'C' | 'B' | 'A' | 'S' | 'S+' | 'S++' | 'Safe';
  cost: number | null;
  weatherPool: string[];
  interiorTypes: Record<string, number>;
  scrapCount: { min: number | null; max: number | null };
  scrapValue: { min: number; max: number };
  sizeMultiplier: number | null;
  hasTime: boolean;
  layoutNotes: string;
  image: string | null;
  imageW: number | null;
  imageH: number | null;
  annotations: MoonAnnotation[];
  strategy: MoonStrategy;
  tips: string[];
  updatedAt: string;
  evidence: MoonEvidence[];
}

export const moons = data.moons as Moon[];
export const annotationTypes = data.annotationTypes as Record<string, AnnotationType>;
export const version = data.version as string;
export const dataUpdatedAt = data.updatedAt as string;

export const getMoon = (slug: string) => moons.find((m) => m.slug === slug);

/** 标题:`${moonId}-${nameEn}` + 可选中文括注;Gordion 特例 */
export const moonTitle = (m: Moon) => {
  if (m.slug === 'gordion') return '公司大楼(Gordion)';
  return `${m.moonId}-${m.nameEn}` + (m.nameZh ? `(${m.nameZh})` : '');
};
