---
name: fe-quality
description: |
  前端质量与安全技能包，涵盖前端安全加固、错误监控集成、前端 CI/CD 流水线、无障碍（a11y）合规。
  当需要加固前端安全防护（XSS/CSP/依赖审计）、集成错误监控（Sentry/自研SDK）、搭建前端 CI/CD 流水线（GitHub Actions/GitLab CI/Lighthouse CI）、或进行无障碍适配（WCAG/ARIA）时触发此技能。
  支持 Angular、Vue、React、原生 JS、Node.js 技术栈。
---

# 前端质量与安全

前端质量保障的四大支柱：安全防护、错误监控、自动化流水线、无障碍合规。

## 快速健康检查

对任意前端项目执行质量快速扫描：

```bash
# 1. 依赖安全审计
pnpm audit --production

# 2. 代码规范检查
npx eslint . --ext .ts,.tsx,.vue,.js

# 3. 无障碍检查（需安装 axe-core CLI）
npx @axe-core/cli http://localhost:3000

# 4. Lighthouse 综合审计
npx lighthouse http://localhost:3000 --output html --output-path report.html
```

## 场景路由

根据具体需求选择对应参考文档：

| 场景 | 参考文档 | 典型触发 |
|------|---------|---------|
| XSS 防御、CSP 配置、依赖漏洞 | [security.md](references/security.md) | "加固安全"、"配置 CSP"、"审计依赖" |
| Sentry 接入、自研监控、Error Boundary | [error-monitoring.md](references/error-monitoring.md) | "接入 Sentry"、"错误上报"、"监控" |
| CI/CD 搭建、Preview Deploy、Lighthouse CI | [cicd-pipeline.md](references/cicd-pipeline.md) | "搭建流水线"、"自动部署"、"CI" |
| WCAG 合规、ARIA 标注、键盘导航 | [accessibility.md](references/accessibility.md) | "无障碍"、"a11y"、"屏幕阅读器" |

## 优先级建议

按风险等级排序处理：

1. **P0 安全漏洞** → 立即修复（XSS、依赖高危漏洞）
2. **P1 错误监控** → 上线前必须具备（生产环境可观测性）
3. **P2 CI/CD** → 提升团队效率（自动化构建、测试、部署）
4. **P3 无障碍** → 持续改进（合规要求、用户体验）

## 组合使用

- 安全 + CI/CD：在流水线中集成 `pnpm audit`、依赖检查
- 监控 + 安全：Sentry 中配置安全相关告警规则
- a11y + CI/CD：在 PR 检查中集成 axe-core 自动化测试
