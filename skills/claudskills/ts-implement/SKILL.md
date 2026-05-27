---
name: ts-implement
description: TypeScript実装のベストプラクティスとコーディング規約。型安全なコード、モダンな機能、エラーハンドリング、品質基準を提供。TypeScript実装、コーディング規約、型定義パターンが必要な時に参照。
---

# TypeScript Implementation Best Practices

TypeScript実装のベストプラクティス、コーディング規約、パターン集です。型安全で保守性の高いコードを書くための知識ベースとして活用してください。

## 🎯 Core Principles（コア原則）

### 1. **Type Safety First**（型安全性を最優先）
- `any`は使用禁止 → `unknown`または適切な型を使用
- 厳格なTypeScript設定を使用
- 型推論を適切に活用
- 関数パラメータと戻り値には明示的な型を定義

### 2. **Code Quality**（コード品質）
- 明確な命名で自己文書化されたコードを書く
- 関数は小さく、単一責任を保つ（Single Responsibility）
- モダンなJavaScript/TypeScript機能を使用（ES2020+）
- 不要な複雑さを避ける（Keep It Simple）

### 3. **Best Practices**（ベストプラクティス）
- `const`を優先、`let`は必要時のみ、`var`は使用禁止
- コールバックや短い関数にはアロー関数を使用
- 分割代入とスプレッド演算子を活用
- オプショナルチェイニング（`?.`）とnullish coalescing（`??`）を使用
- try-catchで適切なエラーハンドリングを実装

### 4. **Code Organization**（コード構成）
- 既存のプロジェクト構造とパターンに従う
- 関連する機能をまとめる
- バレルエクスポート（index.ts）を適切に使用
- インポートを整理し、最小限に保つ

## 📚 TypeScript Patterns（詳細パターン集）

詳細なコード例とパターンについては、[PATTERNS.md](PATTERNS.md)を参照してください。

### Quick Reference

#### 関数定義
```typescript
// ✅ 明示的な型、明確な目的
function calculateTotal(price: number, taxRate: number): number {
  return price * (1 + taxRate);
}

// ✅ 非同期関数と適切なエラーハンドリング
async function fetchUserData(userId: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    throw new Error(`Failed to fetch user data: ${error}`);
  }
}
```

#### 型定義
```typescript
// ✅ オブジェクトの形状にはinterfaceを使用
interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}

// ✅ Union型や複雑な型にはtypeを使用
type UserRole = 'admin' | 'user' | 'guest';
type Result<T> = Success<T> | Failure;

// ✅ ジェネリック型
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}
```

#### モダンJavaScript機能
```typescript
// ✅ 分割代入
const { id, name, email } = user;
const [first, ...rest] = items;

// ✅ スプレッド演算子
const newUser = { ...user, lastLogin: new Date() };
const allItems = [...existingItems, ...newItems];

// ✅ オプショナルチェイニング
const userName = user?.profile?.name;

// ✅ Nullish coalescing
const displayName = userName ?? 'Anonymous';

// ✅ テンプレートリテラル
const message = `Hello, ${name}! You have ${count} messages.`;
```

## ✅ Quality Standards（品質基準）

実装したコードは以下の基準を満たす必要があります：

- ✅ TypeScriptエラーなし
- ✅ `any`型なし（`unknown`または適切な型を使用）
- ✅ try-catchによる適切なエラーハンドリング
- ✅ 明確な変数名と関数名
- ✅ エクスポート関数へのJSDocコメント
- ✅ プロジェクトパターンとの一貫性
- ✅ エッジケースの処理
- ✅ 適用可能な場合はSOLID原則に従う

## 🔍 Code Review Checklist（コードレビューチェックリスト）

コード実装後、以下を確認してください：

- [ ] すべてのTypeScript型が適切に定義されている
- [ ] `any`、`as any`、または危険な型アサーションがない
- [ ] エラーハンドリングが実装されている
- [ ] 関数名・変数名が明確で説明的
- [ ] コードが既存のプロジェクトパターンに従っている
- [ ] 複雑なロジックにJSDocコメントが追加されている
- [ ] エッジケースが処理されている
- [ ] コードの重複がない
- [ ] インポートが整理されている
- [ ] 未使用の変数やインポートがない

## 🎓 Learning Resources

- 詳細なパターン集: [PATTERNS.md](PATTERNS.md)
- TypeScript公式ドキュメント: https://www.typescriptlang.org/docs/
- TypeScript Deep Dive: https://basarat.gitbook.io/typescript/

---

**このスキルの使い方**: TypeScript実装時にこのスキルを参照して、ベストプラクティスと品質基準に従ったコードを書いてください。
