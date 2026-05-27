---

name: vscode-extension-builder

description: Comprehensive VSCode extension development expert that guides you through creating extensions using the official Yeoman generator tool. Provides interactive setup, configuration guidance, and development workflow support. Covers scaffolding with yo code, extension anatomy, debugging, testing, publishing, and API reference. Features primary access to complete VS Code API documentation at `@source/vscode-docs/api/` for authoritative reference. Use when starting new VSCode extensions, setting up development environment, configuring extension manifests, debugging extensions, or when mentioning VSCode extension creation, TypeScript extensions, plugin development, or editor customization. Built with official VS Code documentation, generator best practices, and complete API reference.

allowed-tools: Read, Write, Edit, Glob, Grep, Bash

---

# VSCode Extension Expert

A comprehensive guide for developing Visual Studio Code extensions using TypeScript/JavaScript. This skill is built directly from the official VSCode extension samples repository and covers everything from basic extension creation to advanced language features, custom editors, and publishing workflows.

## 🎯 Getting Started with Official Generator

The best way to create a new VS Code extension is by using the official Yeoman generator tool.

### Prerequisites

Ensure you have [Node.js](https://nodejs.org/) and [Git](https://git-scm.com/) installed.

### Creating a New Extension

**Option 1: One-time use (recommended)**
```bash
npx --package yo --package generator-code -- yo code
```

**Option 2: Global installation**
```bash
npm install --global yo generator-code
yo code
```

### After Creation

1. **Open the extension folder in VS Code**
2. **Navigate to `src/extension.ts`**
3. **Press F5** to launch Extension Development Host
4. **Test** from Command Palette (Ctrl+Shift+P)

## 🛠️ How to Use This Skill

### Starting a New Extension
```
"I want to create a new VS Code extension"
"Help me set up a VS Code extension project"
```

### During Development
```
"How do I add a new command?"
"My extension isn't loading, can you help me debug?"
"I want to create a webview panel"
```

### Working with Generated Projects
I'll respect your choices:
- **Package manager**: npm, yarn, pnpm, or bun
- **Bundler**: webpack, esbuild, or unbundled
- **Language**: TypeScript or JavaScript
- **Extension type**: commands, themes, language support, etc.

## Core Concepts

### Extension Anatomy

**Basic package.json**
```json
{
  "name": "my-extension",
  "displayName": "My Extension",
  "version": "0.0.1",
  "engines": { "vscode": "^1.85.0" },
  "categories": ["Other"],
  "activationEvents": ["onCommand:extension.helloWorld"],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [{
      "command": "extension.helloWorld",
      "title": "Hello World"
    }]
  }
}
```

**Extension Entry Point**
```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('Extension "my-extension" is now active!');

    const disposable = vscode.commands.registerCommand('extension.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World!');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
```

### Common Patterns

**Command Registration**
```typescript
const commands = [
    vscode.commands.registerCommand('extension.doSomething', () => {
        // Implementation
    }),
    vscode.commands.registerCommand('extension.doSomethingElse', () => {
        // Another command
    })
];

context.subscriptions.push(...commands);
```

**Status Bar Integration**
```typescript
const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
);
statusBarItem.text = '$(gear) My Extension';
statusBarItem.tooltip = 'My Extension Status';
statusBarItem.command = 'extension.toggleFeature';
statusBarItem.show();

context.subscriptions.push(statusBarItem);
```

### Webview Development

**Basic Webview**
```typescript
export function createWebviewPanel(context: vscode.ExtensionContext) {
    const panel = vscode.window.createWebviewPanel(
        'myWebview',
        'My Webview',
        vscode.ViewColumn.One,
        {
            enableScripts: true,
            retainContextWhenHidden: true
        }
    );

    panel.webview.html = getWebviewContent(context.extensionUri);

    panel.webview.onDidReceiveMessage(
        message => {
            switch (message.command) {
                case 'alert':
                    vscode.window.showInformationMessage(message.text);
                    return;
            }
        },
        undefined,
        context.subscriptions
    );

    return panel;
}
```

### Tree View Provider

```typescript
export class TreeDataProvider implements vscode.TreeDataProvider<TreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<TreeItem | undefined | null | void> = new vscode.EventEmitter<TreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<TreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private treeItems: TreeItem[] = [];

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: TreeItem): Thenable<TreeItem[]> {
        if (!element) {
            return Promise.resolve(this.treeItems);
        }
        return Promise.resolve([]);
    }
}
```

### Language Features

**Code Completion**
```typescript
export class CompletionItemProvider implements vscode.CompletionItemProvider {
    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
    ): vscode.CompletionItem[] {
        return [
            new vscode.CompletionItem('console.log', vscode.CompletionItemKind.Method),
            new vscode.CompletionItem('console.error', vscode.CompletionItemKind.Method)
        ];
    }
}

vscode.languages.registerCompletionItemProvider(
    'javascript',
    new CompletionItemProvider(),
    '.'
);
```

### Configuration

**Reading Settings**
```typescript
const config = vscode.workspace.getConfiguration('myExtension');
const enabled = config.get<boolean>('enabled', true);
const apiKey = config.get<string>('apiKey', '');
```

**Configuration Schema (package.json)**
```json
{
  "contributes": {
    "configuration": {
      "title": "My Extension",
      "properties": {
        "myExtension.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable/disable the extension"
        }
      }
    }
  }
}
```

### Testing

**Unit Tests**
```typescript
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('publisher.my-extension'));
    });

    test('Should register commands', async () => {
        const commands = await vscode.commands.getCommands();
        assert.ok(commands.includes('extension.helloWorld'));
    });
});
```

### Publishing

```bash
# Install vsce
npm install -g @vscode/vsce

# Create publisher
vsce create-publisher your-publisher-name

# Package and publish
vsce package
vsce publish
```

## 📚 Official Resources

### Primary API Documentation (Authoritative)
**Complete VS Code API**: `@source/vscode-docs/api/` - **FIRST REFERENCE**

**Core References**:
- **Extension API**: `@source/vscode-docs/api/references/vscode-api.md`
- **Extension Manifest**: `@source/vscode-docs/api/references/extension-manifest.md`
- **Contribution Points**: `@source/vscode-docs/api/references/contribution-points.md`

**Development Guides**:
- **Getting Started**: `@source/vscode-docs/api/get-started/`
- **Extension Guides**: `@source/vscode-docs/api/extension-guides/`
- **UX Guidelines**: `@source/vscode-docs/api/ux-guidelines/`

### Code Examples

**Core Features** (`@source/vscode-extension-samples/`):
- `command-sample/` - Command registration
- `tree-view-sample/` - Custom tree views
- `completions-sample/` - Code completion
- `webview-sample/` - Custom UI panels
- `custom-editor-sample/` - Custom file editors

## Quick Reference

### Essential APIs
- `vscode.commands.registerCommand()` - Register commands
- `vscode.window.createWebviewPanel()` - Create webviews
- `vscode.window.createTreeView()` - Create tree views
- `vscode.languages.registerCompletionItemProvider()` - Add completions
- `vscode.workspace.getConfiguration()` - Read settings
- `vscode.window.createStatusBarItem()` - Status bar items

### Common Contribution Points
- `contributes.commands` - Register commands
- `contributes.views` - Add view containers
- `contributes.configuration` - Add settings
- `contributes.languages` - Define new languages
- `contributes.themes` - Custom themes

### Essential Commands
```bash
npx --package yo --package generator-code -- yo code
npm run compile          # Compile TypeScript
npm run watch           # Watch for changes
npm test                # Run tests
npm run package         # Package extension
vsce publish            # Publish to marketplace
```

## Troubleshooting

**Common Issues:**
- Extension not loading: Check `engines.vscode` version
- Commands not registering: Verify command IDs match in package.json
- Activation issues: Check activationEvents

**Debug Techniques:**
- Use `console.log()` (Developer Tools console)
- Help > Toggle Developer Tools
- View > Output > Extension Host

> See [references/ADVANCED.md](references/ADVANCED.md) for advanced topics like file system providers, terminal integration, and performance optimization.
> See [references/EXAMPLES.md](references/EXAMPLES.md) for complete extension templates and detailed implementation examples.
