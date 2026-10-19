# OPC Report 项目长期备忘

## 项目状态（2026-10-16 重建）

- 工作区 F:\电脑文件\opcreport-blog：repo/ = 线上 gh-pages 镜像；site/ = 重建的 Hexo 8.1.2 工程；source/_posts = 反提取的 796 篇文章 md
- 线上 opcreport.cn 真身：OpcReport/OpcReport.github.io 的 gh-pages 分支；域名+AdSense 验证文件不动
- 废弃勿用：GeekQin 账号下的旧 opcreport 仓库、GeekQin.github.io /opcreport/ 路径
- 构建命令（node 直调，勿 npx；需 dangerouslyDisableSandbox）：
  `cd site && node_modules/hexo/bin/hexo generate`（node: C:\Users\77569\.workbuddy\binaries\node\versions\22.22.2-6\node.exe）
- hexo clean 会卡死 → PowerShell 手动删 site/public + site/db.json

## 部署（2026-10-16 已闭环）
- 部署命令：`bash tools/deploy.sh`（沙箱外运行）。浅克隆 gh-pages → robocopy /MIR 同步 → 增量提交推送。
- PAT 在根目录 `.github-token`（OpcReport 账号），严禁提交/输出。
- Git Bash 无 rsync；robocopy 需 cygpath -w 转路径 + MSYS2_ARG_CONV_EXCL="*" 防开关被转义，退出码 0-7 算成功。
- 定时任务：每 4 小时一次（日 4 篇封顶），生成→构建→deploy.sh。
- 本地预览：Python http.server 4173 伺服 site/public/。

## 必守规范

- **md date 必须无时区格式 `YYYY-MM-DD HH:MM:SS`**（hexo-front-matter 对 ISO 偏移解析 -16h bug）
- 文章命名 opc-report-YYYY-MM-DD-HHMM.md（HHMM 北京时间）， permalink :title/ 平铺
- front matter：title / date / description（英文 ≤200 字符）/ categories / tags
- 内容结构（参照 8-9 月范文）：Key Insights / Market Trends / Build Directions / Risk Factors / Action Recommendations / Quick Data Reference，英文 ~1500 词，具名来源+具体数字
- 部署 = hexo generate → public/ 推 gh-pages → GitHub Pages 自动发布；域名/AdSense/验证文件一律不动
- GA4: G-92GE48C3Y0；不蒜子 BSZ_BASE {pv:5737, uv:5271}；捐赠卡 USDT TRC20 TSA1q55N3UZhztmFybchZXnNouqQSTcshp

## SEO 现状与策略（2026-10-16）

- GSC: 490 未索引（"已发现-尚未编入索引"）/ 315 已索引；原因 = 高频同质化（8月峰值日 25 篇）+ 9-28 断更 + 归档薄页稀释抓取预算
- 策略：≤4 篇/天（09/13/17/21 点自动化）、每篇有增量信息、重点文章 GSC 手动提交；断更恢复后索引会逐步回升

## 变现约束（2026-10-19 秦总明确）
- 付费专家（AI代码安全审查师）只在 WorkBuddy 生态内卖，收款走微信支付；微信付费版无独立主页。国际访客没有微信/支付宝，博客英文流量**无法**直接转化到 WorkBuddy 专家。
- 国际流量变现路线：AdSense（Google 自己收款）+ 联盟返佣（全球结算）+ 后期 Gumroad/LemonSqueezy 卖数字产品；国内流量才走 WorkBuddy 专家。
- 博客上挂自家产品推广卡不影响 AdSense（自有产品宣传≠广告位），但要标注清楚、别和广告位混排。

## 源码仓（2026-10-17 闭环）
- Hexo 源码在 OpcReport/opcreport-source（GitHub，main 分支，重建版非原始源码）。deploy.sh 每次部署后自动同步源码提交。
- 本地根目录即 git 仓；.gitignore 严排 .github-token，/source/ 锚定根目录防误伤 site/source/。
- README.md 记录了重建来源与构建注意事项。

## 待办

- 等 OpcReport 账号 GitHub token → 配置部署闭环（automation 部署环节）【已完成 2026-10-16】
