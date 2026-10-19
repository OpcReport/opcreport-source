# -*- coding: utf-8 -*-
"""Batch 3: apply new titles from title_batch_3.json. Only the first `title: ` line of each md file is replaced."""
import json
import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

POSTS = r"F:\电脑文件\opcreport-blog\site\source\_posts"
JSON_PATH = r"F:\电脑文件\opcreport-blog\tools\title_batch_3.json"

with open(JSON_PATH, encoding="utf-8") as f:
    mapping = json.load(f)

errors = []

# Validate titles
for fname, title in mapping.items():
    if len(title) > 65:
        errors.append(f"{fname}: title too long ({len(title)} chars): {title}")
    if '"' in title:
        errors.append(f"{fname}: title contains double quote: {title}")

# Validate files exist and count matches
md_files = {fn for fn in os.listdir(POSTS)
            if re.match(r"^opc-report-2026-(07-2[5-9]|07-3[01]|08-0[0-7])", fn)}
missing = set(mapping) - md_files
uncovered = md_files - set(mapping)
if missing:
    errors.append(f"JSON keys not found on disk: {sorted(missing)}")
if uncovered:
    errors.append(f"Files on disk not in JSON: {sorted(uncovered)}")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print("  " + e)
    sys.exit(1)

print(f"Validation OK: {len(mapping)} files, all titles <= 65 chars, full coverage.")

# Apply
pattern = re.compile(r"(?m)^title: .*$")
changed, unchanged = 0, 0
for fname, title in sorted(mapping.items()):
    path = os.path.join(POSTS, fname)
    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    new_line = 'title: "' + title + '"'
    new_content, n = pattern.subn(lambda m: new_line, content, count=1)
    if n != 1:
        print(f"ERROR: no title line found in {fname}")
        sys.exit(1)
    if new_content == content:
        unchanged += 1
    else:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        changed += 1

print(f"Applied: {changed} files updated, {unchanged} already identical (kept).")
