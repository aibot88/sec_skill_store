---
name: fix-decomposer
description: >
  Descompone un fix grande en porciones atomicas cuando el cambio es demasiado amplio para resolverse de una sola vez.
  Usa esta skill SIEMPRE que la skill fix-developer detecte que un fix supera los criterios de complejidad,
  o cuando el usuario mencione descomponer un fix, dividir un fix en partes, crear porciones de fix, o fix grande.
  La skill advierte al desarrollador, descompone el fix en porciones Front/Back, incluye una porcion de verificacion de regresion,
  y guarda todo en una carpeta de documentacion del modulo afectado.
---

# Fix Decomposer

Cuando un fix es demasiado grande para resolverse de forma quirúrgica, esta skill lo descompone en porciones atómicas documentadas, organizadas para ser desarrolladas con las skills de frontend-developer y backend-developer.

---

## Criterios para activar esta skill

Un fix se considera **grande** y debe descomponerse en porciones cuando cumple **al menos uno** de estos criterios:

- 📁 **Más de 3 archivos** a modificar
- 🗂️ **Afecta más de 1 módulo** del sistema
- 🗄️ **Requiere cambios en la base de datos** (migraciones, nuevos campos, nuevas tablas)

Cuando fix-developer detecta esto durante su análisis de impacto, debe pausar y derivar a esta skill:

> ⚠️ **Este fix es más grande de lo que parece.**
>
> Detecté que requiere {criterio/s que se cumplen: ej. modificar 5 archivos en 2 módulos distintos}. Encararlo como un fix simple tiene riesgo de introducir errores difíciles de rastrear.
>
> Te sugiero descomponerlo en porciones para resolverlo de forma ordenada y documentada. ¿Querés que lo descomponga?

Si el desarrollador acepta, continuar con el flujo de esta skill. Si prefiere seguir con el fix simple de todas formas, respetar la decisión y continuar con fix-developer.

---

## Formato de cada porción de fix

Cada porción se guarda como un archivo `.md` individual.

**Ruta:** `docs/historias-de-usuario/{modulo}-fix/porcion-{NNN}.md`

El nombre de la carpeta usa el nombre del módulo afectado en kebab-case seguido de `-fix`. Ejemplos: `modulo-operaciones-fix/`, `modulo-auth-fix/`, `modulo-stock-fix/`.

```markdown
# porcion-{NNN} — {Título descriptivo} [{FRONT|BACK|FRONT+BACK}]

**Módulo:** {nombre del módulo afectado}
**Tipo de porción:** Fix
**Porción original:** porcion-{NNN} *(porción de desarrollo que se está corrigiendo, si aplica. Si el fix no corrige una porción específica sino comportamiento general, escribir "N/A")*
**Par:** porcion-{NNN} *(si tiene par Front/Back, indicar el número. Si no tiene par, omitir)*
**Prerequisitos:** porcion-{NNN}, porcion-{NNN} *(porciones de fix que deben completarse antes. Si no hay, escribir "Ninguno")*

## Descripción

{Qué se implementa en esta porción, en el lenguaje más sencillo posible.}

## Estado actual vs estado esperado

**Hoy:** {qué hace o muestra actualmente — el comportamiento incorrecto}
**Debería:** {qué debería hacer o mostrar una vez aplicado el fix}

## Criterios de aceptación

- [ ] {criterio 1}
- [ ] {criterio 2}
- [ ] {criterio 3}
- [ ] El componente es responsive y se visualiza correctamente en mobile, tablet y desktop *(solo para porciones FRONT)*

## Pruebas

### Pruebas unitarias

- [ ] {prueba 1: qué se prueba y qué resultado se espera}
- [ ] {prueba 2}

### Pruebas de integración

- [ ] {prueba 1: qué interacción entre componentes/servicios se prueba y qué se espera}
- [ ] {prueba 2}
```

---

## Formato de la porción de regresión

La última porción de todo fix descompuesto es siempre una porción de **verificación de regresión**. No tiene desarrollo — es una checklist de pasos manuales que el dev ejecuta después de completar todas las porciones de fix para confirmar que nada se rompió.

```markdown
# porcion-{NNN} — Verificación de regresión [REGRESION]

**Módulo:** {nombre del módulo afectado}
**Tipo de porción:** Regresión
**Porción original:** N/A
**Prerequisitos:** todas las porciones de fix anteriores

## Descripción

Verificación manual de que el fix no introdujo nuevos errores en los flujos existentes del módulo {nombre}.

## Pasos de verificación

### Flujos del módulo afectado

1. {paso concreto: qué hacer y qué debería verse/pasar si está bien}
2. {paso concreto}
3. {paso concreto}

### Flujos de módulos relacionados *(si el fix tocó más de un módulo)*

1. {paso concreto en el módulo secundario afectado}
2. {paso concreto}

### Verificación de base de datos *(si el fix incluyó migraciones)*

1. {qué tabla/campo verificar y qué valor o estructura se espera encontrar}

## Resultado esperado

Si todos los pasos anteriores se comportan correctamente, el fix está completo y no introdujo regresiones.

**Una vez verificado, marcar esta porción como completada.**
```

---

## Flujo de trabajo

### Paso 1 — Analizar el fix y el proyecto

Leer el problema reportado y explorar el código afectado para entender:

- Qué módulos y archivos están involucrados
- Si requiere cambios en la BD
- Si hay porciones de desarrollo originales que se están corrigiendo (buscar en `docs/historias-de-usuario/` las porciones relacionadas)
- El orden lógico de resolución: qué debe arreglarse primero para que lo siguiente funcione

**Criterio FRONT vs BACK:** igual que en story-decomposer — el criterio es dónde se ejecuta el código, no si es visual. Contextos, hooks, layouts y stores son siempre FRONT aunque sean infraestructura.

---

### Paso 2 — Proponer el plan de porciones

Antes de generar los archivos, presentar el plan al desarrollador para que lo valide:

> **🔧 Propongo descomponer este fix en {N} porciones:**
>
> | # | Porción | Tipo | Par | Porción original | Prerequisitos |
> |---|---------|------|-----|-----------------|---------------|
> | porcion-001 | {título} | FRONT | porcion-002 | porcion-003 | Ninguno |
> | porcion-002 | {título} | BACK | porcion-001 | porcion-004 | Ninguno |
> | porcion-003 | {título} | BACK | — | N/A | porcion-002 |
> | porcion-004 | Verificación de regresión | REGRESION | — | N/A | todas |
>
> **Carpeta:** `docs/historias-de-usuario/{modulo}-fix/`
>
> ¿Este desglose tiene sentido? ¿Querés ajustar algo antes de generar los archivos?

Esperar confirmación antes de continuar.

---

### Paso 3 — Preguntar solo lo necesario

Si hay ambigüedades que impidan definir bien una porción, preguntar puntualmente. **Máximo 3 preguntas a la vez.**

---

### Paso 4 — Generar las porciones

Una vez aprobado el plan, generar cada porción siguiendo los formatos definidos arriba.

**Reglas al generar:**

- Descripción en lenguaje simple, comprensible para cualquier miembro del equipo
- El campo "Estado actual vs estado esperado" debe ser concreto y verificable, no genérico
- Criterios de aceptación verificables con Sí/No
- Mínimo 2 pruebas unitarias y 1 de integración por porción (excepto la porción de regresión)
- Edge cases obligatorios: al menos 2 casos borde por porción
- La porción de regresión siempre va última y cubre todos los flujos que podrían haberse afectado

---

### Paso 5 — Guardar los archivos

```bash
# Crear carpeta del fix
mkdir -p docs/historias-de-usuario/{modulo}-fix

# Guardar cada porción
# docs/historias-de-usuario/{modulo}-fix/porcion-001.md
# docs/historias-de-usuario/{modulo}-fix/porcion-002.md
# ...
# docs/historias-de-usuario/{modulo}-fix/porcion-00N.md  <- regresión siempre última
```

Confirmar al desarrollador:

> ✅ Generadas {N} porciones en `docs/historias-de-usuario/{modulo}-fix/`:
> - porcion-001.md — {título}
> - porcion-002.md — {título}
> - porcion-00N.md — Verificación de regresión
>
> Para desarrollar cada porción usá las skills **frontend-developer** y **backend-developer** en el orden sugerido.

---

## Reglas generales

- **La porción de regresión es obligatoria** — todo fix descompuesto termina con una porción de regresión, sin excepción
- **La regresión no tiene desarrollo** — es solo verificación manual, no se implementa código
- **Referencia a porción original siempre** — si el fix corrige algo desarrollado en una porción específica, debe quedar referenciado. Si no aplica, escribir "N/A"
- **Numeración desde 001** dentro de la carpeta del fix, independientemente de las porciones de la HU
- **Criterio FRONT vs BACK** — el código que se ejecuta en el cliente es siempre FRONT, el que se ejecuta en el servidor es siempre BACK
- **Si el dev rechaza descomponer** — respetar la decisión y continuar con fix-developer normalmente

---

## Relación con otras skills

- **Origen**: fix-developer detecta que el fix supera los criterios de complejidad y deriva a esta skill
- **Desarrollo**: una vez generadas las porciones, se desarrollan con **frontend-developer** y **backend-developer**
- **Regresión**: la porción de regresión se ejecuta manualmente por el dev, no requiere ninguna skill de desarrollo