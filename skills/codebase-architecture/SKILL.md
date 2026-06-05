---
name: codebase-architecture
description: "Use when analyzing existing codebase architecture, module boundaries, refactoring opportunities, testability, tightly coupled code, shallow modules, or when the user asks to zoom out and explain how code fits together. Do not use for PRD or vague-requirement interviews; use design-grill instead."
---

# Codebase Architecture

用于架构理解、模块边界分析、重构候选发现和 zoom-out 解释。默认只分析和给计划，不直接改代码。

## Core Vocabulary

- **Module**：有清晰职责的一组代码。
- **Interface**：调用者看到的入口、参数、返回和约束。
- **Implementation**：接口背后的复杂度。
- **Deep module**：小接口承载大能力，优先保留或加深。
- **Shallow module**：接口复杂但实现很薄，优先合并或简化。
- **Seam**：可切开、替换、测试或注入的边界。
- **Adapter**：隔离外部系统或格式变化的边界层。
- **Locality**：修改一个需求需要触碰的范围。

## Workflow

1. 读取项目说明、`CONTEXT.md`、`docs/adr/`、关键入口和调用链（如果存在）。
2. 画出相关模块地图：调用者、被调用者、数据流、配置流、测试边界。
3. 做 deletion test：如果删除/合并某模块，系统损失什么？如果损失很小，可能是浅模块或重复层。
4. 找候选：深模块加深、浅模块合并、边界补 seam、外部依赖加 adapter、重复概念统一命名。
5. 给改动量/收益权衡：收益低或风险高时不建议改。
6. 用户要求实现时，再进入编码流程。

## Zoom-out Mode

当用户说“zoom out / 上一层 / 解释这块代码怎么串起来”时，输出：

- 这块代码在系统中的角色。
- 相关模块和调用者地图。
- 核心领域词汇。
- 主要数据流和控制流。
- 改这块最容易踩的风险。

## Output

- 架构地图。
- 问题候选，按 Strong / Worth exploring / Speculative 标记。
- 每个候选的改动范围、收益、风险、验证方式。
- 不建议修改的部分和原因。

## 二次确认

- 反查是否基于实际代码而非猜测。
- 反查是否误把风格问题当架构问题。
- 反查建议是否符合极简主义，避免低收益大改。
