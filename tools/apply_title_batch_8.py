# -*- coding: utf-8 -*-
"""Apply new titles to first `title: ` line of each md file in the mapping."""
import json
import os
import sys

POSTS = r"F:\电脑文件\opcreport-blog\site\source\_posts"
MAP = r"F:\电脑文件\opcreport-blog\tools\title_batch_8.json"

with open(MAP, encoding="utf-8") as f:
    mapping = json.load(f)

errors = []
for name, new_title in mapping.items():
    if len(new_title) > 65:
        errors.append(f"{name}: new title too long ({len(new_title)})")
    path = os.path.join(POSTS, name)
    if not os.path.isfile(path):
        errors.append(f"{name}: file not found")
        continue
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.readlines()
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith("title: "):
            eol = "\r\n" if line.endswith("\r\n") else "\n"
            lines[i] = f'title: "{new_title}"' + eol
            replaced = True
            break
    if not replaced:
        errors.append(f"{name}: no title line found")
        continue
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.writelines(lines)
    print(f"OK  {name}: {len(new_title)} chars")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"\nDone: {len(mapping)} files")
