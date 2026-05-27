# 11 - 插件与技能系统

## 本文核心问题

插件系统是 Claude Code 的可扩展机制：用户可以安装插件包，添加命令、技能、MCP 服务器。核心问题：**如何让扩展安全（不被恶意插件攻击）、可管理（有范围优先级）、高效（启动时不阻塞）？**

---

## 1. Settings-First 原则

插件操作的核心动作是**更新配置文件**，而不是直接修改运行时状态。安装插件 = 在 `settings.json` 里写入标记，下次启动时才实际加载。

这让所有操作天然幂等：重复安装同一个插件只是重复写同一个配置值，不会有副作用。配置文件是"意图声明"，实际运行状态是这个意图的实例化。

---

## 2. 三级范围覆盖

```
user < project < local
```

优先级设计解决了团队协作的典型冲突：
- 团队统一启用某插件（`project` scope，写入 `.claude/settings.json`）
- 某个开发者想临时禁用（`local` scope 覆盖，写入个人配置）
- 不需要修改团队共享的配置

低优先级 scope 不能覆盖高优先级 scope——除非显式用 `--scope local`。这防止了意外覆盖。

---

## 3. 后台安装：不阻塞启动

插件安装在启动时是后台异步任务，`setAppState` 驱动进度 UI 更新（pending → installing → installed/failed），主线程继续正常运行。

有新安装和仅更新的处理不同：
- **新安装** → 立即 `refreshActivePlugins()`，刷新运行时状态（避免缓存为空导致的错误）
- **仅更新** → 设置 `needsRefresh = true`，提示用户手动执行 `/reload-plugins`

原因：原地更新正在运行的插件实例可能破坏状态，让用户选择时机重载比自动重载更安全。

---

## 4. 技能就是 Markdown 文件

用户在 `~/.claude/skills/` 放一个 `.md` 文件，系统解析 frontmatter，转成 `Command` 对象。文件内容就是发给 Claude 的提示词，`$ARGUMENTS` 占位符被用户输入替换。

frontmatter 字段（`allowed-tools`、`paths`、`model`、`context: fork`）让技能有了元数据，而不只是裸提示词。`paths` 字段用 gitignore 语法做条件激活——只在接触匹配路径的文件后才显示这个技能。

**就近原则**：从当前工作目录向上遍历父目录，自动发现 `.claude/skills/` 目录，不需要用户手动配置路径。

---

## 5. Promise Memoization 防竞态

内置技能可以携带参考文件（`files` 字段），首次调用时才解压到磁盘。解压是异步操作，多个并发调用可能触发竞态写入。

解决方案：memoize 的是 **Promise 对象本身**，而不是结果值：

```javascript
extractionPromise ??= extractBundledSkillFiles(...)
```

如果三个调用同时到来，第一个调用创建 Promise 并存储，第二三个调用得到同一个 Promise，都 await 它。只有一次实际写入，结果被所有调用方共享。这是 Promise 的天然幂等性。

---

## 6. 安全写入的多层防御

内置技能解压到磁盘时，写入路径包含进程级随机 nonce（每次进程启动随机生成），配合三层文件系统保护：

- `O_EXCL`：文件已存在就失败（防 TOCTOU 竞态）
- `O_NOFOLLOW`：不跟随符号链接（防符号链接注入）
- `0o600` 权限：只有 owner 可读写

注意：代码注释里明确说"故意不在 EEXIST 时 unlink + retry"——因为 unlink 会跟随符号链接，unlink 本身就是攻击向量。遇到 EEXIST 直接失败，不尝试覆盖。

路径穿越防护也是显式的：绝对路径、`..` 组件、URL 风格的 `..` 都被检查并拒绝。

---

## 7. 技能去重

技能目录可能通过符号链接或不同路径被多次扫描到，`deduplicateSkills()` 用 `realpath` 去重，防止同一个技能以多个名字出现在命令列表里。

---

## 设计原则提炼

1. **Settings-First**：配置即意图，运行状态是配置的实例化
2. **范围优先级**：团队共享 vs 个人覆盖，通过 scope 而非文件冲突
3. **Promise memoize**：比加锁更优雅的并发写保护
4. **多层安全防御**：随机路径 + O_EXCL + O_NOFOLLOW + 权限，纵深防御
5. **就近原则**：目录向上遍历自动发现，减少配置负担
