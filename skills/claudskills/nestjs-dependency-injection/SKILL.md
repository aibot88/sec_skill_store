---
name: nestjs-dependency-injection
description: NestJS dependency injection system, providers, injection tokens, scoped providers, and advanced DI patterns. Use when working with dependency injection, creating services, or managing provider lifecycles in NestJS.
license: MIT
metadata:
  author: snowmerak
  version: '1.0'
  category: nestjs
  tags: [di, providers, injection, scoped-providers, dynamic-modules]
---

# NestJS Dependency Injection - DI System & Provider Patterns

## Overview

NestJS는 Angular에서 영감 받은 런타임 의존성 주입(DI) 시스템을 제공합니다. 모듈 구조를 거울처럼 반영하는 계층적 DI 트리를 유지하며, 클래스/값/팩토리/일래스 등 다양한 프로바이더 타입을 지원합니다.

---

## SOP: Step-by-Step Procedures

### SOP-1: 기본 Provider (Service) 생성 및 인젝션

```typescript
// 1. @Injectable() 데코레이터로 마크
@Injectable()
export class CatsService {
  findAll(): Cat[] { /* ... */ }
}

// 2. Module에 providers 배열에 등록
@Module({
  providers: [CatsService],
})
export class CatsModule {}

// 3. Controller 생성자에 인젝션 (클래스 토큰)
@Controller('cats')
export class CatsController {
  constructor(private readonly catsService: CatsService) {}
}
```

### SOP-2: Provider 타입별 선택 가이드

| 상황 | Provider 타입 | 사용법 |
|------|--------------|--------|
| 일반 서비스 | **Class** (기본) | `providers: [CatsService]` |
| 상수/설정 값 | **Value** | `{ provide: 'CONFIG', useValue: { port: 3000 } }` |
| 동적 생성 필요 | **Factory** | `{ provide: 'DB', useFactory: () => createDb() }` |
| 별명 부여 | **Alias** | `{ provide: 'ALIAS', useExisting: CatsService }` |

```typescript
// Factory Provider — 의존성 인젝션 가능
{
  provide: 'API_SERVICE',
  useFactory: (config: ConfigService) => {
    return config.get('USE_MOCK') ? new MockApi() : new RealApi();
  },
  inject: [ConfigService],          // ← 팩토리에서 사용할 의존성 명시
}
```

### SOP-3: Injection Token 사용

| 토큰 타입 | 언제 사용 | 예시 |
|-----------|----------|------|
| **Class** (기본) | 클래스 기반 DI | `constructor(private svc: CatsService)` |
| **String** | 인터페이스/상수 값 | `{ provide: 'CONFIG', useValue }` + `@Inject('CONFIG')` |
| **Symbol** | 충돌 방지 | `export const CONFIG = Symbol('CONFIG')` |

```typescript
// String Token
const CONFIG_TOKEN = 'CONFIG';
constructor(@Inject(CONFIG_TOKEN) private config: Config) {}

// Symbol Token (권장 — 타입 안전 + 충돌 불가)
export const CONFIG_TOKEN = Symbol.for('CONFIG');
constructor(@Inject(CONFIG_TOKEN) private config: Config) {}
```

### SOP-4: Provider Scope 설정

| Scope | 인스턴스 수 | 사용 사례 |
|-------|-----------|----------|
| `DEFAULT` (Singleton) | 모듈당 1개 | 일반 서비스, 레포지토리 (**기본값**) |
| `REQUEST` | 요청당 1개 | Request Context, 트랜잭션 관리 |
| `TRANSIENT` | 인젝션마다 새 인스턴스 | 상태가 격리되어야 할 때 |

```typescript
// Per-Request Scope — 각 HTTP 요청마다 새 인스턴스 생성
@Injectable({ scope: Scope.REQUEST })
export class RequestContextService {
  private requestId: string;
}

// Singleton (기본값 — 명시 안 해도 됨)
@Injectable()  // ≡ @Injectable({ scope: Scope.DEFAULT })
export class ConfigService {}
```

### SOP-5: Dynamic Module 패턴

```typescript
@Module({})
export class DatabaseModule {
  static forRoot(options: DbOptions): DynamicModule {
    return {
      module: DatabaseModule,
      providers: [
        { provide: 'DB_OPTIONS', useValue: options },
        DbConnectionService,
      ],
      exports: [DbConnectionService],
    };
  }

  // 비동기 설정 (ConfigService와 연동) — 권장
  static forRootAsync(options: DynamicModuleOptions): DynamicModule {
    return {
      module: DatabaseModule,
      imports: options.imports || [],
      providers: [
        ...options.providers || [],
        {
          provide: 'DB_OPTIONS',
          useFactory: options.useFactory,
          inject: options.inject || [],
        },
      ],
      exports: [DbConnectionService],
    };
  }
}

// 사용
@Module({
  imports: [DatabaseModule.forRootAsync({
    imports: [ConfigModule],
    inject: [ConfigService],
    useFactory: (cfg: ConfigService) => ({
      host: cfg.get('DB_HOST'),
      port: cfg.get('DB_PORT'),
    }),
  })],
})
export class AppModule {}
```

### SOP-6: Global Module (전역 프로바이더)

```typescript
@Global()     // ← 이 데코레이터가 핵심
@Module({
  providers: [ConfigService],
  exports: [ConfigService],
})
export class ConfigModule {}
// 이제 모든 모듈에서 import 없이 ConfigService 사용 가능
```

---

## Tool Integration

| 작업 | 도구 | 예시 |
|------|------|------|
| DI 그래프 분석 | `search_files` | `search_files("@Injectable", "*.ts")`로 전체 Provider 목록 확인 |
| Module 구조 파악 | `read_file` | `app.module.ts`에서 imports/exports 확인 |
| 코드 생성 | `run_command` | `nest g service users --flat` |

---

## Anti-Patterns & Guardrails

- ❌ **프로퍼티 인젝션(`@Inject()`) 금지** — 항상 생성자 인젝션 사용하세요. 테스트 용이성 + 의존성 명확화
- ❌ **순환 의존성(Circular Dependency) 발생 시 `forwardRef()` 남용 금지** — 코드 구조를 리팩토링하여 순환을 해소하세요
- ❌ **`@Global()` 무분별한 사용 금지** — ConfigService 등 진정한 전역 서비스에만 사용. 대부분의 모듈은 명시적 import 권장
- ❌ **Scoped Provider(REQUEST/TRANSIENT) 오용 금지** — Singleton이 기본값이며, Request Scope는 정말 필요할 때만 사용 (성능 영향 있음)
- ⚠️ **`.$type<>()` 같은 타입 단언은 런타임 체크가 아님** — 컴파일 시점에만 유효

## Best Practices

1. 생성자 인젝션 항상 사용 (프로퍼티 인젝션 금지)
2. 단일 책임 원칙: 각 Service는 한 가지 역할만
3. 인터페이스/추상 클래스에 의존 (구현 클래스가 아닌)
4. Dynamic Module로 설정 기반 모듈 구성
5. `@Global()`은 ConfigService 등 진정한 전역 서비스에만

## References

- [NestJS Providers](https://docs.nestjs.com/providers)
- [Custom Provider Types](https://docs.nestjs.com/fundamentals/custom-providers)
- [Scoped Providers](https://docs.nestjs.com/fundamentals/scoped-providers)
- [Dynamic Modules](https://docs.nestjs.com/fundamentals/dynamic-modules)
