---
name: developer-delphi-to-fpc-horse-basic-auth
description: Middleware HTTP Basic Authentication para Horse. Cobre HorseBasicAuthentication (callback de validação, configuração THorseBasicAuthenticationConfig), Header, RealmMessage, SkipRoutes e proteção por rota. Fonte: app/package/docs/pacotes/horse-basic-auth.md.
model: sonnet
thinking: minimal
category: project
license: MIT
copyright: "Copyright (c) 2026 CSL Tech Solutions"
company: "CSL Tech Solutions"
author: "Claiton de Souza Linhares"
---

# developer-delphi-to-fpc-horse-basic-auth

## Versão interna (ficheiro)

| Campo | Valor |
| --- | --- |
| **FileVersion** | 1.0.0 |
| **Política** | `.cursor/VERSION.md` |

## Responsabilidade única

Middleware de autenticação HTTP Basic (cabeçalho `Authorization: Basic ...`) para Horse.

## When to use

- Validar username/password via cabeçalho Basic Auth
- Proteger rotas com autenticação simples
- Integração servidor-a-servidor (Basic Auth para APIs internas)

## When NOT to use

- Autenticação JWT Bearer → `developer-delphi-to-fpc-horse-jwt`
- Geração/validação de tokens JWT → `developer-delphi-to-fpc-horse-security`

## Documento canônico

`app/package/docs/pacotes/horse-basic-auth.md`

---

## HorseBasicAuthentication — sobrecargas

| Sobrecarga | Descrição |
| --- | --- |
| `HorseBasicAuthentication(callback)` | Middleware com validação custom |
| `HorseBasicAuthentication(callback, config)` | Com configuração avançada |

### IHorseBasicAuthenticationConfig — configuração

| Método | Descrição |
| --- | --- |
| `New` | Cria instância |
| `Header(value)` | Cabeçalho da credencial (padrão: `Authorization`) |
| `RealmMessage(value)` | Mensagem do realm no challenge 401 |
| `SkipRoutes([...])` | Rotas que ignoram autenticação |

---

## Exemplos

### Global — todas as rotas

```delphi
uses Horse, Horse.BasicAuthentication;

begin
  THorse.Use(HorseBasicAuthentication(
    function(const AUsername, APassword: string): Boolean
    begin
      Result := AUsername.Equals('user') and APassword.Equals('password');
    end));

  THorse.Get('/ping',
    procedure(Req: THorseRequest; Res: THorseResponse; Next: TProc)
    begin
      Res.Send('pong');
    end);

  THorse.Listen(9000);
end.
```

### Com configuração completa

```delphi
THorse.Use(HorseBasicAuthentication(
  ValidarCredenciais,
  THorseBasicAuthenticationConfig.New
    .Header('Authorization')
    .RealmMessage('GestorERP API')
    .SkipRoutes(['/health', '/swagger/doc/html', '/auth/refresh'])
));
```

### Validação contra base de dados

```delphi
function ValidarCredenciais(const AUsername, APassword: string): Boolean;
var LQuery: TFDQuery;
begin
  Result := False;
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := DM.Conexao;
    LQuery.SQL.Text :=
      'SELECT 1 FROM usuarios WHERE login = :u AND senha_hash = :p AND ativo = 1';
    LQuery.ParamByName('u').AsString := AUsername;
    LQuery.ParamByName('p').AsString := HashSenha(APassword);
    LQuery.Open;
    Result := not LQuery.IsEmpty;
  finally
    LQuery.Free;
  end;
end;
```

### Proteção por rota (AddCallback)

```delphi
// Rota pública
THorse.Get('/health',
  procedure(Req: THorseRequest; Res: THorseResponse; Next: TProc)
  begin
    Res.Send('ok');
  end);

// Rotas privadas com Basic Auth
THorse
  .AddCallback(HorseBasicAuthentication(ValidarCredenciais))
  .Get('/admin/report', ProcRelatorio);
```

### Lazarus / FPC

```delphi
{$MODE DELPHI}{$H+}
uses Horse, Horse.BasicAuthentication, SysUtils;

function DoLogin(const AUsername, APassword: string): Boolean;
begin
  Result := AUsername.Equals('user') and APassword.Equals('password');
end;

begin
  THorse.Use(HorseBasicAuthentication(DoLogin));
  THorse.Get('/ping', GetPing);
  THorse.Listen(9000);
end.
```

---

## Notas GestorERP

- Basic Auth apenas em canais **HTTPS** — nunca em HTTP puro
- Hashear passwords com BCrypt ou SHA-256+salt (nunca plaintext)
- Preferir JWT para sessões longas; Basic Auth para integrações servidor-a-servidor
- `unit` a usar: `Horse.BasicAuthentication`

---

## Changelog (este arquivo)

- 1.0.0 (12/04/2026): Criação — skill middleware Basic Auth.
