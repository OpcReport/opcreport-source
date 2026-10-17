# -*- coding: utf-8 -*-
"""从产物 HTML 生成 dates.ejs 和 tags-index.ejs 模板（动态区块 EJS 化）"""
import re

REPO = "repo"
OUT = "site/themes/opc/layout"

# ---------- dates ----------
html = open(f"{REPO}/dates/index.html", encoding="utf-8").read()
i = html.find('<div class="container dates-page">')
j = html.find('</section>', html.find('dates-posts-data'))
body = html[i:j].rstrip() + "\n"

# 1. datalist options -> EJS 循环
body = re.sub(
    r'<datalist id="available-dates">.*?</datalist>',
    '''<datalist id="available-dates">
        <% days.forEach(function(d){ %>
          <option value="<%= d.date %>"><%= d.count %> report<%= d.count === 1 ? '' : 's' %></option>
        <% }); %>
      </datalist>''',
    body, flags=re.S)

# 2. date pills -> EJS 循环
body = re.sub(
    r'<summary>All available dates \(\d+ days\)</summary>\s*<div class="dates-all-grid">.*?</div>\s*</details>',
    '''<summary>All available dates (<%= days.length %> days)</summary>
    <div class="dates-all-grid">
      <% days.forEach(function(d){ %>
        <button type="button" class="dates-date-pill" data-date="<%= d.date %>"><%= d.date %> <span class="dates-pill-count">(<%= d.count %>)</span></button>
      <% }); %>
    </div>
  </details>''',
    body, flags=re.S)

# 3. posts-data JSON -> EJS
body = re.sub(
    r'<script id="dates-posts-data" type="application/json">.*?</script>',
    '''<script id="dates-posts-data" type="application/json">
<%- posts_json %>
</script>''',
    body, flags=re.S)

tpl = '''<%
/* dates (Browse by Date) page — rendered by custom generator */
var days = local_data.days;
var posts_json = local_data.posts_json;
%>
''' + body

open(f"{OUT}/dates.ejs", "w", encoding="utf-8", newline="\n").write(tpl)
print("dates.ejs written, len:", len(tpl))

# ---------- tags index ----------
html = open(f"{REPO}/tags/index.html", encoding="utf-8").read()
i = html.find('<div class="container">')
j = html.find('</section>', i)
body = html[i:j].rstrip() + "\n"

body = re.sub(
    r'<p class="tag-page-intro">.*?</p>',
    '<p class="tag-page-intro"><%= tag_count %> tags across <%= post_count %> articles. Browse by topic.</p>',
    body, flags=re.S)

body = re.sub(
    r'<div class="tag-page-cloud">.*?</div>',
    '''<div class="tag-page-cloud">
      <% tags.forEach(function(t){ %>
        <a href="/tags/<%= t.slug %>/"><%= t.name %> <span class="tag-count">(<%= t.count %>)</span></a>
      <% }); %>
    </div>''',
    body, flags=re.S)

tpl = '''<%
/* All Tags page — rendered by custom generator */
var tags = local_data.tags;
var tag_count = local_data.tag_count;
var post_count = local_data.post_count;
%>
''' + body

open(f"{OUT}/tags-index.ejs", "w", encoding="utf-8", newline="\n").write(tpl)
print("tags-index.ejs written, len:", len(tpl))
