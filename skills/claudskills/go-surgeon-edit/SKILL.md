---
name: go-surgeon-edit
description: ALWAYS load when browsing or editing go project. Use this skill whenever you need to read, navigate, explore, or modify Go source code in a project that has `go-surgeon` installed (check for the binary or `go-surgeon` in go.mod). This includes adding, updating, or deleting functions, methods, structs, and interfaces; generating mocks; implementing interface stubs; generating test skeletons; manipulating struct tags; extracting interfaces from structs; and exploring codebase structure. Trigger this skill for ANY Go code editing task — even simple ones like "add a method" or "rename this function" — because go-surgeon produces deterministic, AST-correct results that avoid indentation errors, import issues, and context window waste. Also trigger when the user says "explore the codebase", "find symbol X", "show me the function", "list packages", or wants to understand Go project structure. Do NOT use generic text tools (cat, sed, grep, diff) for Go code editing when go-surgeon is available.
---

# go-surgeon: Edit Skill

You are editing Go code in a project that has `go-surgeon` available. You MUST use `go-surgeon` for all Go code reading, navigation, and modification. Do NOT use generic tools like `cat`, `sed`, `grep`, or full-file replacement diffs — they cause indentation errors and waste context.

`go-surgeon` is a deterministic AST-based byte-range editor. It automatically runs `goimports` on every mutation, so you NEVER need to manage imports or formatting.

---

## 1. Orientation & Navigation

Always start by exploring the codebase structure rather than reading full files.

### List all packages
```bash
go-surgeon graph
```

### List exported symbols in a directory
```bash
go-surgeon graph --symbols --dir <relative_dir>
# Short: go-surgeon graph -s -d <relative_dir>
```

Additional flags:
- `--summary`: Include package doc comment summary
- `--deps`: Show internal import dependencies
- `--tests`: Include `_test.go` files
- `--recursive=false`: Only the target directory (no sub-packages), used with `--symbols`

### Context window management flags
Use these to avoid overwhelming the token budget on large codebases:
```bash
# Limit directory recursion depth (1 = target dir only, 2 = immediate children)
go-surgeon graph --summary --depth 2

# Full detail for one package, path-only for the rest (implies --symbols --summary -r)
go-surgeon graph --focus internal/catalog/domain

# Skip directories matching glob patterns (repeatable)
go-surgeon graph --exclude vendor --exclude "*legacy*"

# Progressive truncation to fit approximate token count
# Strips in order: summaries → deps → symbols → files → package list
go-surgeon graph --summary --deps --token-budget 2000
```

### Progressive discovery strategy
For large codebases, zoom in step by step:
1. `go-surgeon graph --summary --depth 2` — high-level map
2. `go-surgeon graph --focus <package>` — full detail on the interesting area
3. `go-surgeon graph -s -d <subdir>` — symbols in one subtree

### Find a symbol (function, method, struct)
```bash
# Free function or struct
go-surgeon symbol NewBook

# Method on a receiver (Receiver.Method form)
go-surgeon symbol BookHandler.Handle

# With full body (empty lines stripped to save tokens)
go-surgeon symbol NewBook --body

# Scoped to a directory
go-surgeon symbol Validate --dir internal/catalog/domain
# Short: go-surgeon symbol Validate -b -d internal/catalog/domain
```

**Important:** Use `Receiver.Method` form for precise method lookups. If multiple matches are found, a disambiguation index is returned — refine with `Receiver.Method` or `--dir`.

---

## 2. Editing Code

**NEVER use `cat <<'EOF' | go-surgeon ...` heredoc pipes** — they trigger permission prompts. Instead, write YAML plan files to `.tmp/` and execute them with `go-surgeon execute -f`.

### YAML plan files (preferred pattern)

Write one or more actions to a `.tmp/plan_name.yaml` file using the `Write` tool, then execute:

```bash
go-surgeon execute -f .tmp/plan_name.yaml
```

Plans are auto-deleted on success. You can batch multiple actions and run multiple plans in one call:

```bash
go-surgeon execute -f .tmp/plan_a.yaml -f .tmp/plan_b.yaml
```

**Plan file schema:**
```yaml
actions:
  - action: create_file | replace_file
             add_func | update_func | delete_func
             add_struct | update_struct | delete_struct
             add_interface | update_interface | delete_interface
    file: <target file path>
    identifier: <FuncName or Receiver.Method, for update/delete>
    content: |
      <raw Go source — no package declaration, no imports>
    mock_file: <mock output path, for add/update_interface>
    mock_name: <mock struct name, for add/update_interface>
```

### Examples

**Add a function:**
```yaml
# .tmp/plan_add_newbook.yaml
actions:
  - action: add_func
    file: internal/domain/book.go
    content: |
      func NewBook(title string) (*Book, error) {
          if title == "" {
              return nil, errors.New("title required")
          }
          return &Book{Title: title}, nil
      }
```

**Update a function and add a struct in one plan:**
```yaml
# .tmp/plan_book_changes.yaml
actions:
  - action: update_func
    file: internal/domain/book.go
    identifier: NewBook
    content: |
      func NewBook(title, author string) (*Book, error) {
          return &Book{Title: title, Author: author}, nil
      }
  - action: add_struct
    file: internal/domain/book.go
    content: |
      type BookStatus string
```

**Delete (no content needed):**
```yaml
actions:
  - action: delete_func
    file: internal/domain/book.go
    identifier: NewBook
```

**Update a method (Receiver.Method form):**
```yaml
actions:
  - action: update_func
    file: internal/domain/book.go
    identifier: Book.Validate
    content: |
      func (b *Book) Validate() error {
          return nil
      }
```

### Critical rules
1. **Always provide the FULL declaration** in `content` (complete signature + body for functions).
2. **Never add `package` or `import` statements** — goimports handles it.
3. **Never worry about indentation** — goimports reformats everything.
4. **Each action is atomic** with clear error messages including hints.
5. **`update-func`/`update-struct` fall back to `add`** if the identifier is not found, with a warning.
6. **`add-func`/`add-struct` detect duplicates** and return the existing code in the error message.
7. **Never use the `Read` tool on `.go` files** — use `go-surgeon symbol <Name> --body` instead.

---

## 3. Interfaces & Mocks

### Create/update interface with auto-mock

Use a YAML plan file:
```yaml
# .tmp/plan_repo_interface.yaml
actions:
  - action: add_interface
    file: internal/domain/repositories/book/book.go
    mock_file: internal/domain/repositories/book/booktest/mock.go
    mock_name: MockBookRepository
    content: |
      type BookRepository interface {
          Create(ctx context.Context, projectID types.ProjectID, book domain.Book) error
          FindByID(ctx context.Context, projectID types.ProjectID, id types.BookID) (*domain.Book, error)
      }
```

```yaml
# Update (regenerates mock automatically)
actions:
  - action: update_interface
    file: internal/domain/repositories/book/book.go
    identifier: BookRepository
    mock_file: internal/domain/repositories/book/booktest/mock.go
    mock_name: MockBookRepository
    content: |
      type BookRepository interface {
          Create(ctx context.Context, projectID types.ProjectID, book domain.Book) error
          FindByID(ctx context.Context, projectID types.ProjectID, id types.BookID) (*domain.Book, error)
          Delete(ctx context.Context, projectID types.ProjectID, id types.BookID) error
      }
```

```bash
# Delete (mock is NOT auto-deleted — build will break, forcing explicit cleanup)
go-surgeon delete-interface --file internal/domain/repositories/book/book.go --id BookRepository
```

### Implement an interface (generate stubs)
For interfaces you **don't own** (stdlib, third-party, or project-local):
```bash
go-surgeon implement io.ReadCloser --receiver "*MyReader" --file internal/pkg/reader.go
go-surgeon implement context.Context --receiver "*MyCtx" --file internal/ctx.go
```
- Resolves the interface via `go/packages` (stdlib + third-party + local)
- Scans the entire package directory to avoid cross-file duplicates
- Validates signature compatibility of existing methods
- Generated stubs contain `// TODO: implement` + `panic("not implemented")`

### Standalone mock generation
For interfaces you **don't own** and just need a mock:
```bash
go-surgeon mock io.ReadCloser --mock-name MockReadCloser --file internal/mocks/readcloser.go
go-surgeon mock github.com/myorg/myapp/domain.Repository \
  --mock-name MockRepository \
  --file internal/domain/repositorytest/mock.go
```

### Extract interface from a struct
Scans all exported methods of a struct and generates the interface + optional mock:
```bash
go-surgeon extract-interface \
  --file internal/app/service.go \
  --id Service \
  --name ServiceInterface \
  --out internal/domain/service.go \
  --mock-file internal/domain/servicetest/mock.go \
  --mock-name MockService
```

---

## 4. Test Generation

Generate a table-driven test skeleton for any function or method:
```bash
go-surgeon test --file internal/domain/book.go --id NewBook
go-surgeon test --file internal/domain/book.go --id Book.Validate
```
- Creates/appends to `*_test.go` with `_test` package
- Generates struct with `args`, `want*`, and `wantErr` fields
- Uses testify assert/require

---

## 5. Struct Tag Manipulation

```bash
# Auto-generate json tags for all exported fields (camelCase)
go-surgeon tag --file internal/domain/book.go --id Book --auto json

# Auto-generate bson tags (snake_case)
go-surgeon tag --file internal/domain/book.go --id Book --auto bson

# Set exact tag on a specific field
go-surgeon tag --file internal/domain/book.go --id Book --field Title --set 'json:"book_title"'
```

---

## 6. Dry Run / Diff Mode

Preview any change as a unified diff without writing to disk. Write the content to a temp file and pipe it:
```bash
# Write content to a temp file, then pipe to --dry-run
printf 'func NewBook(title, author string) (*Book, error) {\n    return &Book{Title: title, Author: author}, nil\n}\n' \
  > .tmp/newbook.go
go-surgeon update-func --dry-run --file internal/domain/book.go --id NewBook < .tmp/newbook.go
rm .tmp/newbook.go
```

Note: `--dry-run` is not supported in YAML plan files — use the stdin form only for previewing.

---

## Workflow: Before You Edit

1. **Orient:** `go-surgeon graph` (or `graph --summary --depth 2` for large codebases) → find the package
2. **Focus:** `go-surgeon graph --focus <pkg>` → full detail on the target, path-only for the rest
3. **Zoom in:** `go-surgeon graph -s -d <dir>` → find the file and symbol
4. **Read:** `go-surgeon symbol <Name> --body` → understand what you're changing
5. **Find a pattern:** Look at a similar existing implementation before writing new code
6. **Edit:** Use the appropriate subcommand
7. **Verify:** `go build ./...` to confirm the codebase compiles

## Error Handling

go-surgeon returns structured errors with hints:
- `NODE_NOT_FOUND` → "use `go-surgeon symbol X` to locate it"
- `NODE_ALREADY_EXISTS` → "use `update-func` to replace it" (shows existing code)
- `FILE_NOT_FOUND` → "use `go-surgeon graph` to list packages, or `create-file`"
- Unresolved imports → stderr warning when goimports can't resolve a package
