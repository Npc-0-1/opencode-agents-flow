---
name: design-grill
description: "Use when stress-testing requirements, PRDs, plans, designs, feature ideas, architecture decisions, or vague requirements. Interviews one question at a time, checks code/docs when answerable, and sharpens terminology. Do not use for simply mapping existing code architecture; use codebase-architecture instead."
---

# Design Grill

用于在动手前压实需求、设计和术语。目标是发现模糊点、隐藏分支和错误假设。

## Workflow

1. 先读已有上下文、代码、`CONTEXT.md`、ADR 和相关文档；能从资料回答的不要问用户。
2. 找出最可能导致返工的未知项：目标、边界、数据、失败模式、兼容性、测试、交付形态。
3. 一次只问一个问题。
4. 每个问题都给推荐答案或可选答案，说明取舍。
5. 用户回答后更新问题树，直到关键分支闭合。
6. 最后输出确认版决策、未决项和下一步。

## Question Rules

- 问具体问题，不问泛泛的“你想怎么做”。
- 优先问会改变实现方向的问题。
- 挑战模糊术语，要求统一命名。
- 不重复问已经能从代码或文档确认的问题。
- 强自动模式下可先给推荐方案并列出需要用户确认的少数关键点。

## Docs Rules

- 发现稳定领域术语时，可建议写入 `CONTEXT.md`。
- 只有硬逆、令人惊讶、且有真实权衡的决策，才建议 ADR。
- 未经授权不直接修改文档。

## Output

- 已确认决策。
- 仍未确认的问题。
- 推荐方案。
- 需要更新的文档位置（如有）。

## 二次确认

- 反查是否还有会改变实现方向的未问问题。
- 反查推荐答案是否基于资料和用户偏好。
- 反查是否过度追问低价值细节。
