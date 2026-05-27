---
name: vercel-link
description: "vercel link、プロジェクト接続、Vercelプロジェクトをリンク、vercel連携、link Vercel project、connect to Vercel project に関連するリクエストで使用。vercel linkコマンドの安全な実行手順と注意事項を提供する。"
---

# Vercel Link - プロジェクト接続手順

## 安全な vercel link コマンド

```bash
vercel link --yes --project <project-name> --scope <scope-name>
```

### オプションの説明

- `--yes`: `--project` と `--scope` を**両方**明示指定している場合のみ使用可
  - `--project` を省略して `--yes` を使うと、対話なしで**意図しない新規プロジェクトが自動作成される危険がある**
- `--project`: Vercelダッシュボード上のプロジェクト名を正確に指定
- `--scope`: 組織名またはチーム名を指定。省略するとデフォルトアカウントが使われる

## 初回セットアップ（vercel login）

未認証の場合、まず `vercel login` を実行する。

1. `vercel login` 実行
2. ブラウザが自動で開き、Vercelアカウントで認証
3. 認証完了後、CLIに戻って操作可能になる
4. `vercel whoami` で認証状態を確認

## 前提条件

1. **認証状態の確認**
   ```bash
   vercel whoami
   ```

2. **Vercelダッシュボードでプロジェクトが既に作成されていること**
   - `vercel link` はプロジェクトの**接続**のみ行い、新規作成はしない
   - 存在しないプロジェクト名を指定するとエラーになる（安全）

3. **プロジェクト名とスコープ名を正確に把握していること**
   - Vercelダッシュボード → Settings → General で確認可能

## 自動生成されるファイル

`vercel link` 実行後、以下のファイルが自動生成される:

| ファイル | 内容 |
|---------|------|
| `.vercel/project.json` | `projectId`, `orgId`, `projectName` が記録される |
| `.vercel/README.txt` | Vercelが生成する説明文 |
| `.env.local` | development環境の環境変数が自動ダウンロードされる |

また、`.vercel/` と `.env.local` は自動で `.gitignore` に追加される。

## 注意点

- **`.vercel/project.json` はGit管理しない**: プロジェクトIDが含まれるため、`.gitignore` に追加されていることを確認すること
- **worktree内でlinkする場合**: worktreeごとに `vercel link` の実行が必要（`.vercel/` はworktreeごとに独立）
- **link後の環境変数取得**: `vercel env pull` で環境変数を再取得可能

## link後の確認

```bash
# .vercel/project.json の内容確認
cat .vercel/project.json

# 環境変数の再取得（必要な場合）
vercel env pull .env.local
```

## よくあるエラーと対処

| エラー | 原因 | 対処 |
|-------|------|------|
| `Project not found` | プロジェクト名またはスコープ名が誤っている | Vercelダッシュボードで正確な名前を確認 |
| `Authentication required` | ログインしていない | `vercel login` を実行 |
| `Scope not found` | 組織名が誤っている | `vercel teams ls` でチーム一覧を確認（※個人アカウントの場合はチーム一覧は表示されない。`vercel whoami` でアカウント確認を推奨） |
