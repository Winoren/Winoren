#!/usr/bin/env python3
"""Render the public internship project overview; no personal duties or source code."""
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FONT="-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"
MONO="ui-monospace,'SF Mono',Menlo,Consolas,monospace"
for theme,c in {
    'light':dict(fg='#1F2328',secondary='#59636E',muted='#818B98',line='#EAEEF2',accent='#8250DF'),
    'dark':dict(fg='#F0F6FC',secondary='#B1BAC4',muted='#8B949E',line='#30363D',accent='#BC8CFF'),
}.items():
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="962" height="320" viewBox="0 0 962 320" role="img" aria-label="中国电信实习经历：翼龙多云资源管理平台（CMP）">', '<title>中国电信 · 实习经历 · 翼龙多云资源管理平台（CMP）</title>']
    def text(x,y,value,color,size=15,weight=400,mono=False):
        parts.append(f'<text x="{x}" y="{y}" font-family="{escape(MONO if mono else FONT,quote=True)}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')
    parts.append(f'<rect x="40" y="47" width="7" height="7" fill="{c["accent"]}"/>')
    text(56,54,'INTERNSHIP EXPERIENCE',c['accent'],11.5,600,True)
    text(40,111,'中国电信 · 实习经历',c['fg'],28,700)
    text(40,157,'翼龙多云资源管理平台（CMP）',c['fg'],22,600)
    text(40,202,'面向企业云资源使用与运营管理场景，统一管理云主机、存储、网络与备份资源。',c['secondary'],15)
    text(40,230,'对接天翼云等底层云服务，覆盖资源申请、配置、状态同步和运维管理流程。',c['secondary'],15)
    text(40,274,'业务模块：计算资源 / 存储备份 / 网络与安全 / 订单任务 / 资源巡检',c['muted'],13)
    parts.append(f'<line x1="40" y1="298" x2="922" y2="298" stroke="{c["line"]}"/>')
    parts.append('</svg>')
    (ROOT/f'assets/internship-telecom-{theme}.svg').write_text('\n'.join(parts)+'\n')
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="962" height="356" viewBox="0 0 962 356" role="img" aria-label="美的集团实习经历：QMS 智能质量管理 Agent">', '<title>美的集团 · 实习经历 · QMS 智能质量管理 Agent</title>']
    parts.append(f'<rect x="40" y="47" width="7" height="7" fill="{c["accent"]}"/>')
    text(56,54,'INTERNSHIP EXPERIENCE',c['accent'],11.5,600,True)
    text(40,111,'美的集团 · 实习经历',c['fg'],28,700)
    text(40,157,'QMS 智能质量管理 Agent',c['fg'],22,600)
    text(40,202,'面向美的 QMS 质量管理场景，提供质量数据查询与异常处置辅助能力。',c['secondary'],15)
    text(40,230,'围绕来料检验、出货检验和 PDCA 改善，辅助质量异常分析与处置建议生成。',c['secondary'],15)
    text(40,274,'业务功能：质量数据查询 / 异常线索汇总 / 改善建议草拟 / 人工审核',c['muted'],13)
    text(40,307,'Agent 能力：业务工具接入 · 质量处理 SOP · 会话上下文 · 执行权限控制',c['muted'],13)
    parts.append(f'<line x1="40" y1="334" x2="922" y2="334" stroke="{c["line"]}"/>')
    parts.append('</svg>')
    (ROOT/f'assets/internship-midea-{theme}.svg').write_text('\n'.join(parts)+'\n')

print('Rendered telecom and Midea internship project cards in light and dark themes.')
