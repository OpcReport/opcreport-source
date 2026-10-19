import json, os, re, statistics, sys

POSTS = r"F:\电脑文件\opcreport-blog\site\source\_posts"
JSON_PATH = r"F:\电脑文件\opcreport-blog\tools\title_batch_2.json"
PAT = re.compile(r"opc-report-2026-07-(1[1-9]|2[0-4])")

with open(JSON_PATH, encoding="utf-8") as f:
    mapping = json.load(f)

# 1. 目标文件集合比对
actual = set(fn for fn in os.listdir(POSTS) if PAT.match(fn))
keys = set(mapping.keys())
missing = actual - keys
extra = keys - actual
if missing or extra:
    print("MISMATCH missing:", sorted(missing))
    print("MISMATCH extra:", sorted(extra))
    sys.exit(1)

# 2. 标题校验
for fn, t in mapping.items():
    if len(t) > 65:
        print(f"TOO LONG ({len(t)}): {fn}: {t}"); sys.exit(1)
    if '"' in t:
        print(f"HAS QUOTE: {fn}: {t}"); sys.exit(1)
    if "\n" in t or not t.strip():
        print(f"BAD TITLE: {fn}"); sys.exit(1)

# 3. 应用：只替换第一处 title: 行
applied = 0
old_lens, new_lens = [], []
changes = []
for fn, new_title in mapping.items():
    path = os.path.join(POSTS, fn)
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    lines = text.split("\n")
    idx = next((i for i, ln in enumerate(lines) if ln.startswith("title: ")), None)
    if idx is None:
        print(f"NO TITLE LINE: {fn}"); sys.exit(1)
    old_line = lines[idx]
    m = re.match(r'^title:\s*"(.*)"\s*$', old_line)
    old_title = m.group(1) if m else old_line[len("title: "):].strip().strip('"')
    if old_title == new_title:
        new_lens.append(len(new_title)); old_lens.append(len(old_title))
        applied += 1
        continue
    lines[idx] = f'title: "{new_title}"'
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))
    applied += 1
    old_lens.append(len(old_title)); new_lens.append(len(new_title))
    changes.append((fn, old_title, new_title))

print(f"applied: {applied} / {len(mapping)}")
print(f"median old: {statistics.median(old_lens)}, median new: {statistics.median(new_lens)}")
