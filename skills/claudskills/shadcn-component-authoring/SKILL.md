---
type: skill
name: Shadcn Component Authoring
description: Implementar componentes no padrão Shadcn com CSS pré-compilado
skillSlug: shadcn-component-authoring
phases: [E]
version: "2.1.0"
generated: 2026-01-24
status: filled
scaffoldVersion: "2.0.0"
---

# Skill: Shadcn Component Authoring 2.1 🚀

## Visão Geral

Esta skill descreve o processo de criação de componentes com CSS pré-compilado, foco em modularidade, performance e experiência do desenvolvedor.

## 🎯 Objetivos Atualizados

- 🧩 Criar componentes totalmente modulares
- 🎨 Garantir consistência de design
- 🚀 Otimizar performance de renderização
- 🔒 Simplificar consumo de componentes

## 📂 Estrutura de Componente

### Anatomia Padrão

```
packages/ui/src/components/<componente>/
├── index.ts            # Exportações principais
├── <componente>.tsx    # Implementação
└── (opcional) types.ts # Definições avançadas
```

## 🔧 Padrões de Implementação

### 1. Definição de Props

```typescript
interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  // Propriedades específicas
}
```

### 2. Variantes com CVA

```typescript
const buttonVariants = cva("base-button", {
  variants: {
    variant: {
      primary: "bg-primary text-white",
      secondary: "bg-secondary text-gray-800",
    },
    size: {
      sm: "text-sm px-2",
      md: "text-base px-4",
    },
  },
  defaultVariants: {
    variant: "primary",
    size: "md",
  },
});
```

### 3. Implementação com Forward Ref

```typescript
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  ),
);
Button.displayName = "Button";
```

## 🛠️ Ferramentas e Dependências

- **React**: Biblioteca base
- **class-variance-authority (cva)**: Variantes
- **tailwind-merge**: Mesclagem de classes
- **Tailwind CSS**: Sistema de design
- **shadcn CLI**: Instalação de componentes base (opcional)

## 🔄 Fluxo de Criação

### Opção 1: Instalar via shadcn CLI (Recomendado)

Para componentes que existem no registry shadcn:

1. Consultar componente via MCP (ver skill `shadcn-mcp-integration`)
2. Instalar base: `npx shadcn@latest add <componente> --cwd packages/ui -p src/components/<componente> -y`
3. Customizar conforme design system (ajustar variantes, cores, tokens)

**Vantagens:**

- ✅ Componente base já implementado
- ✅ Acessibilidade incluída
- ✅ Padrões shadcn seguidos
- ✅ Mais rápido

### Opção 2: Criar do Zero

Para componentes customizados não disponíveis no registry:

1. Definir contrato de props
2. Implementar variantes com `cva`
3. Criar componente com `forwardRef`
4. Adicionar ao barrel `index.ts`
5. Documentar no Storybook

## 🎨 Personalização e CSS

### Tokens de Design

```css
:root {
  --primary: hsl(210, 100%, 50%);
  --secondary: hsl(260, 100%, 50%);
}
```

### Geração de CSS

- Build automatizado gera `styles.css`
- CSS pré-compilado com todas variantes
- Suporte a temas via variáveis CSS

## ⚠️ Anti-Padrões

- Evitar lógica de negócio em componentes
- Não acoplar estado global
- Não criar componentes muito específicos

## 🚦 Validação

```bash
npm run build:ui     # Compilar biblioteca
npm run test:ui      # Testes
npm run storybook    # Documentação
```

## 🔍 Consumo Simplificado

```typescript
import "@juscash/ui/styles.css";
import { Button } from "@juscash/ui";

function App() {
  return <Button variant="primary">Clique aqui</Button>;
}
```

## 📦 Decisões de Arquitetura

| Aspecto   | Estratégia    | Benefícios                |
| --------- | ------------- | ------------------------- |
| CSS       | Pré-compilado | Performático, Simples     |
| Variantes | CVA           | Flexível, Tipado          |
| Tokens    | CSS Variables | Customizável, Consistente |

## 🚀 Próximos Passos

- [ ] Documentação detalhada
- [ ] Testes abrangentes
- [ ] Exemplos em diferentes contextos

## 📚 Referências

- [Tailwind CSS](https://tailwindcss.com)
- [class-variance-authority](https://github.com/joe-bell/cva)
- [React Docs](https://reactjs.org)
- [Skill: shadcn-mcp-integration](../shadcn-mcp-integration/SKILL.md) - Instalação via CLI
