---
name: typdd
description: Use when user wants to draw, render, visualize, or customize a Binary Decision Diagram (BDD) in Typst, or asks about boolean expression diagrams, decision trees, or logic circuit visualization.
argument-hint: <boolean expression or customization request>
allowed-tools:
  - Write
  - Edit
  - Bash
  - Read
  - Glob
---

# typdd

Render publication-ready BDD diagrams in Typst. Write `#bdd("expr")`, typdd handles parsing, building, reducing, layout, and rendering via fletcher.

## Workflow

1. **New file:** create `.typ` with `#bdd(...)` — **existing file:** add/edit `#bdd(...)` calls
2. Ensure `#import "@preview/typdd:0.1.0": bdd` is at the top
3. Compile: `typst compile file.typ file.png` (add `--root .` for local imports)

## Example

```typst
#import "@preview/typdd:0.1.0": bdd
#set page(width: auto, height: auto, margin: 1em)
#set text(font: "New Computer Modern", size: 10pt)

#grid(
  columns: 3, column-gutter: 2em, align: center + horizon,
  bdd("x1 & x2"),
  bdd("x1 ^ x2", style: "presentation"),
  bdd("a & (b | !c)", labels: (a: $alpha$, b: $beta$, c: $gamma$), compact: true),
)
```

## API — `bdd(expr, ..options)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `expr` | `str` | **required** | Boolean expression |
| `style` | `str` | `"classic"` | `classic` / `paper` / `presentation` / `curved` |
| `order` | `array` | `none` | Variable ordering, e.g. `("x3","x1","x2")` |
| `labels` | `dict` | `(:)` | Display names: `(x1: $alpha$)` or `(a: "emoji")` |
| `show-edge-labels` | `bool` | `false` | Show 0/1 on edges |
| `direction` | `str` | `"TB"` | `TB` / `BT` / `LR` / `RL` |
| `scale` | `float` | `1.0` | Uniform scale factor |
| `compact` | `bool` | `false` | Tighter spacing for large BDDs |
| `reduced` | `bool` | `true` | Apply BDD reduction (set `false` for teaching) |
| `center-root` | `bool` | `true` | Center on root node |
| `node-sep` / `level-sep` | `length` | `auto` | Spacing overrides |
| `show-complement` | `bool` | `false` | Complement edge bubbles |

`bdd-from-json(data, ..options)` — same rendering options, imports from JSON interchange format.

## Operators

`&` AND · `|` OR · `!` NOT · `^` XOR · `=>` IMPLIES · `~&` NAND · `~|` NOR · `~^` XNOR · `ite(c,t,f)`

Precedence (low→high): `=>` → `|` → `^` → `&` → `!`. Variables: alphanumeric (`x1`, `input_A`). Constants: `0`, `1`, `true`, `false`.

## Styles

`classic` (B&W default) · `paper` (thin grayscale) · `presentation` (blue/colored) · `curved` (curved edges)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `#set page(width: auto, height: auto)` | Add it for standalone images |
| Using `&&` or `\|\|` | Single-char: `&` and `\|` |
| Hyphenated variable names | Alphanumeric only: `input_A` not `input-A` |
| >20 variables or >1000 char expression | Simplify or use `compact: true` |
