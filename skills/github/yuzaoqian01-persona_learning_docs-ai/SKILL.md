| 技术栈         | 推荐 Skills 组合                                           |
| :------------- | :--------------------------------------------------------- |
| React 全栈开发 | React + Frontend Design + UI/UX Pro Max + Zustand Patterns |
| Vue 开发       | Vue + Component Api Design + Frontend Design               |
| 移动端开发     | React Native Skills + Radon AI                             |
| UI/UX 设计     | UI/UX Pro Max + UI Audit + Frontend Design Extractor       |
| 性能优化       | Frontend Performance + Browser Devtools Inspector          |





### 安全第一：必装安全工具

> ⚠️ **重要提醒**：在安装任何第三方 Skills 之前，务必先安装这两个安全工具！

**1. Skill Vetter（3.5K 下载）** — 技能安全审查工具

```
clawhub install skill-vetter

# 使用方法：在安装其他技能前先扫描
skill-vetter <skill-name></skill-name>
```

**2. Link Checker（2.1K 下载）** — URL 安全和钓鱼检测

```
clawhub install link-checker
```

### 🏆 前 5 个必装技能（零风险，超高下载量）

**1. Gog（33.8K 下载）** — Google 全家桶集成

一次性接入 Gmail、Calendar、Drive、Docs、Sheets、Contacts 等所有 Google 服务，是目前下载量最高的技能。

```
clawhub install gog
```

**2. self-improving-agent（32K 下载，338 星⭐）** — 自我改进代理

这是 GitHub 星数最高的技能！能让你的 AI 助手自我学习和优化，持续提升能力。

```
clawhub install self-improving-agent
```

**3. Summarize（26.1K 下载）** — 全能内容总结工具

支持总结 URL、PDF、图片、音频、YouTube 视频等多种格式，是内容处理的瑞士军刀。

```
clawhub install summarize
```

**4. Github（24.8K 下载）** — GitHub CLI 集成

管理 issues、PRs、CI 运行，让你在对话中完成所有 GitHub 操作。

```
clawhub install github
```

**5. Weather（21.1K 下载）** — 天气查询

无需 API key，开箱即用的天气查询工具。

```
clawhub install weather
```

如果你是 Mac 用户，这些技能可以直接调用系统原生应用，无需任何配置：

```
# Apple Notes（6.5K下载）
clawhub install apple-notes

# Apple Reminders（5.8K下载）
clawhub install apple-reminders

# Apple Calendar（4.4K下载）
clawhub install apple-calendar

# Apple Shortcuts（5.9K下载）- 运行任何Apple快捷指令
clawhub install apple-shortcuts

# iMessage（3.5K下载）
clawhub install imessage
```

### 🔍 搜索和研究工具

**Tavily Web Search（28K 下载）** — AI 优化的搜索引擎

```
clawhub install tavily-web-search
```

**Brave Search（10.4K 下载）** — 隐私优先的搜索

```
clawhub install brave-search
```

**Multi Search Engine（4.5K 下载）** — 17 个搜索引擎聚合，无需 API key

```
clawhub install multi-search-engine
```

### 📊 生产力和知识管理

**Ontology（27.6K 下载）** — 结构化知识图谱

```
clawhub install ontology
```

**Notion（13.9K 下载）** — Notion API 集成

```
clawhub install notion
```

**Obsidian（12.4K 下载）** — 本地 Markdown 笔记管理

```
clawhub install obsidian
```

### 💻 通信工具

```
# Himalaya（9.2K下载）- IMAP/SMTP邮件，支持任何邮件提供商
clawhub install himalaya

# Slack（8.8K下载）
clawhub install slack

# Discord（6.6K下载）
clawhub install discord

# Signal（5.7K下载）- 安全消息，本地运行
clawhub install signal
```

### ✍️ 媒体和内容创作

**Nano Banana Pro（13.4K 下载）** — Gemini 3 Pro 图像生成和编辑

```
clawhub install nano-banana-pro
```

**OpenAI Whisper（11.5K 下载）** — 本地语音转文字

```
clawhub install openai-whisper
```

**YouTube Watcher（9.1K 下载）** — YouTube 字幕获取

```
clawhub install youtube-watcher
```

### 💻 开发工具（通用）

**API Gateway（13K 下载）** — 连接 100+ API（Stripe、Salesforce 等）

```
clawhub install api-gateway
```

**Mcporter（11.1K 下载）** — 官方 MCP 服务器管理

```
clawhub install mcporter
```

**Commit Message（3K 下载）** — 自动生成 git 提交信息

```
clawhub install commit-message
```

### 🤖 AI 和代理增强

**Free Ride（11.3K 下载）** — 免费 AI 模型访问（OpenRouter）

```
clawhub install free-ride
```

**Model Usage（8.3K 下载）** — 按模型成本跟踪

```
clawhub install model-usage
```

**Oracle（3.3K 下载）** — 第二模型审查调试

```
clawhub install oracle
```

### 🏠 智能家居

**Sonos CLI（20.2K 下载）** — Sonos 音箱控制

```
clawhub install sonos-cli
```

**Home Assistant（6.1K 下载）** — Home Assistant 集成

```
clawhub install home-assistant
```

### Skill 的基本结构

一个标准的 OpenClaw Skill 通常包含以下文件：

```
my-custom-skill/
├── SKILL.md          # Skill的元信息和使用说明
├── skill.json        # 配置文件
├── main.py           # 主逻辑（或其他语言实现）
└── requirements.txt  # 依赖列表
```

### 快速创建一个前端组件生成 Skill

**第一步：[创建 SKILL.md](http://xn--skill-ll6hz28e.md/)**

```
---
name: my-component-generator
description: 自定义前端组件生成器
---

# My Component Generator

用于快速生成前端组件代码。

## 使用方法

`gen component [组件名] [类型]` - 生成指定类型的组件

示例：

- `gen component Button primary` - 生成主按钮组件
- `gen component Card dark` - 生成暗色卡片组件
```

**第二步：编写配置文件 skill.json**

```json
{
  "name": "my-component-generator",
  "version": "1.0.0",
  "description": "自定义前端组件生成器",
  "entry": "main.py",
  "dependencies": ["jinja2"]
}
```

**第三步：编写主逻辑 [main.py](http://main.py/)**

```jsx
import json
from jinja2 import Template

# 组件模板
BUTTON_TEMPLATE = '''
import React from 'react';
import './{{ name }}.css';

interface {{ name }}Props {
  variant?: 'primary' | 'secondary' | 'ghost';
  onClick?: () => void;
  children: React.ReactNode;
}

export const {{ name }}: React.FC<{{ name }}Props> = ({
  variant = 'primary',
  onClick,
  children
}) => {
  return (
    <button classname="{`btn" btn-${variant}`}="" onclick="{onClick}">
      {children}
    </button>
  );
};
'''

CARD_TEMPLATE = '''
import React from 'react';
import './{{ name }}.css';

interface {{ name }}Props {
  title: string;
  content?: string;
  variant?: 'light' | 'dark';
}

export const {{ name }}: React.FC<{{ name }}Props> = ({
  title,
  content,
  variant = 'light'
}) => {
  return (
    <div classname="{`card" card-${variant}`}="">
      <h3 classname="card-title">{title}</h3>
      {content && <p classname="card-content">{content}</p>}
    </div>
  );
};
'''

def handle(request):
    message = request.get("message", "").lower()

    # 解析命令: gen component Button primary
    parts = message.split()
    if len(parts) < 4 or parts[0] != "gen" or parts[1] != "component":
        return {
            "status": "error",
            "message": "请使用格式：gen component [组件名] [类型]
例如：gen component Button primary"
        }

    component_name = parts[2]
    component_type = parts[3]

    # 选择模板
    templates = {
        "button": BUTTON_TEMPLATE,
        "card": CARD_TEMPLATE,
    }

    template_key = component_type if component_type in templates else "button"
    template = Template(templates[template_key])

    code = template.render(name=component_name)

    return {
        "status": "success",
        "message": f"生成的 {component_name} 组件代码：

```{code}```"
    }

if __name__ == "__main__":
    test_request = {"message": "gen component MyButton primary"}
    print(handle(test_request))
```

### Skill 的触发机制

OpenClaw 的 Skills 通过**关键词匹配**或**意图识别**触发。配置时需要注意：

1. **明确的触发词** — 在 [SKILL.md](http://skill.md/) 中用 `code` 格式标注命令格式
2. **合理的参数解析** — 用户输入可能有多种表达方式，需要兼容
3. **清晰的错误提示** — 当用户指令不明确时，给出正确的使用方式

### 发布你的 Skill

开发完成后，可以通过以下方式分享：

1. **提交到 ClawHub** — 让更多开发者可以使用你的 Skill
2. **GitHub 仓库** — 符合 OpenClaw 的目录结构后分享
3. **直接安装** — 告诉朋友“请帮我安装这个 skills，github 链接是 xxx”

### 示例：自动化组件开发工作流

```
用户输入：帮我创建一个用户列表页面

→ UI/UX Pro Max 确定页面布局和设计风格
→ React 生成列表组件代码
→ Frontend Performance 检查性能问题
→ UI Audit 最终体验审核
```

### 示例：技术调研自动化

```
用户输入：调研React 19的Server Actions

→ GitHub 获取官方文档和RFC
→ multi-search-engine 搜索技术博客讨论
→ playwright-scraper-skill 抓取关键页面详情
→ Summarize 生成调研报告
```