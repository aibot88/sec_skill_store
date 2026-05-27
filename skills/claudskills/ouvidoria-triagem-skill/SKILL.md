---
name: ouvidoria-triagem-municipal
description: >
  Roadmap completo end-to-end para implementar um sistema de Triagem Inteligente para Ouvidoria Municipal
  usando Node.js (Express), Cohere API (Zero-Shot Classification + NER) e deploy gratuito no Render/Railway.
  Use esta skill sempre que o usuário mencionar: ouvidoria, triagem de reclamações, classificação automática
  de chamados públicos, NER em reclamações de cidadãos, roteamento para secretaria, pipeline NLP municipal,
  ou qualquer variação de sistema de atendimento ao cidadão com IA. Inclui estrutura de arquivos, código
  de cada serviço, endpoints, exemplos few-shot em português e passos de deploy.
---

# Triagem Inteligente para Ouvidoria Municipal

Sistema end-to-end que recebe reclamações de cidadãos em texto livre, classifica automaticamente
a categoria do problema (Zero-Shot) e extrai entidades relevantes (NER), retornando JSON estruturado
para roteamento direto à secretaria responsável.

**Stack:** Node.js + Express · Cohere API (gratuita) · HTML/CSS/JS puro · Render.com

---

## Pipeline de processamento

```
Texto (Reclamação)
        │
        ▼
[Etapa 1: Zero-Shot Classification]   → categoria + confiança
        │
        ▼
[Etapa 2: NER via Chat Prompt]         → localização, organização, urgência
        │
        ▼
[Mapa categoria → secretaria]          → roteamento automático
        │
        ▼
JSON estruturado para o front-end
```

---

## Fase 0 — Setup do projeto (~30 min)

### Estrutura de arquivos

```
ouvidoria/
├── api/
│   ├── index.js               ← servidor Express principal
│   ├── routes/
│   │   └── triagem.js         ← endpoint POST /api/triagem
│   ├── services/
│   │   ├── classify.js        ← Zero-Shot via Cohere
│   │   └── ner.js             ← NER via Cohere Chat
│   └── .env                   ← variáveis de ambiente (não subir ao Git)
├── client/
│   ├── index.html             ← formulário do cidadão
│   ├── style.css
│   └── app.js                 ← fetch() para a API
├── .gitignore
└── package.json
```

### Instalação

```bash
mkdir ouvidoria && cd ouvidoria
npm init -y
npm install express cors dotenv cohere-ai
npm install --save-dev nodemon
```

### `.env` (em `api/`)

```
COHERE_API_KEY=sua_chave_aqui
PORT=3000
```

> Chave gratuita (Trial): https://dashboard.cohere.com — sem cartão de crédito.

### `.gitignore`

```
node_modules/
.env
```

---

## Fase 1 — Serviço de classificação Zero-Shot (~1h)

**Arquivo:** `api/services/classify.js`

Usa `cohere.classify()` com exemplos few-shot em português. Não precisa de dados rotulados
nem treino prévio — os exemplos ensinam o modelo na hora.

> **Regra obrigatória da API:** mínimo 2 exemplos por label.

```js
const { CohereClient } = require('cohere-ai');
const cohere = new CohereClient({ token: process.env.COHERE_API_KEY });

const LABELS = ['Infraestrutura', 'Saúde', 'Trânsito', 'Iluminação', 'Outros'];

// Exemplos few-shot (2+ por label obrigatório)
const EXAMPLES = [
  { text: 'Tem um buraco gigante na avenida principal',       label: 'Infraestrutura' },
  { text: 'Calçada quebrada na frente da escola municipal',   label: 'Infraestrutura' },
  { text: 'Falta dipirona no posto de saúde do bairro',       label: 'Saúde' },
  { text: 'Médico não apareceu na UBS hoje de manhã',         label: 'Saúde' },
  { text: 'Semáforo quebrado na esquina da rua 7 com a 15',   label: 'Trânsito' },
  { text: 'Ônibus 302 não passa há dois dias no meu bairro',  label: 'Trânsito' },
  { text: 'Poste apagado há três noites na rua das flores',   label: 'Iluminação' },
  { text: 'Toda a praça central está sem luz',                label: 'Iluminação' },
  { text: 'Quero elogiar o atendimento do servidor João',     label: 'Outros' },
  { text: 'Preciso de informação sobre alvará de funcionamento', label: 'Outros' },
];

async function classify(text) {
  const res = await cohere.classify({
    inputs: [text],
    examples: EXAMPLES,
  });
  const result = res.classifications[0];
  return {
    categoria: result.prediction,
    confianca: parseFloat(result.confidence.toFixed(2)),
  };
}

module.exports = { classify };
```

---

## Fase 2 — Serviço NER via prompt estruturado (~1h)

**Arquivo:** `api/services/ner.js`

Usa `cohere.chat()` com `preamble` (system prompt) que instrui o modelo a responder
somente em JSON. O modelo `command-r` é gratuito no plano Trial.

> **Sempre** envolva `JSON.parse()` em `try/catch` — o modelo pode ocasionalmente
> retornar texto extra antes do JSON.

```js
const { CohereClient } = require('cohere-ai');
const cohere = new CohereClient({ token: process.env.COHERE_API_KEY });

async function extractEntities(text) {
  const res = await cohere.chat({
    model: 'command-r',
    message: text,
    preamble: `Você é um extrator de entidades de reclamações municipais brasileiras.
Retorne APENAS um objeto JSON válido, sem explicações, sem markdown, sem backticks.
Formato obrigatório:
{
  "localizacao": ["lista de ruas, bairros, pontos de referência mencionados"],
  "organizacao": ["postos de saúde, escolas, órgãos públicos citados"],
  "urgencia": "alta | media | baixa"
}
Critério de urgência: alta = risco à vida ou segurança; media = impacto no cotidiano; baixa = informativo.`,
  });

  try {
    // Remove possíveis blocos de markdown caso o modelo ignore a instrução
    const clean = res.text.replace(/```json|```/g, '').trim();
    return JSON.parse(clean);
  } catch {
    // Fallback seguro se o parse falhar
    return { localizacao: [], organizacao: [], urgencia: 'media' };
  }
}

module.exports = { extractEntities };
```

---

## Fase 3 — API Express: endpoint de triagem (~45 min)

### Mapa de roteamento

**Arquivo:** `api/routes/triagem.js`

```js
const express = require('express');
const router = express.Router();
const { classify }        = require('../services/classify');
const { extractEntities } = require('../services/ner');

const ROUTING = {
  'Infraestrutura': 'Secretaria de Obras e Infraestrutura',
  'Saúde':          'Secretaria Municipal de Saúde',
  'Trânsito':       'DETRAN / Secretaria de Mobilidade',
  'Iluminação':     'Secretaria de Serviços Urbanos',
  'Outros':         'Ouvidoria Geral',
};

// POST /api/triagem
router.post('/', async (req, res) => {
  const { texto } = req.body;

  if (!texto || texto.trim().length < 10) {
    return res.status(400).json({ erro: 'Texto muito curto. Descreva melhor o problema.' });
  }

  try {
    // Roda classificação e NER em paralelo
    const [classificacao, entidades] = await Promise.all([
      classify(texto),
      extractEntities(texto),
    ]);

    return res.json({
      texto,
      categoria:           classificacao.categoria,
      confianca:           classificacao.confianca,
      entidades,
      secretaria_sugerida: ROUTING[classificacao.categoria] ?? 'Ouvidoria Geral',
      timestamp:           new Date().toISOString(),
    });
  } catch (err) {
    console.error('[triagem]', err);
    return res.status(500).json({ erro: 'Erro interno ao processar a reclamação.' });
  }
});

module.exports = router;
```

### Servidor principal

**Arquivo:** `api/index.js`

```js
require('dotenv').config();
const express = require('express');
const cors    = require('cors');
const path    = require('path');

const app  = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Serve o front-end estático
app.use(express.static(path.join(__dirname, '..', 'client')));

// Rotas da API
app.use('/api/triagem', require('./routes/triagem'));

// Health check — obrigatório para Render/Railway detectar o serviço
app.get('/health', (_, res) => res.json({ status: 'ok' }));

app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));
```

### Exemplo de resposta JSON

```json
{
  "texto": "Buraco enorme na Av. Principal perto do posto Petrobras",
  "categoria": "Infraestrutura",
  "confianca": 0.94,
  "entidades": {
    "localizacao": ["Av. Principal"],
    "organizacao": ["posto Petrobras"],
    "urgencia": "media"
  },
  "secretaria_sugerida": "Secretaria de Obras e Infraestrutura",
  "timestamp": "2024-01-15T14:32:00.000Z"
}
```

---

## Fase 4 — Interface web do cidadão (~1h)

**Arquivo:** `client/index.html`

HTML estático servido pelo próprio Express. Sem framework, sem build step.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ouvidoria Municipal</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main>
    <h1>Ouvidoria Municipal</h1>
    <p>Descreva seu problema e encaminharemos ao setor responsável.</p>

    <textarea id="texto" placeholder="Ex: Tem um buraco na Rua das Flores, perto da escola..." rows="5"></textarea>
    <button id="enviar" onclick="enviar()">Enviar reclamação</button>

    <div id="resultado" hidden>
      <div id="categoria-badge"></div>
      <p id="secretaria"></p>
      <div id="localizacao"></div>
      <div id="urgencia-badge"></div>
    </div>
  </main>
  <script src="app.js"></script>
</body>
</html>
```

**Arquivo:** `client/app.js`

```js
const URGENCIA_COR = { alta: '#dc2626', media: '#d97706', baixa: '#16a34a' };

async function enviar() {
  const texto = document.getElementById('texto').value.trim();
  if (!texto) return alert('Digite uma reclamação.');

  document.getElementById('enviar').disabled = true;
  document.getElementById('enviar').textContent = 'Processando...';

  try {
    const res  = await fetch('/api/triagem', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texto }),
    });
    const data = await res.json();

    document.getElementById('categoria-badge').textContent =
      `${data.categoria} (${Math.round(data.confianca * 100)}% confiança)`;

    document.getElementById('secretaria').textContent =
      `Encaminhado para: ${data.secretaria_sugerida}`;

    const locs = data.entidades.localizacao;
    document.getElementById('localizacao').textContent =
      locs.length ? `📍 ${locs.join(', ')}` : '';

    const urg = document.getElementById('urgencia-badge');
    urg.textContent  = `Urgência: ${data.entidades.urgencia}`;
    urg.style.color  = URGENCIA_COR[data.entidades.urgencia] ?? '#555';

    document.getElementById('resultado').hidden = false;
  } catch (err) {
    alert('Erro ao enviar. Tente novamente.');
  } finally {
    document.getElementById('enviar').disabled = false;
    document.getElementById('enviar').textContent = 'Enviar reclamação';
  }
}
```

---

## Fase 5 — Deploy no Render.com (~30 min)

### `package.json` — scripts obrigatórios

```json
{
  "scripts": {
    "start": "node api/index.js",
    "dev":   "nodemon api/index.js"
  },
  "engines": {
    "node": ">=18"
  }
}
```

### Passos no Render.com (plano Free)

```
1. Criar conta em render.com (sem cartão)
2. New > Web Service > Connect a repository (GitHub)
3. Configurar:
   - Build Command:  npm install
   - Start Command:  node api/index.js
4. Environment Variables (aba Environment):
   - COHERE_API_KEY = <sua chave>
   - NODE_ENV       = production
5. Create Web Service → aguardar build (~2 min)
6. URL pública gerada: https://seu-projeto.onrender.com
```

> **Atenção:** o plano Free "dorme" após 15 min de inatividade e leva ~30s para acordar
> na primeira requisição. Para uso em produção, considere o plano Starter ($7/mês) ou Railway.

### Railway como alternativa

```
1. railway.app > New Project > Deploy from GitHub
2. Variáveis: COHERE_API_KEY + PORT=3000
3. Deploy automático a cada push
```

---

## Resumo dos endpoints

| Método | Rota           | Descrição                        |
|--------|----------------|----------------------------------|
| `POST` | `/api/triagem` | Classifica e extrai entidades    |
| `GET`  | `/health`      | Health check para o cloud        |
| `GET`  | `/`            | Serve o front-end estático       |

---

## Limites do plano gratuito Cohere

| Recurso            | Limite Trial          |
|--------------------|-----------------------|
| `classify()`       | 1.000 req/mês         |
| `chat()` (command-r) | 1.000 req/mês       |
| Rate limit         | ~5 req/seg            |

Para produção com volume maior: plano Production (pay-as-you-go, ~$0.001/req).

---

## Checklist de entrega

- [ ] `.env` no `.gitignore`
- [ ] `try/catch` em todos os `JSON.parse()`
- [ ] `/health` respondendo `200 OK`
- [ ] Pelo menos 2 exemplos por label no `classify()`
- [ ] Testar os 5 labels manualmente antes do deploy
- [ ] Variáveis de ambiente configuradas no Render/Railway
