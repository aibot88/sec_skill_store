---
name: hermes-agent-inline-logging
description: Logging automático 100% inline no Hermes Agent via sitecustomize.py — monkey-patch de model_tools.handle_function_call e AIAgent.run_conversation. Loga tool calls + mensagens user/agent no SQLite automaticamente. Sobrevive a pip install -U.
---

# Hermes Agent — Inline Logging via sitecustomize.py

## Problema Original

O `hermes-session-logger` é procedural/manual — o agente precisa chamar `log()` explicitamente. Cron jobs não funcionam porque não conseguem ver o contexto em memória da sessão ativa. Precisávamos de logging **automático e inline**.

## Arquitetura Implementada

### Arquivo: `~/.hermes/hermes-agent/venv/lib/python3.11/site-packages/sitecustomize.py`

Python auto-importa `sitecustomize.py` de qualquer package/site-packages ao iniciar. O plugin:

1. **Hook de import** (`sys.meta_path`) — detecta quando `model_tools` ou `run_agent` forem carregados
2. **Aplica monkey-patch** — substitui `handle_function_call` e `AIAgent.run_conversation` por wrappers que logam antes/depois
3. **Loga no SQLite** — via `hermes_logger.py` em `~/.hermes/`

### O que é logado

| Evento | Como | Tabela |
|--------|------|--------|
| `user_message` | Patch em `AIAgent.run_conversation` | `events` |
| `agent_response` | Patch em `AIAgent.run_conversation` | `events` |
| `tool_call_start` | Patch em `handle_function_call` | `events` |
| `tool_call_result` | Patch em `handle_function_call` | `events` |

## Armadilha Crítica: "multiple values for tool_call_id"

### O Problema

`run_agent.py` chama `handle_function_call` de **duas formas diferentes**:

```python
# Forma A — tool_call_id como KEYWORD
handle_function_call(fn, args, task_id, tool_call_id=tc.id, session_id=s, ...)

# Forma B — tool_call_id como 5o POSICIONAL
handle_function_call(fn, args, task_id, "tc_id_val", session_id=s, ...)
```

O wrapper precisa aceitar **ambos os padrões** sem duplicar o argumento.

### Solução Anti-Regressão (Definitiva)

```python
def _logged_handle_function_call(
    function_name,
    function_args,
    task_id=None,
    *args_extra,      # capta tool_call_id SE vier como 5o positional
    **kwargs          # capta tool_call_id SE vier como keyword
):
    # 1. Extrai tool_call_id de kwargs (se existir)
    tool_call_id = kwargs.pop('tool_call_id', None)

    # 2. Se não veio em kwargs, verifica se veio como positional (5a posição)
    if tool_call_id is None and args_extra:
        tool_call_id = args_extra[0]

    # 3. Chama original — tool_call_id vai OU como positional OU como keyword (nunca ambos)
    if tool_call_id is not None:
        result = _original(
            function_name, function_args, task_id,
            tool_call_id,           # 4o posicional — NUNCA como keyword
            **kwargs
        )
    else:
        result = _original(
            function_name, function_args, task_id,
            **kwargs
        )
```

**Regra de ouro:** `tool_call_id` NUNCA é parâmetro nomeado do wrapper. Sempre extraído via `pop()` de kwargs ou `args_extra`, e passado ao original ou como positional ou como keyword — nunca os dois.

## Arquivo Completo (sitecustomize.py)

```python
#!/usr/bin/env python3
"""
Hermes Auto-Logging Plugin — sitecustomize.py
===============================================
Faz monkey-patch de:
  1. model_tools.handle_function_call — logging de toda tool call
  2. run_agent.AIAgent.run_conversation — logging de mensagens user/agent

Sobrevive a pip install -U hermes-agent porque vive no
venv/site-packages/ (pip não sobrescreve sitecustomize.py).
"""
import sys
import os

HERMES_LOGGER_PATH = os.path.expanduser("~/.hermes")
_hermes_logger = None
_logger_available = False

if HERMES_LOGGER_PATH not in sys.path:
    sys.path.insert(0, HERMES_LOGGER_PATH)

try:
    import hermes_logger as _hermes_logger
    _logger_available = True
except Exception:
    _logger_available = False
    _hermes_logger = None


# ════════════════════════════════════════════════════════════
# PATCH 1 — handle_function_call (tool calls)
# ════════════════════════════════════════════════════════════
_model_tools_patched = False


def _apply_model_tools_patch():
    global _model_tools_patched

    if not _logger_available or _hermes_logger is None:
        return
    if _model_tools_patched:
        return

    try:
        import model_tools as mt
    except ImportError:
        return

    if hasattr(mt, '_hermes_logging_patched'):
        _model_tools_patched = True
        return

    _original = mt.handle_function_call

    def _logged_handle_function_call(
        function_name,
        function_args,
        task_id=None,
        *args_extra,      # tool_call_id se vier como 5o positional
        **kwargs
    ):
        # Log do início
        try:
            _hermes_logger.log_tool_auto(function_name, function_args, started=True)
        except Exception:
            pass

        # Extrai tool_call_id SEM duplicação
        tool_call_id = kwargs.pop('tool_call_id', None)
        if tool_call_id is None and args_extra:
            tool_call_id = args_extra[0]

        # Chama original — tool_call_id vai posicional OU keyword, nunca ambos
        if tool_call_id is not None:
            result = _original(
                function_name, function_args, task_id,
                tool_call_id,
                **kwargs
            )
        else:
            result = _original(
                function_name, function_args, task_id,
                **kwargs
            )

        # Log do resultado
        try:
            _hermes_logger.log_tool_auto(function_name, function_args, result, started=False)
        except Exception:
            pass

        return result

    mt.handle_function_call = _logged_handle_function_call
    mt._hermes_logging_patched = True
    _model_tools_patched = True


class _ModelToolsPatcher:
    def find_module(self, fullname, path=None):
        if fullname == 'model_tools':
            return self
        return None

    def load_module(self, fullname):
        sys.meta_path = [x for x in sys.meta_path if x is not self]
        import importlib
        mod = importlib.import_module(fullname)
        _apply_model_tools_patch()
        return mod


# ════════════════════════════════════════════════════════════
# PATCH 2 — AIAgent.run_conversation (mensagens user/agent)
# ════════════════════════════════════════════════════════════
_run_agent_patched = False


def _apply_run_agent_patch():
    global _run_agent_patched

    if not _logger_available or _hermes_logger is None:
        return
    if _run_agent_patched:
        return

    try:
        from run_agent import AIAgent
    except ImportError:
        return

    if hasattr(AIAgent, '_hermes_msg_logging_patched'):
        _run_agent_patched = True
        return

    _original_run_conv = AIAgent.run_conversation

    def _logged_run_conversation(
        self,
        user_message,
        system_message=None,
        conversation_history=None,
        task_id=None,
        stream_callback=None,
        persist_user_message=None,
        **kwargs
    ):
        sess_id = task_id or getattr(self, 'session_id', None) or 'cli'
        if not _hermes_logger.get_active_session():
            _hermes_logger.set_active_session(sess_id)

        # Loga mensagem do usuário (entrada)
        msg_to_log = persist_user_message if persist_user_message else user_message
        if msg_to_log:
            try:
                _hermes_logger.log_user(sess_id, str(msg_to_log)[:10000])
            except Exception:
                pass

        # Chama original
        result = _original_run_conv(
            self, user_message,
            system_message=system_message,
            conversation_history=conversation_history,
            task_id=task_id,
            stream_callback=stream_callback,
            persist_user_message=persist_user_message,
            **kwargs
        )

        # Loga resposta do agent (saída)
        if result and isinstance(result, dict):
            final = result.get('final_response', '')
            if final:
                try:
                    _hermes_logger.log_agent(sess_id, str(final)[:10000])
                except Exception:
                    pass

        return result

    AIAgent.run_conversation = _logged_run_conversation
    AIAgent._hermes_msg_logging_patched = True
    _run_agent_patched = True


class _RunAgentPatcher:
    def find_module(self, fullname, path=None):
        if fullname == 'run_agent':
            return self
        return None

    def load_module(self, fullname):
        sys.meta_path = [x for x in sys.meta_path if x is not self]
        import importlib
        mod = importlib.import_module(fullname)
        _apply_run_agent_patch()
        return mod


# ─── Instala hooks ──────────────────────────────────────────
if _logger_available:
    sys.meta_path.insert(0, _ModelToolsPatcher())
    sys.meta_path.insert(0, _RunAgentPatcher())
```

## Pré-requisitos: hermes_logger.py

O `hermes_logger.py` precisa existir em `~/.hermes/` com estas funções:

```python
def log_user(session_id, message): ...
def log_agent(session_id, response): ...
def log_tool_auto(function_name, function_args, result=None, started=True): ...
def set_active_session(session_id): ...
def get_active_session(): ...
```

## Verificação Pós-Instalação

```bash
cd ~/.hermes/hermes-agent && source venv/bin/activate
python -c "from model_tools import handle_function_call; print('model_tools OK')"
python -c "from run_agent import AIAgent; print('AIAgent patched:', hasattr(AIAgent, '_hermes_msg_logging_patched'))"
hermes tools list  # não pode crashar

# Verificar logs
sqlite3 ~/.hermes/hermes_sessions.db "SELECT event_type, COUNT(*) FROM events GROUP BY event_type;"
```

Resultado esperado: `user_message`, `agent_response`, `tool_call_start`, `tool_call_result`.

## Garantias

- **100% automático** — não requer chamada explícita de `log()` em nenhum lugar
- **Todas as plataformas** — CLI, Telegram, gateway (o hook funciona globalmente)
- **Resiste a updates** — vive em `venv/site-packages/`, pip não sobrescreve
- **Thread-safe** — hermes_logger usa `threading.Lock`
- **Anti-regressão** — `tool_call_id` nunca duplicado

## NÃO Confundir Com

- **Callback nativo do AIAgent** — era a abordagem anterior (skill antiga); não foi o que funcionou
- **Cron job de logging** — inútil para contexto inline
- **Git hooks** — não relacionado

## Histórico

- 15/04/2026 — Primeira versão com monkey-patch de `handle_function_call`; bug "multiple values for tool_call_id" identificado e correção inicial
- 16/04/2026 — Versão definitiva com `*args_extra` + `**kwargs`; adicionada captura de `user_message` e `agent_response` via patch em `AIAgent.run_conversation`; todas as ferramentas testadas e funcionando
