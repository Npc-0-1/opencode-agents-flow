---
name: tdd-workflow
description: "Use when the behavior target is known or the user explicitly requests test-first development, red-green-refactor, behavior tests, integration tests, minimal fixtures, or one vertical slice at a time. For failures or exceptions with unknown root cause, use diagnose first."
---

# TDD Workflow

用于测试先行开发。目标是用最小垂直切片获得稳定反馈，而不是一次写完大量测试或代码。

## Loop

1. **Plan slice**：选一个可演示的端到端行为。
2. **Red**：写一个失败测试，验证真实需求，不测实现细节。
3. **Green**：写最少代码让测试通过。
4. **Refactor**：只在 Green 后重构，保持测试通过。
5. **Repeat**：继续下一个小切片。

## Test Rules

- 测公共接口和用户可观察行为，不测私有函数、内部变量或临时实现。
- 每次只新增一个主要失败点。
- fixture 尽量小；NLP/数据任务先用小样本确认，再扩展到完整数据。
- 避免横向切片：不要先写完所有模型/接口/UI/测试再统一实现。
- 测试名写清行为和边界。

## Implementation Rules

- 红灯时不重构。
- 绿灯前不扩大功能。
- 如果测试难写，先检查模块接口是否过浅或耦合过高。
- 用户未明确要求自动改代码时，只给测试位置、代码片段和原因。

## Output

- 当前切片目标。
- 新增/修改测试。
- 实现文件。
- 验证命令与结果。
- 下一切片建议。

## 二次确认

- 确认测试会在旧实现下失败、在新实现下通过。
- 确认测试没有绑定实现细节。
- 确认每个切片可独立解释和验证。
