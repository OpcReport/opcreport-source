# OPC Report — Hexo 源码（重建版）

opcreport.cn 的 Hexo 源码。**注意：这是 2026-10 从线上产物反向工程重建的版本，不是原始源码**（原始源码随硬盘损坏丢失，旧备份仓未存上）。构建结果与线上 gh-pages 产物逐字节对比 99.9% 一致。

## 来源

- `site/source/_posts/`：从 gh-pages 产物 HTML 反提取的 803 篇文章 md（tools/extract_posts.py）
- `site/themes/opc/`：Hexo 8.1.2 主题，照产物 DOM 反写的 landscape 深度定制变体
- 静态资源（css/js/images/fancybox）：直接取自 gh-pages 产物与 main 分支 custom/
- `site/scripts/`：dates 页、tags 索引、404 重定向 MAP、旧日期路径 stub 等 Hexo 自定义脚本

## 构建

```bash
cd site
node_modules/hexo/bin/hexo generate   # 勿用 npx；Hexo 8.1.2
```

注意：
- **md 的 date 必须无时区格式 `YYYY-MM-DD HH:MM:SS`**——hexo-front-matter 对 `+08:00`/`Z` 时区偏移解析有 -16h 的 bug
- `hexo clean` 在部分环境会卡死，手动删 `site/public` + `site/db.json` 即可
- 构建/部署需沙箱外运行（文件写入量大）

## 部署

```bash
bash tools/deploy.sh
```

- robocopy 镜像同步 `site/public/` → `site/.deploy_git/` → 增量提交推送 `OpcReport/OpcReport.github.io` 的 gh-pages 分支
- 凭证：根目录 `.github-token`（**已被 .gitignore 排除，绝不入库**）
- 定时生成由 WorkBuddy automation 驱动（每 4 小时一次，日 4 篇封顶）

## 结构

```
site/               Hexo 工程（_config.yml / themes/opc / scripts / source）
tools/              extract_posts.py（反提取）、deploy.sh（部署）、gen_date_templates.py
.workbuddy/memory/  工作记忆（项目备忘与关键坑）
```
