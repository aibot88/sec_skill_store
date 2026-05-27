---
name: vb6-ado-late-binding
description: Applies the ADO late-binding pattern when writing or modifying database access code in Visual Basic 6, supporting both Microsoft SQL Server and PostgreSQL. Covers declaration as Object with CreateObject instantiation (never As ADODB.Connection or New ADODB.Recordset), ADO constants defined locally instead of referencing the type library, mandatory ConnectionTimeout before Open, the disconnected recordset pattern (CursorLocation client-side, then ActiveConnection = Nothing after Open), parameterized queries via ADODB.Command with Parameters.Append to prevent SQL injection and improve query plan caching, the AddADOParameter and SetADOCommandParameters helper functions that accumulate parameters in a Dictionary before applying them to a Command, multibank parameter naming (@param for MSSQL versus in_param/out_param for PostgreSQL) handled by SetParameter and GetParameter helpers, and structural SQL concatenation (table names, dynamic joins) versus value parameterization. Activates for any task involving ADODB, Connection, Recordset, Command, Parameters, SQL queries, database access, late binding, or CreateObject in VB6 context.
---

# ADO Late Binding — VB6

ADO is accessed via **late binding** to avoid version-locking the MDAC stack on
client machines. No reference to "Microsoft ActiveX Data Objects x.x Library"
is added to the project. Both Microsoft SQL Server and PostgreSQL are
supported through the same ADO surface, with small naming differences in
parameter handling.

## 1. Declaration and instantiation

```vb
' Declarations — always As Object
Private mobjCnn As Object
Private mrsCustomers As Object

' Instantiation — always CreateObject
Set mobjCnn = CreateObject("ADODB.Connection")
Set objRs = CreateObject("ADODB.Recordset")
Set objCmd = CreateObject("ADODB.Command")
```

**Never:**

- `Dim cnn As ADODB.Connection`
- `Dim rs As ADODB.Recordset`
- `Set rs = New ADODB.Recordset`
- Adding a reference to the ADO type library

**Rationale:** different Windows versions ship different MDAC versions. Early
binding to a specific type library version causes "ActiveX component can't
create object" or "type mismatch" errors when the client has a different
version installed. Late binding works against whatever ADO is present.

## 2. ADO constants — defined locally

Because the type library is not referenced, ADO constants must be defined as
local constants or used as literals. The recommended approach for new code is
to declare them at the top of any module that uses ADO, or in a shared
`modADOConstants.bas`.

```vb
Option Explicit

' Command types
Private Const adCmdText         As Long = 1
Private Const adCmdTable        As Long = 2
Private Const adCmdStoredProc   As Long = 4

' Parameter directions
Private Const adParamInput      As Long = 1
Private Const adParamOutput     As Long = 2
Private Const adParamInputOutput As Long = 3
Private Const adParamReturnValue As Long = 4

' Cursor types
Private Const adOpenForwardOnly As Long = 0
Private Const adOpenKeyset      As Long = 1
Private Const adOpenDynamic     As Long = 2
Private Const adOpenStatic      As Long = 3

' Lock types
Private Const adLockReadOnly    As Long = 1
Private Const adLockPessimistic As Long = 2
Private Const adLockOptimistic  As Long = 3

' Cursor locations
Private Const adUseServer       As Long = 2
Private Const adUseClient       As Long = 3

' Connection states
Private Const adStateClosed     As Long = 0
Private Const adStateOpen       As Long = 1

' Data types (common subset)
Private Const adInteger         As Long = 3
Private Const adBigInt          As Long = 20
Private Const adVarChar         As Long = 200
Private Const adLongVarChar     As Long = 201
Private Const adVarWChar        As Long = 202
Private Const adLongVarWChar    As Long = 203
Private Const adBoolean         As Long = 11
Private Const adCurrency        As Long = 6
Private Const adDouble          As Long = 5
Private Const adDate            As Long = 7
Private Const adDBTimeStamp     As Long = 135
Private Const adGUID            As Long = 72
Private Const adBinary          As Long = 128
```

A complete reference list is in `reference/ado-constants.bas`.

Older code may use numeric literals directly (`rs.Open SQL, cnn, 0, 1`).
**Preserve those as-is** — see `vb6-guidelines` section 1 on case-preservation;
the same principle applies to literal-vs-constant style.

## 3. Connection setup

```vb
If mobjCnn Is Nothing Then
    Set mobjCnn = CreateObject("ADODB.Connection")
End If

If mobjCnn.State = adStateClosed Then
    mobjCnn.ConnectionTimeout = 10                  ' mandatory before Open
    mobjCnn.Open BuildConnectionString()
End If
```

**`ConnectionTimeout` is mandatory before `Open`.** Without it, a network
failure or a misconfigured server can block the UI thread for 30+ seconds
(the OLE DB default). 10 seconds is a sensible default for LAN; adjust for
remote/cloud databases.

## 4. Disconnected recordset (standard pattern for SELECT)

For read queries that fetch and release, use the disconnected pattern:

```vb
Dim objRs As Object

Set objRs = CreateObject("ADODB.Recordset")
objRs.CursorLocation = adUseClient                  ' required to disconnect
Set objRs.ActiveConnection = mobjCnn
objRs.Open strSQL, mobjCnn, adOpenForwardOnly, adLockReadOnly

Set objRs.ActiveConnection = Nothing                ' disconnect

' ... use objRs ...

' in _Exit / _Err:
Set objRs = Nothing
```

The line `Set objRs.ActiveConnection = Nothing` after `Open` decouples the
recordset from the connection. The recordset becomes a client-side snapshot
and the connection is immediately available for other queries. Without this
line, connection handles accumulate in the database server.

**`CursorLocation = adUseClient` must be set before `Open`** — setting it
after has no effect.

## 5. Parameterized queries — the rule for any user-supplied value

**Concatenating values into SQL strings is forbidden.** Use parameters for
every value that comes from user input, business logic, or any source that is
not a hardcoded structural part of the query.

| What goes in parameters                          | What may be concatenated                              |
| ------------------------------------------------ | ----------------------------------------------------- |
| Any value (`WHERE id = ?`)                       | Table names (`FROM ` & strTable)                      |
| Dates, numbers, booleans, strings, NULLs         | Column names in `SELECT` lists                        |
| Result of business logic                         | Conditional `JOIN` clauses                            |
| Input from forms, files, network                 | Optional `WHERE` clauses (the keyword, not the value) |

**Reasons parameters win:**

1. **Security**: prevents SQL injection. Even on an internal LAN PDV, a free
   text field ("L'Oréal" with an apostrophe) breaks concatenated SQL.
2. **Performance**: SQL Server caches query plans by SQL text. Parameterized
   queries reuse one plan; concatenated queries fill the plan cache with
   equivalent variants.
3. **Type safety**: dates, decimals, and NULLs serialize correctly without
   manual `ToSQL()` calls or locale-dependent formatting (decimal `,` vs `.`).
4. **Readability**: SQL stays clean; values appear in a separate block.

## 6. Parameter pattern — direct ADODB.Command usage

For one-off queries, use the Command object directly:

```vb
'CSEH: ErrRaise
Public Function GetActiveCustomer(ByVal lngCustomerID As Long, _
                                   ByVal blnIncludeInactive As Boolean) As Object

        '<EhHeader>
        On Error GoTo GetActiveCustomer_Err
        EnterMethod "modDB", "GetActiveCustomer"
        '</EhHeader>

        Dim objCmd As Object
        Dim objRs  As Object
        Dim strSQL As String

100     InitializeDBConnection

105     Set objCmd = CreateObject("ADODB.Command")
110     Set objCmd.ActiveConnection = mobjCnn
115     objCmd.CommandType = adCmdText

120     strSQL = ""
125     strSQL = strSQL & "SELECT idCustomer, custName, custCNPJ " & vbNewLine
130     strSQL = strSQL & "  FROM Customer " & vbNewLine
135     strSQL = strSQL & " WHERE idCustomer = ? " & vbNewLine
140     strSQL = strSQL & "   AND (custActive = ? OR ? = 1) " & vbNewLine

145     objCmd.CommandText = strSQL

150     objCmd.Parameters.Append objCmd.CreateParameter("idCustomer", adInteger, adParamInput, , lngCustomerID)
155     objCmd.Parameters.Append objCmd.CreateParameter("custActive", adBoolean, adParamInput, , True)
160     objCmd.Parameters.Append objCmd.CreateParameter("includeInactive", adBoolean, adParamInput, , blnIncludeInactive)

165     Set objRs = objCmd.Execute

170     Set GetActiveCustomer = objRs

    '<EhFooter>
        On Error GoTo 0

GetActiveCustomer_Exit:
        Set objCmd = Nothing
        ExitMethod "modDB", "GetActiveCustomer"
        Exit Function

GetActiveCustomer_Err:
        Dim sGetActiveCustomer_Err As String
        sGetActiveCustomer_Err = "Error: " & Err.Number & " - " & Err.Description & " (" & Erl & ")"

        Set objCmd = Nothing
        Set objRs = Nothing
        ExitMethod "modDB", "GetActiveCustomer"

        Err.Raise vbObjectError + 100, "SampleApp.modDB.GetActiveCustomer", sGetActiveCustomer_Err
    '</EhFooter>
End Function
```

### Notes

- `CreateParameter(name, type, direction, size, value)` — `size` is omitted
  (`,`) for fixed-size types like `adInteger`
- For variable-size types (`adVarChar`, `adVarWChar`), specify size:
  `CreateParameter("custName", adVarChar, adParamInput, 100, strName)`
- Use `?` placeholders in MSSQL for positional binding (the names you give in
  `CreateParameter` are documentation only when using `?`)

## 7. Parameter pattern — accumulator helpers

For procedures with many parameters or repeated parameter setup, an
accumulator pattern keeps the code clean. Typical project helpers:

```vb
' Add a parameter to the internal accumulator
Public Sub AddADOParameter(ByVal ParName As String, _
                            ByVal ParType As EnumADODataType, _
                            ByVal Value As Variant, _
                            Optional ByVal InputPar As Boolean = True)

' Apply all accumulated parameters to a Command and clear the accumulator
Public Function SetADOCommandParameters(objCommand As Object, _
                                         Optional ByVal AfterClearParameters As Boolean = True)
```

Usage:

```vb
105     AddADOParameter "idCustomer", adInteger, lngCustomerID
110     AddADOParameter "custActive", adBoolean, True
115     AddADOParameter "includeInactive", adBoolean, blnIncludeInactive

120     SetADOCommandParameters objCmd
```

The accumulator is a module-level `Dictionary` that holds `clsADOParameter`
instances until applied. After `SetADOCommandParameters` runs, the dictionary
is cleared (unless `AfterClearParameters = False` is passed). See
`reference/command-pattern.bas` for the helper module skeleton.

## 8. Stored procedures and bidirectional parameters

For stored procedures (or any call with output parameters), use
`SetParameter` and `GetParameter` to abstract the database-specific naming:

```vb
' MSSQL: parameters named @idCustomer, @result
' PostgreSQL: parameters named in_idCustomer, out_result

105     Set objCmd = CreateObject("ADODB.Command")
110     Set objCmd.ActiveConnection = mobjCnn
115     objCmd.CommandType = adCmdStoredProc
120     objCmd.CommandText = "sp_GetCustomerDetails"

125     ' Append parameters (names without prefix; helpers add it)
130     objCmd.Parameters.Append objCmd.CreateParameter(ParamName("idCustomer", adParamInput), adInteger, adParamInput, , 0)
135     objCmd.Parameters.Append objCmd.CreateParameter(ParamName("result", adParamOutput), adVarChar, adParamOutput, 200)

140     SetParameter objCmd, "idCustomer", lngCustomerID

145     objCmd.Execute

150     strResult = GetParameter(objCmd, "result")
```

The `SetParameter` and `GetParameter` helpers consult a global like
`gParameters.DatabaseType` to construct the correct parameter name:

```vb
Public Sub SetParameter(objCommand As Object, ByVal ParName As String, _
                         ByVal Value As Variant, Optional ByVal InputPar As Boolean = True)
    If gParameters.DatabaseType = EnumDatabaseType.Postgres Then
        ParName = IIf(InputPar, "in_", "out_") & ParName
    ElseIf gParameters.DatabaseType = EnumDatabaseType.MSSQL Then
        ParName = "@" & ParName
    End If
    objCommand.Parameters(ParName).Value = Value
End Sub

Public Function GetParameter(objCommand As Object, ByVal ParName As String) As Variant
    If gParameters.DatabaseType = EnumDatabaseType.Postgres Then
        ParName = "out_" & ParName
    ElseIf gParameters.DatabaseType = EnumDatabaseType.MSSQL Then
        ParName = "@" & ParName
    End If
    GetParameter = objCommand.Parameters(ParName)
End Function
```

This isolates the database-specific naming convention to two helpers; the rest
of the code uses logical parameter names (`"idCustomer"`, `"result"`).

## 9. Provider strings for the two databases

### Microsoft SQL Server (SQLNCLI)

```
Provider=SQLNCLI10;DataTypeCompatibility=80;Server=<server>;Database=<db>;User Id=<user>;Password=<pwd>;
```

`DataTypeCompatibility=80` is required when the schema uses pre-2008 type
mappings. Newer providers (SQLNCLI11, MSOLEDBSQL) are drop-in replacements
with different version numbers — pick what is deployed on client machines.

### PostgreSQL (via MSDASQL)

```
Provider=MSDASQL.1;Driver={PostgreSQL UNICODE};Server=<server>;Port=5432;Database=<db>;Uid=<user>;Pwd=<pwd>;
```

`MSDASQL.1` is the OLE DB Provider for ODBC; the actual driver is the
PostgreSQL ODBC driver installed on the machine.

A `BuildConnectionString` function typically inspects a project parameter
(connection mode, DSN flag) and chooses the provider:

```vb
If InStr(1, strDBPath, "DSN", vbTextCompare) > 0 Then
    ' Postgres via DSN
    BuildConnectionString = "Provider=MSDASQL.1;" & strDBPath & "Pwd=<pwd>;"
    gParameters.DatabaseType = EnumDatabaseType.Postgres
Else
    ' MSSQL
    BuildConnectionString = "Provider=SQLNCLI10;DataTypeCompatibility=80;" & strDBPath
    gParameters.DatabaseType = EnumDatabaseType.MSSQL
End If
```

## 10. Cleanup

### Recordset

```vb
' In _Exit and _Err:
If Not objRs Is Nothing Then
    If objRs.State = adStateOpen Then objRs.Close
    Set objRs = Nothing
End If
```

For disconnected recordsets, `Close` is optional but harmless — keep it for
consistency with connected recordsets.

### Connection

Use a dedicated dispose routine with `On Error Resume Next`:

```vb
Public Sub CloseDBConnection()
    On Error Resume Next
    If Not mobjCnn Is Nothing Then
        If mobjCnn.State <> adStateClosed Then mobjCnn.Close
    End If
    Set mobjCnn = Nothing
End Sub
```

### Command

```vb
Set objCmd = Nothing
```

Setting `ActiveConnection = Nothing` on the Command before disposing is
unnecessary — releasing the reference is enough.

## 11. Transactions

ADO transactions wrap multiple statements on a single connection:

```vb
        mobjCnn.BeginTrans
        
        On Error GoTo Rollback
        
        ' ... multiple commands ...
        
        mobjCnn.CommitTrans
        Exit Sub

Rollback:
        mobjCnn.RollbackTrans
        Err.Raise ...
```

Watch for nested calls: ADO's `BeginTrans` returns the nesting level. Most
projects keep transactions single-level and use a module-level
`mblnInTransaction` flag to detect and forbid nesting from the application
side.

## 12. Anti-patterns

| Anti-pattern                                                | Why it breaks                                                                |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `Dim cnn As ADODB.Connection`                               | Forces type library reference; breaks on clients with different MDAC         |
| `Open` without `ConnectionTimeout`                          | UI hangs 30+ seconds on network failure                                      |
| Concatenating user input into SQL                           | SQL injection; query plan cache pollution; locale-dependent formatting       |
| `CursorLocation = adUseClient` set after `Open`             | No effect; recordset stays server-side; cannot disconnect                    |
| Forgetting `Set rs.ActiveConnection = Nothing`              | Connection stays "in use"; server-side handles accumulate                    |
| Hot loop calling `CreateObject("ADODB.Recordset")`          | Allocation cost per iteration; reuse one recordset where possible            |
| `rs.MoveNext` without `If rs.EOF Then Exit`                 | Infinite loop on empty resultset                                             |
| Closing connection inside an error handler without `On Error Resume Next` | Cleanup itself raises and masks the original error                |

## 13. Pre-flight check

- [ ] Connections and recordsets declared `As Object`
- [ ] Instantiated via `CreateObject`, not `New`
- [ ] No ADO type library reference in the `.vbp`
- [ ] `ConnectionTimeout` set before `Open`
- [ ] `CursorLocation = adUseClient` set before `Open` for disconnected pattern
- [ ] `ActiveConnection = Nothing` after `Open` for disconnected pattern
- [ ] All user-supplied values passed via `Parameters.Append`, not concatenated
- [ ] Structural SQL (table names, conditional JOINs) concatenated, not
      parameterized
- [ ] Cleanup in both `_Exit` and `_Err`
- [ ] For stored procs / output params, use `SetParameter`/`GetParameter`
      helpers (or equivalent abstraction)
