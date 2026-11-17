#!/usr/bin/env python3
"""最小化更新：只改数字和补充 PR 明细，不动样式。"""
import subprocess, os, json, re

os.chdir("/tmp/Winoren_push")

# === 1. 更新 CONTRIBUTIONS.md 里的数字 ===
contrib = open("CONTRIBUTIONS.md").read()

# 更新 overview 部分的 alt 数字
# dify 37->38
contrib = contrib.replace('alt="查看 37 个 PR"', 'alt="查看 38 个 PR"')
# weknora 18->35, remove ?v=weknora-18
contrib = re.sub(r'alt="查看 18 个 PR"', 'alt="查看 35 个 PR"', contrib)
contrib = re.sub(r'\?v=weknora-18', '', contrib)

# 更新 contribution-project-XX 的 alt 数字（项目分区头）
contrib = re.sub(r"langgenius/dify · 37 个 PR", "langgenius/dify · 38 个 PR", contrib)
contrib = re.sub(r"Tencent/WeKnora · 18 个 PR", "Tencent/WeKnora · 35 个 PR", contrib)

print("CONTRIBUTIONS.md counts updated")

# === 2. 更新 stats.json（保持旧顺序，只更新数字 + 加 BrowserSkill）===
stats = json.load(open("assets/stats.json"))
stats["total"] = 131
# 更新已有 repos 的 count
repo_map = {r["name"]: r for r in stats["repos"]}
repo_map["openclaw/openclaw"]["count"] = 0
repo_map["openclaw/openclaw"]["adopted"] = 2
repo_map["langgenius/dify"]["count"] = 38
repo_map["Tencent/WeKnora"]["count"] = 35

# 检查 BrowserSkill 是否存在
if "Tencent/BrowserSkill" not in repo_map:
    stats["repos"].append({
        "avatar": "https://avatars.githubusercontent.com/u/18461506?v=4",
        "count": 1, "adopted": 0,
        "name": "Tencent/BrowserSkill",
        "stars": 10486
    })
    print("Added Tencent/BrowserSkill")

stats["repo_count"] = len(stats["repos"])
json.dump(stats, open("assets/stats.json", "w"), indent=2, ensure_ascii=False)
print(f"stats.json: total={stats['total']}, repos={stats['repo_count']}")

# === 3. 检查 CONTRIBUTIONS.md 里有哪些 PR ===
existing_prs = set()
for m in re.finditer(r'\[#(\d+)\]\(https://github\.com/([^/)]+/[^/)]+)/pull/', contrib):
    existing_prs.add((m.group(2), int(m.group(1))))
print(f"Existing PRs in CONTRIBUTIONS.md: {len(existing_prs)}")

# === 4. 从 API 拉取最新数据 ===
TOKEN = subprocess.run('printf "protocol=https\\nhost=github.com\\n" | git credential fill', shell=True, capture_output=True, text=True).stdout
TOKEN = TOKEN.split("password=")[1].split("\n")[0].strip()

import urllib.request, urllib.parse, collections

def req(url):
    r = urllib.request.Request(url)
    r.add_header("Authorization", "token " + TOKEN)
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("User-Agent", "winoren")
    with urllib.request.urlopen(r) as resp:
        return json.load(resp)

items = []
page = 1
while True:
    q = urllib.parse.quote('is:pr is:merged author:Winoren')
    d = req(f"https://api.github.com/search/issues?q={q}&per_page=100&page={page}&sort=created&order=desc")
    items.extend(d["items"])
    if len(items) >= d["total_count"] or not d["items"]:
        break
    page += 1

groups = collections.OrderedDict()
for it in items:
    repo = "/".join(it["repository_url"].split("/repos/")[1].split("/")[-2:])
    pr = it["number"]
    merged_at = (it.get("pull_request") or {}).get("merged_at", "")[:10]
    groups.setdefault(repo, []).append({"number": pr, "title": it["title"], "merged_at": merged_at})

# 找新 PR（API 里有但 CONTRIBUTIONS.md 里没有）
new_prs_by_repo = {}
for repo, prs in groups.items():
    new = [p for p in prs if (repo, p["number"]) not in existing_prs]
    if new:
        new_prs_by_repo[repo] = new

print("\n=== NEW PRs to add ===")
for repo, prs in sorted(new_prs_by_repo.items()):
    print(f"  {repo}: {len(prs)} new")
    for p in sorted(prs, key=lambda x: x["merged_at"], reverse=True):
        print(f"    #{p['number']} [{p['merged_at']}] {p['title'][:60]}")

# === 5. 补充新 PR 到 CONTRIBUTIONS.md ===
def insert_after_block(text, anchor_marker, new_pr_records):
    """在项目区块的 SVG 图片后、现有 PR 列表前插入新条目"""
    anchor = f'<a name="{anchor_marker}"></a>'
    # 找到 anchor 后的 contribution-project SVG
    idx = text.find(anchor)
    if idx == -1:
        return text, False
    # 找下一个 ``` 之前（即 markdown 代码块开始前）
    end_marker = "\n\n> **["
    end_idx = text.find(end_marker, idx)
    if end_idx == -1:
        return text, False
    # 新条目插在 end_idx 处（即第一个现有 PR 之前）
    insert_text = "\n\n" + "\n\n".join(new_pr_records)
    new_text = text[:end_idx] + insert_text + text[end_idx:]
    return new_text, True

def make_pr_record(repo, pr):
    title = pr["title"]
    title = re.sub(r'^[A-Za-z0-9_-]+/[A-Za-z0-9_-]+:\s*', '', title)
    return f"> **[#{pr['number']}](https://github.com/{repo}/pull/{pr['number']})**\n>\n> {title}"

def anchor_for(repo):
    return "pr-" + re.sub(r'[^a-z0-9]+', '-', repo.lower()).strip('-')

# 处理新 PR
for repo, new_prs in new_prs_by_repo.items():
    new_prs_sorted = sorted(new_prs, key=lambda x: x["merged_at"], reverse=True)
    records = [make_pr_record(repo, p) for p in new_prs_sorted]
    
    if repo in repo_map or repo == "Tencent/BrowserSkill":
        if repo == "Tencent/BrowserSkill":
            # 新增项目区块 - 插在 AntOmniEvo 之后
            anchor = anchor_for(repo)
            # 找最后一个项目的结尾
            last_anchor = anchor_for("ant-research/AntOmniEvo")
            idx = contrib.rfind(last_anchor)
            # 找这个区块的结尾（下一个空行+anchor 或文件末尾）
            # 简化：找 contrib 最后一个 PR 块的末尾
            last_pr_block = contrib.rfind("> **[#")
            block_end = contrib.find("\n\n", last_pr_block)
            if block_end == -1:
                block_end = len(contrib)
            # 插在末尾
            new_section = f"\n\n<a name=\"{anchor}\"></a>\n\n> **[#746](https://github.com/Tencent/BrowserSkill/pull/746)**\n>\n> fix(vom): handle unpaired surrogates in token estimates\n"
            contrib = contrib[:block_end] + new_section + contrib[block_end:]
            print(f"  Added new repo Tencent/BrowserSkill to CONTRIBUTIONS.md")
        else:
            anchor = anchor_for(repo)
            contrib, ok = insert_after_block(contrib, anchor, records)
            if ok:
                print(f"  Inserted {len(records)} new PRs into {repo}")
            else:
                print(f"  WARNING: couldn't find anchor for {repo}")

open("CONTRIBUTIONS.md", "w").write(contrib)
print(f"\nCONTRIBUTIONS.md updated: {len(contrib)} bytes")
print(f"  PR links: {contrib.count('/pull/')}")
