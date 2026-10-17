#!/bin/bash
# deploy.sh — OPC Report 增量部署：将 site/public/ 推送到 OpcReport/OpcReport.github.io 的 gh-pages 分支
# 用法: bash deploy.sh   （需已先 hexo generate）
# 凭证: ../.github-token（OpcReport 账号 PAT，Contents 读写）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"     # opcreport-blog 根目录
PUBLIC="$ROOT/site/public"
DEPLOY="$ROOT/site/.deploy_git"
TOKEN="$(tr -d '\r\n' < "$ROOT/.github-token")"
REPO_URL="https://x-access-token:${TOKEN}@github.com/OpcReport/OpcReport.github.io.git"

[ -d "$PUBLIC" ] || { echo "ERROR: $PUBLIC 不存在，请先 hexo generate"; exit 1; }

# 首次：浅克隆 gh-pages 作为部署工作区
if [ ! -d "$DEPLOY/.git" ]; then
  echo ">> 初始化部署工作区（浅克隆 gh-pages）..."
  for i in 1 2 3; do
    git clone --depth 1 --branch gh-pages --single-branch "$REPO_URL" "$DEPLOY" && break
    rm -rf "$DEPLOY"
    [ "$i" = 3 ] && { echo "ERROR: 克隆 3 次均失败（网络）"; exit 1; }
    echo ">> 克隆失败，10 秒后重试 ($i/3)..."
    sleep 10
  done
fi

cd "$DEPLOY"
git config user.name  "OpcReport"
git config user.email "bot@opcreport.cn"

# 同步产物（robocopy /MIR 镜像；cygpath 转换 Windows 路径；保留 .nojekyll 后面重建）
# robocopy 退出码 0-7 均视为成功
RC=0
MSYS2_ARG_CONV_EXCL="*" robocopy "$(cygpath -w "$PUBLIC")" "$(cygpath -w "$DEPLOY")" /MIR /NFL /NDL /NJH /NJS /NP /XD .git > /dev/null || RC=$?
[ $RC -le 7 ] || { echo "ERROR: robocopy 同步失败 (exit $RC)"; exit 1; }
# GitHub Pages Jekyll 开关：Hexo 产物需要保留 .nojekyll
touch "$DEPLOY/.nojekyll" 2>/dev/null || true

# 变更才提交推送
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "Deploy: $(date -u '+%Y-%m-%d %H:%M UTC') auto content update"
  git push origin gh-pages 2>&1 | sed "s/${TOKEN}/[REDACTED]/g"
  echo ">> 部署完成: $(git log -1 --format='%h %ad %s' --date=format:'%Y-%m-%d %H:%M')"
else
  echo ">> 无变更，跳过推送"
fi
