// 天气数据模块 —— 唯一数据源 weather.json(parse_data.py 生成,只读)
import data from './weather.json';

export interface WeatherEvidence {
  source: string;
  page: string;
  revid: number;
  timestamp: string;
}

export interface Weather {
  slug: string;
  nameEn: string;
  nameZh: string;
  aliases: string[];
  /** 核自 Module:WikiAutomated WEATHER_TYPE_NAMES(0=Clear…5=Eclipsed) */
  enumIndex: number;
  effect: string;
  danger: string | null;
  affectedItems: string[];
  counter: string[];
  updatedAt: string;
  evidence: WeatherEvidence[];
}

export const weathers = data.weathers as Weather[];
export const version = data.version as string;
export const dataUpdatedAt = data.updatedAt as string;
