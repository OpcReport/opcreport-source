# -*- coding: utf-8 -*-
"""Batch 4: apply new titles from title_batch_4.json. Only replaces the first
line starting with 'title: ' in each file; nothing else is touched."""
import json, os, statistics, sys

POSTS = r"F:\电脑文件\opcreport-blog\site\source\_posts"
MAP = r"F:\电脑文件\opcreport-blog\tools\title_batch_4.json"

with open(MAP, encoding="utf-8") as f:
    mapping = json.load(f)

old_lens, new_lens = [], []
missing, applied = [], 0

for fname, new_title in mapping.items():
    path = os.path.join(POSTS, fname)
    if not os.path.isfile(path):
        missing.append(fname)
        continue
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    lines = text.split("\n")
    idx = None
    for i, line in enumerate(lines):
        if line.startswith("title: "):
            idx = i
            break
    if idx is None:
        print(f"NO TITLE LINE: {fname}", file=sys.stderr)
        continue
    old_line = lines[idx]
    old_title = old_line[len("title: "):].strip().strip('"')
    old_lens.append(len(old_title))
    new_lens.append(len(new_title))
    lines[idx] = 'title: "' + new_title + '"'
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))
    applied += 1

over = [k for k, v in mapping.items() if len(v) > 65]
print(f"mapping entries: {len(mapping)}")
print(f"applied: {applied}, missing files: {len(missing)}")
print(f"titles over 65 chars: {len(over)} {over}")
print(f"old median: {statistics.median(old_lens):.1f}  new median: {statistics.median(new_lens):.1f}")
print(f"old max: {max(old_lens)}  new max: {max(new_lens)}")
