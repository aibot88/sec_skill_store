---
name: structify
description: Contexto completo del proyecto Structify CLI. Leer SIEMPRE al inicio de cualquier sesión de trabajo en este proyecto antes de tocar código, planificar tareas, o responder preguntas sobre la arquitectura.
---

# Structify — Contexto del Proyecto

## ¿Qué es Structify?
CLI multilenguaje para scaffolding de proyectos basado en arquitecturas de software.
Permite a desarrolladores crear la estructura base de un proyecto eligiendo arquitectura (Clean, Vertical Slice, etc.) y lenguaje (Go, TypeScript, Rust, C#, etc.) en segundos.

## Stack Técnico
| Componente | Elección | Razón |
|---|---|---|
| Lenguaje | Go | Conocimiento del dev + binario único + velocidad de entrega |
| CLI framework | Cobra | Estándar de facto en Go para CLIs |
| TUI / Wizard | Bubbletea | TUI interactivo de alta calidad |
| Configuración | Viper | Config global en `~/.structify/config.yaml` |
| Motor templates | DSL propio | Ver SKILL-dsl.md para spec completa |
| Sharing MVP | GitHub repos | Sin backend propio en v1 |
| Module path | `github.com/user/structify` | Ajustar con usuario real al init |

---

## Estructura de Carpetas del Proyecto

```
structify/
├── cmd/                        # Comandos Cobra
│   ├── root.go                 # Comando raíz, setup global
│   ├── new.go                  # structify new
│   ├── template/
│   │   ├── template.go         # Subcomando base
│   │   ├── list.go
│   │   ├── add.go
│   │   ├── create.go
│   │   ├── validate.go
│   │   ├── remove.go
│   │   ├── info.go
│   │   ├── update.go
│   │   └── publish.go
│   └── version.go
├── internal/
│   ├── dsl/                    # Motor DSL completo
│   │   ├── lexer.go
│   │   ├── parser.go
│   │   ├── evaluator.go
│   │   ├── interpolator.go
│   │   ├── filters.go
│   │   └── validator.go
│   ├── engine/                 # Engine de scaffolding
│   │   ├── engine.go           # Orquestador principal
│   │   ├── resolver.go         # Buscar templates
│   │   ├── executor.go         # Ejecutar steps
│   │   ├── file_processor.go   # Copiar/excluir archivos
│   │   └── rollback.go         # Limpiar en caso de error
│   ├── template/               # Modelo y gestión de templates
│   │   ├── model.go            # Structs: Template, Input, Step, etc.
│   │   ├── loader.go           # Cargar scaffold.yaml
│   │   ├── store.go            # CRUD en ~/.structify/templates/
│   │   └── github.go           # Clonar desde GitHub
│   ├── tui/                    # Componentes Bubbletea
│   │   ├── wizard.go           # Wizard principal
│   │   ├── selector.go         # Lista de templates
│   │   ├── inputs.go           # Formulario de variables
│   │   └── progress.go         # Spinner + progreso de steps
│   └── config/
│       └── config.go           # Config global con Viper
├── templates/                  # Templates built-in embebidos
│   ├── clean-architecture-go/
│   ├── vertical-slice-go/
│   ├── clean-architecture-ts/
│   ├── vertical-slice-ts/
│   └── clean-architecture-rust/
├── tasks/
│   ├── todo.md                 # Plan maestro con checkboxes
│   ├── lessons.md              # Lecciones aprendidas
│   ├── SKILL-structify.md      # Este archivo
│   ├── SKILL-dsl.md            # Spec del DSL
│   └── SKILL-workflow.md       # Metodología de trabajo
├── docs/                       # Documentación pública
├── .github/
│   └── workflows/
│       └── ci.yml
├── Makefile
├── go.mod
├── go.sum
└── main.go
```

---

## Flujo Principal: `structify new`

```
Usuario ejecuta: structify new
        │
        ▼
1. Resolver lista de templates disponibles (~/.structify/templates/ + built-ins)
        │
        ▼
2. TUI: Mostrar lista de templates al usuario (selector Bubbletea)
        │
        ▼
3. TUI: Por cada `input` del scaffold.yaml → hacer pregunta al usuario
        │
        ▼
4. Engine: Evaluar `when:` de cada archivo/carpeta → incluir o excluir
        │
        ▼
5. Engine: Copiar archivos al destino, interpolando {{ variables }}
        │
        ▼
6. Engine: Ejecutar `steps` en orden (con evaluación de `when:`)
        │    Si falla → rollback completo
        ▼
7. TUI: Mostrar resumen de lo generado + próximos pasos
```

---

## Estructura de una Plantilla

```
my-template/
├── scaffold.yaml           # Metadata + DSL (OBLIGATORIO)
├── template/               # Archivos fuente a copiar/renderizar
│   ├── cmd/
│   │   └── main.go.tmpl   # Archivos con .tmpl son procesados
│   ├── internal/
│   └── ...
└── README.md               # Documentación de la plantilla
```

### Reglas de archivos template
- Archivos con extensión `.tmpl` → se interpola `{{ }}` y se elimina `.tmpl`
- Archivos sin `.tmpl` → se copian tal cual
- Carpetas cuyo `when:` evalúa a `false` → se omiten completamente

---

## Comandos del CLI

```bash
# Crear nuevo proyecto
structify new                                    # Wizard interactivo
structify new --template clean-go --name myapp  # Con flags (CI-friendly)
structify new --template clean-go --name myapp --var orm=gorm --dry-run

# Gestión de templates
structify template list                          # Listar templates locales
structify template add <github-url>              # Importar desde GitHub
structify template add github.com/user/repo@v1.2.0  # Con versión específica
structify template create                        # Wizard para nueva plantilla
structify template validate <path>               # Validar scaffold.yaml
structify template remove <name>                 # Eliminar template local
structify template info <name>                   # Ver detalle
structify template update <name>                 # Actualizar desde origen
structify template publish                       # Checklist para publicar

# Otros
structify version
structify --help
```

---

## Directorio de datos del usuario

```
~/.structify/
├── config.yaml             # Configuración global
└── templates/              # Templates instalados por el usuario
    ├── clean-go/
    ├── my-custom-template/
    └── ...
```

---

## Templates Built-in

Los templates built-in se embeben en el binario con `//go:embed templates/`.
Esto garantiza que el CLI funcione sin conexión y sin instalación adicional.

Lista de built-ins a implementar (Fase 7):
- `clean-architecture-go`
- `vertical-slice-go`
- `clean-architecture-ts`
- `vertical-slice-ts`
- `clean-architecture-rust`

---

## Fases de Desarrollo (resumen)

| Fase | Descripción | Estado |
|---|---|---|
| F1 | Fundación del proyecto (Go, Cobra, Viper, Bubbletea) | Pendiente |
| F2 | DSL: Lexer + Parser + Evaluator + Interpolador | Pendiente |
| F3 | Engine de scaffolding (resolver, executor, rollback) | Pendiente |
| F4 | Comando `structify new` end-to-end | Pendiente |
| F5 | Sistema de templates local (CRUD) | Pendiente |
| F6 | Sharing vía GitHub | Pendiente |
| F7 | Templates built-in | Pendiente |
| F8 | Distribución (GoReleaser, brew, docs) | Pendiente |

**Orden obligatorio:** F1 → F2 → F3 → F4 → F5 → F6 → F7 → F8
F2 es el núcleo. Sin DSL sólido, todo lo demás es frágil.

---

## Dependencias Go (go.mod)

```go
require (
    github.com/spf13/cobra       // CLI framework
    github.com/spf13/viper       // Configuración
    github.com/charmbracelet/bubbletea  // TUI
    github.com/charmbracelet/lipgloss   // Estilos TUI
    github.com/charmbracelet/bubbles    // Componentes TUI (spinner, list, textinput)
    gopkg.in/yaml.v3             // Parsear scaffold.yaml
    github.com/go-git/go-git/v5  // Clonar repos GitHub
)
```

---

## Convenciones de Código

- Errores: siempre wrappear con contexto → `fmt.Errorf("loading template: %w", err)`
- No usar `panic()` en producción, solo en `main()` para errores de setup
- Tests: tabla de casos (`table-driven tests`) como estándar en Go
- Nombres de archivos: `snake_case.go`
- Packages: nombres cortos, sin underscores (`dsl`, `engine`, `template`, `tui`)
- Exportar solo lo necesario, preferir interfaces pequeñas
