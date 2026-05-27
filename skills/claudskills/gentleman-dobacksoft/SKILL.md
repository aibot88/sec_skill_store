---
name: gentleman-dobacksoft
description: Gentleman.Dots / Gentleman Programming alongside DobackSoft. Tono y jerarquía ya aplican siempre vía .cursor/rules/gentleman-dobacksoft.mdc; esta skill amplía instalación y globs de archivos Gentleman.
globs:
  - docs/DESARROLLO/GENTLEMAN-DOTS-INSTALACION.md
  - scripts/setup/install-gentleman-dots.sh
---

# Gentleman + DobackSoft V3

## Orden de prioridad

| Ámbito | Fuente |
|--------|--------|
| Código backend/frontend, Prisma, API, tenant | **AGENTS.md**, **.cursorrules**, skill **dobacksoft** |
| Entorno local (Neovim, shell, TUI Gentleman) | **Gentleman.Dots** upstream; guía en este repo abajo |

**Nunca** las reglas de dots sustituyen: `api.ts`, `logger` (no `console.log`), `organizationId`, puertos **9998/5174**, inicio con **`iniciar.ps1`** / **`./iniciar.sh`**, menú V3 fijo.

## Cómo debe “responder” el agente

- **Tono:** pair programming claro y directo (línea Gentleman Programming), sin relleno.
- **Código en este repo:** TypeScript estricto, multi-tenant, mismas convenciones que el resto del equipo DobackSoft.
- **Solo dots / fuera del repo:** ayuda normal; no imponer estructura del producto V3 ahí.

## Instalación Gentleman en el proyecto

- Documentación: [docs/DESARROLLO/GENTLEMAN-DOTS-INSTALACION.md](../../../docs/DESARROLLO/GENTLEMAN-DOTS-INSTALACION.md)
- Script: `scripts/setup/install-gentleman-dots.sh` (detecta macOS/Linux y arquitectura).

## Prohibido mezclar

- No tratar “Gentleman” como módulo nuevo del menú DobackSoft.
- No arrancar backend/frontend con flujos del instalador; el stack DobackSoft usa los scripts oficiales de inicio.
- No commitear el binario `gentleman.dots` ni dejarlo en la raíz del repo.

## Cursor

Regla **siempre activa:** `.cursor/rules/gentleman-dobacksoft.mdc` (`alwaysApply: true`). Esta skill aporta detalle al trabajar con la guía o el script de instalación (`globs`).
