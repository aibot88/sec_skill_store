---
name: vb6-guidelines
description: Applies general Visual Basic 6 conventions when editing .bas, .cls, .frm, .frx, .vbp, .vbg, .ctl, or .dob files, or any code identified as VB6 (not VB.NET, not VBA). Covers case-preservation in existing code (VB6 is case-insensitive but diff tools are not), Option Explicit requirement, Hungarian notation with scope prefix plus type prefix (mstr/mint/mcur for module-level in .bas; m_str/m_int/m_cur for module-level in .cls; gstr/gint for global; str/int/cur for parameters and locals), file header blocks for .cls modules with 80-hyphen delimiters, comment-per-field convention, Property Get/Let/Set patterns without public fields, ByVal/ByRef explicit declarations, Long over Integer for performance and overflow safety, preservation of Windows-1252 encoding and CRLF line endings, and never editing .frx files manually due to binary offset corruption. Activates for any Visual Basic 6 development task, code review, refactoring, or new file creation in a VB6 project.
---

# VB6 Guidelines

VB6 is not VB.NET. It is not C#. It is not VBA. The rules below reflect what the
VB6 compiler (1998) requires and what the COM ecosystem expects.

## 1. Case-preservation is absolute in existing code

VB6 is case-insensitive at the compiler level. Diff tools (Git, GitHub, GitLab,
Bitbucket, code review tools) are case-sensitive. Changing the case of an
identifier in existing code pollutes pull requests with ghost changes, hides the
real diff, and breaks `git blame`.

**Absolute rule:** when editing existing code, the case of every identifier
stays exactly as it is. No exceptions.

This applies to:

- Variables and parameters (`m_StrName` stays `m_StrName` even if the current
  convention is `m_strName`)
- Properties and procedures (`Public Sub ReadFile` is not "normalized" to
  `ReadFile` if it is already `ReadFile`)
- Keywords (`If`/`Then`/`End If` — preserve as written; the IDE may have
  normalized different files differently)
- Type names (`As String`, `As Long`)
- Constants (`vbCrLf` vs `vbCRLF`)
- References to module and class names

**When you may use the "correct" case:**

- **New** code (new procedure, new module, new variable)
- When the user explicitly asks for normalization

**When you may not, even when it looks obvious:**

- "Taking advantage" of a bugfix commit to normalize
- "Since I'm already here" during a legitimate refactor of something else
- Cosmetic cleanup without explicit request

The cost of polluting the diff outweighs the value of uniformity. Always.

## 2. Option Explicit and type declarations are mandatory

VB6 allows implicit typing for VB3/4 backward compatibility. In new code, this
is guaranteed technical debt.

- **Always** `Option Explicit` at the top of every module (`.bas`, `.cls`,
  `.frm`)
- **Always** declare type: `Dim i As Long`, never `Dim i`
- **Prefer** `Long` over `Integer` — VB6 `Integer` is 16 bits, overflows at
  32,768
- **Avoid** `Variant` except when interacting with APIs that return `Variant`
  (e.g., ADO `GetRows`)
- **Declare** return type in every `Function`: `Public Function X() As String`,
  not `Public Function X()`

## 3. Hungarian notation — scope prefix plus type prefix

The convention is two-part: a scope prefix followed by a type prefix, both in
lowercase in new code.

### 3.1. Scope prefix

| Scope                          | Prefix       | Example                          |
| ------------------------------ | ------------ | -------------------------------- |
| Module-level in `.bas`         | `m`          | `Private mobjCnn As Object`      |
| Module-level in `.cls`         | `m_`         | `Private m_strName As String`    |
| Global public in `.bas`        | `g`          | `Public gstrServer As String`    |
| Parameter / local              | (none)       | `Dim strValue As String`         |

### 3.2. Type prefix (lowercase, follows scope prefix)

| VB6 Type            | Prefix |
| ------------------- | ------ |
| `String`            | `str`  |
| `Integer`           | `int`  |
| `Long`              | `lng`  |
| `Currency`          | `cur`  |
| `Boolean`           | `bln`  |
| `Double`            | `dbl`  |
| `Date`              | `dtm`  |
| `Byte`              | `byt`  |
| `Object` (generic)  | `obj`  |
| `Variant`           | `var`  |
| `Recordset` (ADO)   | `rs`   |
| `Dictionary`        | `dic`  |
| `Collection`        | `col`  |

Canonical examples:

```vb
Private mobjCnn As Object              ' module-level Object Connection
Private mrsCustomers As Object         ' module-level Recordset
Private mdicConfig As New Dictionary
Private m_strName As String            ' in .cls
Public gstrServer As String

Public Sub DoWork(ByVal strInput As String, ByVal lngCount As Long)
    Dim intIndex As Integer
End Sub
```

### 3.3. Acronyms preserved in uppercase

Acronyms keep uppercase within the identifier: `m_strNSU`, `m_strCNPJ`,
`m_strXML`, `m_strCPF`. Not `m_strNsu`.

### 3.4. Legitimate exceptions

Project-wide "infrastructure" globals widely known across the codebase may omit
the type prefix (e.g., `gParameters`, `gAgent`). For new code, the type prefix
is recommended.

### 3.5. Existing code never gets re-cased

See section 1. If a variable already exists as `m_StrName` or `mObjCnn`, it
**stays exactly that way** in any edit.

## 4. Class module file header

Every new `.cls` starts with a delimited header block:

```vb
'--------------------------------------------------------------------------------
'    Component  : clsCustomer
'    Project    : SampleApp
'
'    Description: Domain object representing a customer record.
'                 Mirrors the structure of the Customer table.
'       <reference URL when applicable>
'    Modified   :
'--------------------------------------------------------------------------------
Option Explicit
```

Delimiters are 80 hyphens. Indentation inside the block uses spaces, not tabs.

## 5. Comment-per-field convention in classes

Each private field gets a one-line comment above it:

```vb
' Variable to hold 'Name' property value
Private m_strName As String

' Variable to hold 'Active' property value
Private m_blnActive As Boolean
```

Yes, it is repetitive. It is the convention. New classes follow it.

## 6. Property Get/Let/Set — never public fields

Class modules expose state through properties, not public fields. Public fields
break binary compatibility in ActiveX DLLs, prevent validation, and break
IntelliSense for late-bound consumers.

```vb
Private m_strName As String
Private m_objConnection As Object

Public Property Get Name() As String
    Name = m_strName
End Property

Public Property Let Name(ByVal strValue As String)
    m_strName = strValue
End Property

Public Property Set Connection(ByVal objValue As Object)
    Set m_objConnection = objValue
End Property
```

- `Property Get` reads
- `Property Let` writes a value type (`String`, `Long`, `Boolean`, etc.)
- `Property Set` writes an object reference

Parameter naming in setters follows the type prefix: `strValue`, `lngValue`,
`blnValue`, `objValue`.

### 6.1. Property style — CRUD direct, no logic in setter

Setters do not validate, do not transform, do not log:

```vb
Public Property Let Name(ByVal strValue As String)
    m_strName = strValue
End Property
```

When validation or transformation is needed, it goes in a dedicated method
(`LoadByID`, `Validate`, `Normalize`), not in the property setter.

### 6.2. Derived properties for representation

Store raw state, expose human-readable form as a `Get`-only derived property:

```vb
' Stored as raw code
Public Property Get Status() As String
    Status = m_strStatus
End Property

Public Property Let Status(ByVal strValue As String)
    m_strStatus = strValue
End Property

' Derived for display
Public Property Get StatusDescription() As String
    Select Case Val(m_strStatus)
        Case 1: StatusDescription = "1-Authorized"
        Case 2: StatusDescription = "2-Denied"
        Case 3: StatusDescription = "3-Cancelled"
    End Select
End Property
```

Do not put `Select Case` inside the `Let`.

### 6.3. Procedure header when domain semantics matter

Trivial CRUD properties do not need a header. Properties that carry domain
rules (valid values, code tables, references to external specifications) get a
header block:

```vb
'--------------------------------------------------------------------------------
' Project    :       SampleApp
' Procedure  :       Status
' Description:       Document status. Valid values:
'                    1 - Authorized
'                    2 - Denied
'                    3 - Cancelled
' Created by :       author
' Date-Time  :       DD/MM/YYYY-HH:MM:SS
'
' Parameters :       strValue (String) - status code
'--------------------------------------------------------------------------------
```

Criterion: **if a reader would need to open external documentation to
understand the property, it gets a header**.

A lighter format is acceptable for utility functions (where `Project` is
irrelevant because the utility is reused across projects):

```vb
'---------------------------------------------------------------------------------------
' Procedure : NormalizePhone
' Author    : author
' Date      : DD/MM/YYYY
' Purpose   : Strips non-digit characters from a phone number string.
'---------------------------------------------------------------------------------------
```

### 6.4. Discriminator property `Type`

Classes that belong to a hierarchy identify themselves via
`Public Property Get Type() As String` returning a constant string
(e.g., `"CUSTOMER"`, `"INVOICE"`). When creating a new class in the same group,
include the discriminator.

## 7. ByVal / ByRef must be explicit

In VB6, parameters default to `ByRef`, unlike most modern languages.

- **Always be explicit**: every signature uses `ByVal` or `ByRef` — never rely
  on the default
- **`ByVal` for primitives** that do not need to be modified (`Long`, `String`,
  `Boolean`)
- **`ByRef` only when** the function actually needs to modify the caller's
  variable
- Passing `String` by `ByRef` accidentally lets the function mutate the
  caller's variable

## 8. Encoding and line endings

- File encoding: **Windows-1252**, not UTF-8 (the VB6 IDE may refuse or corrupt
  UTF-8 files)
- Line endings: **CRLF**, not LF
- Indentation: **4 spaces**, not tabs
- Identifiers contain no accented characters; comments and string literals may

## 9. Never edit .frx manually

`.frx` files are binary. They store images, icons, and long strings referenced
by their companion `.frm`. Any manual edit corrupts the offset table and breaks
the form.

Reformatting `.frm` files is equally dangerous — the declarative section at the
top has strict ordering requirements; the IDE depends on it.

## 10. Comments in the programmer's language

Comments and string literals follow the team's working language. Identifiers
remain unaccented for IDE compatibility. New code matches the language already
established in the file or module.

## 11. UI dialogs through wrappers, not raw MsgBox

VB6 codebases typically wrap `MsgBox` in custom dialog forms (for theming,
logging integration, consistent button layouts). When such wrappers exist in
the project (commonly named `MsgBoxCritical`, `MsgBoxInfo`, `MsgBoxWarning`,
`MsgBoxQuestion`), new code uses them — not raw `MsgBox`.

## Pre-flight check before finalizing

- [ ] `Option Explicit` at the top of the module
- [ ] Every `Dim` and every `Function`/`Sub` has an explicit type
- [ ] `ByVal` / `ByRef` explicit on every parameter
- [ ] No `Variant` unless interacting with a Variant-returning API
- [ ] `Long` instead of `Integer` for loop counters and quantities
- [ ] New private fields prefixed with `m_<type>` in classes or `m<type>` in
      modules, lowercase type prefix
- [ ] New global publics prefixed with `g<type>`, lowercase
- [ ] Class file has the 80-hyphen header
- [ ] `.frx` untouched
- [ ] Encoding preserved (Windows-1252), CRLF preserved
- [ ] No `MsgBox` direct call when wrapper functions exist
- [ ] Edited only what was requested — no opportunistic re-casing
