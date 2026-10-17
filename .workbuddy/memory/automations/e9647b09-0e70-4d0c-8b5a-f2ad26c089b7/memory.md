# Automation e9647b09 执行记录

## 2026-10-16 23:09 运行
- 频控检查：当天(2026-10-16)文件数 0，允许生成。date 字段无跳变。
- 生成 1 篇：opc-report-2026-10-16-2310.md，标题 "Open Weights Hit the Desktop: Frontier AI Goes Self-Hosted as $1.5B a Day Funds the Agent Plumbing"（~1500词，含两个表格）。
- 素材：Meta Muse Spark Open 816B 开源权重（2台 Mac Studio 可跑）、10-15 单日 $1.51B 融资（Modal $750M@$15.75B/ARR $1B、Labelbox $100M+、Scuba $34M、Uvi $7.5M）、EU SMB agent WAU 8.1x、Codex CLI 自更新守护进程争议、HTTP 头 prompt injection（30 站点/2.17亿响应）、Third Moment 1万 agent 实测、CoreWeave 债务担忧、IrisGo/DEV·TV 独立开发者分发经验、Character.AI 破产、Cursor 取消独立 $20 Pro。
- 构建：hexo generate 成功（2266 files，3.77min，无 ERROR），public/opc-report-2026-10-16-2310/index.html 已生成。
- 部署：跳过。OpcReport GitHub token 仍未配置；git ls-remote 直连亦失败（代理 502）。**待部署：文章已构建完成。**

## 2026-10-17 09:44 运行
- 频控检查：当天(2026-10-17)文件数 0，允许生成。
- 生成 1 篇：opc-report-2026-10-17-0944.md，标题 "The Zero-Employee Proof Points: A Solo Founder Hits $4B, an Agent CEO Runs 1,000 Companies, and AI Now Works 6x Longer Than Its Humans"（~1500词，3 表格）。角度与 10-16 篇（Modal/开源权重/安全周）无重叠。
- 素材：micro1 $4B 估值 solo founder（Forbes 10-16）、Polsia 零员工 $7M run-rate、ReddGrow $1M ARR bootstrapped、Anthropic 10-16 报告（agent 工时 6x、初级技术招聘 27%→9%、commits 5x、meta-work 22%）、Opsin $21M seed（agent 治理）、OpenAI 模型红队测试黑掉钱包、TypeSafe AI $870M（非文本模型 Jev）、Perplexity 开源 SPACE 沙箱（Apache 2.0）、OpenCode 免费 GLM 5.3 Flash + Reflection Beam（1M ctx）、Gemini 4 Argon 4 agent 27h 通关 Minecraft、Replit 弃 Anthropic 转 OpenAI、Apate.AI $8.15M 反诈、Vectorwire 30 天 $144.9B。
- 构建：hexo generate 成功（2269 files，35s，无 ERROR），public HTML 已验证。
- 部署：成功，commit b09b7e27 推送 gh-pages（deploy.sh 正常，.github-token 生效）。10-16 待部署的那篇也随本次全量同步上线。

## 2026-10-17 18:11 运行
- 频控检查：当天(2026-10-17)文件数 2（<4），允许生成。
- 生成 1 篇：opc-report-2026-10-17-1811.md，标题 "Containment Week: Anthropic Unplugs Its Agents, Beijing Draws Export Lines, and Two Engineers Triple Stack Overflow's Agent Signups"（~1500词，2 表格）。主题"管控周"，与前两篇（0944 零员工实证 / 1353 开源反击）无重叠。
- 素材：Anthropic 切断内部 agent 评测联网（141,006 次评测/3 起真实入侵、PyPI 恶意包 1 小时 15 台主机、harness 配置失败非对齐失败）、CERT-In 印度多厂商 agent 凭据泄露入侵（零漏洞利用）、商务部/科技部 48 号公告出口管制（40 项技术/23 项 AI/开源豁免自动许可）、Stack Overflow for Agents（2 工程师+Codex、注册量一夜 3x/agent 创建 10x、连接器 3-6 周→<4 天）、Anthropic OSS Scanner（29,000 候选漏洞/88% 精度）、Ramp $1.85B@$60B、Genesis AI ~$500M@3B pre（Bloomberg 未确认）、Stand/North.cloud/Mueon/RapidCanvas/Confido、Nvidia 9 笔欧洲投资+$250M 英国算力、印度家族办公室 $760M(+50%)、唐山 OPC 社区（100 单/日、8 分钟上架）、context-mode/CLI-Anything 工具链。
- 构建：hexo generate 成功（2292 files，28s，无 ERROR），public HTML 已验证（74KB）。
- 部署：**成功**，commit ac608c4b 推送 gh-pages；上次的积压 commit 7435f508（13:53 篇）随本次全量同步一并上线。源码仓同步 3cad63b 推送 main 成功。

## 2026-10-17 13:53 运行
- 频控检查：当天(2026-10-17)文件数 1（<4），允许生成。
- 生成 1 篇：opc-report-2026-10-17-1353.md，标题 "The Open-Source Agent Counterattack: Alibaba Rewires Computer-Use, a $1B Concierge Bet, and the $125M Answer to Rogue Agents"（~1500词，2 表格）。与 0944 篇（micro1/Polsia/Anthropic 报告）无重叠。
- 素材：阿里 Tongyi-MAI 开源 OpenGCUA/MAI-Gym（OSWorld-v2 +19.6、8 模型、20k 并行 RL、19.4x token 效率差）、Instinct $1B@$10B（Sequoia/Benchmark/Coatue，现实世界 concierge agent）、Nous Research $90M B 轮@$1.5B（Nvidia/Samsung/YC）、Zenity $125M C 轮（agent 安全，总收入 $185M）、Workday 收购 C1.ai、ServiceNow AI Passport、Xbow $40K 算力挖出 Chrome 3 零日链、OpenAI 官方 skill 仓幻觉域名供应链风险、Elorian Glimpse、bigarrow、Cal AI $30M 分发案例、TrustMRR 独立开发者基率（中位 $145 MRR 等）、8 州诉 OpenAI、Anthropic 控制台 100x 扣款 bug。
- 构建：hexo generate 成功（2289 files，1.2min，无 ERROR），public HTML 已验证。
- 部署：**失败**。deploy.sh 两次 + 直接 push 一次，共 3 次推送均遇 github.com 连接重置/超时（本地网络问题）。commit 7435f508 已本地提交在 .deploy_git（gh-pages ahead 1），下次部署随全量同步自动上线。源码仓同步同样推送失败（main 77fae51 本地已提交）。
