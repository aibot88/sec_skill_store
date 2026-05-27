---
name: Composio Toolkit - Integración de Servicios para Agentes IA
description: Guía técnica completa para integrar 250+ servicios externos con agentes IA usando Composio. Cubre instalación, autenticación OAuth, gestión de herramientas, triggers y flujos multi-servicio.
triggers:
  - oauth_flow_initiated
  - external_event_detected
  - tool_execution_request
  - service_connection_changed
  - trigger_webhook_received
---

## ¿Qué es Composio?

Composio es un **toolkit de código abierto** que permite a agentes IA y LLMs ejecutar acciones en más de 250 servicios externos. A diferencia de APIs tradicionales, Composio optimiza herramientas para que agentes IA las usen de forma natural, con manejo automático de autenticación, validación de parámetros y gestión de errores.

### Características principales:
- Conexión uniforme a múltiples servicios (Gmail, Slack, GitHub, Jira, HubSpot, etc.)
- Gestión de OAuth 2.0 integrada
- Descubrimiento dinámico de herramientas
- Sistema de triggers para eventos externos
- Validación automática de argumentos
- Soporte nativo para agentes OpenAI, Claude y frameworks personalizados

---

## Instalación

```bash
# Instalación base
npm install composio-core @composio/core

# Con integración OpenAI (recomendado)
npm install composio-core @composio/openai @openai/agents

# Con soporte Vercel AI SDK
npm install composio-core ai
```

### Configuración inicial del cliente:

```javascript
import { Composio } from 'composio-core';

const composio = new Composio({
  apiKey: process.env.COMPOSIO_API_KEY,
  baseUrl: 'https://api.composio.dev' // Default
});
```

---

## Autenticación y Gestión de OAuth

Composio maneja OAuth 2.0 automáticamente. Flujo típico:

### 1. Crear configuración de autenticación:

```javascript
const authConfig = await composio.createAuthConfig({
  integrationName: 'gmail',
  scopes: ['https://www.googleapis.com/auth/gmail.readonly'],
  redirectUrl: 'http://localhost:3000/auth/callback'
});
```

### 2. Iniciar flujo OAuth:

```javascript
// Obtener URL de autorización para presentar al usuario
const { authUrl } = authConfig;
console.log(`Abre esta URL: ${authUrl}`);

// Usuario autoriza y retorna con código
const urlCallback = 'http://localhost:3000/auth/callback?code=AUTH_CODE';
```

### 3. Manejar callback:

```javascript
app.get('/auth/callback', async (req, res) => {
  const { code } = req.query;
  
  const connection = await composio.completeOAuthFlow({
    configId: authConfig.configId,
    code: code,
    userId: req.session.userId
  });
  
  // Estado: INITIATED → ACTIVE
  console.log(`Conexión estado: ${connection.status}`); // ACTIVE
});
```

---

## Servicios Soportados

Composio integra servicios en estas categorías:

### Comunicación
- **Gmail** (leer, enviar, drafts, etiquetas)
- **Slack** (mensajes, canales, threads, uploads)
- **Discord** (servidores, canales, mensajes)
- **Microsoft Teams** (chats, reuniones, archivos)
- **Telegram** (mensajes, grupos)

### Gestión de Proyectos
- **Jira** (issues, sprints, workflows, comentarios)
- **Asana** (tareas, proyectos, portfolios)
- **Linear** (issues, sprints, estados)
- **Trello** (tableros, tarjetas, listas)
- **Notion** (páginas, bases de datos)

### CRM
- **HubSpot** (contactos, deals, tickets, pipelines)
- **Salesforce** (cuentas, oportunidades, registros)

### Herramientas de Desarrollo
- **GitHub** (repos, PRs, issues, actions, releases)
- **GitLab** (repositorios, merge requests, pipelines)
- **Bitbucket** (repos, pull requests)

### Productividad
- **Google Calendar** (eventos, disponibilidad)
- **Google Sheets** (hojas, celdas, rangos)
- **Google Docs** (documentos, comentarios)
- **Google Drive** (archivos, carpetas)
- **Dropbox** (archivos, carpetas, compartir)
- **OneDrive** (archivos, sincronización)

### Redes Sociales & Programación
- **LinkedIn** (posts, conexiones, mensajes)
- **Twitter/X** (tweets, retweets, trending)
- **Calendly** (citas, disponibilidad)

---

## Descubrimiento Dinámico de Herramientas

### Buscar herramientas por palabra clave:

```javascript
// Buscar todas las herramientas de Gmail
const gmailTools = await composio.searchTools({
  integrationName: 'gmail',
  keyword: 'email'
});

// { 
//   tools: [
//     { id: 'gmail_read_email', name: 'Read Email', description: '...' },
//     { id: 'gmail_send_email', name: 'Send Email', description: '...' },
//     { id: 'gmail_list_labels', name: 'List Labels', description: '...' }
//   ]
// }
```

### Listar herramientas de un servicio:

```javascript
const jiraTools = await composio.getTools({
  integrationName: 'jira'
});

for (const tool of jiraTools) {
  console.log(`${tool.name}: ${tool.description}`);
  console.log(`  Parámetros: ${JSON.stringify(tool.inputSchema)}`);
}
```

---

## Ejecución de Herramientas

### Ejecutar herramienta con validación automática:

```javascript
const result = await composio.executeTool({
  tool: 'gmail_send_email',
  input: {
    to: 'user@example.com',
    subject: 'Actualización de proyecto',
    body: 'El sprint ha completado 8/10 tareas.'
  },
  userId: 'user_123' // Usa la conexión autenticada
});

console.log(`Email enviado: ${result.messageId}`);
```

### Manejo de errores:

```javascript
try {
  const result = await composio.executeTool({
    tool: 'jira_create_issue',
    input: {
      project: 'PROJ',
      summary: 'Bug crítico',
      description: 'No valida entrada de usuario',
      issueType: 'Bug'
    },
    userId: 'user_456'
  });
} catch (error) {
  if (error.code === 'INVALID_ARGUMENTS') {
    console.log('Parámetros inválidos:', error.details);
  } else if (error.code === 'RATE_LIMIT') {
    console.log('Límite de rate excedido. Reintenta en:', error.retryAfter);
  } else if (error.code === 'CONNECTION_EXPIRED') {
    console.log('Token OAuth expirado. Requiere reautenticación.');
  }
}
```

---

## Sistema de Triggers (Eventos Externos)

Escucha eventos de servicios externos sin polling:

### Configurar webhook:

```javascript
const trigger = await composio.setupTrigger({
  event: 'gmail_new_email',
  userId: 'user_789',
  webhookUrl: 'https://api.ejemplo.com/webhooks/email',
  filters: {
    from: 'boss@company.com', // Solo de jefe
    hasAttachment: true
  }
});

// { triggerId: 'trigger_abc123', status: 'ACTIVE' }
```

### Manejar eventos webhook:

```javascript
app.post('/webhooks/email', async (req, res) => {
  const { event, data, userId } = req.body;
  
  if (event === 'gmail_new_email') {
    console.log(`Nuevo email de: ${data.from}`);
    console.log(`Asunto: ${data.subject}`);
    
    // Ejecutar acción automática
    await composio.executeTool({
      tool: 'slack_send_message',
      input: {
        channel: '#alertas',
        message: `📧 Email nuevo: ${data.subject}`
      },
      userId: userId
    });
  }
  
  res.json({ received: true });
});
```

### Triggers populares:

```javascript
// GitHub: nuevo PR
await composio.setupTrigger({
  event: 'github_pull_request_opened',
  webhookUrl: 'https://api.ejemplo.com/webhooks/github'
});

// Jira: issue completada
await composio.setupTrigger({
  event: 'jira_issue_status_changed',
  filters: { newStatus: 'Done' },
  webhookUrl: 'https://api.ejemplo.com/webhooks/jira'
});

// Slack: reacción emoji (requiere scope especial)
await composio.setupTrigger({
  event: 'slack_message_reacted',
  webhookUrl: 'https://api.ejemplo.com/webhooks/slack'
});
```

---

## Ejemplo: Flujo Multi-Servicio

Lea email → Cree ticket Jira → Notifique en Slack:

```javascript
async function processEmailToTicket(emailData, userId) {
  // 1. Extraer información del email
  const { from, subject, body } = emailData;
  
  // 2. Crear ticket en Jira
  const jiraTicket = await composio.executeTool({
    tool: 'jira_create_issue',
    input: {
      project: 'SUPPORT',
      summary: `[${from}] ${subject}`,
      description: body,
      issueType: 'Task',
      priority: 'Medium',
      labels: ['email-imported']
    },
    userId: userId
  });
  
  // 3. Notificar en Slack
  await composio.executeTool({
    tool: 'slack_send_message',
    input: {
      channel: '#support-team',
      message: `🎫 Nuevo ticket creado: ${jiraTicket.key}\nDe: ${from}\nAsunto: ${subject}\nURL: https://jira.company.com/browse/${jiraTicket.key}`
    },
    userId: userId
  });
  
  // 4. Enviar confirmación por email
  await composio.executeTool({
    tool: 'gmail_send_email',
    input: {
      to: from,
      subject: 'Re: ' + subject,
      body: `Tu solicitud ha sido registrada como ticket ${jiraTicket.key}. Será atendida pronto.`
    },
    userId: userId
  });
}
```

---

## Integración con Agentes OpenAI

```javascript
import { OpenAIClient } from '@openai/agents';
import { ComposioToolset } from 'composio-core/openai';

// Crear toolset de Composio
const toolset = new ComposioToolset({
  apiKey: process.env.COMPOSIO_API_KEY,
  userId: 'agent_user_123'
});

// Obtener herramientas como funciones OpenAI
const composioTools = await toolset.getTools({
  integrations: ['gmail', 'jira', 'slack']
});

// Crear agente con herramientas
const agent = await openai.beta.agents.create({
  name: 'Integration Agent',
  instructions: 'Eres un asistente que gestiona tareas en múltiples servicios.',
  tools: composioTools,
  model: 'gpt-4-turbo'
});

// Ejecutar agente
const thread = await openai.beta.threads.create();
await openai.beta.threads.messages.create(thread.id, {
  role: 'user',
  content: 'Lee mis emails nuevos y crea tickets en Jira para cada cliente'
});

// El agente usa herramientas automáticamente
const run = await openai.beta.threads.runs.create(thread.id, {
  assistant_id: agent.id
});
```

---

## Gestión de Conexiones y Persistencia

### Verificar estado de conexión:

```javascript
const connection = await composio.getConnection({
  userId: 'user_101',
  integrationName: 'gmail'
});

console.log(`Estado: ${connection.status}`); // ACTIVE, EXPIRED, FAILED
console.log(`Última sincronización: ${connection.lastSyncAt}`);

if (connection.status === 'EXPIRED') {
  // Requerir reautenticación
  const refreshed = await composio.refreshConnection({
    connectionId: connection.id
  });
}
```

### Desconectar servicio:

```javascript
await composio.disconnect({
  userId: 'user_101',
  integrationName: 'slack'
});
// Estado cambia a INACTIVE
```

---

## Mejores Prácticas de Seguridad

### 1. Almacenamiento de tokens:
```javascript
// NUNCA guardes tokens en cliente
// Siempre usa servidor como intermediario

// En servidor:
const token = await composio.getAccessToken({
  connectionId: connection.id,
  refresh: true // Obtener token fresco si expiró
});
// Token guardado en sesión del servidor (encriptado)
```

### 2. Gestión de scopes:
```javascript
// Solicitar solo scopes necesarios
const auth = await composio.createAuthConfig({
  integrationName: 'gmail',
  scopes: [
    'https://www.googleapis.com/auth/gmail.readonly', // Solo leer
    'https://www.googleapis.com/auth/gmail.send' // Enviar
  ]
  // NO incluyas: https://www.googleapis.com/auth/gmail.modify
});
```

### 3. Rate limiting:
```javascript
// Composio maneja rate limits automáticamente
// Pero implementa backoff exponencial para mayor control
const executeWithRetry = async (tool, input, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await composio.executeTool({ tool, input });
    } catch (error) {
      if (error.code === 'RATE_LIMIT' && i < maxRetries - 1) {
        const delayMs = Math.pow(2, i) * 1000;
        await new Promise(r => setTimeout(r, delayMs));
      } else {
        throw error;
      }
    }
  }
};
```

### 4. Auditoría y logs:
```javascript
// Loguear todas las ejecuciones de herramientas
composio.on('tool_execution', (event) => {
  logger.info('Tool executed', {
    tool: event.tool,
    userId: event.userId,
    status: event.status,
    timestamp: new Date(),
    input: event.input // Sanitizar datos sensibles
  });
});
```

---

## Composio vs Alternativas

| Aspecto | **Composio** | **Zapier** | **n8n** |
|--------|-----------|---------|--------|
| **Uso Principal** | Agentes IA | Automatización manual | Automatización general |
| **Optimización IA** | Nativa (validación, contexto) | Limitada | Básica |
| **Integraciones** | 250+ | 7000+ | 400+ |
| **Curva Aprendizaje** | Baja (SDK limpio) | Muy baja (UI) | Media |
| **Self-hosted** | Sí (Pro) | No | Sí |
| **Cost** | API pay-as-you-go | Seats + acciones | Self-hosted gratis |
| **Ideal para** | Agentes personalizados | Usuarios no-técnicos | DevOps / workflows complejos |

---

## Configuración Completa: Agente Multi-Servicio

```javascript
import { Composio } from 'composio-core';
import { OpenAIClient } from '@openai/agents';

class SmartAgent {
  constructor() {
    this.composio = new Composio({
      apiKey: process.env.COMPOSIO_API_KEY
    });
    this.openai = new OpenAIClient({
      apiKey: process.env.OPENAI_API_KEY
    });
  }

  async setupTools(userId) {
    // Obtener herramientas de múltiples servicios
    const tools = await this.composio.getTools({
      integrations: [
        'gmail', 'jira', 'slack', 'github', 'notion'
      ]
    });

    return tools;
  }

  async executeAgentTask(userId, task) {
    const tools = await this.setupTools(userId);
    
    const agent = await this.openai.beta.agents.create({
      name: 'Smart Agent',
      model: 'gpt-4-turbo',
      instructions: `Ejecuta tareas complejas usando múltiples servicios.
      Siempre confirma acciones de impacto alto.`,
      tools: tools
    });

    const thread = await this.openai.beta.threads.create();
    await this.openai.beta.threads.messages.create(thread.id, {
      role: 'user',
      content: task
    });

    const run = await this.openai.beta.threads.runs.create(thread.id, {
      assistant_id: agent.id
    });

    // Monitorear ejecución
    while (run.status !== 'completed') {
      await new Promise(r => setTimeout(r, 1000));
      // Manejar tool calls del agente
    }

    return run;
  }
}
```

---

## Resumen

Composio simplifica la integración de agentes IA con servicios empresariales:

- **Autenticación uniforme** a través de OAuth
- **Descubrimiento dinámico** de herramientas
- **Triggers basados en eventos** para automatización
- **Validación automática** de parámetros
- **Gestión de errores** robusta
- **Rate limiting** transparente

Ideal para crear agentes IA productivos que ejecuten acciones reales en ecosistemas empresariales.
