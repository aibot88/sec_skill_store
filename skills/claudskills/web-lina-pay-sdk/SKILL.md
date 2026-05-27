---
name: web-lina-pay-sdk
description: >-
  Documentação e integração do pacote npm @lina-openx/web-lina-pay-sdk (Lina OpenX / Open Finance).
  Use este skill sempre que o utilizador pedir ajuda com este SDK: exemplos de chamadas, payloads TypeScript,
  tipos exportados, fluxos de consentimento, payment request, getPaymentRequest, pagamento OAuth, enrollment e FIDO,
  participantes, configure / ambientes IAM e API, LinaPayError, ou organização do repo web-lina-pay-sdk.
  Inclua também pagamento automático/recorrente: createAutomaticPaymentRequest, getAutomaticPaymentRequest,
  CreateAutomaticPaymentRequest, AutomaticPaymentRequestCreated, GetAutomaticPaymentRequest, AutomaticPaymentRequest,
  autenticação com LinaPayCredentials ou TokenCredentials (access_token direto, sem IAM no SDK para esse fluxo),
  sweeping/automatic. Inclua contas de recebimento e identificadores bancários (ISPB): createReceivingAccount,
  listReceivingAccounts, getReceivingAccount, updateReceivingAccount, deleteReceivingAccount, getBankIdentifiers,
  getBankIdentifier, tipos ReceivingAccount, BankIdentifier, GetBankIdentifiersRequest, GetBankIdentifierRequest,
  rotas sub-tenants-accounts (incl. /bank-identifiers), RECEIVING_ACCOUNTS. Prefira consultar README.md na raiz
  e reference.md nesta pasta.
---

# Web Lina Pay SDK — skill de documentação

Skill para orientar assistentes e desenvolvedores com base na documentação oficial do SDK e nas tipagens de referência.

## Fonte da verdade (ordem de consulta)

1. **`README.md`** na raiz do repositório — descrição, instalação, métodos, exemplos, estrutura de pastas, execução local, erros e tipos principais.
2. **`reference.md`** (nesta pasta) — catálogo consolidado de tipagens alinhado ao README e ao que o pacote exporta em `src/types/index.ts` e `src/index.ts` (inclui **pagamento automático / recorrente** e **contas de recebimento** em § dedicados).
3. **Código em `src/`** — quando o README não cobrir um detalhe ou houver divergência; prefira citar arquivos concretos (`controllers/`, `services/`, `types/`).

## Mapa do README (seções → conteúdo)

| Seção README | O que cobre |
|--------------|-------------|
| Descrição | Escopo do SDK (consentimento, payment request, pagamento automático/recorrente, contas de recebimento do subtenant, consulta de payment request, pagamento, enrollment, participantes, FIDO/WebAuthn). |
| Instalação | `npm` / `yarn` / `pnpm` para `@lina-openx/web-lina-pay-sdk`. |
| Como usar → Importação | Funções e `LinaPayError` exportados pelo pacote. |
| Configuração inicial | `configure({ iamBaseUrl, apiBaseUrl })` — HML vs produção. |
| Métodos 1–12 + §13 contas / ISPB | API pública: 1–11 README; **§12** pagamento automático (**12.1** criação, **12.2** consulta `getAutomaticPaymentRequest`); **§13** cinco funções de contas de recebimento + **§13.6–13.7** `getBankIdentifiers` / `getBankIdentifier` (identificadores bancários); ver tabela abaixo. |
| Organização de pastas | `src/config`, `controllers`, `services`, `types`, `utils`, `index.ts`. |
| Como rodar localmente | Node 18+, scripts `dev`, `test`, `format`, `build`, `ci`, clone, pasta `example/`. |
| Tratamento de erros | `try/catch`, `instanceof LinaPayError`, `statusCode`. |
| Tipos principais | Credenciais (`LinaPayCredentials`, **`TokenCredentials`** para automatic-payments e para contas/ISPB quando aplicável), consentimento, `CreatePaymentRequestDTO`, `CreateAutomaticPaymentRequest` / `AutomaticPaymentRequestCreated` / **`GetAutomaticPaymentRequest`** / **`AutomaticPaymentRequest`**, `ReceivingAccount`, **`BankIdentifier`**, **`GetBankIdentifiersRequest`**, **`GetBankIdentifierRequest`**, DTOs de contas de recebimento, `PaymentRequestCreated`, `PaymentRequestData` + `PaymentRequestPaymentItem`, demais tipos citados nos exemplos. |
| Licença / Suporte | MIT, contatos e issues GitLab. |

## Métodos públicos (ordem do README)

| # | Função | Resumo |
|---|--------|--------|
| 1 | `configure` | URLs base IAM e API (`LinaPayConfig`). |
| 2 | `createConsent` | Consentimento de pagamento (`CreateConsentRequest` → `CreateConsentResponse`). |
| 3 | `createPayment` | Pagamento pós-OAuth (`CreatePaymentRequest`: state, code, idToken, tenantId → `CreatePaymentResponse`). |
| 4 | `createPaymentRequest` | Solicitação de pagamento distinta de `createPayment` (`CreatePaymentRequestDTO` → `Promise<PaymentRequestCreated>`: `id`, `redirectUri`); validação Zod; erro `Invalid payload`. |
| 5 | `getPaymentRequest` | Consulta detalhes (`GET` …/requests/:id); `(credentials, id)` → `Promise<PaymentRequestData>`; o `id` costuma ser `PaymentRequestCreated.id`; SDK devolve só o `data` do envelope; datas ISO em **string** (não `Date` em runtime) — ver tabela de campos no README §5. |
| 6 | `createEnrollment` | Enrollment FIDO (`CreateEnrollmentRequest` → `CreateEnrollmentResponse`). |
| 7 | `registerDevice` | Callback pós-enrollment (`RegisterDeviceRequest` → tipo exportado como `Enrollment`). |
| 8 | `getEnrollmentList` | Lista por CPF (`EnrollmentList`). |
| 9 | `revokeEnrollment` | Revoga por ID (`RevokeEnrollmentResponse`). |
| 10 | `createPaymentWithEnrollment` | Pagamento com enrollment (`PaymentWithEnrollmentRequest` → `RetornoJsrPaymentDto`). |
| 11 | `getParticipants` | Participantes (`Participant[]`). |
| 12.1 | `createAutomaticPaymentRequest` | **Criação** de solicitação de pagamento automático/recorrente. Parâmetro **`credentials`**: `LinaPayCredentials` (IAM + cache) **ou** `TokenCredentials` (`access_token` Bearer já obtido). `CreateAutomaticPaymentRequest` → `Promise<AutomaticPaymentRequestCreated>`; `POST` em `PAYMENTS_REQUEST`; validação Zod; `Invalid payload` se falhar. |
| 12.2 | `getAutomaticPaymentRequest` | **Consulta** por `paymentRequestId`: `GET …/payments/request/:paymentRequestId` (base `PAYMENTS_REQUEST`). Mesmo union de **`credentials`** que 12.1. Payload `GetAutomaticPaymentRequest`; retorno `Promise<AutomaticPaymentRequest>` (unwrap `data`). Validação `getAutomaticPaymentRequestSchema` / `validateGetAutomaticPaymentRequestPayload`. |
| 13 | `createReceivingAccount` | `POST` em `apiBaseUrl` + **`/api/v1/sub-tenants-accounts/:subTenantId/receiving-accounts`** — corpo só **`account`** (JSON). `CreateReceivingAccountRequest` → `Promise<ReceivingAccount>`. Validação em `receiving-accounts.utils`. |
| 14 | `listReceivingAccounts` | `GET …/:subTenantId/receiving-accounts`. Payload `{ subTenantId }` → `Promise<ReceivingAccount[]>`. |
| 15 | `getReceivingAccount` | `GET …/:subTenantId/:accountId`. Exige **`accountId`**. → `Promise<ReceivingAccount>`. |
| 16 | `updateReceivingAccount` | `PATCH …/:subTenantId/:accountId` — corpo serializado = **payload completo** (`UpdateReceivingAccountRequest`). → `Promise<ReceivingAccount>`. |
| 17 | `deleteReceivingAccount` | `DELETE …/:subTenantId/:accountId`. Exige **`accountId`**. → `Promise<ReceivingAccount>`. |
| 18 | `getBankIdentifiers` | `GET …/sub-tenants-accounts/bank-identifiers` com query opcional **`search`** / **`limit`** (só enviados se não vazios). `GetBankIdentifiersRequest` → `Promise<BankIdentifier[]>`. **`LinaPayCredentials | TokenCredentials`**. Validação Zod (`getBankIdentifiersRequestSchema`). |
| 19 | `getBankIdentifier` | `GET …/sub-tenants-accounts/bank-identifiers/:bankIspb` (ISPB na rota, URL-encoded). `GetBankIdentifierRequest` → `Promise<BankIdentifier>`. **`LinaPayCredentials | TokenCredentials`**. Validação Zod (`bankIspb` não vazio). |

## Distinções importantes (evitar confusão)

- **`createPayment`** vs **`createPaymentRequest`**: o primeiro finaliza fluxo com tokens OAuth; o segundo envia dados do pagamento (valor, credor, redirect, schedule etc.) e retorna **`PaymentRequestCreated`** (`id`, `redirectUri`).
- **`createPaymentRequest`** vs **`getPaymentRequest`**: o primeiro cria a solicitação (`POST`) e retorna **`PaymentRequestCreated`** (`id`, `redirectUri`); o segundo consulta (`GET`) e retorna **`PaymentRequestData`** (objeto completo tipado no README e em `reference.md`).
- **`createPaymentRequest`** vs **`createAutomaticPaymentRequest`**: ambos usam `POST` no mesmo path base de pagamentos (`PAYMENTS_REQUEST`), mas o **payload** é diferente — DTO de solicitação simples (`redirectUri`, `value`, `creditor`, `schedule`…) vs **consentimento recorrente** (`redirectUrl`, `details`, `recurringConsent` com `automatic` ou `sweeping`). Retornos distintos: `PaymentRequestCreated` (`id`) vs **`AutomaticPaymentRequestCreated`** (`paymentRequestId`, `redirectUrl`). Ver README §12.1 e `reference.md` § pagamento automático.
- **`createAutomaticPaymentRequest`** vs **`getAutomaticPaymentRequest`**: primeiro cria (`POST`); segundo consulta (`GET` com `paymentRequestId` no path). Ambos aceitam **`LinaPayCredentials | TokenCredentials`** — ver README §12.
- **`LinaPayCredentials`** vs **`TokenCredentials`**: no primeiro o SDK obtém o Bearer no IAM quando `subtenantId` está presente; com **`TokenCredentials`** o integrador passa **`access_token`** já válido. **Pagamento automático** e **contas de recebimento / identificadores bancários** (`createReceivingAccount` … `getBankIdentifier`) aceitam o **union** `LinaPayCredentials | TokenCredentials` no primeiro argumento — ver controllers. Outros métodos (ex.: consentimento clássico, `createPaymentRequest`) podem continuar só com `LinaPayCredentials`; confirmar assinatura em `src/index.ts` se houver dúvida.
- **`CreatePaymentRequest`** (OAuth) vs **`CreatePaymentRequestDTO`** (solicitação de pagamento): nomes parecidos, payloads completamente diferentes — ver `reference.md`.
- **Credenciais IAM** (`LinaPayCredentials.subtenantId` / `subtenantSecret`) vs **`subTenantId` no payload** das contas de recebimento: o primeiro serve para obter o Bearer; o segundo é o segmento **`:subTenantId`** na URL da API de contas (`/api/v1/sub-tenants-accounts/...`). Podem coincidir ou não, conforme o modelo da integração — ver README §13.
- **`listReceivingAccounts`** vs **`getReceivingAccount` / `deleteReceivingAccount`**: a listagem valida só `subTenantId`; consulta e exclusão exigem também **`accountId`** (schemas distintos em `receiving-accounts.utils.ts`).
## Como responder perguntas sobre o SDK

- Preferir exemplos em TypeScript alinhados ao README (nomes de campos e enums: `PESSOA_NATURAL`, `CACC`, dias da semana em português com `_FEIRA`, etc.).
- Mencionar `configure` quando o ambiente não for o padrão.
- Para payloads de **`createPaymentRequest`**, lembrar que a validação runtime exige `schedule` presente (pode ser `{}`) conforme documentação do README.
- Para **`createAutomaticPaymentRequest`** e **`getAutomaticPaymentRequest`**, o primeiro argumento pode ser **`{ access_token }`** (`TokenCredentials`) quando o token já existir; caso contrário **`{ subtenantId, subtenantSecret }`**. Resolução em `resolveAutomaticPaymentsAccessToken` em `automatic-payments.controller.ts`.
- Para **`createAutomaticPaymentRequest`**, o payload é inferido do schema Zod (`CreateAutomaticPaymentRequest`): `recurringConfiguration` deve ter **apenas um** ramo (`automatic` **ou** `sweeping`); dentro de `sweeping.periodicLimits`, **apenas um** de `day` | `week` | `month` | `year`. Campos monetários/configuração vêm em grande parte como **string** (ex.: `amount`, `totalAllowedAmount`). Detalhe completo em **`reference.md`**.
- Para **`getAutomaticPaymentRequest`**, validar `paymentRequestId` não vazio; retorno **`AutomaticPaymentRequest`** é extenso — remeter a `reference.md` / `automatic-payment.types.ts`.
- Para **`getPaymentRequest`**, usar `created.id` após `createPaymentRequest` (padrão do README §5); implementação em `src/controllers/payment.controller.ts` / `getPaymentRequestService` em `src/services/payment.service.ts`.
- Para **contas de recebimento** e **identificadores bancários**, lembrar validação Zod (`Invalid payload`): listagem de contas ≠ por `accountId`; **`updateReceivingAccount`** envia o objeto payload completo no `PATCH` (inclui `subTenantId` e `accountId` no corpo, conforme serviço atual). **`getBankIdentifiers`** / **`getBankIdentifier`** não usam `subTenantId` na URL (endpoints globais sob `RECEIVING_ACCOUNTS`); retornam **`BankIdentifier`** (`name`, `ispb`).
- Tipos exportados: **`PaymentRequestCreated`**, **`PaymentRequestData`**, **`PaymentRequestPaymentItem`**, **`TokenCredentials`**, **`CreateAutomaticPaymentRequest`**, **`AutomaticPaymentRequestCreated`**, **`GetAutomaticPaymentRequest`**, **`AutomaticPaymentRequest`**, **`ReceivingAccount`**, **`BankIdentifier`**, **`GetBankIdentifiersRequest`**, **`GetBankIdentifierRequest`** e DTOs de contas de recebimento — ver README “Tipos principais” e `reference.md`.
- Erros: descrever `LinaPayError` e uso de `statusCode` quando aplicável.

## Progressive disclosure

- Para **assinaturas completas, unions e interfaces aninhadas**, abrir **`reference.md`** nesta pasta em vez de duplicar tudo no corpo deste skill (inclui § **Autenticação** com `TokenCredentials`, § **Pagamento automático** com criação/consulta e tipo `AutomaticPaymentRequest`, e § **Contas de recebimento** com **identificadores bancários** e tipos `BankIdentifier` / requests associados).
- Para **comportamento HTTP ou endpoints**, seguir `src/config/environment.ts` (`ENDPOINTS`: `RECEIVING_ACCOUNTS` = `/api/v1/sub-tenants-accounts`, `PAYMENTS_REQUEST`, etc.) e serviços em `src/services/` (`receiving-accounts.service.ts`, `automatic-payments.service.ts`).

## Idioma

- Responder em **português** quando o usuário do projeto utilizar português (alinhado ao README e ao repositório).
