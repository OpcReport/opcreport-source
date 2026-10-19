# -*- coding: utf-8 -*-
"""Apply new titles from title_batch_1.json to matching md files (batch 1)."""
import json
import os
import statistics
import sys

POSTS = r"F:\电脑文件\opcreport-blog\site\source\_posts"
JSON_PATH = r"F:\电脑文件\opcreport-blog\tools\title_batch_1.json"
BACKUP_PATH = r"F:\电脑文件\opcreport-blog\tools\title_backup_batch1.txt"
LIST_PATH = r"C:\Users\77569\AppData\Local\Temp\target_files.txt"

with open(JSON_PATH, encoding="utf-8") as f:
    mapping = json.load(f)

with open(LIST_PATH, encoding="utf-8") as f:
    target_files = [ln.strip() for ln in f if ln.strip()]

# --- Validation ---
assert len(target_files) == 190, f"target file count {len(target_files)} != 190"
missing = [f for f in target_files if f not in mapping]
extra = [k for k in mapping if k not in set(target_files)]
if missing or extra:
    print("MISSING:", missing[:5])
    print("EXTRA:", extra[:5])
    sys.exit(1)

for name, title in mapping.items():
    if len(title) > 65:
        print(f"TOO LONG ({len(title)}): {name}: {title}")
        sys.exit(1)
    if '"' in title:
        print(f"HAS QUOTE: {name}")
        sys.exit(1)

# --- Backup original title lines + stats ---
backup_lines = []
old_lengths = []
new_lengths = []
changed = 0

for name in target_files:
    path = os.path.join(POSTS, name)
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.readlines()

    idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("title: "):
            idx = i
            break
    if idx is None:
        print(f"NO TITLE LINE: {name}")
        sys.exit(1)

    old_line = lines[idx]
    stripped = old_line.strip()
    # old title text between quotes
    old_title = stripped[len('title: "'):-1] if stripped.endswith('"') else stripped[7:]
    old_lengths.append(len(old_title))
    backup_lines.append(f"{name}\t{old_line.rstrip(chr(10)).rstrip(chr(13))}\n")

    new_title = mapping[name]
    new_lengths.append(len(new_title))
    new_line = f'title: "{new_title}"' + ("\r\n" if old_line.endswith("\r\n") else "\n")

    if lines[idx] != new_line:
        lines[idx] = new_line
        changed += 1

    before = len(lines)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.writelines(lines)

with open(BACKUP_PATH, "w", encoding="utf-8", newline="") as f:
    f.writelines(backup_lines)

print(f"files processed: {len(target_files)}")
print(f"files changed: {changed}")
print(f"median title length before: {statistics.median(old_lengths)}")
print(f"median title length after: {statistics.median(new_lengths)}")
print(f"max new length: {max(new_lengths)}")
print(f"over 65: {sum(1 for x in new_lengths if x > 65)}")
