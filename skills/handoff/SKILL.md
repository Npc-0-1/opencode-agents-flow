---
name: handoff
description: "Do not use as durable memory; use `memory` for long-term technical memory. Use when compacting the current conversation into a handoff document for another agent or future session, including current state, decisions, artifacts, blockers, next steps, suggested skills, and redacted sensitive info."
---

# Handoff

用于把当前会话压缩成交接文档，方便下一个 agent 或未来会话继续。

## Storage

- 只有用户明确要求“保存/生成交接文档/写入文件”时，才写到系统临时目录：`C:\Users\15523\AppData\Local\Temp\opencode`。
- 用户只要求“总结/交接内容”时，默认在回复中输出 handoff 内容，不写文件。
- 不默认写入当前项目，除非用户明确要求。
- 不复制大段已有文档，引用路径或 URL。

## Content

```markdown
# Handoff

## Goal

## Current State

## Decisions Made

## Files / Artifacts

## Commands Run

## Validation Results

## Blockers / Risks

## Next Steps

## Suggested Skills

## Sensitive Info Redacted
```

## Rules

- 脱敏 API key、token、密码、cookie、私有路径中不必要的个人信息。
- 区分事实、推断和待确认事项。
- 只把长期技术决策、根因、偏好、项目状态写入 `memory`；普通临时上下文保留在 handoff。
- 如果当前环境只允许只读，或用户未明确授权写文件，则输出模板内容，不写文件。

## 二次确认

- 反查是否遗漏当前任务状态、验证结果和下一步。
- 反查是否泄露敏感信息。
- 反查引用路径是否存在或说明其来源。
