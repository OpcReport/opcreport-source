# -*- coding: utf-8 -*-
"""Apply new titles to batch 5 md files: replace only the first line starting with 'title: '."""
import json, os, sys

BASE = r"F:\电脑文件\opcreport-blog\site\source\_posts"
MAP_FILE = r"F:\电脑文件\opcreport-blog\tools\title_batch_5.json"

with open(MAP_FILE, encoding="utf-8") as f:
    mapping = json.load(f)

errors = []
applied = 0
old_lens, new_lens = [], []

for fname, new_title in sorted(mapping.items()):
    assert len(new_title) <= 65, f"{fname}: new title >65 ({len(new_title)})"
    assert '"' not in new_title, f"{fname}: title contains double quote"
    path = os.path.join(BASE, fname)
    if not os.path.isfile(path):
        errors.append(f"missing file: {fname}")
        continue
    with open(path, encoding="utf-8", newline="") as f:
        content = f.read()
    lines = content.split("\n")
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith("title: "):
            old = line[len("title: "):].strip().strip('"')
            old_lens.append(len(old))
            new_lens.append(len(new_title))
            lines[i] = 'title: "' + new_title + '"'
            replaced = True
            break
    if not replaced:
        errors.append(f"no title line: {fname}")
        continue
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))
    applied += 1

# sanity: JSON keys must exactly match actual file names
actual = {n for n in os.listdir(BASE) if n in mapping}
if len(actual) != len(mapping):
    errors.append("key/filename mismatch detected")

print(f"applied: {applied}/{len(mapping)}")
print(f"old median len: {sorted(old_lens)[len(old_lens)//2] if old_lens else '-'}")
print(f"new median len: {sorted(new_lens)[len(new_lens)//2] if new_lens else '-'}")
if errors:
    print("ERRORS:"); [print(" -", e) for e in errors]; sys.exit(1)
print("OK")
