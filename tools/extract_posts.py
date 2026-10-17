# -*- coding: utf-8 -*-
"""
OPC Report - 从 gh-pages 产物反提取文章 markdown
输入: repo/opc-report-*/index.html (Hexo 生成的静态页)
输出: source/_posts/opc-report-YYYY-MM-DD-HHMM.md (Hexo 源码 front matter 规范)
front matter 规范见 main 分支 README: title/date/tags/categories/description
"""
import os
import re
import glob
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from markdownify import markdownify as md

REPO = os.path.join(os.path.dirname(__file__), "..", "repo")
OUT = os.path.join(os.path.dirname(__file__), "..", "source", "_posts")
OUT_PAGES = os.path.join(os.path.dirname(__file__), "..", "source")

os.makedirs(OUT, exist_ok=True)


def html_to_markdown(entry_html):
    """article-entry HTML -> markdown, 保留链接/加粗/表格/标题"""
    text = md(entry_html, heading_style="ATX", bullets="-")
    # markdownify 会留下大量空行, 压缩 3+ 空行为 2 空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 表格前后空行保证
    return text.strip()


def extract_post(path):
    html = open(path, encoding="utf-8").read()
    soup = BeautifulSoup(html, "lxml")

    og_title = soup.find("meta", property="og:title")
    title = og_title["content"].strip() if og_title else soup.title.get_text().strip()
    title = re.sub(r"\s*\|\s*OPC Report\s*$", "", title)

    pub = soup.find("meta", property="article:published_time")
    if pub:
        dt = datetime.fromisoformat(pub["content"].replace("Z", "+00:00"))
    else:
        # 回退: 从目录名取
        dirname = os.path.basename(os.path.dirname(path))
        m = re.match(r"opc-report-(\d{4}-\d{2}-\d{2})-(\d{4})", dirname)
        dt = datetime.strptime(m.group(1) + m.group(2), "%Y-%m-%d%H%M").replace(tzinfo=timezone(timedelta(hours=8)))
    # Hexo 源码原来用 +08:00, UTC 转 +08:00
    dt8 = dt.astimezone(timezone(timedelta(hours=8)))

    tags = [m["content"] for m in soup.find_all("meta", property="article:tag")]

    cat_div = soup.find("div", class_="article-category")
    categories = []
    if cat_div:
        # 面包屑结构: 链接之间有 ► 分隔符
        links = [a.get_text(strip=True) for a in cat_div.find_all("a")]
        categories = [l for l in links if l]

    og_desc = soup.find("meta", property="og:description")
    description = og_desc["content"].strip() if og_desc else ""

    entry = soup.find("div", class_="article-entry")
    if not entry:
        raise ValueError(f"no article-entry in {path}")
    body = html_to_markdown(str(entry))

    fm = [
        "---",
        f'title: "{title.replace(chr(34), chr(39))}"',
        # 注意: hexo-front-matter 对 ISO+时区偏移的解析有 bug(-16h),
        # 必须用无时区格式, 由构建机本地时区(Asia/Shanghai)解释
        f"date: {dt8.strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    if description:
        fm.append(f'description: "{description.replace(chr(34), chr(39))}"')
    if categories:
        fm.append("categories: " + "[" + ", ".join(categories) + "]")
    if tags:
        fm.append("tags: [" + ", ".join(tags) + "]")
    fm.append("---")

    return "\n".join(fm) + "\n\n" + body + "\n"


def main():
    files = sorted(glob.glob(os.path.join(REPO, "opc-report-*", "index.html")))
    ok, fail = 0, []
    for f in files:
        dirname = os.path.basename(os.path.dirname(f))
        if not re.match(r"opc-report-\d{4}-\d{2}-\d{2}(-\d{4})?$", dirname):
            continue
        try:
            content = extract_post(f)
            with open(os.path.join(OUT, dirname + ".md"), "w", encoding="utf-8", newline="\n") as w:
                w.write(content)
            ok += 1
        except Exception as e:
            fail.append((dirname, str(e)))
    print(f"posts extracted: {ok}/{len(files)}")
    for d, e in fail[:10]:
        print(f"FAIL {d}: {e}")

    # 静态页面 about/contact/privacy/start-here -> source/<page>/index.md
    for page in ["about", "contact", "privacy", "start-here"]:
        pf = os.path.join(REPO, page, "index.html")
        if not os.path.exists(pf):
            print(f"page missing: {page}")
            continue
        try:
            content = extract_post(pf)
            os.makedirs(os.path.join(OUT_PAGES, page), exist_ok=True)
            with open(os.path.join(OUT_PAGES, page, "index.md"), "w", encoding="utf-8", newline="\n") as w:
                w.write(content)
            print(f"page extracted: {page}")
        except Exception as e:
            print(f"page FAIL {page}: {e}")


if __name__ == "__main__":
    main()
