import json, os, statistics, sys

POSTS = r"F:\电脑文件\opcreport-blog\site\source\_posts"
MAP = r"F:\电脑文件\opcreport-blog\tools\title_batch_6.json"

with open(MAP, encoding="utf-8") as f:
    mapping = json.load(f)

# 校验
for name, title in mapping.items():
    if len(title) > 65:
        sys.exit(f"FAIL: {name} new title is {len(title)} chars: {title}")
    path = os.path.join(POSTS, name)
    if not os.path.isfile(path):
        sys.exit(f"FAIL: missing file {name}")

old_lens, new_lens, examples = [], [], []
applied = 0
for name, title in mapping.items():
    path = os.path.join(POSTS, name)
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.readlines()
    idx = None
    for i, line in enumerate(lines):
        if line.startswith("title: "):
            idx = i
            break
    if idx is None:
        sys.exit(f"FAIL: no title line in {name}")
    old_title = lines[idx][len("title: "):].strip().strip('"')
    old_lens.append(len(old_title))
    new_lens.append(len(title))
    lines[idx] = 'title: "%s"\n' % title
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.writelines(lines)
    applied += 1
    examples.append((name, old_title, title))

print(f"applied: {applied}")
print(f"old median len: {statistics.median(old_lens)}")
print(f"new median len: {statistics.median(new_lens)}")
for name, o, n in examples[:3]:
    print(f"EXAMPLE {name}\n  OLD ({len(o)}): {o}\n  NEW ({len(n)}): {n}")
