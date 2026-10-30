#!/usr/bin/env python3
"""Render readable contribution records using the profile's visual palette."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
GROUPS = json.loads((ROOT / 'assets/contributions.json').read_text())
STATS = json.loads((ROOT / 'assets/stats.json').read_text())
REPOS = {repo['name']: repo for repo in STATS['repos']}
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"
PALETTES = {
    'light': dict(fg='#1F2328', secondary='#59636E', muted='#818B98', line='#EAEEF2', accent='#8250DF'),
    'dark': dict(fg='#F0F6FC', secondary='#B1BAC4', muted='#8B949E', line='#30363D', accent='#BC8CFF'),
}

def picture(stem, alt):
    return f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/{stem}-dark.svg">
  <img src="./assets/{stem}-light.svg" width="100%" alt="{escape(alt, quote=True)}">
</picture>'''

parts = [picture('merged-prs', 'Winoren 的开源贡献统计'), picture('contributions-detail', 'Pull request details')]
for i, group in enumerate(GROUPS):
    stem = f'contribution-project-{i+1:02}'
    repo = REPOS[group['name']]
    for theme, c in PALETTES.items():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="962" height="112" viewBox="0 0 962 112" role="img" aria-label="{escape(group['name'])}">
<title>{escape(group['name'])} · {len(group['prs'])} 个 PR</title>
<rect x="0" y="40" width="7" height="7" fill="{c['accent']}"/>
<text x="18" y="49" font-family="{escape(MONO,quote=True)}" font-size="21" font-weight="600" fill="{c['fg']}">{escape(group['name'])}</text>
<text x="962" y="49" text-anchor="end" font-family="{escape(FONT,quote=True)}" font-size="14" fill="{c['secondary']}">{len(group['prs'])} 个 PR · ☆ {repo['stars']/1000:.1f}k</text>
<line x1="0" y1="78" x2="962" y2="78" stroke="{c['line']}"/>
</svg>
'''
        (ROOT / f'assets/{stem}-{theme}.svg').write_text(svg)
    parts.append(picture(stem, f"{group['name']} · {len(group['prs'])} 个 PR"))
    for record in group['prs']:
        match = re.match(r'(\[#\d+\]\(https://github.com/[^)]+\)) — (.*)', record)
        if not match:
            raise ValueError(record)
        pr, description = match.groups()
        # Native Markdown keeps PR links clickable and descriptions selectable.
        description, *adoption = description.split('<br>')
        card = f'> **{pr}**\n>\n> {description}'
        if adoption:
            card += '\n>\n> <sub>' + '<br>'.join(adoption) + '</sub>'
        parts.append(card)
(ROOT / 'CONTRIBUTIONS.md').write_text('\n\n'.join(parts)+'\n')
print(f"Rendered {len(GROUPS)} project sections and {sum(len(g['prs']) for g in GROUPS)} PR records.")
