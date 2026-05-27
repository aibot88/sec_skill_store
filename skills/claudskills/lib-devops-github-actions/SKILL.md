---
name: github-actions
description: Best practices for GitHub Actions workflows including security, performance, and maintenance
goal: ใช้ GitHub Actions ตาม best practices
outcome: Workflows มีความปลอดภัยและประสิทธิภาพ
---

# GitHub Actions

## When to Apply

ใช้ Skill นี้เมื่อพัฒนาและจัดการ GitHub Actions workflows

- เมื่อต้องสร้างหรือแก้ไข GitHub Actions workflows
- เมื่อต้องตรวจสอบความปลอดภัยของ workflows
- เมื่อต้องปรับปรุงประสิทธิภาพของ CI/CD pipelines
- เมื่อต้องจัดการ secrets และ permissions
- เมื่อต้องใช้งาน third-party actions

## Rules

| Priority | Impact | Reference | Name | Description | Prefix | Condition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `CRITICAL` | [secrets-management.md](./rules/secrets-management.md) | Secrets Management | การจัดการ secrets อย่างปลอดภัย | `gha-` | เมื่อจัดการ secrets |
| 2 | `HIGH` | [third-party-actions.md](./rules/third-party-actions.md) | Third-party Actions | การใช้งาน third-party actions อย่างปลอดภัย | `gha-` | เมื่อใช้ third-party actions |
| 3 | `HIGH` | [workflow-security.md](./rules/workflow-security.md) | Workflow Security | ความปลอดภัยของ workflows | `gha-` | เมื่อสร้าง workflows |
| 4 | `MEDIUM` | [performance-optimization.md](./rules/performance-optimization.md) | Performance Optimization | การปรับปรุงประสิทธิภาพ | `gha-` | เมื่อ optimize workflows |
| 5 | `MEDIUM` | [self-hosted-runners.md](./rules/self-hosted-runners.md) | Self-hosted Runners | การจัดการ self-hosted runners | `gha-` | เมื่อใช้ self-hosted runners |

## Knowledge

| Reference | Name | Description | Prefix |
| :--- | :--- | :--- | :--- |

## Overview

### Rules

แต่ละไฟล์ Rule ประกอบด้วย:

- เหตุผล (Why)
- ตัวอย่างที่ไม่ดี (Anti-patterns)
- ตัวอย่างที่ดี (Best practices)
- กฎที่ต้องปฏิบัติตาม (Rules)
- ผลกระทบถ้าไม่ทำตาม (Impact)
- เอกสารอ้างอิง (References)

### Knowledge

แต่ละไฟล์ Knowledge ประกอบด้วย:

- Overview: ภาพรวมของ topic
- Key Concepts: concepts สำคัญที่ต้องรู้
- Examples: ตัวอย่างการใช้งาน
- Best Practices: best practices ที่ควรทำตาม
- References: ลิงก์ไปยังแหล่งข้อมูลต้นฉบับ

## How to Use

แต่ละไฟล์ Rule อธิบายถึง:

- เหตุผลที่ต้องทำตามกฎ
- ตัวอย่างที่ไม่ดีและดี
- กฎที่ต้องปฏิบัติตาม
- ผลกระทบถ้าไม่ทำตาม
- เอกสารอ้างอิง

แต่ละไฟล์ Knowledge อธิบายถึง:

- ภาพรวมของ topic
- Concepts สำคัญที่ต้องรู้
- ตัวอย่างการใช้งาน
- Best practices ที่ควรทำตาม
- เอกสารอ้างอิง

## References

- [GitHub Actions Security Best Practices](https://www.stepsecurity.io/blog/github-actions-security-best-practices)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Security Cheat Sheet](https://blog.gitguardian.com/github-actions-security-cheat-sheet/)
