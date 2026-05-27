---
name: jshook-reverse
description: "AI-powered JavaScript reverse engineering tool. 资深JavaScript逆向工程专家助手。Actions: collect, search, deobfuscate, understand, summarize, detect-crypto, browser, debugger, breakpoint, debug-step, debug-eval, debug-vars, script, hook, stealth, dom, page. Capabilities: 混淆代码分析、VM破解、Webpack解包、AST转换、Puppeteer/CDP自动化、反检测、指纹伪造、加密识别、参数提取、算法还原、Canvas/WebGL指纹、WebDriver隐藏、CDP调试、断点分析、动态追踪、Hook注入、DOM检查、页面控制。"
---

# JavaScript逆向工程专家

资深JavaScript逆向工程专家，精通浏览器自动化、代码分析和反混淆。

## 核心能力

- **逆向工程**：混淆代码分析、VM破解、Webpack解包、AST转换
- **浏览器自动化**：Puppeteer/CDP、反检测、指纹伪造
- **加密识别**：AES/RSA/MD5/SHA识别、参数提取、算法还原
- **反爬虫绕过**：Canvas/WebGL指纹、WebDriver隐藏、行为模拟
- **调试分析**：CDP调试、断点分析、动态追踪、Hook注入
- **Hook注入**：函数拦截、网络监控、属性劫持、事件追踪、反调试绕过
- **反检测伪装**：Stealth脚本注入、指纹伪造、平台预设、WebDriver隐藏
- **DOM检查**：元素查询、结构分析、可点击元素定位
- **页面控制**：导航、点击、输入、截图、性能监控

## 工作原理

所有命令通过执行 `node dist/skill.js <command> [args]` 来调用工具。

## 功能特性

- 智能代码收集 - 支持摘要/优先级/增量模式，防止Token溢出
- AI驱动反混淆 - 支持20+种混淆类型，自动还原代码
- 代码语义理解 - AI辅助分析业务逻辑和加密算法
- AI代码摘要 - 单文件/批量/项目级摘要，自动检测加密/API/混淆特征
- 加密算法检测 - 自动识别AES/RSA/MD5/SHA和自定义算法
- 浏览器自动化 - 自动检测和启动Chrome/Edge，支持任意盘符
- 反检测伪装 - 16项反检测功能，5种平台预设，Canvas/WebGL/AudioContext指纹伪造
- CDP调试器 - 完整的断点管理、执行控制、变量查看
- 脚本管理 - 脚本列表、源码获取、模式查找、内容搜索
- 运行时分析 - 表达式求值、作用域变量、动态追踪
- 统计和缓存 - 完善的缓存机制和统计信息
- 高性能 - 智能压缩、增量收集、按需加载

## 工具详情

### 代码收集

| 工具 | 说明 | 功能 |
|------|------|------|
| collect_code | 智能代码收集 | 自动收集页面内联脚本、外部脚本、动态加载脚本、智能摘要模式（防止Token溢出）、优先级模式（关键词优先）、增量模式（按需获取） |
| search_in_scripts | 搜索关键词 | 正则表达式搜索、上下文行数控制、最大匹配数限制、高亮显示匹配结果 |

### 代码分析

| 工具 | 说明 | 功能 |
|------|------|------|
| deobfuscate | AI驱动的代码反混淆 | 支持20+种混淆类型、变量名还原、控制流平坦化还原、字符串解密、死代码消除 |
| understand | AI辅助的代码语义理解 | 业务逻辑分析、加密算法识别、API调用分析、数据流追踪 |
| summarize | AI生成代码摘要 | 单文件AI摘要生成、批量文件并发摘要、项目级摘要分析、加密/API/混淆特征检测、安全风险评估、复杂度评估和建议 |
| detect_crypto | 检测和分析加密算法 | 标准算法识别（AES/RSA/MD5/SHA）、自定义算法检测、参数提取、密钥定位 |

### 浏览器控制

| 工具 | 说明 | 功能 |
|------|------|------|
| browser_launch | 启动浏览器 | 自动检测Chrome/Edge、支持任意盘符（C-Z）、多浏览器选择、CDP远程调试连接、反检测脚本注入 |
| browser_status | 获取浏览器状态 | 连接状态、当前页面信息、CDP会话状态 |
| browser_close | 关闭浏览器 | 优雅断开连接、清理CDP会话、进程管理 |

### 调试分析

| 工具 | 说明 | 功能 |
|------|------|------|
| debugger_control | 调试器控制和状态管理 | 启用/禁用调试器、获取调试器状态、初始化高级功能、Watch表达式管理、XHR断点管理、事件断点管理 |
| breakpoint_manager | 断点管理 | 按URL设置断点、按脚本ID设置断点、条件断点支持、断点列表查看、断点删除和清除 |
| execution_control | 执行控制 | 暂停执行、继续执行、单步进入（Step Into）、单步跳过（Step Over）、单步跳出（Step Out） |
| runtime_evaluator | 运行时表达式求值 | 在当前上下文求值表达式、访问全局变量、访问局部变量、执行任意JavaScript代码 |
| variable_inspector | 变量查看和作用域分析 | 查看当前作用域变量、查看调用帧变量、对象属性展开、变量类型识别 |
| script_manager | 脚本管理和源码获取 | 列出所有已加载脚本、获取脚本源码、按URL模式查找脚本、脚本内容搜索、支持内联和外部脚本 |

### 反检测伪装

| 工具 | 说明 | 功能 |
|------|------|------|
| stealth_inject | 注入反检测脚本 | 5种平台预设、Chrome 131+ UA字符串、隐藏navigator.webdriver、模拟window.chrome对象、Canvas/WebGL/AudioContext指纹噪声、navigator属性一致性、Permissions/Battery/MediaDevices/Notifications/NetworkInformation API模拟、document.hasFocus()覆盖、16项独立可控功能 |
| stealth_presets | 平台预设管理 | windows-chrome (Win10+Chrome131)、mac-chrome (macOS+Chrome131)、mac-safari (macOS+Safari18.2)、linux-chrome (Linux+Chrome131)、windows-edge (Win10+Edge131) |

### 数据管理

| 工具 | 说明 | 功能 |
|------|------|------|
| stats | 获取统计信息 | 缓存统计（文件数、大小、命中率）、压缩统计（压缩率、节省空间）、收集统计（URL数、文件数） |
| clear | 清除所有数据 | 清除文件缓存、清除压缩缓存、重置收集状态 |

## 命令参考

### 代码收集与搜索

```bash
# 收集代码
collect <url>
collect <url> --smart-mode=summary
collect <url> --smart-mode=priority --priorities=encrypt,sign
collect <url> --compress --max-total-size=5000000

# 搜索脚本
search <keyword>
search "X-Bogus" --context=10
search "function.*encrypt" --regex --max-matches=50
```

### 代码分析

```bash
# AI反混淆
deobfuscate <code>

# 代码理解
understand <code>
understand <code> --focus=security

# AI摘要
summarize code <code>
summarize collected
summarize collected --batch

# 加密检测
detect-crypto <code>
```

### 浏览器控制

```bash
browser launch          # 自动检测并启动
browser status          # 查看状态
browser close           # 关闭浏览器
```

### 调试器

```bash
# 调试器控制
debugger enable
debugger disable
debugger status
debugger init-advanced  # 初始化Watch/XHR/Event/Blackbox

# 断点管理
breakpoint set-url https://example.com/app.js 100
breakpoint set-url https://example.com/app.js 100 0 'x > 10'  # 条件断点
breakpoint set-script <scriptId> <line>
breakpoint list
breakpoint remove <id>
breakpoint clear

# 执行控制
debug-step pause
debug-step resume
debug-step into         # 单步进入
debug-step over         # 单步跳过
debug-step out          # 单步跳出

# 表达式求值
debug-eval window.location.href
debug-eval document.cookie
debug-eval JSON.stringify(userData)

# 变量查看
debug-vars
debug-vars <callFrameId>
```

### 脚本管理

```bash
script list             # 列出所有已加载脚本
script get <scriptId>   # 获取脚本源码
script find *app.js     # 按URL模式查找
script search encrypt   # 搜索脚本内容
```

### Hook注入

```bash
# 快速生成
hook generate function encryptData
hook generate fetch */api/*
hook generate xhr *sign*
hook generate property window.navigator
hook generate cookie
hook generate websocket
hook generate eval
hook generate timer

# 管理
hook list
hook remove <id>
hook enable <id>
hook disable <id>
hook clear
hook anti-debug         # 反调试绕过
hook export json
hook-data               # 查看捕获数据
hook-data <hookId>
hook-types              # 列出Hook类型
```

### 监视表达式

```bash
watch add "window.location.href" "当前URL"
watch add "userData.token"
watch list
watch evaluate          # 求值所有监视表达式
watch remove <id>
watch export
watch import <json>
watch clear
```

### XHR断点

```bash
xhr-breakpoint set */api/*
xhr-breakpoint set *sign*
xhr-breakpoint list
xhr-breakpoint remove <id>
xhr-breakpoint clear
```

### 事件断点

```bash
event-breakpoint set click
event-breakpoint set-mouse       # 所有鼠标事件
event-breakpoint set-keyboard    # 所有键盘事件
event-breakpoint set-timer       # 定时器事件
event-breakpoint set-websocket   # WebSocket事件
event-breakpoint list
event-breakpoint remove <id>
event-breakpoint clear
```

### 脚本黑盒化

```bash
blackbox set *jquery*.js
blackbox set *node_modules/*
blackbox set-common     # 黑盒化常用库
blackbox list
blackbox remove <pattern>
blackbox clear
```

### 反检测伪装

```bash
stealth inject                          # 默认注入
stealth inject-preset windows-chrome    # 平台预设
stealth inject-preset mac-safari
stealth inject-preset mac-chrome
stealth inject-preset linux-chrome
stealth inject-preset windows-edge
stealth set-ua windows                  # 设置User-Agent
stealth presets                         # 列出预设
stealth status                          # 注入状态
stealth features                        # 列出所有功能
```

反检测功能（16项）：

| 功能 | 说明 |
|------|------|
| hideWebdriver | 隐藏 `navigator.webdriver` 属性 |
| mockChrome | 模拟 `window.chrome` 对象 |
| canvasNoise | Canvas 会话级随机种子指纹噪声 |
| webglVendor | 覆盖 WebGL 厂商和渲染器 |
| audioNoise | AudioContext 指纹噪声 |
| navigatorProps | 一致的平台/厂商/核心数/内存 |
| permissionsAPI | 修复 Permissions API 检测 |
| batteryAPI | 模拟 Battery API |
| mediaDevices | 模拟媒体设备 |
| notifications | 模拟 Notifications API |
| networkInfo | 模拟网络信息 API |
| hasFocus | 覆盖 `document.hasFocus()` |

### DOM检查器

```bash
dom query #login-button
dom query-all .product-item 20
dom structure 3 true            # 深度3，包含文本
dom clickable 登录               # 按文本查找可点击元素
dom style #header
dom wait .loading-spinner 5000  # 等待元素出现
```

### 页面控制器

```bash
page navigate https://example.com
page reload
page back
page forward
page click #submit-button
page type #username admin
page select #country US
page hover .menu-item
page scroll 0 500
page wait-selector .result
page wait-nav
page eval document.title
page url
page title
page content
page screenshot output.png
page metrics
```

### 工具命令

```bash
stats                   # 收集和缓存统计
stats --type=cache
clear                   # 清除所有数据
```

## 逆向工程工作流

### 核心理念

逆向的本质：理解需求 → 定位目标 → 分析实现 → 复现逻辑

核心技巧：从结果反推过程
- 看到加密参数 → 反推生成函数
- 看到混淆代码 → 反推原始逻辑
- 看到网络请求 → 反推调用链路

### 标准流程

```
1. 启动浏览器并收集
   browser launch
   collect https://target.com

2. 快速侦查
   search "encrypt"
   search "sign"
   search "token"
   detect-crypto <suspicious_code>

3. 定位目标函数
   script list
   script find *app*.js
   script search "X-Bogus"

4. 动态分析
   debugger enable
   breakpoint set-url https://target.com/app.js 1234
   xhr-breakpoint set */api/sign*
   debug-step pause → into → over
   debug-vars
   debug-eval <expression>

5. Hook监控
   hook generate function encryptData
   hook generate fetch */api/*
   hook-data

6. 反混淆与理解
   deobfuscate <obfuscated_code>
   understand <clean_code> --focus=security

7. 复现逻辑
   根据分析结果，复现加密/签名逻辑
```

## 最佳实践

1. 使用智能摘要模式避免数据过大
2. 优先收集关键代码（encrypt、crypto、sign）
3. 使用增量模式按需获取
4. 从结果反推过程，避免盲目调试
5. 使用断点和变量查看进行动态分析
6. 使用dom命令定位页面元素，避免盲目点击
7. 使用page命令进行页面交互和自动化操作

## 环境要求

- **Node.js** >= 18.0.0
- **浏览器**：Chrome 或 Edge（自动检测）
- **依赖**：puppeteer、openai 或 anthropic（AI功能）

## 配置

环境变量配置在 `.env` 文件中：

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | OpenAI API密钥（可选） |
| `ANTHROPIC_API_KEY` | Anthropic API密钥（可选） |
| `DEFAULT_LLM_PROVIDER` | 默认LLM提供商（openai/anthropic） |
| `REMOTE_DEBUGGING_PORT` | 远程调试端口（默认9222） |

## 故障排除

### 浏览器启动失败
- 检查Chrome/Edge是否已安装
- 检查端口9222是否被占用
- 尝试使用外部浏览器模式

### AI分析失败
- 检查API密钥是否配置正确
- 检查网络连接
- 检查API配额是否充足

### DOM查询失败
- 确保浏览器已启动
- 确保页面已加载完成
- 检查选择器是否正确
