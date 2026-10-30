#!/usr/bin/env python3
"""Render readable contribution records using the profile's visual palette."""
from pathlib import Path
from html import escape
import json
import re
import base64
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen

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

# Keep the detail overview complete while the profile remains a short selection.
cache_path = ROOT / 'assets/repo-avatars.json'
avatars = json.loads(cache_path.read_text()) if cache_path.exists() else {}
home = (ROOT / 'assets/merged-prs-light.svg').read_text()
for repo, data in zip(STATS['repos'][:8], re.findall(r'<image[^>]+href="(data:[^"]+)"', home)):
    avatars.setdefault(repo['name'], data)

def fetch_avatar(repo):
    request = Request(repo['avatar'], headers={'User-Agent': 'Winoren-profile'})
    with urlopen(request, timeout=15) as response:
        return repo['name'], 'data:' + response.headers.get_content_type() + ';base64,' + base64.b64encode(response.read()).decode()

missing = [repo for repo in STATS['repos'] if repo['name'] not in avatars]
with ThreadPoolExecutor(max_workers=6) as pool:
    for name, data in pool.map(fetch_avatar, missing):
        avatars[name] = data
cache_path.write_text(json.dumps(avatars, ensure_ascii=False)+'\n')

for theme, c in PALETTES.items():
    base = (ROOT / f'assets/merged-prs-{theme}.svg').read_text()
    prefix = base.split('<defs>', 1)[0]
    height = 768 + (len(STATS['repos'])-8)*52
    prefix = prefix.replace('height="768"', f'height="{height}"', 1).replace('viewBox="0 0 962 768"', f'viewBox="0 0 962 {height}"', 1)
    prefix = prefix.replace(f"覆盖 {STATS['repo_count']} 个他人仓库", f"全部 {len(STATS['repos'])} 个贡献项目")
    rows = [prefix]
    for i, repo in enumerate(STATS['repos']):
        y = 335 + i*52
        rows.append(f'<defs><clipPath id="full-avatar-{i}"><rect x="40" y="{y-23}" width="30" height="30" rx="7"/></clipPath></defs>')
        rows.append(f'<image x="40" y="{y-23}" width="30" height="30" href="{avatars[repo["name"]]}" clip-path="url(#full-avatar-{i})"/>')
        rows.append(f'<text x="88" y="{y}" font-family="{escape(MONO,quote=True)}" font-size="16" font-weight="600" fill="{c["fg"]}">{escape(repo["name"])}</text>')
        rows.append(f'<text x="770" y="{y}" text-anchor="end" font-family="{escape(FONT,quote=True)}" font-size="14" font-weight="600" fill="{c["fg"]}">{repo["count"] or repo["adopted"]} 个 PR</text>')
        rows.append(f'<text x="922" y="{y}" text-anchor="end" font-family="{escape(MONO,quote=True)}" font-size="14" font-weight="600" fill="{c["secondary"]}">☆ {repo["stars"]/1000:.1f}k</text>')
        if i < len(STATS['repos'])-1:
            rows.append(f'<line x1="88" y1="{y+22}" x2="922" y2="{y+22}" stroke="{c["line"]}"/>')
    footer = f'<line x1="40" y1="{height-24}" x2="922" y2="{height-24}" stroke="{c["line"]}"/></svg>'
    rows.append(footer)
    (ROOT / f'assets/contributions-overview-{theme}.svg').write_text('\n'.join(rows))

parts = [picture('contributions-overview', 'Winoren 的全部项目贡献统计'), picture('contributions-detail', 'Pull request details')]
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

# Add native links after rendering the visual overview and PR records.
import subprocess
import sys
subprocess.run([sys.executable, str(ROOT/'scripts/render_clickable_overviews.py')], check=True)
