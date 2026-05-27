---
name: ghl-clickup-task-builder
description: Crea tareas y subtareas en ClickUp para implementaciones de GoHighLevel. Usar SIEMPRE que el usuario quiera subir workflows de GHL a ClickUp, registrar tareas de automatización, o cuando el output de ghl-onboarding-mapper necesite convertirse en tareas accionables. También usar cuando el usuario mencione "crear tareas en ClickUp", "subir workflows", "registrar WFs", "cargar implementación en ClickUp", o cuando haya un listado de workflows LS, SP, AP, PS, RP listos para ejecutar. Esta skill es especialista en la anatomía completa de workflows GHL y genera subtareas atómicas ejecutables — 1 subtarea = 1 nodo en el builder de GHL.
---

# GHL ClickUp Task Builder

Transforma workflows de GHL en tareas estructuradas en ClickUp. Cada workflow se convierte en una **tarea padre con contexto completo** + **subtareas atómicas** donde cada subtarea = un nodo en el builder de GHL.

---

## Modos de operación — verificación vs. from-scratch

La skill opera en **dos modos** según el contexto. Detectar el modo antes de empezar.

### Modo A — Cliente existente / Adición a cuenta viva
Cuando se generan tareas para una cuenta GHL ya implementada y la tarea menciona pipelines, campos, asesores o calendarios **que se asume que ya existen**.

**Pre-flight check obligatorio:**

1. **Leer `references/ghl-api-capabilities.md`** — saber qué se puede crear vía API/MCP y qué requiere implementación manual.

2. **Pullear el snapshot vivo** (ver `references/ghl-live-context-template.md`):
   - `mcp__ghl__opportunities_get-pipelines`
   - `mcp__ghl__locations_get-custom-fields`
   - `mcp__ghl__locations_get-location`
   - `GET /users/?locationId=...` (REST)
   - `GET /calendars/?locationId=...` (REST)

3. **Validar cada referencia por nombre contra el snapshot.** Si el input menciona "Pipeline Residencial" o "campo Tipo de Cliente" o "asignar a Carlos", confirmá que existe antes de escribir la subtarea. Si no existe:
   - Avisar al usuario y ofrecer: (A) crear el recurso ahora, (B) corregir el nombre, (C) marcarlo como `⚠️ DEPENDENCIA FALTANTE`.

### Modo B — Cliente nuevo / Implementación desde cero
Cuando se está armando un cliente desde cero, o cuando el usuario pasa un mapeo previo de implementación, o cuando explicita "es un cliente nuevo / desde cero / cliente testeo".

**No hace falta validar que las cosas existan — se crean como parte de la implementación.**

1. **Sí leer `references/ghl-api-capabilities.md`** — para saber cuáles tareas son ejecutables vía API y cuáles son manuales (workflows, funnels, etc.).

2. **No es necesario pullear el snapshot completo.** Como mucho, leer el `locations_get-location` para confirmar timezone si la implementación incluye calendarios o mensajería con horarios.

3. **Pipelines, custom fields, calendarios, stages, tags se crean** como parte de las tareas de implementación. Marcar con `🔧 SETUP` las que se ejecutan vía API antes que el WF.

### Cómo detectar el modo

| Señal | Modo |
|---|---|
| Usuario dice "cliente nuevo", "desde cero", "cliente testeo", "primera implementación", "snapshot inicial" | B |
| Usuario pasa un mapeo o roadmap pre-armado (ej: output de `ghl-onboarding-mapper`) | B |
| Usuario menciona dependencias por nombre y asume que existen | A |
| Usuario dice "agregar al WF existente", "modificar X", "este cliente ya tiene Y" | A |
| Si hay duda → preguntar al usuario antes de empezar | — |

### Clasificación de operaciones (en cualquier modo)

Por cada operación que la tarea propone:
- ✅ **Automatizable vía API/MCP** → puede ejecutarse desde la skill (ahora o en Fase 2)
- 🔧 **SETUP previo** → recursos a crear antes del WF (pipelines, fields, calendarios) — automatizables
- ⚠️ **MANUAL** → workflows, funnels, forms, configuraciones de Conversation AI, integraciones OAuth — el implementador lo arma a mano siguiendo la subtarea

---

## Principio central: 1 subtarea = 1 acción atómica

El nombre de la subtarea ES la instrucción. La descripción tiene **dos secciones fijas y obligatorias**:

- `## Acción en GHL` → qué configurar exactamente (tabla de campos y valores). Esto es lo que el implementador ejecuta.
- `## Contexto` → por qué existe ese nodo, cómo se conecta con otros workflows, qué pasa antes y después. Esto es referencia, no instrucción.

**❌ MAL — subtarea agrupada o sin estructura:**
```
Nombre: ⚡ Acciones
Descripción: ACCIÓN 1 - Update Canal... ACCIÓN 2 - Update Área... ACCIÓN 3 - If/Else...
```

```
Nombre: Guard IF: Fecha de primer contacto está vacía
Descripción: Nodo IF. Si está vacío continúa, si no salta.
(sin separar qué hacer de por qué hacerlo)
```

**✅ BIEN — subtarea atómica con secciones:**
```
Nombre: Guard IF: Fecha de primer contacto está vacía

## Acción en GHL

| Campo GHL       | Valor                          |
|-----------------|-------------------------------|
| Action type     | IF / Else                     |
| Condition object| Contact                       |
| Field           | Fecha de primer contacto      |
| Operator        | is empty                      |
| Rama TRUE       | Continúa → nodo siguiente     |
| Rama FALSE      | Salta al nodo Crear oportunidad|

## Contexto

Protege contra re-entradas. Si el contacto ya existe en el CRM y
vuelve a escribir, este Guard evita pisar su fecha original de primer
contacto. Sin este nodo, los reportes de tiempo de conversión quedan
contaminados con fechas incorrectas.
```

**Regla sobre qué va en cada sección:**

| ¿Qué tipo de contenido? | Sección |
|---|---|
| Tabla de configuración GHL (campos, valores, opciones) | `## Acción en GHL` |
| Paso a paso para encontrar el nodo en la UI | `## Acción en GHL` |
| Por qué existe este nodo | `## Contexto` |
| Qué workflow lo precede o lo sigue | `## Contexto` |
| Qué pasa si no se configura | `## Contexto` |
| Relación con otros WF (SP01, WF08, etc.) | `## Contexto` |
| Diagrama visual del flujo (rama TRUE/FALSE) | `## Contexto` |

---

## Flujo de trabajo

### Paso 1: Recibir el input
- Output de `ghl-onboarding-mapper`, descripción manual, o tarea existente a reescribir
- Si hay ambigüedad, preguntar antes de crear

### Paso 2: Confirmar List ID
Si no se conoce: *"¿List ID de ClickUp? Es el número al final de la URL de la lista."*

### Paso 3: Construir la tarea padre

Nombre: `[LS01] Nombre` o `WF-001 · NOMBRE_CAPS`

Descripción de la tarea padre con estas secciones:
```
Descripción — qué hace, por qué existe
Trigger — nombre exacto + canal/pipeline/etapa
Guards de entrada — IF de detención antes de cualquier acción (si aplica)
Lógica / Branches — resumen de If/Else (si aplica)
Dependencias — qué debe existir antes de activar
Orden de activación — si depende de otro WF activo primero
```

### Paso 4: Descomponer en subtareas atómicas

Un nodo en GHL = una subtarea en ClickUp:

| Nodo GHL | → Subtarea |
|---|---|
| Trigger | `Trigger: [nombre] ([canal/etapa])` |
| Guard IF de detención | `Guard IF: [condición] → STOP` |
| Update Contact/Opportunity Field | `Update Field: [campo] = [valor]` |
| If/Else con branches | `IF: [condición] → [rama TRUE] / [rama FALSE]` |
| Send Message | `Send [WhatsApp/SMS/Email]: "[primeras palabras del mensaje]"` |
| Wait | `Wait: [duración] / Wait Until: [campo fecha]` |
| Add/Remove Tag | `Add Tag: [nombre-tag]` |
| Create Opportunity | `Crear oportunidad → [etapa]` |
| Webhook → n8n | `Webhook → n8n: [nombre_accion]` |
| Assign to User | `Assign to User: [Round Robin / Owner / nombre]` |
| End Workflow | `End Workflow` *(solo si hay múltiples salidas)* |

---

## Guía de UI — Valores exactos por tipo de nodo

Interfaz de GHL en **español**. Usar estos términos exactos.

### Update Contact Field
```
Tipo de acción: "Actualizar datos de campo"
→ Clickeá "Añadir Campo"
→ Dropdown campos: Standard Fields (arriba) / Custom fields (hacer scroll abajo)
→ Seleccionar: [nombre exacto del campo]
→ Valor:
   Dropdown → seleccionar: [valor exacto]
   Text     → escribir: [valor]
   Date     → ícono 🏷️ → Contact Created At (para "now")
```

### If / Else
```
→ Clickeá "Añadir filtros"
→ Tipo: Contacto / Oportunidad
→ Campo: [nombre]
→ Condición: está vacío / es igual a / contiene / no está vacío
→ Valor: [si aplica]
Branch SÍ = condición cumplida
Branch NONE = no cumplida (equivale al Else)
```

### Crear oportunidad (nueva — NO la deprecada)
```
⚠️ "Crear O Actualizar Oportunidad" está DEPRECADA (banner naranja). Usar "Crear oportunidad".
→ IN SECUENCIA → [pipeline]
→ IN SECUENCIA PASO → [etapa exacta]
→ Nombre → ícono 🏷️ → First Name + Last Name
→ Fuente → texto libre: "Widget Web" / "WhatsApp" / "Instagram"
```

### Send Message
```
→ Canal: WhatsApp / SMS / Email
→ Tipo: Template aprobado / Mensaje libre
→ Texto: [mensaje exacto]
→ Usar ícono 🏷️ para insertar nombre: First Name
```

### Wait
```
Wait fijo: duración en días/horas desde ejecución del paso
Wait Until Date: ícono 🏷️ → campo de fecha → + offset si aplica
```

### Add/Remove Tag
```
→ Tag: [nombre exacto, sensible a mayúsculas/minúsculas]
```

### Webhook → n8n
```
→ Acción: Webhook
→ URL: Custom Value con la URL del webhook de n8n
→ Método: POST
→ Body: incluir {{contact.id}} + campos necesarios
```

### Variables con ícono 🏷️

| Valor | Variable |
|---|---|
| Fecha/hora actual | `Contact Created At` |
| Nombre | `First Name` |
| Apellido | `Last Name` |
| Teléfono | `Phone` |
| Email | `Email` |
| UTM Source | `utm_source` *(puede no existir en widget)* |
| UTM Medium | `utm_medium` |
| UTM Campaign | `utm_campaign` |

> ⚠️ **Círculo naranja** en un bloque = campos incompletos. El WF no se puede publicar hasta resolverlos.

---

## Referencias GHL

**Lectura obligatoria al inicio de cualquier sesión** (Pre-flight Check):
- `references/ghl-api-capabilities.md` — qué se puede crear/leer/actualizar vía API/MCP, schemas verificados, gotchas. Distingue automatizable (✅) vs manual (❌).
- `references/ghl-live-context-template.md` — qué snapshot pullear de la cuenta antes de proceder.

**Lectura por tipo de tarea** (capa workflow / UI builder):

| Si vas a generar... | Leer |
|---|---|
| Triggers (Contact Created, Opportunity Stage Changed, Customer Replied, etc.) | `references/ghl-triggers-reference.md` |
| Acciones (Update Field, IF/Else, Send Message, Webhook, Wait, etc.) | `references/ghl-actions-reference.md` |
| Tareas de Conversation AI / Aurora bot | `references/ghl-conversation-ai-reference.md` |
| Limitaciones del builder (variables que no existen, aritmética, días hábiles, etc.) | `references/ghl-limitations.md` |

Para workflows que mezclan triggers + acciones, leer ambos archivos de referencia antes de empezar.

**Distinción importante entre los dos archivos de limitaciones:**
- `ghl-api-capabilities.md` → "¿se puede hacer vía API/MCP?" (capa de automatización)
- `ghl-limitations.md` → "¿GHL lo soporta en absoluto, ni siquiera manualmente?" (capa de producto)

Cuando una funcionalidad **no existe en GHL nativamente**, usar el formato `⚠️ REVISAR` de `ghl-limitations.md`.
Cuando una funcionalidad existe pero **no es automatizable vía API/MCP**, usar `⚠️ MANUAL` con la justificación de `ghl-api-capabilities.md`.

---

## Estructura visual en ClickUp

### Tarea padre — formato de descripción

```markdown
## Descripción
[Qué hace el workflow y la lógica de negocio central. 2-4 líneas.]

## Trigger
[Nombre exacto del trigger + pipeline/canal/etapa si aplica.]

## Pipelines involucrados (si el WF mueve entre pipelines)
| Pipeline | Rol |
|---|---|
| `Nombre pipeline` | Origen / Destino / Temporal |

## Dependencias
- [Qué debe existir creado antes de activar este WF]
- [Otros workflows que deben estar activos primero]

## Estructura de nodos
| # | Tipo de nodo | Nombre de subtarea |
|---|---|---|
| 1 | Trigger | Trigger: ... |
| 2 | Guard IF | Guard IF: ... |
| 3 | Update Field | Update Field: ... |
```

### Subtarea — formato de descripción

Cada subtarea tiene **dos secciones fijas**. Siempre en este orden:

```markdown
## Acción en GHL

| Campo GHL | Valor |
|---|---|
| Action type | [nombre exacto del nodo en GHL] |
| [campo 1] | [valor 1] |
| [campo 2] | [valor 2] |
| Rama TRUE | [qué pasa si se cumple] |
| Rama FALSE | [qué pasa si no se cumple] |

## Contexto

[Por qué existe este nodo. Qué workflow lo precede o lo sigue.
Qué pasa si no se configura. Relación con otros WFs. 2-5 líneas.]
```

**Para nodos IF/Else con dos caminos, agregar diagrama visual al final del Contexto:**
```
¿[condición]?
    ├── SÍ → [acción rama TRUE]
    └── NO → [acción rama FALSE / STOP]
```

---

## Ejemplo completo — [LS01] Widget Chat + UTM Capture

**Tarea padre:**
```markdown
## Descripción
Captura contactos nuevos desde Widget Chat web. Extrae UTMs, clasifica
la fuente y crea la oportunidad inicial en el pipeline.

## Trigger
Contact Created. Sin filtros. Allow re-enrollment: OFF.

## Dependencias
- Pipeline Residencial B2C creado con etapa Contactos Recibidos
- Custom fields: Canal de primer contacto, Área de origen,
  Fecha de primer contacto, UTMs, Tipo de cliente

## Estructura de nodos
| # | Tipo | Subtarea |
|---|---|---|
| 1 | Trigger | Trigger: Contact Created |
| 2 | Update Fields | Update Fields: Canal + Área |
| 3 | Update Fields | Update Fields: UTM Source + Medium + Campaign + Content + Term |
| 4 | Guard IF | Guard IF: Fecha de primer contacto está vacía |
| 5 | Update Field | Update Field: Fecha de primer contacto = now (rama TRUE) |
| 6 | Create Opportunity | Crear oportunidad → Contactos Recibidos |
| 7 | Update Field | Update Field: Tipo de cliente = cliente_final |
| 8 | Assign | Assign to User: Round Robin asesores |
```

**Subtareas (ejemplos con el formato correcto):**

```markdown
── Subtarea: Guard IF: Fecha de primer contacto está vacía

## Acción en GHL

| Campo GHL        | Valor                              |
|------------------|------------------------------------|
| Action type      | IF / Else                          |
| Condition object | Contact                            |
| Field            | Fecha de primer contacto           |
| Operator         | is empty                           |
| Rama TRUE        | Continúa → nodo 5 (setear fecha)   |
| Rama FALSE       | Salta → nodo 6 (Crear oportunidad) |

## Contexto

Protege contra re-entradas. Si el contacto ya existe en el CRM y vuelve
a escribir por el widget, sin este Guard IF se pisaría la fecha original
de primer contacto con la del re-ingreso, contaminando los reportes de
tiempo de conversión.
```

```markdown
── Subtarea: Update Field: Tipo de cliente = cliente_final

## Acción en GHL

| Campo GHL   | Valor          |
|-------------|----------------|
| Action type | Actualizar datos de campo (Update Contact Field) |
| Field       | Tipo de cliente |
| Value       | cliente_final  |

## Contexto

Este campo es el trigger de SP01. Cuando GHL detecta que Tipo de cliente
pasó de vacío a tener un valor, SP01 arranca y asigna el asesor. Sin
este nodo SP01 nunca dispara.

⚠️ **Tipo de cliente es un campo de Contacto**, no de Oportunidad.
Usar "Actualizar datos de campo" (Update Contact Field), no "Update Opportunity Field".
```
