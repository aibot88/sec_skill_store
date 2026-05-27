---
name: springboot-skills
description: Spring Boot 项目全套开发规范合集，涵盖 RESTful API 设计、编码规范、数据库设计、异常处理、日志监控、性能优化和安全开发。确保代码质量、一致性和可维护性。
---

# Spring Boot 项目开发规范合集

本合集包含 Spring Boot 项目的全套开发规范，共 7 个核心技能模块。**这些规范是底线，不是建议**——违反规则会导致严重的可维护性问题和性能隐患。

## 技能模块总览

| 技能名称                                                                    | 触发场景                                                        | 核心内容                                                                         |
| --------------------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [springboot-api-standards](#springboot-api-standards)           | 编写 Controller、设计 API 接口、参数校验、分页接口、接口文档    | RESTful URL 设计、统一响应格式、Controller 规范、参数校验、分页策略、DTO/VO 规范 |
| [springboot-coding-conventions](#springboot-coding-conventions) | 编写 Java 代码、设计类结构、依赖注入、事务管理、Redis 使用      | 分层架构、命名规范、@Resource 注入、设计模式、Redis 规范、事务管理、Lombok 使用  |
| [springboot-db-design](#springboot-db-design)                   | 创建表、编写 SQL、设计 schema、MyBatis Mapper、索引设计         | 表设计规范、Entity 规范、Mapper 规范、批量操作、数据库迁移                       |
| [springboot-exception-handling](#springboot-exception-handling) | 异常处理、错误码定义、自定义异常类、全局异常处理器              | 异常分类、错误码设计、全局异常处理器、Service 层异常策略、事务回滚               |
| [springboot-logging-monitoring](#springboot-logging-monitoring) | 日志输出、日志级别配置、链路追踪、Metrics 埋点、异步日志        | 日志级别规范、结构化日志、日志脱敏、日志文件配置、链路追踪、监控指标             |
| [springboot-performance](#springboot-performance)               | 数据库查询、列表接口、批量数据、缓存策略、高并发场景            | 禁止 N+1 查询、禁止 OFFSET 深分页、缓存防护、查询优化、连接池配置、异步处理      |
| [springboot-security-standards](#springboot-security-standards) | 认证鉴权、用户输入处理、SQL 查询、敏感数据、文件上传、CORS 配置 | SQL 注入防护、XSS 防护、密码安全、JWT/API Key 安全、敏感数据脱敏、输入校验       |

---

## 核心规范速查

### 1. 分层架构（必须遵守）

```
Controller（接口层）
    ↓ 调用
BizManageService（业务合并层）
    ↓ 调用一个或多个
Service（数据库业务层，基于 MyBatis Plus）
    ↓ 调用
Mapper/DAO（数据访问层）
    ↓ 操作
Database
```

**关键规则**：

- Controller 只接收参数、调用 BizManageService、返回响应，**不写业务逻辑**
- BizManageService 负责编排业务流程、组合多个 Service、事务管理
- Service 只做单表 CRUD，继承 MyBatis Plus `ServiceImpl`
- 依赖只能向下，不能反向或跳层

### 2. RESTful API 设计

```
GET    /api/v1/users/list          # 分页查询用户列表
GET    /api/v1/users/detail?id=1   # 查询单个用户
POST   /api/v1/users/save          # 创建用户
POST   /api/v1/users/update        # 更新用户
DELETE /api/v1/users/1,2,3         # 删除用户（支持批量）
```

**统一响应格式**：

```java
{
    "code": 200,
    "message": "操作成功",
    "data": { ... },
    "timestamp": 1711180800000
}
```

### 3. 依赖注入规范

**统一使用 `@Resource` 注入**（不用 `@Autowired` 和 `@RequiredArgsConstructor`）：

```java
@Service
@Slf4j
public class OrderBizManageService {

    @Resource
    private OrderService orderService;

    @Resource
    private OrderItemService orderItemService;
}
```

### 4. 事务管理

```java
@Transactional(rollbackFor = Exception.class)
public void createOrder(CreateOrderDTO dto) {
    // 涉及多表写操作必须加事务
    orderService.save(order);
    orderItemService.saveBatch(items);
    stockService.deduct(dto.getItems());
}
```

### 5. Redis 使用规范

**Key 命名必须带系统前缀**：

```java
// 格式：{系统前缀}:{业务模块}:{类型}:{标识}
"systemCode:user:info:123"
"systemCode:group:config:gpt-4"
"systemCode:lock:order:ORD001"
```

**所有缓存必须设置过期时间**：

```java
redisTemplate.opsForValue().set(key, value, 1, TimeUnit.HOURS);
```

### 6. 性能红线（绝对禁止）

**禁止循环查库（N+1 问题）**：

```java
// ❌ 禁止
for (Order order : orders) {
    User user = userMapper.selectById(order.getUserId());
}

// ✅ 正确：批量查询 + 内存关联
Set<Long> userIds = orders.stream().map(Order::getUserId).collect(Collectors.toSet());
Map<Long, User> userMap = userMapper.selectBatchIds(userIds).stream()
    .collect(Collectors.toMap(User::getId, Function.identity()));
```

**禁止 OFFSET 深分页**：

```java
// ❌ 禁止：深分页时性能极差
SELECT * FROM users LIMIT 10 OFFSET 100000;

// ✅ 正确：游标分页
SELECT * FROM users WHERE id > lastId ORDER BY id ASC LIMIT 10;
```

### 7. 异常处理

**Service 层主动抛异常，全局异常处理器统一兜底**：

```java
// Service 层
if (user == null) {
    throw new ResourceNotFoundException("用户", id);
}

// 全局异常处理器
@ExceptionHandler(ResourceNotFoundException.class)
public ResponseEntity<ApiResponse<Void>> handleResourceNotFound(ResourceNotFoundException ex) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ApiResponse.error(ex.getCode(), ex.getMessage()));
}
```

### 8. 日志级别规范

| 级别  | 场景                       | 示例                           |
| ----- | -------------------------- | ------------------------------ |
| ERROR | 系统错误，需要立即关注     | 数据库连接失败、外部服务不可用 |
| WARN  | 可预期的异常情况           | 用户认证失败、资源不存在       |
| INFO  | 关键业务节点               | 服务启动、用户登录、订单创建   |
| DEBUG | 开发调试信息，生产环境关闭 | 方法入参出参、SQL 参数         |

### 9. SQL 注入防护

```xml
<!-- ✅ 安全：#{} 使用 PreparedStatement 预编译 -->
<select id="getUserByName" resultType="User">
    SELECT * FROM users WHERE username = #{username}
</select>

<!-- ❌ 危险：${} 是字符串拼接 -->
<select id="getUserByName" resultType="User">
    SELECT * FROM users WHERE username = '${username}'
</select>
```

### 10. 密码安全

```java
// ✅ 正确：使用 BCrypt（自带盐值）
user.setPassword(passwordEncoder.encode(rawPassword));

// ❌ 禁止：明文存储、MD5、SHA-1
user.setPassword(rawPassword);
user.setPassword(DigestUtils.md5Hex(rawPassword));
```

---

## 代码检查清单

每次编写代码时逐条自检：

### 架构分层

- [ ] Controller 中是否写了业务逻辑？（应该只调用 BizManageService）
- [ ] 是否正确使用了 BizManageService 层？（涉及多表操作时）
- [ ] 依赖注入是否使用 `@Resource`？（不用 `@Autowired` 和 `@RequiredArgsConstructor`）

### API 设计

- [ ] URL 是否符合 RESTful 规范？（复数名词、动作路径统一）
- [ ] 是否返回统一的 `ApiResponse<T>` 结构？
- [ ] 参数校验注解是否带 `message`？

### 数据库

- [ ] 表设计是否包含 `created_at` 和 `updated_at`？
- [ ] 是否每个字段都有 COMMENT？
- [ ] 是否避免了 N+1 查询？
- [ ] 分页是否避免了深分页（OFFSET）？

### 性能

- [ ] 是否在循环中调用了 Mapper/Service/Redis？（应改为批量查询）
- [ ] 缓存是否设置了过期时间？
- [ ] 是否考虑了缓存穿透/击穿/雪崩防护？

### 安全

- [ ] SQL 查询是否全部使用 `#{}` 或 LambdaQueryWrapper？
- [ ] 用户输入是否经过校验？
- [ ] 密码是否使用 BCrypt 加密？
- [ ] 日志中是否打印了敏感信息？（密码、API Key、token）

### 异常与日志

- [ ] 业务异常是否继承 `BusinessException`？
- [ ] 事务是否加了 `rollbackFor = Exception.class`？
- [ ] 日志级别是否正确？（ERROR 记录堆栈、WARN 用于可预期异常）

---

## 各技能模块详细说明

完整规范请参考 `references/` 目录下的详细文档。

| 技能模块               | 触发场景                                           | 核心内容                                                |
| ---------------------- | -------------------------------------------------- | ------------------------------------------------------- |
| **api-standards**      | 编写 Controller、设计 API 接口、参数校验、分页接口 | URL 规范、统一响应格式、Controller 规范、DTO/VO 规范    |
| **coding-conventions** | 编写业务代码、依赖注入、事务管理、Redis 使用       | 分层架构、命名规范、@Resource 注入、事务管理、设计模式  |
| **db-design**          | 创建表、编写 SQL、MyBatis Mapper、索引设计         | 表设计规范、Entity 规范、Mapper 规范、批量操作          |
| **exception-handling** | 异常处理、错误码定义、全局异常处理器               | 异常分类、错误码设计、全局异常处理器、Service 层策略    |
| **logging-monitoring** | 日志输出、链路追踪、Metrics 埋点、异步日志         | 日志级别、结构化日志、日志脱敏、链路追踪、监控指标      |
| **performance**        | 数据库查询、列表接口、批量数据、缓存策略、高并发   | 禁止 N+1 查询、禁止深分页、缓存防护、查询优化、异步处理 |
| **security-standards** | 认证鉴权、用户输入、敏感数据、文件上传、CORS 配置  | SQL 注入防护、XSS 防护、密码安全、数据脱敏、输入校验    |

---

## 使用方式

本技能合集适用于以下开发场景：

| 开发场景                    | 应用规范                       |
| --------------------------- | ------------------------------ |
| 编写 Controller 或 API 接口 | API 设计规范                   |
| 编写业务逻辑代码            | 编码规范和分层架构             |
| 设计数据库表或编写 SQL      | 数据库设计规范                 |
| 处理异常或错误              | 异常处理规范                   |
| 添加日志输出                | 日志规范                       |
| 编写查询或列表接口          | 性能规范（检查 N+1、深分页等） |
| 处理用户输入或敏感数据      | 安全规范                       |

---

## 文档结构

```
ai-coding-java-springboot-skills/
├─ skill.md                                       # 本文件：技能合集总览
├─ README.md                                      # 使用说明
├─ spec/                                          # 规范定义（待补充）
└─ references/                                    # 各技能详细文档
   ├─ springboot-api-standards.md
   ├─ springboot-coding-conventions.md
   ├─ springboot-db-design.md
   ├─ springboot-exception-handling.md
   ├─ springboot-logging-monitoring.md
   ├─ springboot-performance.md
   └─ springboot-security-standards.md
```

---

**版本**: 1.0.0
**适用范围**: Spring Boot + MyBatis Plus + Redis 项目
