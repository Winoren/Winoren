#!/usr/bin/env python3
"""Render profile SVGs from a checked-in GitHub statistics snapshot."""
import base64
from collections import Counter
from datetime import datetime, timedelta, timezone
from html import escape
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'assets/stats.json').read_text())
NOW = datetime.now(timezone(timedelta(hours=8)))
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"
PALETTES = {
    'light': dict(fg='#1F2328', secondary='#59636E', muted='#818B98', line='#EAEEF2', accent='#8250DF'),
    'dark': dict(fg='#F0F6FC', secondary='#B1BAC4', muted='#8B949E', line='#30363D', accent='#BC8CFF'),
}

def start(height, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="962" height="{height}" viewBox="0 0 962 {height}" role="img" aria-label="{escape(title)}">', f'<title>{escape(title)}</title>']

def text(parts, x, y, value, color, size=15, weight=400, mono=False, anchor=None):
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    parts.append(f'<text x="{x}" y="{y}" font-family="{escape(MONO if mono else FONT, quote=True)}" font-size="{size}" font-weight="{weight}" fill="{color}"{attrs}>{escape(str(value))}</text>')

def label(parts, value, palette):
    parts.append(f'<rect x="40" y="47" width="7" height="7" fill="{palette["accent"]}"/>')
    text(parts, 56, 54, value, palette['accent'], 11.5, 600, True)

def line(parts, y, palette, x=40):
    parts.append(f'<line x1="{x}" y1="{y}" x2="922" y2="{y}" stroke="{palette["line"]}"/>')

# Embed repository owners' avatars so GitHub's image proxy needs no external resources.
AVATARS = {}
for repo in DATA['repos'][:8]:
    try:
        req = Request(repo['avatar'] + '&s=64' if '?' in repo['avatar'] else repo['avatar'] + '?s=64', headers={'User-Agent':'Winoren-profile'})
        with urlopen(req, timeout=15) as response:
            AVATARS[repo['name']] = 'data:' + response.headers.get_content_type() + ';base64,' + base64.b64encode(response.read()).decode()
    except Exception:
        pass

merged = [datetime.fromisoformat(p['merged_at'].replace('Z','+00:00')) for p in DATA['prs'] if p.get('merged_at')]
recent = sum(d >= NOW-timedelta(days=30) for d in merged)
first = min(merged) if merged else NOW
span = max(1, (NOW-first).total_seconds())

for theme, c in PALETTES.items():
    hero = start(358, 'Winoren · Agent 开发 · 后端工程 · 获奖经历')
    label(hero, 'AGENT DEVELOPER · BACKEND ENGINEERING', c)
    text(hero, 38, 128, 'Winoren', c['fg'], 48, 700)
    hero.append(f'<rect x="256" y="92" width="12" height="43" rx="2" fill="{c["accent"]}" opacity="0.45"/>')
    text(hero, 40, 173, '探索业务 Agent，也持续向 Dify、deer-flow 等 AI 开源项目贡献代码。', c['secondary'], 15.5)
    text(hero, 40, 204, '2027 届软件工程本科 · Agent Harness / MCP / 上下文工程 / Eval', c['muted'], 13)
    text(hero, 40, 231, '实习经历', c['muted'], 13)
    text(hero, 118, 231, '中国电信', c['secondary'], 14, 700)
    text(hero, 118, 259, '美的集团', c['secondary'], 14, 700)
    text(hero, 40, 301, '获奖经历', c['muted'], 13)
    text(hero, 118, 301, '第十五届蓝桥杯大赛软件赛全国一等奖', c['secondary'], 14, 500)
    text(hero, 118, 329, '睿抗（RAICOM）编程技能竞赛全国二等奖', c['secondary'], 14, 500)
    hero.append('</svg>')
    (ROOT/f'assets/hero-{theme}.svg').write_text('\n'.join(hero)+'\n')

    height = 768
    parts = start(height, f"Winoren · {DATA['total']} 个 PR 已合并")
    label(parts, 'MERGED PULL REQUESTS', c)
    text(parts, 922, 54, 'github.com/Winoren', c['muted'], 12, mono=True, anchor='end')
    line(parts, 74, c)
    text(parts, 36, 162, DATA['total'], c['fg'], 76, 700, True)
    text(parts, 155, 160, '个 PR 已合并', c['fg'], 18, 600)
    text(parts, 40, 194, f"覆盖 {DATA['repo_count']} 个他人仓库", c['secondary'], 14)
    # Every dot represents a merged PR. Stack dots by date without overlap.
    daily = Counter(d.astimezone(NOW.tzinfo).date() for d in merged)
    for day, count in sorted(daily.items()):
        d = datetime.combine(day, datetime.min.time(), tzinfo=NOW.tzinfo)
        x = 46 + max(0,min(1,(d-first).total_seconds()/span))*870
        for j in range(count):
            y = 238 - (j%4)*10
            dx = (j//4)*8
            parts.append(f'<circle cx="{x+dx:.1f}" cy="{y}" r="3.2" fill="{c["accent"]}"/>')
    line(parts, 247, c)
    text(parts, 40, 270, first.astimezone(NOW.tzinfo).strftime('%m-%d'), c['muted'], 11, mono=True)
    text(parts, 922, 270, NOW.strftime('%m-%d'), c['muted'], 11, mono=True, anchor='end')
    line(parts, 292, c)
    for idx, repo in enumerate(DATA['repos'][:8]):
        y = 335 + idx*52
        if repo['name'] in AVATARS:
            parts.append(f'<defs><clipPath id="avatar{idx}"><rect x="40" y="{y-23}" width="30" height="30" rx="7"/></clipPath></defs>')
            parts.append(f'<image x="40" y="{y-23}" width="30" height="30" href="{AVATARS[repo["name"]]}" clip-path="url(#avatar{idx})"/>')
        else:
            text(parts, 42, y, '◇', c['accent'], 24)
        text(parts, 88, y, repo['name'], c['fg'], 16, 600, True)
        detail = f"{repo['count'] or repo['adopted']} 个 PR"
        text(parts, 770, y, detail, c['fg'], 14, 600, anchor='end')
        text(parts, 922, y, f"☆ {repo['stars']/1000:.1f}k", c['secondary'], 14, 600, True, 'end')
        if idx < 7: line(parts, y+22, c, 88)
    line(parts, 744, c)
    parts.append('</svg>')
    (ROOT/f'assets/merged-prs-{theme}.svg').write_text('\n'.join(parts)+'\n')
    header = start(226, 'Winoren · PR 明细')
    label(header, 'OPEN SOURCE CONTRIBUTIONS', c)
    text(header, 38, 126, 'PR 明细', c['fg'], 42, 700)
    text(header, 40, 166, 'Winoren · 开源贡献与合并记录', c['secondary'], 15.5)
    text(header, 40, 198, f"{DATA['total']} 个 PR 已合并 · {DATA['repo_count']} 个项目", c['muted'], 13)
    text(header, 922, 198, NOW.strftime('%Y-%m-%d'), c['muted'], 12, mono=True, anchor='end')
    line(header, 225, c)
    header.append('</svg>')
    (ROOT/f'assets/contributions-header-{theme}.svg').write_text('\n'.join(header)+'\n')

    detail = start(88, 'Pull request details')
    label(detail, 'PULL REQUEST DETAILS', c)
    line(detail, 74, c)
    detail.append('</svg>')
    (ROOT/f'assets/contributions-detail-{theme}.svg').write_text('\n'.join(detail)+'\n')

print('Rendered light and dark profile and contribution SVGs.')
