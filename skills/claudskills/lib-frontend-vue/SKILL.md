---
name: vue
description: Best practices for Vue.js development including security, performance, and developer experience
goal: พัฒนา Vue.js ตาม best practices
outcome: Vue.js applications มีคุณภาพและประสิทธิภาพ
---

# Vue.js Development

## When to Apply

ใช้ Skill นี้เมื่อพัฒนา Vue.js applications

- เมื่อสร้าง Vue applications ใหม่
- เมื่อ refactor existing components
- เมื่อ ensure application security และ accessibility
- เมื่อ optimize application performance

## Rules

| Priority | Impact | Reference | Name | Description | Prefix | Condition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `CRITICAL` | [vue-security.md](./rules/vue-security.md) | Security | Guidelines สำหรับการปกป้อง Vue applications จาก vulnerabilities | `vue-` | เมื่อ ensure security |
| 2 | `HIGH` | [vue-performance.md](./rules/vue-performance.md) | Performance | Best practices สำหรับการสร้าง high-performance Vue components | `vue-` | เมื่อ optimize performance |
| 2 | `HIGH` | [vue-optimzation.md](./rules/vue-optimzation.md) | Optimization | Techniques สำหรับ optimizing Vue application performance | `vue-` | เมื่อ optimize |
| 2 | `HIGH` | [vue-reactivity.md](./rules/vue-reactivity.md) | Reactivity | การเข้าใจและใช้ reactivity system ของ Vue | `vue-` | เมื่อใช้ reactivity |
| 2 | `HIGH` | [vue-composables.md](./rules/vue-composables.md) | Composables | การสร้างและใช้ composables สำหรับ reusable logic | `vue-` | เมื่อสร้าง composables |
| 2 | `HIGH` | [vue-reuseables.md](./rules/vue-reuseables.md) | Reusables | Patterns สำหรับการสร้าง reusable components และ utilities | `vue-` | เมื่อสร้าง reusable code |
| 4 | `MEDIUM` | [vue-dx.md](./rules/vue-dx.md) | DX | Practices สำหรับการปรับปรุง developer experience | `vue-` | เมื่อ improve DX |
| 4 | `MEDIUM` | [vue-styles.md](./rules/vue-styles.md) | Styles | Guidelines สำหรับการจัดการ component styling อย่าง scalable | `vue-` | เมื่อจัดการ styles |
| 5 | `MEDIUM` | [vue-accessibility.md](./rules/vue-accessibility.md) | Accessibility | การรับรองว่า Vue applications ของคุณเข้าถึงได้สำหรับทุก users | `vue-` | เมื่อ ensure accessibility |

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

- [Vue.js Documentation](https://vuejs.org/)
