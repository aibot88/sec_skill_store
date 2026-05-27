---
name: photino-powershell-integration
description: "PowerShell SDK integration in Photino.NET: runspace architecture, SessionManager, streaming execution, TabExpansion2, function injection, PSObject conversion, disposal patterns. PowerShell SDK嵌入Photino.NET。 Use when: embedding PowerShell in .NET app, managing runspace lifecycle, implementing tab completion, injecting functions, serializing PSObjects"
disable-model-invocation: true
---

# PowerShell SDK Integration

Photino.NET應用嵌入PowerShell SDK之法：runspace生命周期、會話管理、流式輸出、Tab補全、函數注入及對象序列化。

## Runspace Architecture

PowerShell SDK提供進程內PowerShell引擎。每會話獲獨立runspace及隔離狀態：

```
┌──────────────────────────────────────────┐
│              SessionManager              │
│  ┌────────┐  ┌────────┐  ┌────────┐    │
│  │Session 1│  │Session 2│  │Session 3│   │
│  │Runspace │  │Runspace │  │Runspace │   │
│  │Pipeline │  │Pipeline │  │Pipeline │   │
│  └────────┘  └────────┘  └────────┘    │
│  Each session has independent:           │
│  - Variables ($PWD, $LASTEXITCODE)       │
│  - Functions (custom + injected)         │
│  - History                               │
│  - Working directory                     │
└──────────────────────────────────────────┘
```

## SessionManager

SessionManager創建、追蹤並釋放PowerShell會話：

```csharp
public sealed class SessionManager : IDisposable
{
    private readonly ConcurrentDictionary<string, PowerShellSession> _sessions = new();

    public PowerShellSession CreateSession(string sessionId)
    {
        var session = new PowerShellSession(sessionId);
        if (!_sessions.TryAdd(sessionId, session))
            throw new InvalidOperationException($"Session '{sessionId}' already exists");
        return session;
    }

    public PowerShellSession? GetSession(string sessionId)
    {
        _sessions.TryGetValue(sessionId, out var session);
        return session;
    }

    public void CloseSession(string sessionId)
    {
        if (_sessions.TryRemove(sessionId, out var session))
            session.Dispose();
    }

    public void Dispose()
    {
        foreach (var session in _sessions.Values)
            session.Dispose();
        _sessions.Clear();
    }
}
```

## PowerShellSession

每會話封裝runspace，提供執行、補全及取消功能：

```csharp
public sealed class PowerShellSession : IDisposable
{
    private readonly Runspace _runspace;
    private System.Management.Automation.PowerShell? _currentPipeline;
    private readonly string _sessionId;

    public event Action<string>? OutputReceived;
    public event Action<string>? ErrorReceived;
    public event Action<int>? ExecutionCompleted;

    public PowerShellSession(string sessionId)
    {
        _sessionId = sessionId;
        var iss = InitialSessionState.CreateDefault2();
        _runspace = RunspaceFactory.CreateRunspace(iss);
        _runspace.Open();
        InjectFunctions();
    }

    public async Task ExecuteAsync(string command, CancellationToken ct = default)
    {
        using var ps = System.Management.Automation.PowerShell.Create();
        ps.Runspace = _runspace;
        _currentPipeline = ps;

        ps.AddScript(command);

        // Stream output as it arrives
        var output = new PSDataCollection<PSObject>();
        output.DataAdded += (sender, e) =>
        {
            var data = ((PSDataCollection<PSObject>)sender!)[e.Index];
            OutputReceived?.Invoke(FormatPSObject(data));
        };

        ps.Streams.Error.DataAdded += (sender, e) =>
        {
            var err = ((PSDataCollection<ErrorRecord>)sender!)[e.Index];
            ErrorReceived?.Invoke(err.ToString());
        };

        try
        {
            await Task.Factory.FromAsync(
                ps.BeginInvoke<PSObject, PSObject>(null, output),
                ps.EndInvoke);
        }
        finally
        {
            _currentPipeline = null;
        }

        ExecutionCompleted?.Invoke(ps.HadErrors ? 1 : 0);
    }

    public void Cancel()
    {
        _currentPipeline?.Stop();
    }

    public void Dispose()
    {
        _currentPipeline?.Dispose();
        _runspace.Close();
        _runspace.Dispose();
    }
}
```

## Streaming Execution

PowerShell對象產生時即流式輸出，非命令完成後。此使實時顯示成為可能：

```csharp
// The PSDataCollection fires DataAdded for each object
var output = new PSDataCollection<PSObject>();
output.DataAdded += (sender, e) =>
{
    var data = ((PSDataCollection<PSObject>)sender!)[e.Index];
    // This fires immediately as each object is produced
    OutputReceived?.Invoke(FormatPSObject(data));
};
```

### Output Streams

PowerShell具多輸出流：

| Stream | Property | Use |
|--------|----------|-----|
| Output (1) | `PSDataCollection<PSObject>` | Normal output objects |
| Error (2) | `ps.Streams.Error` | Error records |
| Warning (3) | `ps.Streams.Warning` | Warning messages |
| Verbose (4) | `ps.Streams.Verbose` | Verbose messages |
| Debug (5) | `ps.Streams.Debug` | Debug messages |
| Information (6) | `ps.Streams.Information` | Information records |
| Progress | `ps.Streams.Progress` | Progress bars |

訂閱各流以獲全量輸出：

```csharp
ps.Streams.Warning.DataAdded += (s, e) =>
{
    var warn = ((PSDataCollection<WarningRecord>)s!)[e.Index];
    OutputReceived?.Invoke($"WARNING: {warn.Message}");
};

ps.Streams.Progress.DataAdded += (s, e) =>
{
    var progress = ((PSDataCollection<ProgressRecord>)s!)[e.Index];
    // Forward progress percentage to frontend
};
```

## TabExpansion2

PowerShell SDK含`TabExpansion2`以供命令補全：

```csharp
public CompletionResult[] GetCompletions(string input, int cursorPosition)
{
    using var ps = System.Management.Automation.PowerShell.Create();
    ps.Runspace = _runspace;

    ps.AddCommand("TabExpansion2")
      .AddParameter("inputScript", input)
      .AddParameter("cursorColumn", cursorPosition);

    var results = ps.Invoke();
    if (results.Count == 0) return Array.Empty<CompletionResult>();

    var completions = results[0].Properties["CompletionMatches"].Value;
    if (completions is not IList<CompletionResult> matches)
        return Array.Empty<CompletionResult>();

    return matches.ToArray();
}
```

### Completion Result Structure

```csharp
// Each CompletionResult has:
// - CompletionText: What to insert
// - ListItemText: What to show in the dropdown
// - ResultType: Command, ProviderItem, ParameterName, etc.
// - ToolTip: Additional description
```

### Gotcha: TabExpansion2 Runs Synchronously

`TabExpansion2`可能緩慢（100-500ms），因其審視runspace。務必：
1. 在後台線程運行，絕不阻塞UI
2. 用戶再次輸入時取消進行中補全
3. 對補全請求進行防抖（150-200ms為典型值）

```csharp
private CancellationTokenSource? _completionCts;

public async Task<CompletionResult[]> GetCompletionsAsync(string input, int cursor)
{
    // Cancel previous completion request
    _completionCts?.Cancel();
    _completionCts = new CancellationTokenSource();
    var ct = _completionCts.Token;

    return await Task.Run(() =>
    {
        ct.ThrowIfCancellationRequested();
        return GetCompletions(input, cursor);
    }, ct);
}
```

## Function Injection

向每會話runspace注入自定義PowerShell函數，以供應用特定功能：

```csharp
private void InjectFunctions()
{
    using var ps = System.Management.Automation.PowerShell.Create();
    ps.Runspace = _runspace;

    // Inject a function that the frontend can call
    ps.AddScript(@"
        function global:__beagle_notify {
            param([string]$Message, [string]$Type = 'info')
            $global:__service.Notify($Message, $Type)
        }

        function global:__beagle_setvar {
            param([string]$Name, [object]$Value)
            $global:__service.SetVariable($Name, $Value)
        }
    ");

    ps.Invoke();
}
```

### The `$global:__service` Pattern

通過全局變量向PowerShell暴露C#對象：

```csharp
// Set a C# service object accessible from PowerShell
_runspace.SessionStateProxy.SetVariable("__service", new PowerShellServiceBridge(this));

// The bridge exposes methods that PowerShell can call
public class PowerShellServiceBridge
{
    private readonly PowerShellSession _session;

    public PowerShellServiceBridge(PowerShellSession session)
        => _session = session;

    public void Notify(string message, string type)
    {
        _session.NotificationReceived?.Invoke(message, type);
    }

    public void SetVariable(string name, object value)
    {
        _session.VariableChanged?.Invoke(name, value);
    }
}
```

## PSObject Conversion

PowerShell返回`PSObject`包裝器。將其轉換為前端JSON友好結構：

```csharp
private static string FormatPSObject(PSObject obj)
{
    if (obj.BaseObject is string s)
        return s;

    // For complex objects, extract properties into a dictionary
    var dict = new Dictionary<string, object?>();
    foreach (var prop in obj.Properties)
    {
        try
        {
            dict[prop.Name] = prop.Value?.ToString();
        }
        catch
        {
            dict[prop.Name] = null;
        }
    }

    return JsonSerializer.Serialize(dict);
}
```

### Rich Object Rendering

已知類型提供結構化輸出：

```csharp
private static object ConvertPSObject(PSObject obj)
{
    return obj.BaseObject switch
    {
        string s => new { type = "text", value = s },
        System.Diagnostics.Process p => new
        {
            type = "process",
            pid = p.Id,
            name = p.ProcessName,
            cpu = p.TotalProcessorTime,
            memory = p.WorkingSet64
        },
        System.IO.FileInfo f => new
        {
            type = "file",
            name = f.Name,
            size = f.Length,
            modified = f.LastWriteTime
        },
        _ => new { type = "object", properties = ExtractProperties(obj) }
    };
}
```

## Disposal Pattern

PowerShell runspace持有原生資源，正確釋放至關重要：

```csharp
public sealed class PowerShellSession : IDisposable
{
    private bool _disposed;

    public void Dispose()
    {
        if (_disposed) return;
        _disposed = true;

        // Cancel any running pipeline first
        try { _currentPipeline?.Stop(); } catch { }
        try { _currentPipeline?.Dispose(); } catch { }

        // Close runspace (blocks until pipeline finishes)
        try
        {
            if (_runspace.RunspaceStateInfo.State == RunspaceState.Opened)
                _runspace.Close();
        }
        catch { }

        _runspace.Dispose();
    }
}
```

### Disposal Order

1. 停止運行中管道
2. 關閉runspace（優雅停機）
3. 釋放runspace（釋放原生資源）
4. 從SessionManager移除

管道執行中絕不釋放runspace——先調用`Stop()`。

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `PSInvalidOperationException: Runspace is not opened` | Using disposed session | Check `_disposed` before operations |
| Memory leak in long sessions | Unreleased pipelines | Always dispose `PowerShell` objects |
| Deadlock in event handlers | Blocking STA thread | Use `_ = HandleAsync()` pattern |
| Slow first command | Runspace initialization | Pre-warm with dummy command on creation |
| `ApartmentState` error | Wrong thread model | Ensure `[STAThread]` on Main |
