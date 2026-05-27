---
name: pdf-decrypt
description: 自动猜密码解 PDF（银行账单 / 投资报告 / 信用卡对账单等）。读 ~/.personal_env 的 PDF_ID_* 身份变量，按发行方密码规则生成候选并用 qpdf 试解。当用户提供加密 PDF 且未提供密码（"读不了" / "解密一下" / "这个 PDF 加密了"）时触发。
---

# pdf-decrypt · v0.1

> **依赖**：`qpdf`（`brew install qpdf`，已装 v12+）
> **身份配置**：`~/.personal_env` 的 `PDF_ID_*` 变量（首次用先 setup）
> **命中日志**：`~/.cache/pdf-decrypt/hits.tsv`（rule + id 类型，不存密码明文）

## 何时触发

用户给一个加密 PDF（路径 / 拖文件）且**未提供密码** → **第一动作**就跑本 skill，不要让用户手输密码。典型 trigger：

- "这个 PDF 你能读吗 / 读不了 / 加密了"
- "解一下这个账单" / "qpdf 解密一下"
- 用户给路径后 Read tool 返回二进制 / "encrypted"
- HSBC / 渣打 / 中银 / Citi / 美林 等银行/券商发的月结、投资结单
- 政府报告 / 公报 PDF 标"禁止打印/复制"（permissions-only 加密）

## 加密类型分流（自动）

脚本先 `qpdf --show-encryption` 分类，按类型走不同路径：

| 类型 | 特征 | 处理 |
|---|---|---|
| `none` | 完全未加密 | 退出，不动文件 |
| `permissions-only` | user password 为空，仅权限位限制（禁打印/复制/编辑） | **`qpdf --decrypt` 一发去权限**，不需要密码 |
| `user-password` | 真加密，必须正确密码才能开 | 走"猜密码"流程（候选规则 × 证件号） |

`--force-guess` 强制即使 permissions-only 也走猜密码（一般用不到）。

## 用法

```bash
# 默认（全规则跑）
python3 ~/.claude/skills/pdf-decrypt/scripts/decrypt.py /path/to/file.pdf

# 只用某个发行方规则
python3 ~/.claude/skills/pdf-decrypt/scripts/decrypt.py file.pdf --issuer hsbc-hk

# 直接指定密码
python3 ~/.claude/skills/pdf-decrypt/scripts/decrypt.py file.pdf --password 289CJ6NG

# 只列候选不试（debug 用）
python3 ~/.claude/skills/pdf-decrypt/scripts/decrypt.py file.pdf --dry-run

# 列出所有支持的规则
python3 ~/.claude/skills/pdf-decrypt/scripts/decrypt.py --list

# 命中后明文打印密码（默认遮罩）
python3 ~/.claude/skills/pdf-decrypt/scripts/decrypt.py file.pdf --show
```

输出：`<file>-decrypted.pdf`（同目录）。命中规则 + ID 类型写日志 `~/.cache/pdf-decrypt/hits.tsv`，密码不入日志。

## 身份配置（首次必做）

在 `~/.personal_env` 加（不要进 git）：

```bash
export PDF_ID_BIRTH_DATE="1989-12-13"        # YYYY-MM-DD
export PDF_ID_SURNAME_PY="ZENG"              # 姓拼音大写
export PDF_ID_GIVEN_PY="TIANLI"              # 名拼音大写
export PDF_ID_HKID=""                        # 香港身份证（不含括号校验位）
export PDF_ID_PASSPORT_HK="CJ6664388"        # 港澳通行证
export PDF_ID_PASSPORT_INTL=""               # 国际护照
export PDF_ID_CN_ID=""                       # 大陆身份证
```

**所有字段都可留空** —— 脚本会跳过不能算的规则。证件号至少填 1 个，否则规则库大半失效。

## 当前规则库

| Rule ID | 描述 | 用到字段 |
|---|---|---|
| `hsbc-hk` | HSBC HK 投资 / WPL / 信用卡：月末位 + 年末2位 + 证件首3位 + 姓末2字母大写 | birth_date, surname_py, 任一证件 |
| `dob-yyyymmdd` | 生日 YYYYMMDD | birth_date |
| `dob-ddmmyyyy` | 生日 DDMMYYYY（英式 / 部分港行） | birth_date |
| `dob-mmddyy` | 生日 MMDDYY（部分美行） | birth_date |
| `id-full` | 证件号原文 | 任一证件 |
| `id-last4` | 证件号末 4 位 | 任一证件 |
| `id-last6` | 证件号末 6 位 | 任一证件 |
| `surname-dob` | 姓 + DDMMYYYY | surname_py, birth_date |

每条规则会跨所有非空证件号产生候选；总候选数 ≈ 规则数 × 证件数（去重）。一般 < 30 个，全跑 < 5 秒。

## 扩展新规则（加发行方）

在 `scripts/decrypt.py` 加函数：

```python
def rule_citibank_hk(i: Identity, id_value: str) -> str | None:
    """Citi HK：MMDDYY + ID 末 4 位"""
    if not (i.birth_month and i.birth_day and i.birth_year_last2 and len(id_value) >= 4):
        return None
    return i.birth_month + i.birth_day + i.birth_year_last2 + id_value[-4:]
```

注册到 `RULES` 字典即可。每个新规则带：
- 规则名（kebab-case，如 `citi-hk`）
- 一行中文描述
- 函数签名 `(Identity, id_value: str) -> str | None`（不能算时返回 `None`）

新规则上线前先用 `--issuer <new-rule>` 验证至少一份历史 PDF 能解开。

## 流程（CC 怎么用）

```
1. 用户给加密 PDF 路径（无密码）
2. CC 跑：python3 ~/.claude/skills/pdf-decrypt/scripts/decrypt.py <path>
3. 输出 <path>-decrypted.pdf
4. CC 用 Read 读解密后 PDF，回答用户问题
```

**不要**：
- ❌ 让用户手输密码（除非全规则失败 + dry-run 看过候选都不对）
- ❌ 直接 Read 加密 PDF（会拿到无意义文本 / 错误）
- ❌ 不试就放弃，告诉用户"读不了"

**全规则都失败**：报告候选数 + 让用户给密码（`--password`），或问规则细节加进规则库。

## 改 SSOT

源码：`~/Dev/tools/cc-configs/skills/pdf-decrypt/`
分发：`~/.claude/skills/pdf-decrypt/`（symlink，install.sh 自动建）
