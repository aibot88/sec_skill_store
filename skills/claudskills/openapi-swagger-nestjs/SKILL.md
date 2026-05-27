---
name: openapi-swagger-nestjs
description: >
  Documentación de APIs REST con OpenAPI 3.0 y Swagger UI en NestJS usando @nestjs/swagger.
  Usar PROACTIVAMENTE cuando se escriban controllers, DTOs, o endpoints que necesiten
  documentación, cuando se configure el módulo Swagger, cuando se añadan decoradores de
  API a propiedades de DTOs, o cuando se genere un contrato OpenAPI para el frontend
  o equipos externos. Activar siempre que aparezcan las palabras clave: Swagger, OpenAPI,
  @ApiProperty, @ApiOperation, @ApiResponse, @ApiTags, @ApiBearerAuth, SwaggerModule,
  DocumentBuilder, @nestjs/swagger, swagger.json, api-docs, documentar endpoint,
  contrato de API, o schema de respuesta.
---

# OpenAPI / Swagger en NestJS — Documentación de API HADA

Guía completa para documentar la API REST de HADA con OpenAPI 3.0 y Swagger UI
usando `@nestjs/swagger`. Cubre configuración, decoradores en controllers y DTOs,
seguridad JWT, y generación del contrato OpenAPI para el equipo de frontend móvil.

## Referencias disponibles

- `references/setup.md` — Instalación, SwaggerModule, DocumentBuilder, entornos
- `references/decorators.md` — Todos los decoradores: @ApiTags, @ApiOperation, @ApiResponse, @ApiProperty
- `references/dtos.md` — DTOs documentados de los módulos principales de HADA
- `references/security.md` — @ApiBearerAuth, esquema JWT en Swagger UI

---

## Cuándo usar cada referencia

| Tarea                                   | Referencia      |
| --------------------------------------- | --------------- |
| Configurar Swagger por primera vez      | `setup.md`      |
| Documentar un controller o endpoint     | `decorators.md` |
| Documentar DTOs de request/response     | `dtos.md`       |
| Configurar autenticación JWT en Swagger | `security.md`   |

---

## Reglas críticas (siempre en contexto)

### 1. Todo endpoint del MVP debe estar documentado — es entregable obligatorio

```typescript
// ✅ Mínimo requerido por endpoint
@ApiOperation({ summary: 'Reservar un regalo' })
@ApiResponse({ status: 200, type: ReserveGiftResponseDto })
@ApiResponse({ status: 403, description: 'No perteneces al círculo de esta lista' })
@ApiResponse({ status: 409, description: 'El regalo ya está reservado' })
```

### 2. Todos los DTOs de respuesta deben tener @ApiProperty en sus campos

```typescript
// ✅ DTO documentado
export class GiftStatusResponseDto {
  @ApiProperty({ example: 'uuid-gift-123' })
  giftId: string;

  @ApiProperty({ enum: ['AVAILABLE', 'RESERVED', 'RECEIVED'] })
  estado: GiftStatus;
  // ⚠️ NUNCA añadir reservedById aquí — invariante de privacidad
}
```

### 3. @ApiHideProperty para campos que NUNCA deben exponerse en el contrato

```typescript
export class InternalReservationDto {
  @ApiHideProperty()  // ← No aparece en Swagger ni en el contrato OpenAPI
  reservedById: string;
}
```

### 4. Generar el JSON del contrato en CI para que el equipo móvil lo consuma

```typescript
// scripts/generate-openapi.ts
const app = await NestFactory.create(AppModule);
const document = SwaggerModule.createDocument(app, config);
writeFileSync('./docs/openapi.json', JSON.stringify(document, null, 2));
```

---

## Fuentes y documentación oficial

- **@nestjs/swagger Docs**: https://docs.nestjs.com/openapi/introduction
- **NestJS OpenAPI — Decorators**: https://docs.nestjs.com/openapi/decorators
- **NestJS OpenAPI — Types and Parameters**: https://docs.nestjs.com/openapi/types-and-parameters
- **NestJS OpenAPI — Security**: https://docs.nestjs.com/openapi/security
- **OpenAPI 3.0 Specification**: https://swagger.io/specification/
- **Swagger UI**: https://swagger.io/tools/swagger-ui/
