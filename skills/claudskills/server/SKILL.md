---
name: nestjs-ddd-backend
description: |
  Arquitectura backend NestJS con DDD (Domain-Driven Design), Prisma ORM, PostgreSQL, Redis y JWT Auth.
  Guía completa para replicar este patrón en cualquier dominio de negocio (hoteles, restaurantes, e-commerce, etc.).
  Cubre: estructura de módulos, capas DDD, inyección de dependencias, autenticación, paginación, Docker y convenciones de código.
---

# 🏗️ Backend NestJS — Arquitectura DDD Completa

Guía para replicar la arquitectura backend en cualquier dominio de negocio.
Proyecto de referencia: **MediClick** (sistema médico).

---

## 📋 Stack Tecnológico

| Tecnología        | Versión  | Propósito                          |
|-------------------|----------|------------------------------------|
| NestJS            | ^11.x    | Framework backend                  |
| Prisma ORM        | ^7.x     | ORM con adaptador PostgreSQL       |
| PostgreSQL        | 17       | Base de datos relacional           |
| Redis             | 7        | Cache + almacenamiento de tokens   |
| Passport + JWT    | ^11.x    | Autenticación                      |
| Swagger            | ^11.x    | Documentación de API               |
| class-validator   | ^0.14    | Validación de DTOs                 |
| class-transformer | ^0.5     | Transformación de datos            |
| bcrypt            | ^6.x     | Hashing de contraseñas             |
| pnpm              | latest   | Package manager                    |
| TypeScript        | ^5.7     | Lenguaje                           |

---

## 📁 Estructura de Directorios

```
server/
├── docker-compose.yml          # PostgreSQL + Redis
├── package.json                # Scripts y dependencias
├── tsconfig.json               # Configuración TypeScript
├── nest-cli.json               # Configuración NestJS CLI
├── prisma/
│   ├── schema.prisma           # Modelos de base de datos
│   ├── seed.js                 # Seed inicial (admin user)
│   └── migrations/             # Historial de migraciones
├── src/
│   ├── main.ts                 # Bootstrap de la app
│   ├── app.module.ts           # Módulo raíz
│   ├── prisma/                 # PrismaService global
│   │   ├── prisma.module.ts
│   │   └── prisma.service.ts
│   ├── shared/                 # Código compartido entre módulos
│   │   ├── constants/
│   │   ├── decorators/
│   │   ├── guards/
│   │   ├── domain/
│   │   │   ├── enums/
│   │   │   ├── interfaces/
│   │   │   └── contracts/
│   │   ├── redis/
│   │   └── utils/
│   └── modules/                # Módulos de dominio (DDD)
│       ├── auth/
│       ├── users/
│       └── [tu-modulo]/
```

---

## 🧱 Arquitectura DDD por Módulo

Cada módulo de dominio sigue esta estructura de 4 capas:

```
src/modules/{nombre-modulo}/
├── application/              # 🎯 Capa de Aplicación
│   ├── {nombre}.module.ts    #    Wiring de NestJS (imports, providers, exports)
│   ├── dto/                  #    Data Transfer Objects (validación + Swagger)
│   │   ├── create-*.dto.ts
│   │   ├── update-*.dto.ts
│   │   ├── find-all-*.dto.ts
│   │   └── *-response.dto.ts
│   └── use-cases/            #    Casos de uso (lógica de negocio)
│       ├── create-*.use-case.ts
│       ├── find-all-*.use-case.ts
│       ├── find-*-by-id.use-case.ts
│       ├── update-*.use-case.ts
│       └── delete-*.use-case.ts
│
├── domain/                   # 💎 Capa de Dominio (sin dependencias externas)
│   ├── entities/             #    Entidades de dominio (clases simples)
│   │   └── *.entity.ts
│   ├── repositories/         #    Interfaces de repositorio (contratos)
│   │   └── *.repository.ts
│   ├── interfaces/           #    Interfaces de datos auxiliares
│   │   └── *-data.interface.ts
│   ├── services/             #    Servicios de dominio (opcional)
│   │   └── *.service.ts
│   └── enums/                #    Enums de dominio (opcional, preferir shared)
│       └── *.enum.ts
│
├── infrastructure/           # 🔧 Capa de Infraestructura
│   ├── persistence/          #    Implementaciones concretas de repositorios
│   │   └── prisma-*.repository.ts
│   ├── repositories/         #    Repositorios que usan Redis u otros
│   │   └── redis-*.repository.ts
│   ├── services/             #    Servicios de infraestructura
│   │   └── *.service.ts
│   └── strategies/           #    Estrategias (JWT, etc.)
│       └── *.strategy.ts
│
└── interfaces/               # 🌐 Capa de Interfaces (API)
    └── controllers/
        └── *.controller.ts   #    Endpoints REST + Swagger
```

---

## 📝 Patrones de Código por Capa

### 1. 💎 Entity (Dominio)

Clase simple sin decoradores de framework, solo tipado TypeScript:

```typescript
// src/modules/{modulo}/domain/entities/{nombre}.entity.ts
import { UserRole } from '../../../../shared/domain/enums/user-role.enum.js';

export class UserEntity {
  id: number;
  name: string;
  email: string;
  password: string;
  photo: string | null;
  role: UserRole;
  isActive: boolean;
  deleted: boolean;
  createdAt: Date;
  updatedAt: Date | null;
}
```

> **Convención**: Las entidades son POJOs tipados. No usan decoradores ni lógica de persistencia.

---

### 2. 📜 Repository Interface (Dominio)

Define el contrato que la infraestructura debe cumplir:

```typescript
// src/modules/{modulo}/domain/repositories/{nombre}.repository.ts
import { UserEntity } from '../entities/user.entity.js';
import { PaginationParams } from '../../../../shared/domain/interfaces/pagination-params.interface.js';
import { PaginatedResult } from '../../../../shared/domain/interfaces/paginated-result.interface.js';

export interface IUserRepository {
  findByEmail(email: string): Promise<UserEntity | null>;
  findById(id: number): Promise<UserEntity | null>;
  existsByEmail(email: string): Promise<boolean>;
  createInternalUser(data: CreateInternalUserData): Promise<UserEntity>;
  findAllPaginated(params: PaginationParams, role?: UserRole): Promise<PaginatedResult<UserWithProfile>>;
  findByIdWithProfile(id: number): Promise<UserWithProfile | null>;
  updateUser(id: number, data: UpdateUserData): Promise<UserWithProfile>;
  softDelete(id: number): Promise<void>;
}
```

> **Convención**: Las interfaces usan el prefijo `I` (ej: `IUserRepository`). Se registran como token de inyección con string `'IUserRepository'`.

---

### 3. 🔧 Prisma Repository (Infraestructura)

Implementación concreta del repositorio usando Prisma:

```typescript
// src/modules/{modulo}/infrastructure/persistence/prisma-{nombre}.repository.ts
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../../prisma/prisma.service.js';
import { IUserRepository } from '../../domain/repositories/user.repository.js';

// Helper: mapear Prisma raw → Entity
function mapToUserEntity(prismaUser: any): UserEntity {
  const entity = new UserEntity();
  Object.assign(entity, { ...prismaUser, role: prismaUser.role as UserRole });
  return entity;
}

@Injectable()
export class PrismaUserRepository implements IUserRepository {
  constructor(private readonly prisma: PrismaService) {}

  async findByEmail(email: string): Promise<UserEntity | null> {
    const user = await this.prisma.users.findUnique({ where: { email } });
    return user ? mapToUserEntity(user) : null;
  }

  // Transacciones multi-tabla:
  async createInternalUser(data: CreateInternalUserData): Promise<UserEntity> {
    return this.prisma.$transaction(async (tx) => {
      const user = await tx.users.create({ data: { ... } });
      await tx.profiles.create({ data: { ...data.profile, userId: user.id } });
      return mapToUserEntity(user);
    });
  }

  // Paginación estándar:
  async findAllPaginated(params: PaginationParams): Promise<PaginatedResult<T>> {
    const { limit, offset, searchValue, orderBy, orderByMode } = params;
    const where = { deleted: false, ...(searchValue && { OR: [...] }) };

    const [rows, count] = await Promise.all([
      this.prisma.modelo.findMany({ where, skip: offset, take: limit, orderBy: { ... } }),
      this.prisma.modelo.count({ where }),
    ]);

    return {
      totalRows: count,
      rows: rows.map(mapToEntity),
      totalPages: Math.ceil(count / limit),
      currentPage: Math.floor(offset / limit) + 1,
    };
  }

  // Soft Delete:
  async softDelete(id: number): Promise<void> {
    await this.prisma.modelo.update({
      where: { id },
      data: { deleted: true, updatedAt: new Date() },
    });
  }
}
```

> **Convención**:
> - Usa `$transaction` con callback para operaciones multi-tabla.
> - Paginación devuelve `{ totalRows, rows, totalPages, currentPage }`.
> - Soft delete en lugar de eliminación real (`deleted: true`).
> - Helper functions `mapTo*()` fuera de la clase para transformar datos de Prisma a Entity.

---

### 4. 🎯 Use Case (Aplicación)

Cada operación es un caso de uso independiente:

```typescript
// src/modules/{modulo}/application/use-cases/{accion}.use-case.ts
import { Injectable, Inject, ConflictException, NotFoundException } from '@nestjs/common';
import type { IUserRepository } from '../../domain/repositories/user.repository.js';

@Injectable()
export class CreateUserUseCase {
  constructor(
    @Inject('IUserRepository')
    private readonly userRepository: IUserRepository,
    @Inject('IPasswordService')             // Otros servicios inyectados por token
    private readonly passwordService: IPasswordService,
  ) {}

  async execute(dto: CreateUserDto): Promise<UserResponseDto> {
    // 1. Validaciones de negocio
    const exists = await this.userRepository.existsByEmail(dto.email);
    if (exists) throw new ConflictException('El email ya está registrado');

    // 2. Lógica de dominio
    const hashedPassword = await this.passwordService.hash(dto.password);

    // 3. Persistencia
    const user = await this.userRepository.createInternalUser({ ...dto, password: hashedPassword });

    // 4. Mapear respuesta (sin password)
    return { id: user.id, name: user.name, email: user.email, role: user.role };
  }
}
```

> **Convención**:
> - Un archivo = un caso de uso.
> - Inyecta repositorios con `@Inject('INombreRepository')` usando `type import`.
> - Lanza excepciones HTTP de NestJS directamente (`ConflictException`, `NotFoundException`, etc.).
> - El método principal siempre se llama `execute()`.

---

### 5. 📋 DTO (Aplicación)

Con validación y documentación Swagger:

```typescript
// src/modules/{modulo}/application/dto/create-*.dto.ts
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsEmail, IsEnum, IsNotEmpty, IsOptional, IsString, MinLength, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateUserDto {
  @ApiProperty({ example: 'Juan Pérez' })
  @IsString()
  @IsNotEmpty({ message: 'El nombre es obligatorio' })
  name: string;

  @ApiProperty({ example: 'juan@ejemplo.com' })
  @IsEmail({}, { message: 'El email debe tener un formato válido' })
  @IsNotEmpty({ message: 'El email es obligatorio' })
  email: string;

  @ApiProperty({ example: 'Password123!' })
  @IsString()
  @MinLength(6, { message: 'La contraseña debe tener al menos 6 caracteres' })
  password: string;

  // Para DTOs anidados:
  @ApiProperty({ type: ProfileDto })
  @ValidateNested()
  @Type(() => ProfileDto)
  profile: ProfileDto;
}

// Response DTO (sin decoradores de validación):
export class UserResponseDto {
  @ApiProperty() id: number;
  @ApiProperty() name: string;
  @ApiProperty() email: string;
  @ApiProperty() role: string;
}

// DTO de paginación para Query params:
export class FindAllDto {
  @ApiPropertyOptional() @IsOptional() @IsString() searchValue?: string;
  @ApiPropertyOptional({ default: 1 }) @IsOptional() currentPage?: number;
  @ApiPropertyOptional({ default: 10 }) @IsOptional() pageSize?: number;
  @ApiPropertyOptional() @IsOptional() @IsString() orderBy?: string;
  @ApiPropertyOptional() @IsOptional() @IsString() orderByMode?: string;
}
```

> **Convención**:
> - Mensajes de validación en español.
> - `@ApiProperty()` en todos los campos para Swagger.
> - Campos opcionales usan `@ApiPropertyOptional()` + `@IsOptional()`.
> - DTOs anidados usan `@ValidateNested()` + `@Type(() => SubDto)`.

---

### 6. 🌐 Controller (Interfaz)

Endpoints REST con decoradores de seguridad y Swagger:

```typescript
// src/modules/{modulo}/interfaces/controllers/{nombre}.controller.ts
import { Controller, Post, Get, Patch, Delete, Body, Param, Query, HttpCode, HttpStatus, ParseIntPipe } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { Auth } from '../../../../shared/decorators/index.js';
import { UserRole } from '../../../../shared/domain/enums/user-role.enum.js';

@ApiTags('NombreModulo')
@Controller('nombre-modulo')
export class NombreController {
  constructor(
    private readonly createUseCase: CreateUseCase,
    private readonly findAllUseCase: FindAllUseCase,
    private readonly findByIdUseCase: FindByIdUseCase,
    private readonly updateUseCase: UpdateUseCase,
    private readonly deleteUseCase: DeleteUseCase,
  ) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @Auth(UserRole.ADMIN)                    // Decorador combinado: JwtGuard + RolesGuard
  @ApiOperation({ summary: 'Crear recurso' })
  @ApiResponse({ status: 201, description: 'Creado exitosamente', type: ResponseDto })
  @ApiResponse({ status: 401, description: 'No autenticado' })
  @ApiResponse({ status: 403, description: 'No tiene permisos' })
  async create(@Body() dto: CreateDto): Promise<ResponseDto> {
    return this.createUseCase.execute(dto);
  }

  @Get()
  @Auth(UserRole.ADMIN, UserRole.RECEPTIONIST)   // Múltiples roles permitidos
  @ApiOperation({ summary: 'Listar con paginación' })
  async findAll(@Query() dto: FindAllDto): Promise<PaginatedResponseDto> {
    const pagination = new PaginationImproved(dto.searchValue, dto.currentPage, dto.pageSize);
    return this.findAllUseCase.execute(pagination);
  }

  @Get(':id')
  @Auth(UserRole.ADMIN)
  async findById(@Param('id', ParseIntPipe) id: number): Promise<ResponseDto> {
    return this.findByIdUseCase.execute(id);
  }

  @Patch(':id')
  @Auth(UserRole.ADMIN)
  async update(@Param('id', ParseIntPipe) id: number, @Body() dto: UpdateDto): Promise<ResponseDto> {
    return this.updateUseCase.execute(id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  @Auth(UserRole.ADMIN)
  async remove(@Param('id', ParseIntPipe) id: number): Promise<void> {
    return this.deleteUseCase.execute(id);
  }
}
```

> **Convención**:
> - `@ApiTags()` agrupa endpoints en Swagger.
> - `@Auth(...roles)` = `@UseGuards(JwtAuthGuard, RolesGuard)` + `@Roles(...)` + `@ApiBearerAuth()`.
> - IDs de rutas se parsean con `ParseIntPipe`.
> - Delete retorna `204 No Content`.

---

### 7. 🔗 Module (Aplicación)

Wiring de la inyección de dependencias:

```typescript
// src/modules/{modulo}/application/{nombre}.module.ts
import { Module, forwardRef } from '@nestjs/common';

@Module({
  imports: [forwardRef(() => OtroModule)],    // forwardRef para dependencias circulares
  controllers: [NombreController],
  providers: [
    {
      provide: 'INombreRepository',            // Token de inyección (string)
      useClass: PrismaNombreRepository,        // Implementación concreta
    },
    CreateUseCase,
    FindAllUseCase,
    FindByIdUseCase,
    UpdateUseCase,
    DeleteUseCase,
  ],
  exports: ['INombreRepository'],              // Exportar para uso en otros módulos
})
export class NombreModule {}
```

> **Convención**:
> - Repositorios se registran con `provide: 'INombreRepository'` / `useClass: PrismaNombreRepository`.
> - Use Cases se registran directamente como providers.
> - `forwardRef()` para resolver dependencias circulares entre módulos.

---

## 🔐 Módulo de Autenticación

### Estructura

```
src/modules/auth/
├── application/
│   ├── auth.module.ts
│   ├── dto/
│   │   ├── login.dto.ts
│   │   ├── auth-response.dto.ts
│   │   ├── refresh-token.dto.ts
│   │   ├── logout.dto.ts
│   │   └── update-profile.dto.ts
│   └── use-cases/
│       ├── login.use-case.ts
│       ├── refresh-token.use-case.ts
│       ├── logout.use-case.ts
│       ├── logout-all-devices.use-case.ts
│       ├── get-profile.use-case.ts
│       └── update-profile.use-case.ts
├── domain/
│   ├── contracts/
│   │   ├── refresh-token-repository.interface.ts
│   │   └── token-service.interface.ts
│   ├── entities/
│   │   └── auth-tokens.entity.ts
│   └── interfaces/
│       ├── jwt-payload.interface.ts
│       └── refresh-token-data.interface.ts
├── infrastructure/
│   ├── repositories/
│   │   └── redis-refresh-token.repository.ts     # Refresh tokens en Redis
│   ├── services/
│   │   ├── password.service.ts                   # bcrypt hash/compare
│   │   └── token.service.ts                      # JWT sign/verify
│   └── strategies/
│       └── jwt.strategy.ts                       # Passport JWT Strategy
└── interfaces/
    └── controllers/
        └── auth.controller.ts
```

### Flujo de Auth

1. **Login**: Email + Password → Valida usuario activo → bcrypt compare → Genera access + refresh tokens → Guarda refresh en Redis → Retorna tokens en cookies
2. **JWT Strategy**: Extrae token de cookies (`accessToken`) O del header `Authorization: Bearer <token>` → Valida y decodifica → Retorna `{ id, email, role }` en `request.user`
3. **Refresh**: Usa refresh token para obtener nuevo access token
4. **Logout**: Invalida refresh token en Redis

### Tokens de Inyección del Auth Module

```typescript
// Auth module registra estos tokens:
{ provide: 'IPasswordService', useClass: PasswordService }       // bcrypt
{ provide: 'ITokenService', useClass: TokenService }             // JWT
{ provide: 'IRefreshTokenRepository', useClass: RedisRefreshTokenRepository }

// Auth module exporta:
exports: ['IPasswordService', 'ITokenService']
```

---

## 🛡️ Shared Layer (Código Compartido)

### Decoradores

```typescript
// src/shared/decorators/auth.decorator.ts — Decorador combinado
export function Auth(...roles: UserRole[]) {
  return applyDecorators(
    Roles(...roles),
    UseGuards(AuthGuard('jwt'), RolesGuard),
    ApiBearerAuth(),
  );
}

// src/shared/decorators/current-user.decorator.ts — Extraer usuario del JWT
// src/shared/decorators/roles.decorator.ts — Metadata de roles
```

### Guards

```typescript
// src/shared/guards/roles.guard.ts — Valida roles del JWT
@Injectable()
export class RolesGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<UserRole[]>(ROLES_KEY, [...]);
    if (!requiredRoles || requiredRoles.length === 0) return true;
    const user = request.user;
    if (!user || !requiredRoles.includes(user.role)) throw new ForbiddenException();
    return true;
  }
}
```

### Interfaces Compartidas

```typescript
// src/shared/domain/interfaces/paginated-result.interface.ts
export interface PaginatedResult<T> {
  totalRows: number;
  rows: T[];
  totalPages: number;
  currentPage: number;
}

// src/shared/domain/interfaces/pagination-params.interface.ts
export interface PaginationParams {
  offset: number;
  limit: number;
  searchValue?: string;
  orderBy?: string;
  orderByMode?: string;
}
```

### Paginación Value Object

```typescript
// src/shared/utils/value-objects/pagination-improved.value-object.ts
export class PaginationImproved {
  constructor(
    public readonly searchValue?: string,
    public readonly currentPage: number = 1,
    public readonly pageSize: number = 10,
    public readonly orderBy?: string,
    public readonly orderByMode?: string,
  ) {}

  getOffsetLimit(): { limit: number; offset: number } { ... }
  formatResponse<T>(data: { rows: T[]; count: number }): PaginatedResult<T> { ... }
  getOrderBy(defaultField: string = 'id'): { [key: string]: string } { ... }
  hasSearch(): boolean { ... }
}
```

### Enums Compartidos

```typescript
// src/shared/domain/enums/user-role.enum.ts
export enum UserRole { ADMIN, DOCTOR, PATIENT, RECEPTIONIST, USER }

// Para tu nuevo proyecto, adapta los roles:
// export enum UserRole { ADMIN, MANAGER, RECEPTIONIST, HOUSEKEEPING, GUEST }
```

---

## 🗄️ Prisma ORM

### PrismaService

```typescript
// src/prisma/prisma.service.ts
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  constructor() {
    const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
    const adapter = new PrismaPg(pool);
    super({ adapter });          // Usa @prisma/adapter-pg
  }
  async onModuleInit() { await this.$connect(); }
  async onModuleDestroy() { await this.$disconnect(); }
}
```

> **Nota**: Se usa el adaptador `@prisma/adapter-pg` con `pg.Pool` en lugar de la conexión directa de Prisma.

### Convenciones del Schema

```prisma
// Nombres de modelos: PascalCase plural (Users, Profiles, Appointments)
// Campos comunes en TODOS los modelos:
model MiModelo {
  id        Int      @id @default(autoincrement())
  // ... campos del modelo ...
  isActive  Boolean  @default(true)      // Estado lógico
  deleted   Boolean  @default(false)     // Soft delete
  createdAt DateTime @default(now())     // Auditoría
  updatedAt DateTime?                    // Auditoría

  @@index([campo_frecuente])             // Índices para consultas frecuentes
}
```

### Seed Script

```javascript
// prisma/seed.js — Crea usuario admin inicial
// Usa pg.Pool directamente (no Prisma Client) + bcrypt para hash
const hashedPassword = await bcrypt.hash('123456', 10);
await pool.query(
  `INSERT INTO "Users" (...) VALUES ($1, $2, ...) RETURNING id, email, role`,
  ['admin', 'admin@sistema.com', hashedPassword, 'ADMIN', true, true, false]
);
```

---

## 🐳 Docker Compose

```yaml
services:
  postgres:
    image: postgres:17-alpine
    container_name: proyecto-db
    restart: unless-stopped
    ports:
      - "5435:5432"         # Puerto externo → interno
    environment:
      POSTGRES_USER: miproyecto
      POSTGRES_PASSWORD: 123456
      POSTGRES_DB: miproyecto
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: proyecto-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

---

## ⚙️ Configuración Global (main.ts)

```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // CORS con credenciales (cookies)
  app.enableCors({
    origin: process.env.CLIENT_URL ?? 'http://localhost:3000',
    credentials: true,
  });

  // Cookie parser para auth
  app.use(cookieParser());

  // Validación global
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,              // Elimina campos no declarados en DTO
    forbidNonWhitelisted: true,   // Error si envían campos extra
    transform: true,              // Auto-transforma tipos (string→number, etc.)
  }));

  // Swagger
  const config = new DocumentBuilder()
    .setTitle('Mi API')
    .setDescription('Descripción del sistema')
    .setVersion('1.0')
    .addBearerAuth()
    .addCookieAuth('accessToken')
    .addCookieAuth('refreshToken')
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);

  await app.listen(process.env.PORT ?? 5100);
}
```

---

## 🔑 Variables de Entorno (.env)

```env
# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5435/miproyecto

# JWT
JWT_SECRET=tu-secreto-aqui
JWT_EXPIRES_IN=15m
JWT_REFRESH_SECRET=otro-secreto
JWT_REFRESH_EXPIRES_IN=7d

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# App
PORT=5100
CLIENT_URL=http://localhost:3000
```

---

## 📦 Scripts de Package.json

```json
{
  "scripts": {
    "build": "nest build",
    "start": "nest start",
    "start:dev": "nest start --watch",
    "start:debug": "nest start --debug --watch",
    "start:prod": "node dist/main",
    "prisma:generate": "prisma generate",
    "prisma:migrate": "prisma migrate dev",
    "lint": "eslint \"{src,apps,libs,test}/**/*.ts\" --fix",
    "format": "prettier --write \"src/**/*.ts\""
  }
}
```

---

## 🚀 Checklist para Nuevo Proyecto

### 1. Setup Inicial
- [ ] Crear proyecto NestJS: `npx -y @nestjs/cli@latest new ./`
- [ ] Instalar dependencias: `pnpm add @nestjs/config @nestjs/swagger @nestjs/jwt @nestjs/passport passport passport-jwt @prisma/client @prisma/adapter-pg pg bcrypt class-transformer class-validator cookie-parser ioredis rxjs`
- [ ] Dev deps: `pnpm add -D prisma @types/bcrypt @types/cookie-parser @types/passport-jwt @types/pg`
- [ ] Crear `docker-compose.yml` con PostgreSQL + Redis
- [ ] Crear `.env` con todas las variables
- [ ] Inicializar Prisma: `npx prisma init`

### 2. Shared Layer
- [ ] Crear `src/prisma/prisma.service.ts` y `prisma.module.ts`
- [ ] Crear `src/shared/redis/redis.service.ts` y `redis.module.ts`
- [ ] Crear `src/shared/domain/enums/user-role.enum.ts` con roles del nuevo dominio
- [ ] Crear `src/shared/domain/interfaces/` (PaginatedResult, PaginationParams)
- [ ] Crear `src/shared/utils/value-objects/pagination-improved.value-object.ts`
- [ ] Crear `src/shared/decorators/` (Auth, Roles, CurrentUser)
- [ ] Crear `src/shared/guards/roles.guard.ts`
- [ ] Crear `src/shared/constants/roles.constant.ts`

### 3. Auth Module
- [ ] Crear módulo Auth siguiendo la estructura documentada
- [ ] Implementar PasswordService (bcrypt)
- [ ] Implementar TokenService (JWT)
- [ ] Implementar RedisRefreshTokenRepository
- [ ] Implementar JwtStrategy (Passport)
- [ ] Crear LoginUseCase, RefreshTokenUseCase, LogoutUseCase
- [ ] Crear AuthController con endpoints: POST /login, POST /refresh, POST /logout

### 4. Users Module
- [ ] Crear módulo Users siguiendo la estructura DDD
- [ ] Definir UserEntity, IUserRepository, PrismaUserRepository
- [ ] Crear CRUD use cases
- [ ] Crear DTOs con validación y Swagger
- [ ] Crear UsersController

### 5. Módulos de Dominio
- [ ] Por cada módulo de tu negocio, replicar la estructura DDD:
  - [ ] Entity → Repository Interface → Prisma Repository
  - [ ] DTOs → Use Cases → Controller → Module

### 6. Configuración Final
- [ ] Configurar `main.ts` (CORS, ValidationPipe, Swagger, cookies)
- [ ] Registrar todos los módulos en `app.module.ts`
- [ ] Crear schema.prisma con modelos del dominio
- [ ] Crear seed.js para usuario admin
- [ ] Ejecutar: `docker compose up -d` → `npx prisma migrate dev` → `node prisma/seed.js`

---

### Roles
```typescript
export enum UserRole { ADMIN, MANAGER, RECEPTIONIST, HOUSEKEEPING, GUEST }
```

## ⚠️ Reglas Importantes

1. **Imports con `.js`**: Todos los imports relativos deben terminar en `.js` (requerido por el módulo ESM de NestJS)
2. **`type import`** para interfaces de repositorio en use-cases: `import type { IRepo } from '...'`
3. **No poner lógica de negocio en controllers** — solo en use-cases
4. **No poner lógica de persistencia en use-cases** — solo en repositorios
5. **Soft delete** como estándar (`deleted: true`), nunca `DELETE` real
6. **`@Inject('IToken')`** para inyectar dependencias por token string
7. **Swagger obligatorio** en todos los endpoints con `@ApiTags`, `@ApiOperation`, `@ApiResponse`
8. **ValidationPipe global** — no necesitas `@UsePipes()` en cada controller