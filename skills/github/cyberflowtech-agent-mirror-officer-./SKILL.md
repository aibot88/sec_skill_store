name: git-commit-bot description: 规范化 Git 提交助手。自动分析 diff、提交前同步 README 防过期，并生成精简的 Conventional Commits 中文 commit message；同时检查分支命名、敏感文件和 lint 错误。Use when the user asks to commit, create commits, push changes, or review staged changes before committing.

Git Commit Bot
用户要求提交代码时，严格按以下流程执行。

第一步：环境检查
并行执行以下命令收集信息：

git status
git diff --cached --stat    # 暂存区概览
git diff --stat             # 工作区概览
git branch --show-current
git log --oneline -5        # 近期 commit 风格参考
第二步：安全门禁
2.1 分支命名检查
合法格式：{Owner}_{Version} 或 feature/xxx、fix/xxx、hotfix/xxx、release/xxx

如果当前在 main / master 上，警告用户并建议切换分支
分支名不符合规范时提示，但不阻断
2.2 敏感文件检查
扫描 git status 输出，若发现以下文件被改动或新增，警告并排除：

.env、.env.*
*credentials*、*secret*、*token*
*.p12、*.pem、*.key、*.keystore
GoogleService-Info.plist（含推送/Firebase 密钥）
2.3 Lint 检查
对已修改的源码文件调用 ReadLints 检查。若发现新引入的 lint 错误：

能快速修复的 → 自动修复
不能快速修复的 → 列出错误，询问用户是否继续
第三步：Diff 分析与拆分建议
3.1 分析变更范围
统计改动文件数和改动行数。当满足以下任一条件时，建议拆分提交：

条件	阈值
改动文件数	> 10 个
改动行数	> 500 行
跨多个不相关模块	> 2 个独立功能模块
3.2 拆分策略
按以下优先级拆分：

按功能模块：不同业务模块分开提交
按变更类型：feat / fix / refactor / chore 分开
按文件类型：源码 vs 配置 vs 文档 分开
提出拆分建议后，让用户确认再执行。

第四步：提交前更新 README
在执行 git add / git commit 前，先检查并同步 README，避免文档过期。

4.1 检查 README 是否需要更新
优先检查这些文件（按存在情况）：

README.md
README.zh-CN.md / README_CN.md
其他项目约定的主文档入口
如果本次改动涉及以下任一内容，必须更新 README：

安装/构建/运行方式变化
配置项、环境变量、依赖变化
功能行为、接口、使用示例变化
目录结构或开发流程变化
4.2 更新原则
仅更新与本次改动直接相关的段落，避免无关重写
优先保证“可执行性”：命令、路径、示例可直接使用
若确认无需更新 README，在回复中明确说明原因后再提交
第五步：生成 Commit Message（精简）
格式规范（Conventional Commits + 中文，默认单行）
<type>(<scope>): <简述>
仅在必要时追加：

<type>(<scope>): <简述>

<1-3 行原因/影响>
Type 对照表
Type	场景
feat	新功能
fix	Bug 修复
refactor	重构（不改变外部行为）
chore	构建、依赖、配置等杂项
docs	文档变更
style	代码格式（不影响逻辑）
perf	性能优化
test	测试相关
ci	CI/CD 配置
Scope 规则
从改动文件路径推断 scope：

路径含	Scope
IM/、EaseIMKit/、Chat/	IM
Wallet/、ZapryWallet/	wallet
Manager/	core
Podfile、xcodeproj	build
doc/	docs
Util/	util
多个 scope 时取最主要的一个，或省略 scope。

简述撰写规则
中文
不超过 30 字，尽量 20 字内
动词开头：添加 / 修复 / 重构 / 优化 / 移除 / 更新
只写一个核心改动，避免堆砌细节
说清「改了什么」，效果放到 body（如需）
Body 规则
默认不写 body。仅当改动较大或需要解释原因时添加：

解释「为什么」而非「做了什么」
最多 1-3 行，列出关键影响点
每行不超过 72 字
示例
feat(IM): 添加消息已读回执
fix(wallet): 修复转账网络切换后余额未刷新
refactor: 拆分 EaseChatViewController 输入栏交互到独立 Category
chore(build): 更新 Podfile Xcode26 链接器配置
第六步：执行提交
git add 相关文件（不要盲目 git add .，按分析结果精确添加）
使用 HEREDOC 格式提交：
# 默认：精简单行提交
git commit -m "$(cat <<'EOF'
type(scope): 简述
EOF
)"

# 仅在必要时补充 body
git commit -m "$(cat <<'EOF'
type(scope): 简述

body（如有）
EOF
)"
提交后执行 git status 确认成功
第七步：后续建议
提交成功后，根据情况提示：

还有未提交的改动 → 提醒并建议下一次提交内容
分支领先 remote → 提示可以 push（不自动 push）
如果用户要求创建 PR → 按标准 PR 流程执行