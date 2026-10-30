#!/usr/bin/env python3
"""Split overview rows so only the PR count is a native GitHub link."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
STATS=json.loads((ROOT/'assets/stats.json').read_text())
AVATARS=json.loads((ROOT/'assets/repo-avatars.json').read_text())
FONT="-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"
MONO="ui-monospace,'SF Mono',Menlo,Consolas,monospace"

def anchor(name):
    return 'pr-'+re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')

def picture(stem,alt,width='100%'):
    return f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{stem}-dark.svg"><img src="./assets/{stem}-light.svg" width="{width}" alt="{escape(alt,quote=True)}"></picture>'

for theme in ['light','dark']:
    fg,secondary,line=('#1F2328','#59636E','#EAEEF2') if theme=='light' else ('#F0F6FC','#B1BAC4','#30363D')
    for source in ['merged-prs','contributions-overview']:
        base=(ROOT/f'assets/{source}-{theme}.svg').read_text()
        prefix=base.split('<defs>',1)[0]
        prefix=re.sub(r'height="\d+"', 'height="309"',prefix,count=1)
        prefix=re.sub(r'viewBox="0 0 962 \d+"','viewBox="0 0 962 309"',prefix,count=1)
        (ROOT/f'assets/{source}-header-{theme}.svg').write_text(prefix+'</svg>\n')
    for i,repo in enumerate(STATS['repos']):
        count=repo['count'] or repo['adopted']
        name=escape(repo['name'])
        pieces={
            'name':(0,650,f'<defs><clipPath id="avatar"><rect x="40" y="3" width="30" height="30" rx="7"/></clipPath></defs><image x="40" y="3" width="30" height="30" href="{AVATARS[repo["name"]]}" clip-path="url(#avatar)"/><text x="88" y="26" font-family="{escape(MONO,quote=True)}" font-size="16" font-weight="600" fill="{fg}">{name}</text><line x1="88" y1="48" x2="650" y2="48" stroke="{line}"/>'),
            'count':(650,140,f'<text x="770" y="26" text-anchor="end" font-family="{escape(FONT,quote=True)}" font-size="14" font-weight="600" fill="{fg}">{count} 个 PR</text><line x1="650" y1="48" x2="790" y2="48" stroke="{line}"/>'),
            'stars':(790,172,f'<text x="922" y="26" text-anchor="end" font-family="{escape(MONO,quote=True)}" font-size="14" font-weight="600" fill="{secondary}">☆ {repo["stars"]/1000:.1f}k</text><line x1="790" y1="48" x2="922" y2="48" stroke="{line}"/>'),
        }
        for kind,(x,width,body) in pieces.items():
            (ROOT/f'assets/overview-row-{i+1:02}-{kind}-{theme}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="52" viewBox="{x} 0 {width} 52"><title>{name} · {kind}</title>{body}</svg>\n')

def overview(source,count):
    rows=[picture(source+'-header','开源贡献统计')]
    for i,repo in enumerate(STATS['repos'][:count]):
        stem=f'overview-row-{i+1:02}'
        url='https://github.com/Winoren/Winoren/blob/main/CONTRIBUTIONS.md#'+anchor(repo['name'])
        row=picture(stem+'-name',repo['name'],'67.5%')
        row+=f'<a href="{url}" title="查看 {escape(repo["name"],quote=True)} 的 PR 明细">'+picture(stem+'-count',f"查看 {repo['count'] or repo['adopted']} 个 PR",'14.5%')+'</a>'
        row+=picture(stem+'-stars','Star 数','17.9%')
        rows.append('<div>'+row+'</div>')
    return '\n'.join(rows)

p=ROOT/'README.md'
s=p.read_text()
a=s.index('<picture>',s.index('</picture>')+len('</picture>'))
b=s.index('[查看 PR 明细]')
p.write_text(s[:a]+overview('merged-prs',8)+'\n\n'+s[b:])
p=ROOT/'CONTRIBUTIONS.md'
s=p.read_text()
b=re.search(r'<picture>\s*<source[^>]+contributions-detail-dark.svg',s).start()
s=overview('contributions-overview',len(STATS['repos']))+'\n\n'+s[b:]
# Explicit anchors keep deep links stable even though project headings are images.
for i,group in enumerate(json.loads((ROOT/'assets/contributions.json').read_text())):
    marker=f'  <img src="./assets/contribution-project-{i+1:02}-light.svg"'
    if f'<a name="{anchor(group["name"])}"></a>' in s:
        continue
    end=s.index(marker)
    start=s.rfind('<picture>',0,end)
    s=s[:start]+f'<a name="{anchor(group["name"])}"></a>\n\n'+s[start:]
p.write_text(s)
print('Linked 8 profile counts and all 21 detail counts to project anchors.')
