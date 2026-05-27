---
name: fix-developer
description: >
  Resuelve bugs, ajustes visuales, refactors y mejoras de comportamiento en el proyecto.
  Usa esta skill SIEMPRE que el usuario mencione fix, bug, error, no funciona, arreglar, corregir, ajustar, modificar comportamiento,
  o cuando describa algo que no está funcionando como se espera o quiere cambiar algo puntual del código existente.
  La skill entiende el problema, analiza el impacto, propone la solución mínima necesaria, espera confirmación y recién implementa.
---

# Fix Developer

Toma un bug o modificación reportada por el desarrollador y lo resuelve de forma quirúrgica: entiende el problema, analiza el código y el impacto, propone la solución mínima, espera confirmación e implementa manteniendo los lineamientos del proyecto.

---

## Reglas de eficiencia (NO negociables)

Estas reglas tienen prioridad sobre cualquier otra instrucción del flujo.

- **Un archivo, una lectura.** Si necesitás distintas partes de un archivo, leelo completo en una sola llamada. Nunca en rangos separados.
- **Máximo 2 archivos leídos para analizar el problema.** El archivo donde ocurre el error + el archivo donde se integra o consume (si aplica). Si con eso no alcanza, leer un tercero y justificarlo.
- **No usar glob patterns.** Ir directamente al archivo por su ruta. Si no se conoce la ruta exacta, preguntar al desarrollador antes de explorar.
- **No releer después de editar.** Si el `str_replace` fue exitoso, asumir que está bien. No verificar releyendo.
- **Usar `str_replace` quirúrgico.** Solo el contexto mínimo necesario para que el reemplazo sea único. No reescribir archivos completos salvo que el fix lo requiera.
- **No leer archivos para "entender el contexto general".** Leer solo lo necesario para resolver el problema concreto reportado.

---

## Flujo de trabajo

### Paso 1 — Entender el problema

Leer con atención lo que describió el desarrollador. Puede ser:
- Un **bug**: algo que falla, un error en consola, un comportamiento inesperado
- Un **ajuste visual**: algo que no se ve como debería
- Un **refactor**: reorganizar o limpiar código sin cambiar comportamiento
- Una **mejora de comportamiento**: algo que funciona pero debería funcionar diferente

Repetirle al desarrollador lo que se entendió:

> **🔍 Entendí lo siguiente:**
>
> **Tipo:** Bug | Ajuste visual | Refactor | Mejora de comportamiento
>
> **Problema:** {describir en 1-3 oraciones qué está pasando o qué se quiere cambiar}
>
> **Dónde ocurre:** {componente, página, endpoint o área del sistema afectada}
>
> **Comportamiento actual:** {qué hace hoy}
>
> **Comportamiento esperado:** {qué debería hacer}
>
> ¿Es correcto esto, o hay algo que no entendí bien?

Esperar confirmación antes de continuar. Si el desarrollador corrige algo, actualizar el entendimiento y confirmar nuevamente.

---

### Paso 2 — Analizar el código (máximo 2 lecturas)

Una vez confirmado el entendimiento, leer ÚNICAMENTE:

1. El archivo donde ocurre el problema
2. El archivo donde se integra o consume ese código (si la causa raíz podría estar ahí)

**STOP.** Con eso identificar:

- **Causa raíz**: por qué está pasando, no solo dónde
- **Contexto relevante**: imports, estado, props, llamadas a servicios que afectan el comportamiento
- **Convenciones del proyecto**: el fix debe seguirlas sin excepción

Si después de leer esos 2 archivos la causa raíz no es clara, leer un tercero y mencionárselo al desarrollador antes de hacerlo.

---

### Paso 3 — Análisis de impacto

Antes de proponer la solución, identificar qué otros archivos o flujos podrían verse afectados.

**Preguntas a responder** (sin leer más archivos — inferir del código ya leído):

- ¿Este código es usado en otros lugares del proyecto?
- ¿El cambio puede alterar el comportamiento de algo que hoy funciona correctamente?
- ¿Hay efectos secundarios posibles?

**Análisis de impacto en clientes existentes en producción:**

Verificar si el cambio puede romper la app para clientes que ya están deployados. Revisar estos casos:

| # | Caso | Remedio obligatorio |
|---|------|-------------------|
| 1 | **Campo nuevo en BD sin valor por defecto** | Definir `DEFAULT` en la migración o manejar `null` en código |
| 2 | **Campo nuevo obligatorio (`NOT NULL` sin `DEFAULT`)** | Nunca aplicar sin `DEFAULT` o sin migrar datos existentes primero |
| 3 | **Campo renombrado o eliminado en BD** | Verificar que ningún query activo lo referencie antes de deployar |
| 4 | **Nueva variable de entorno requerida** | Documentar en `.env.example` y agregar error claro al iniciar si falta |
| 5 | **Nueva relación/FK requerida** | Seedear o migrar los datos relacionados para registros existentes |
| 6 | **Nuevo dato de configuración asumido como existente** | Incluir seeder/migración de datos junto con la migración de esquema |
| 7 | **Cambio en contrato de API** | Versionar el endpoint o mantener retrocompatibilidad en el response |

Si se detecta alguno de estos casos, incluirlo explícitamente en la propuesta del Paso 4 con el remedio concreto. No omitir aunque parezca menor.

Clasificar el impacto:

| Nivel | Criterio |
|-------|----------|
| 🟢 **Bajo** | El cambio está aislado, afecta solo el archivo indicado |
| 🟡 **Medio** | Afecta 2-3 archivos o un componente usado en varios lugares |
| 🔴 **Alto** | Afecta lógica central, múltiples módulos o comportamiento global |

**⚠️ Detección de fix grande — derivar a fix-decomposer:**

Si se cumple **cualquiera** de estos criterios, advertir y sugerir `fix-decomposer`:

- 📁 Más de **3 archivos** a modificar
- 🗂️ Afecta **más de 1 módulo** del sistema
- 🗄️ Requiere **cambios en la base de datos**

> ⚠️ **Este fix es más grande de lo que parece.**
>
> Detecté que {criterio detectado}. En lugar de hacer todos los cambios de una vez, te sugiero descomponerlo en porciones más pequeñas y verificables.
>
> ¿Querés que lo descomponga en porciones de fix?

- Si acepta → activar `fix-decomposer`
- Si prefiere continuar → respetar y continuar al Paso 4

---

### Paso 4 — Proponer la solución

Con el análisis completo, presentar la propuesta antes de tocar una sola línea de código:

> **💡 Propuesta de solución:**
>
> **Causa raíz:** {explicar en lenguaje simple por qué está pasando el problema}
>
> **Solución:** {describir qué se va a cambiar y cómo, sin código todavía}
>
> **Archivos a modificar:**
> - `{archivo 1}` — {qué se cambia ahí}
> - `{archivo 2}` — {qué se cambia ahí, si aplica}
>
> **Impacto:** 🟢 Bajo | 🟡 Medio | 🔴 Alto — {breve explicación}
>
> ¿Implementamos?

Esperar confirmación explícita antes de escribir código.

**Regla de oro:** proponer siempre la solución **mínima** que resuelva el problema. No aprovechar el fix para refactorizar otras cosas ni mejorar código cercano no pedido. Si se detecta algo mejorable fuera del scope, mencionarlo como observación al final — nunca tocarlo sin que lo pidan.

---

### Paso 5 — Implementar el fix

Una vez confirmado, implementar con `str_replace` quirúrgico.

**Reglas de implementación:**

- Tocar **solo** los archivos identificados en la propuesta
- Mantener el mismo estilo de código del archivo modificado (indentación, naming, patrones)
- No cambiar funcionalidad que no fue pedida
- Si el impacto es 🟡 medio o 🔴 alto, mencionar explícitamente qué verificar en los archivos relacionados

---

### Paso 6 — Verificación post-fix

> **✅ Fix implementado. Para verificar que quedó resuelto:**
>
> 1. {paso concreto para reproducir el escenario que fallaba}
> 2. {qué debería verse/pasar ahora que está corregido}
>
> {Si aplica: "Además verificá que {flujo relacionado} sigue funcionando correctamente."}
>
> ¿Quedó resuelto, o hay algo más que ajustar?

Si el desarrollador reporta que no quedó resuelto o apareció algo nuevo, volver al Paso 2 con la nueva información.

---

### Paso 7 — Observaciones opcionales

Si durante el análisis se detectaron cosas mejorables fuera del scope, mencionarlas **después** de confirmar que el fix funcionó:

> **📝 Observaciones (fuera del scope de este fix):**
> - {algo mejorable que no fue pedido}
> - {deuda técnica detectada}
>
> ¿Querés que encaremos alguna de estas en un fix aparte?

---

## Reglas generales

- **Nunca implementar antes de la confirmación del Paso 4**
- **Solución mínima siempre** — no refactorizar ni mejorar cosas no pedidas
- **Confirmar entendimiento antes de analizar** — un fix sobre el problema equivocado es peor que no hacer nada
- **Siempre reportar el impacto** — el desarrollador tiene que saber qué más podría verse afectado
- **Verificación explícita** — siempre decir exactamente cómo reproducir el escenario para confirmar que está resuelto
- **Observaciones al final** — si se ve algo mejorable, mencionarlo después del fix, nunca tocarlo sin permiso
- **Seguir las convenciones del proyecto** — el código del fix debe ser indistinguible del resto del código existente
- **Derivar a fix-decomposer cuando corresponde** — si el fix supera los criterios de complejidad, no intentar resolverlo todo de una vez

---

## Relación con otras skills

- **Fix grande**: si el análisis detecta más de 3 archivos, más de 1 módulo afectado o cambios en BD → derivar a `fix-decomposer`
- **Desarrollo de porciones**: las porciones generadas por `fix-decomposer` se desarrollan con `frontend-developer` y `backend-developer`