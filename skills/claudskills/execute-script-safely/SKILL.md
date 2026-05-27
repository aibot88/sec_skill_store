---
name: execute-script-safely
description: |
  使い捨ての Python / shell スクリプトを sandbox 内で実行する前に、
  haiku Agent で security pre-review を通して安全性を判定する。

  サンドボックスは外部ネット exfil は防ぐが secret 読取や CWD 内の
  source code poisoning は防げないため、実行前チェックが必要。

  以下の場面で使用 (review-loop skill からも呼ばれる):
  - 動作確認のため /tmp/check_*.py 等の一時スクリプトを実行
  - 調査 snippet を uv run python や .venv/bin/python で走らせる
  - サブエージェントが生成したスクリプトを実行する

  以下では使用しない:
  - プロジェクトに commit 済みのスクリプト (scripts/run.py 等) の実行
  - allowlist 済み固定 entrypoint (pytest, ruff) の起動
  - python -c "print(1+1)" レベルの 1 行 snippet
    (ただし未知モジュールを import する場合は対象)
allowed-tools: Agent, Read, Write, Bash
model: haiku
license: MIT
metadata:
  origin: "https://github.com/ebal5/agent-skills"
---

# Execute Script Safely

一時スクリプトを sandbox 内で実行する前に haiku Agent で security review を
通し、判定結果に応じて実行 / 停止 / ユーザー確認を切り分ける。

## なぜ必要か

サンドボックス単体では**完全に安全ではない**:

| 層 | 防御 | 攻撃経路 |
| --- | --- | --- |
| Network | 限定 host のみ許可 | 外部 exfil は防げる ✅ |
| FS read | 制限なし | HOME 内 secret (`~/.ssh/`, `~/.aws/`, `.env`) 読める ❌ |
| FS write | CWD / `$TMPDIR` のみ | HOME 持続化は防げるが **CWD 内 source poisoning は可能** ❌ |
| Process | 子プロセス継承不明 | subprocess spawn が escape する可能性 ⚠️ |

**最大脅威**: **source code poisoning → sandbox 外実行**。スクリプトが
CWD 内の `.py` / `.github/workflows/*.yml` / `pyproject.toml` を書き換え、
ユーザーが sandbox 外 (CI, ローカル shell) で実行した瞬間に secret 流出 /
任意コード実行が成立する。

## Workflow

### Step 1: スクリプトをファイルに書き出す

メモリ上ではなく以下のいずれかに配置:

- `/tmp/claude/xxx.py` (ephemeral)
- CWD 内 `.tmp-scripts/xxx.py` (gitignore 済み前提)

### Step 2: haiku Agent で pre-review

pre-review プロンプトは `pre-review-prompt.md` を読み込み、スクリプト本体を差し込んで `Agent` に渡す。

### Step 3: 判定別の対応

| 判定 | 対応 |
| --- | --- |
| **clean** | 7 項目いずれも該当しない or 意図明白で害なし。**実行 OK** |
| **suspicious** | 1 項目以上該当するが直接的悪意は見えない。**ユーザー確認** |
| **dangerous** | 明確な exfil / secret 読取 / source 改変。**即停止、報告** |

### Step 4: 実行

clean なら:

- `uv run python <path>` (allow 済み)
- `.venv/bin/python <path>` (allow 済み)

suspicious / dangerous なら **ユーザーに判定と根拠を提示**し、許可を仰ぐ。
silent pass は絶対に行わない (後から辿れなくなる)。

## スキップ可能な場合

以下は pre-review なしで実行 OK:

- プロジェクトに commit 済みのスクリプト (履歴でレビュー済み前提)
- pytest / ruff / 特定 CLI の allow 済み entrypoint
- `uv run python -c "print(1+1)"` 級の 1 行 snippet
  (ただし未知モジュール import を含む場合は対象)

## 実装 Tips

- **haiku モデル指定**: `Agent(subagent_type: "general-purpose", model: "haiku", ...)`
  で低コスト固定
- **ファイル渡し**: スクリプトをファイル化してから Agent に渡す
  (生コード貼るより再読込可能、大きなスクリプトでも欠損しない)
- **判定結果はユーザー出力必須**: 「実行前に haiku で判定: clean、理由: ...」
  のように見える形で 1 行残す
- **ループ化しない**: 1 スクリプト 1 review。判定後に edit した場合は再 review

## よくある誤検出 (clean なケース)

- `open("data.json", "w")` で CWD に書く → clean (CWD 内書込は想定内)
- `subprocess.run(["git", "status"])` 引数固定 → clean (injection 余地なし)
- `os.environ.get("HOME")` 単独 → clean (exfil 先がなければ無害)
- `requests.get("https://docs.anthropic.com/...")` → clean (allow host)

## dangerous 例

- `open(Path.home() / ".ssh/id_rsa")` + `print(f.read())` → exfil 経路準備
- `Path(".github/workflows/ci.yml").write_text(attacker_controlled)` → poisoning
- `exec(base64.b64decode(blob))` → 難読化実行
- `subprocess.run(f"curl {url} | bash", shell=True)` → 命令 injection

## 判定に迷ったら

`suspicious` に寄せてユーザーに判断を仰ぐ。誤判定で `dangerous` 扱いしても
実行が止まるだけだが、誤判定で `clean` として悪意コードが走ると取り返しが
つかない。**保守的に判定**する。
