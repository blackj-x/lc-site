// 终端指令数据模块 —— 唯一数据源 terminal-commands.json(parse_data.py 生成,只读)
import data from './terminal-commands.json';

export interface CommandEvidence {
  source: string;
  page: string;
  revid: number;
  timestamp: string;
}

export interface CommandCategory {
  name: string;
  icon: string;
}

export interface TerminalCommand {
  slug: string;
  /** 指令原文,不翻译 */
  command: string;
  category: 'navigation' | 'store' | 'bestiary' | 'radar' | 'utilities' | 'misc';
  usage: string;
  effect: string;
  evidence: CommandEvidence[];
}

export const cmdCategories = data.categories as Record<string, CommandCategory>;
export const commands = data.commands as TerminalCommand[];
export const version = data.version as string;
export const dataUpdatedAt = data.updatedAt as string;
