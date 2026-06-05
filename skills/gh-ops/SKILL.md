---
name: gh-ops
description: "Use for GitHub platform objects/API operations: Issues, issue PRDs, triage, splitting, Pull Requests, Releases, or repository search. Not for code-reviewer-style source review; PR review triggers only for GitHub PR API actions like `gh pr review`. Mutating gh actions require explicit confirmation. Uses `gh` CLI API commands ONLY; never touches `.git` or runs git commands."
---

# GitHub Operations

Operate on GitHub via `gh` CLI. All git operations (commit, push, pull, branch) are handled by the user.

## Hard Rule

- `gh` API commands only: `gh issue`, `gh pr`, `gh release`, `gh search`, `gh repo view`, `gh api`
- NEVER run `git *` commands. The user manages git themselves.

## Common Commands

```bash
# Issues
gh issue list     --repo owner/repo --limit 20 --state open
gh issue view     --repo owner/repo 42
gh issue create   --repo owner/repo --title "..." --body "..."
gh issue comment  --repo owner/repo 42 --body "..."

# Pull Requests
gh pr list        --repo owner/repo --state open
gh pr view        --repo owner/repo 99
gh pr diff        --repo owner/repo 99
gh pr review      --repo owner/repo 99 --approve --body "LGTM"
gh pr review      --repo owner/repo 99 --comment --body "Needs changes"
gh pr merge       --repo owner/repo 99 --squash

# Releases
gh release list   --repo owner/repo --limit 10
gh release view   --repo owner/repo v1.0.0
gh release create --repo owner/repo v1.0.0 --title "..." --notes "..."

# Search
gh search issues  "label:bug state:open" --repo owner/repo
gh search prs     "is:open review:required" --repo owner/repo
gh search repos   "topic:nlp language:python" --limit 20

# Generic API
gh api repos/owner/repo/issues --jq '.[].title'
```

## Workflow

1. Always verify `--repo` is correct before running commands.
2. For readonly operations (list/view/search), run without asking.
3. For mutating operations (create/comment/merge), confirm with user first.
4. If `gh` CLI is not authenticated, report the gap and provide the commands user would need.
5. Before applying or recommending labels, inspect existing labels with `gh label list --repo owner/repo`. If labels do not exist, keep state as analysis text and do not invent labels.

## Issue Triage

Use this when the user asks to triage, classify, label, refine, or prepare issues.

1. Read the issue and relevant code/docs before deciding.
2. Classify one category: `bug` or `enhancement`.
3. Choose one state:
   - `needs-triage` — not enough signal yet.
   - `needs-info` — blocked on user/domain detail.
   - `ready-for-agent` — clear, bounded, agent-executable.
   - `ready-for-human` — needs product/design/security judgment.
   - `wontfix` — out of scope, duplicate, or rejected by prior policy.
4. For bugs, try to reproduce or identify the missing reproduction before asking questions.
5. For unclear issues, ask the minimum necessary question and include a recommended answer.

## PRD → GitHub Issue

Use this when turning conversation context or a plan into a GitHub issue. Do not invent missing decisions.

```markdown
## Problem Statement

## Solution

## User Stories

## Implementation Decisions

## Testing Decisions

## Out of Scope

## Further Notes
```

## Split Into Issues

Use vertical slices only: each issue should be independently useful and demoable end-to-end. Do not split by horizontal layers like schema-only, API-only, UI-only, or tests-only unless the user explicitly wants that.

```markdown
## Parent

## What to build

## Acceptance criteria

## Blocked by

## Agent brief
```

Rules:
- Keep issues narrow but complete.
- Put dependencies in order.
- Mark HITL items when human judgment is required.
- Use `gh issue create/comment/edit` only after user confirms mutating actions.

## 二次确认（输出前必须执行）

- 反查 `--repo` 参数是否正确，查询条件是否准确。
- 确认输出内容是 gh API 返回的真实数据，非推断。
- mutating 操作确认是否已得到用户授权。
- 确认 issue 拆分是垂直切片，不是重复或横向拆分。
