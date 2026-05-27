---
name: dart-oss-fresh
description: 学习 felangel/fresh 开源项目，通过 OAuth Token 自动刷新库理解 Dart 异步编程模式（Future、拦截器、Stream、网络请求链），掌握实际异步架构设计。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-async-concurrency
    - dart-classes-objects
  project:
    url: https://github.com/felangel/fresh
    stars: 421
    difficulty: intermediate
    category: library
---

# 学习 Fresh Token 自动刷新库项目

## Contents

- [项目概览](#项目概览)
- [与 dart-async-concurrency 的关联](#与-dart-async-concurrency-的关联)
- [项目架构分析](#项目架构分析)
- [异步编程模式详解](#异步编程模式详解)
- [Workflow: 通过 Fresh 学习 Dart 异步编程](#workflow-通过-fresh-学习-dart-异步编程)
- [Examples](#examples)

## 项目概览

**项目名称**: fresh
**作者**: felangel (bloc 作者)
**GitHub**: https://github.com/felangel/fresh
**Stars**: 421 | **难度**: 中等

一个纯 Dart 的 OAuth Token 自动刷新库。支持 dio、http 和 graphql 三种 HTTP 客户端。核心设计模式是拦截器——在请求发送前自动检查 Token 是否过期，若过期则自动刷新后再发送原请求。项目中 Future 链式处理、Stream 监听、异步错误恢复等技术是学习 `dart-async-concurrency` 的绝佳案例。

## 与 dart-async-concurrency 的关联

该项目集中展示了 `dart-async-concurrency` 技能的核心内容：

| dart-async-concurrency 主题 | 项目中的应用 |
|--------------------------|------------|
| Future 链式处理 | `then` / `catchError` / `whenComplete` |
| async/await | Token 刷新方法 |
| Stream 控制 | Token 变化通知流 |
| 异步错误处理 | 401 拦截 → 刷新 → 重试 |
| Future.wait | 批量并发请求 Token 刷新等待 |
| 异步状态管理 | 刷新锁防止重复刷新 |

## 项目架构分析

### 核心模型

```
TokenStorage<T> (abstract)
    ├── read()   → Future<T>
    ├── write(T) → Future<void>
    ├── delete() → Future<void>

TokenRefresher<T> (typedef)
    └── Future<T> Function(T? token)

Fresh<T> (class)
    ├── token → Stream<T?>
    ├── authenticationStatus → Stream<AuthenticationStatus>
    ├── setToken(T)
    ├── refreshToken(T?)
    └── close()
```

### 拦截器机制

```dart
class Fresh<T> {
  final TokenStorage<T> _tokenStorage;
  final TokenRefresher<T> _refreshToken;
  final StreamController<T?> _tokenController;

  final Stream<T?> get token => _tokenController.stream;

  Future<T> _getOrRefreshToken() async {
    final current = await _tokenStorage.read();
    if (current == null || _isExpired(current)) {
      return _refreshToken(current);
    }
    return current;
  }
}
```

## 异步编程模式详解

### Token 刷新锁模式

防止多个并发请求同时触发刷新：

```dart
Future<T?> _refreshLock;
bool _refreshing = false;

Future<T> _validateAndRefresh(T token) async {
  if (_isFresh(token)) return token;

  if (_refreshing) {
    return _refreshLock!; // 等待正在进行的刷新
  }

  _refreshing = true;
  _refreshLock = _refreshToken(token)
      .then((newToken) {
        _refreshing = false;
        return newToken;
      })
      .catchError((error) {
        _refreshing = false;
        throw error;
      });

  return _refreshLock!;
}
```

### Stream 广播模式

```dart
enum AuthenticationStatus { authenticated, unauthenticated }

final _authController = StreamController<AuthenticationStatus>.broadcast();

Stream<AuthenticationStatus> get authenticationStatus =>
    _authController.stream;

setToken(T token) {
  _authController.add(AuthenticationStatus.authenticated);
}

signOut() async {
  await _tokenStorage.delete();
  _authController.add(AuthenticationStatus.unauthenticated);
}
```

## Workflow: 通过 Fresh 学习 Dart 异步编程

### Task Progress

- [ ] **Step 1: 阅读 Fresh 接口定义。** 从抽象类 `TokenStorage` 和 `typedef TokenRefresher` 理解架构意图。
- [ ] **Step 2: 分析拦截器流程。** 跟踪一次请求从发出到收到完整响应的 Future 链路。
- [ ] **Step 3: 理解 Stream 使用。** 标注 token Stream 和 authenticationStatus Stream 的生产和消费逻辑。
- [ ] **Step 4: 运行测试。** `dart test` 观察各个异步场景的测试用例。
- [ ] **Step 5: 实现自定义 TokenStorage。** 基于 `dart:io` 文件系统创建持久化的 TokenStorage。
- [ ] **Step 6: 编写异步单元测试。** 使用 `expectLater` / `emitsInOrder` 验证 Stream 行为。
- [ ] **Step 7: 添加超时处理。** 为 Token 刷新添加超时和重试逻辑。
- [ ] **Step 8: Feedback Loop。** 运行测试 → 分析异步错误栈 → 修正 → 重复。

### 条件逻辑

- **如果对 Future 链不理解：** 使用 `dart-async-concurrency` 技能中 Future 章节逐一对照。
- **如果需要处理并发刷新：** 参考项目的刷新锁模式，避免构造竞态条件。
- **如果 Stream 消费逻辑不对：** 检查是单订阅流还是广播流，确保使用正确的 StreamController 类型。
- **如果异步错误被吞没：** 在 Future 链中添加 `.catchError` 或使用 try/catch 包裹 await 调用。

## Examples

### 从项目中学到的拦截器模式

```dart
Future<Response> _intercept(RequestOptions options) async {
  final token = await _getOrRefreshToken();
  options.headers['Authorization'] = 'Bearer $token';
  return _client.get(options.uri.toString(), headers: options.headers);
}
```

### 结合 dart-async-concurrency 的延伸练习：超时重试

```dart
Future<T> _refreshWithRetry(T? token, {int retries = 3}) async {
  for (var i = 0; i < retries; i++) {
    try {
      return await _refreshToken(token).timeout(
        const Duration(seconds: 10),
      );
    } on TimeoutException {
      if (i == retries - 1) rethrow;
      await Future.delayed(Duration(seconds: 1 << i)); // 指数退避
    }
  }
  throw Exception('Token 刷新失败，已达最大重试次数');
}
```
