# opencode-agents-flow

Agent orchestration that stays light by default, escalates only when needed, and keeps implementation, QA, review, and UI/E2E evidence separate.

## English

### Highlights

- Lightweight default controller: `auto-flash` chooses the shortest reliable path for clear tasks.
- Complex-work escalation: `auto-max` takes sole control for multi-stage, high-risk, or blocked work.
- Single-controller discipline: one task has one controller; no competing orchestration.
- `build` is the only implementation unit; it reads current files, edits minimally, and self-verifies.
- `qa` validates independently; `code-reviewer` reviews independently.
- `ui-operator` handles real browser/UI/E2E paths when explicitly required.
- Skills trigger by task object, not by context length or general complexity.
- High-risk boundaries are explicit: `.git`, provider/auth/model/API keys, production, deployment, plugins/MCP, destructive data operations, and GitHub mutation.

### Why this exists

Most agent setups fail in one of two ways: simple tasks become heavy process, or complex tasks get patched by a single loop with no independent evidence. This suite keeps the fast path fast while making escalation, validation, review, and safety boundaries explicit.

### At a glance

```text
User task
   |
   v
auto-flash  -- clear + bounded --> build --> self-check --> delivery
   |
   +-- missing facts -----------> researcher
   +-- route/scope unclear -----> decision-planner
   +-- independent validation --> qa
   +-- independent review ------> code-reviewer
   +-- real UI/E2E -------------> ui-operator
   +-- complex/high-risk -------> auto-max
   +-- repeated failures -------> reflector

auto-max --> plan --> research --> build --> qa --> review --> optional UI/E2E --> gated delivery
```

## Table of Contents

- [English](#english)
  - [Highlights](#highlights)
  - [Why this exists](#why-this-exists)
  - [At a glance](#at-a-glance)
  - [Architecture](#architecture)
  - [Agent Roles](#agent-roles)
  - [Task Flow](#task-flow)
  - [Auto-Max Project Flow](#auto-max-project-flow)
  - [Routing Decision](#routing-decision)
  - [Review and QA Model](#review-and-qa-model)
  - [Delivery Report](#delivery-report)
  - [Skills](#skills)
  - [Required Skills](#required-skills)
  - [Skill Routing Notes](#skill-routing-notes)
  - [Safety Boundaries](#safety-boundaries)
  - [Quality Gates](#quality-gates)
  - [Usage](#usage)
- [中文](#中文)
  - [亮点](#亮点)
  - [为什么存在](#为什么存在)
  - [一眼看懂](#一眼看懂)
  - [架构](#架构)
  - [Agent 角色](#agent-角色)
  - [任务流程](#任务流程)
  - [Auto-Max 项目级流程](#auto-max-项目级流程)
  - [路由判断](#路由判断)
  - [审查与 QA 模型](#审查与-qa-模型)
  - [交付报告](#交付报告)
  - [Skills](#skills-1)
  - [必要 Skills](#必要-skills)
  - [Skill 路由说明](#skill-路由说明)
  - [安全边界](#安全边界)
  - [质量门禁](#质量门禁)
  - [使用方法](#使用方法)

### Architecture

Repository layout:

```text
opencode.jsonc
AGENTS.md
agents/
  auto-flash.md
  auto-max.md
  build.md
  decision-planner.md
  researcher.md
  qa.md
  code-reviewer.md
  ui-operator.md
  reflector.md
skills/
  <skill-name>/SKILL.md
```

Control model:

```text
Controller layer
  auto-flash: default lightweight controller
  auto-max: project-level controller for complex work

Specialist layer
  build: implementation
  researcher: read-only facts
  decision-planner: read-only planning
  qa: independent validation
  code-reviewer: independent review
  ui-operator: real UI/E2E operation
  reflector: read-only failure reflection

Skill layer
  Loaded only when the task object matches the skill domain
```

Core principles:

- One controller per task.
- Simple tasks stay lightweight.
- Complex tasks escalate instead of being patched blindly.
- Implementation, validation, review, planning, research, and UI operation stay separate.
- Agents read current files before editing, validating, or reviewing.
- Delivery is evidence-based, not assertion-based.

### Agent Roles

| Agent | Role | Output |
| --- | --- | --- |
| `auto-flash` | Default lightweight controller for clear low/medium-complexity tasks | Route, delegation, compact final delivery |
| `auto-max` | Sole project controller for complex, multi-stage, high-risk, or blocked work | Phase plan, state ledger, gates, final delivery |
| `build` | Only execution unit for code, config, script, agent, skill, test, and doc changes | Minimal change plus focused self-verification |
| `decision-planner` | Read-only route, boundary, priority, phase, and validation advisor | Execution boundary, stop condition, gate recommendation |
| `researcher` | Read-only fact finder for files, config, dependencies, call chains, and evidence | Current facts with source references |
| `qa` | Independent validation unit | PASS / FAIL / BLOCKED / NOT_COVERED with command or evidence |
| `code-reviewer` | Independent risk review unit | Requirement fit, regression risk, edge cases, safety, test gaps |
| `ui-operator` | Real UI/E2E operator | Browser path, screenshot, console/network, or E2E evidence |
| `reflector` | Read-only failure reflection on repeated failures or repeated error types | Temporary context_injection (max 3 items, not persisted, does not reset loop count) |

### Task Flow

`auto-flash` is the default entry. It keeps the path short unless the task itself requires escalation.

```text
User task
  |
  v
auto-flash: classify goal, scope, risk, and missing facts
  |
  +-- clear + bounded -----------------------------> build
  |                                                   |
  |                                                   v
  |                                           delivery summary
  |
  +-- missing facts -------------------------------> researcher
  +-- route/scope/priority unclear ----------------> decision-planner
  +-- independent validation needed ---------------> qa
  +-- independent risk review needed --------------> code-reviewer
  +-- real UI/browser/E2E evidence needed ---------> ui-operator
  +-- complex/high-risk/multi-stage/blocked -------> auto-max
  +-- repeated failures / same errors -------------> reflector
```

The default path is intentionally small: `auto-flash -> build -> self-check -> delivery`. Specialist agents are used only when they add necessary evidence, planning, review, or UI/E2E coverage.

### Auto-Max Project Flow

`auto-max` is used when one lightweight loop would hide risk: broad scope, multiple dependent phases, high-risk operations, unclear success criteria, repeated failures, or a delivery gate requiring independent QA/review.

```text
auto-flash detects escalation signal
  |
  v
auto-max takes sole controller ownership
  |
  v
decision-planner: phases, boundaries, gates, stop conditions
  |
  v
researcher: current facts, call chains, dependencies, config evidence
  |
  v
build: minimal implementation for the approved phase
  |
  v
qa: independent validation when required
  |
  v
code-reviewer: independent requirement and regression review
  |
  +-- UI/E2E required --> ui-operator: real browser evidence
  |
  v
phase gate: pass, replan, route failure, or stop
  |
  v
final delivery: changes, reads, validation, review, blockers, residual risk
```

| Phase | Owner | Gate |
| --- | --- | --- |
| Escalation | `auto-flash` -> `auto-max` | `auto-max` accepts sole control and records why escalation is needed. |
| Plan | `decision-planner` | Scope, success criteria, allowed changes, validation level, and stop conditions are executable. |
| Research | `researcher` | Missing facts are resolved or reported as blockers. |
| Build | `build` | Latest files were read; only approved files changed. |
| Validate | `qa` | Required validation is independently covered or honestly marked NOT_COVERED / BLOCKED. |
| Review | `code-reviewer` | Blocking requirement, regression, safety, or over-modification risks are routed. |
| UI/E2E | `ui-operator` | Required browser/UI/E2E evidence is captured or blocked with reason. |
| Deliver | `auto-max` | All gates are closed or residual risk is explicit. |

State ledger entries should stay compact: goal, scope, forbidden scope, active phase, owner, files read, files changed, commands, artifacts, decisions, assumptions, blockers, failed loop count, and residual NOT_COVERED items.

### Routing Decision

| Signal | Route | Purpose |
| --- | --- | --- |
| Clear target, narrow scope, low/medium risk | `auto-flash -> build` | Apply the smallest correct change and verify it. |
| Missing file, dependency, config, call-chain, or evidence facts | `researcher` | Read and report facts without modifying files. |
| Unclear scope, route, priority, phase boundary, or stop condition | `decision-planner` | Define a safe execution boundary. |
| Code/config/script/agent/skill/test/doc change | `build` | Implement inside the approved boundary. |
| Need independent test/build/typecheck/static evidence | `qa` | Validate without reusing `build` conclusions. |
| Need requirement, regression, edge-case, safety, or over-modification review | `code-reviewer` | Review risk without editing files. |
| Need browser interaction, screenshot, real UI path, or E2E | `ui-operator` | Collect real UI/E2E evidence. |
| Complex, high-risk, multi-stage, repeated failure, or gate-heavy work | `auto-max` | Coordinate phases, specialists, QA/review, and replanning. |
| Repeated failures, repeated error types, or agent conclusion conflicts | `reflector` | Produce temporary context_injection without resetting the loop count. |

### Review and QA Model

`build` self-check is necessary but not sufficient for non-trivial risk. It proves the implementation loop is not obviously broken; it does not replace independent validation or review.

| Layer | Owner | Checks | Output |
| --- | --- | --- | --- |
| Implementation self-check | `build` | Latest-file reads, minimal diff, references, syntax/static structure, focused validation | PASS / FAIL / BLOCKED / NOT_COVERED |
| Independent validation | `qa` | Tests, build, typecheck, reproduction, integration path, or requested validation level | Evidence-based PASS / FAIL / BLOCKED / NOT_COVERED |
| Independent review | `code-reviewer` | Requirement fit, regression risk, edge cases, test gaps, safety/data risk, over-modification | Blocking and non-blocking findings |
| UI/E2E evidence | `ui-operator` | Real page path, browser actions, screenshots, console/network when relevant | UI/E2E result and artifacts |

Failure handling:

1. Classify the failure: fact gap, route error, implementation defect, validation environment, review risk, UI/E2E behavior, requirement conflict, or high-risk boundary.
2. Route it to the role that can resolve it.
3. On repeated failures, invoke `reflector` for temporary `context_injection` before retrying; `reflector` does not reset the loop count.
4. Retry from the current file state only; do not roll back to snapshots.
5. Stop after three failed repair/validation loops and report evidence, blockers, residual risk, and recommended next owner.

### Delivery Report

Final delivery should be compact and auditable:

- Changed files: file, operation, purpose.
- Latest reads: files, ranges, dependencies, call paths, or artifacts checked before editing/reviewing.
- Change summary: what each change solves and whether scope stayed minimal.
- Validation record: level, command or method, output summary, PASS / FAIL / BLOCKED / NOT_COVERED.
- Review record: QA/review/UI evidence when used, or why it was not covered.
- Failure loop: failed attempts, fixes, current state, remaining blockers.
- Boundaries: confirmation that scope, safety rules, and high-risk limits were respected.
- Residual risk: what remains unverified and who should handle it next if needed.

### Skills

Skills are domain tools, not complexity badges. Load a skill only when the task object matches its trigger.

Examples:

- Editing opencode config, `AGENTS.md`, permissions, plugins, or MCP -> `customize-opencode`.
- Creating or changing agent files -> `opencode-agent-designer`.
- Governing the skills directory -> `opencode-skill-designer`.
- Creating one skill -> `skill-creator`.
- Installing a supplied skill -> `skill-installer`.
- Unknown root cause or failing behavior -> `diagnose`.
- Test-first known behavior -> `tdd-workflow`.
- Raw CSV/Excel/JSONL/TXT or pandas data work -> `data-processing`.
- BERT, text matching, Cross-Encoder, hard negatives, training/evaluation -> `nlp-modeling`.
- Docker, services, logs, health checks, deployment/server ops -> `deploy-ops`.
- GitHub platform objects -> `gh-ops`.
- Long-term technical memory -> `memory`.
- Non-technical daily-life memory -> `daily-memory`.

Provider/auth/model/API key work is high risk. Real API keys must not be committed or published.

### Required Skills

| Skill | Use when | Safety note |
| --- | --- | --- |
| `customize-opencode` | opencode config, `AGENTS.md`, plugins, MCP, permission schema | Restart opencode after config-time changes. |
| `opencode-agent-designer` | Agent creation, modification, or audit | Not for provider/auth/model work. |
| `opencode-skill-designer` | Skill directory scan, audit, registration, routing, overlap governance | Not for creating one specific skill. |
| `opencode-model-provider` | Provider/auth/model/API key/capability/variant work | Requires explicit confirmation; never expose real keys. |
| `skill-creator` | Create or update one skill | Avoid overlapping skills when narrowing works. |
| `skill-installer` | Install a skill from a supplied repo/path/URL | Use download/API methods; do not operate on `.git`. |
| `diagnose` | Unknown root cause, broken behavior, failing tests, exceptions, flaky failures | Reproduce and gather evidence before fixing. |
| `tdd-workflow` | Test-first known behavior or red-green-refactor | Use `diagnose` first when root cause is unknown. |
| `data-processing` | Raw data cleanup, conversion, sampling, splitting, labels, pandas | Treat user data as sensitive. |
| `nlp-modeling` | NLP modeling, BERT, text matching, Cross-Encoder, training/evaluation | Do not use for raw table cleanup unless tied to training design. |
| `codebase-architecture` | Existing architecture, module boundaries, coupling, refactor/testability analysis | Analysis does not authorize broad refactors. |
| `design-grill` | Stress-test PRDs, plans, designs, feature ideas, vague requirements | Ask one key question at a time. |
| `deploy-ops` | Docker, service logs, health checks, deployment config, server operations | Production/deployment changes require confirmation. |
| `gh-ops` | GitHub issues, PRs, releases, triage, repository search | Mutating GitHub actions require confirmation; do not touch `.git`. |
| `prototype` | Throwaway prototype, UI mock, state-machine sandbox, quick experiment | Not for production implementation. |
| `handoff` | Compact current state for another agent or future session | Redact sensitive data; not durable memory. |
| `memory` | Durable technical decisions, project state, preferences, confirmed root causes | Privacy-sensitive; store only valuable non-sensitive context. |
| `daily-memory` | Non-technical daily notes, feelings, relationships, health, family | Privacy-sensitive; never use for code/project memory. |

### Skill Routing Notes

- Skills trigger by task object and domain match, not by long context, general complexity, or automatic mode.
- Complex work still needs the right task object: diagnosis, TDD, data, modeling, deployment, GitHub, architecture, design, prototype, handoff, memory, or daily memory.
- Provider/auth/API key work requires explicit confirmation and must never publish real keys.
- GitHub mutation requires explicit confirmation and must not operate on `.git`.
- Deployment and production/service operations require explicit confirmation.
- `memory` and `daily-memory` are privacy-sensitive and must stay separated.

### Safety Boundaries

The suite is conservative by default:

- Do not operate on `.git`.
- Do not delete, move, rename, or destructively migrate user data without explicit confirmation.
- Do not perform file-level rollback or overwrite current files with old snapshots.
- Do not start persistent background services.
- Do not mutate production services, deployment state, provider/auth/model/API key settings, MCP/plugin high-risk settings, or GitHub objects without confirmation.
- Do not run formatting, fix, snapshot, golden, fixture update, or write-producing validation commands unless explicitly allowed.
- Do not commit real API keys, private memory, private daily-memory data, secrets, tokens, or local-only personal configuration.

### Quality Gates

Validation levels:

- L0: syntax, imports, config format, frontmatter, Markdown structure, closed code blocks, anchor readability, and static readability.
- L1: focused unit tests, lint, typecheck, or minimal script/sample validation.
- L2: functional path, integration path, key call chain, data flow, or regression path validation.
- L3: UI/E2E, training dry-run, deployment dry-run, service health check, or specialized validation.

Failure loop:

1. Classify the failure.
2. Fix only within the approved boundary.
3. Revalidate from current file state.
4. Stop after three failed repair/validation loops and report evidence, blockers, residual risk, and recommended next owner.

### Usage

#### 1. Keep the expected layout

```text
opencode.jsonc
AGENTS.md
agents/
  *.md
skills/
  */SKILL.md
```

#### 2. Copy into an opencode configuration directory

```bash
mkdir -p ~/.config/opencode
cp opencode.jsonc ~/.config/opencode/opencode.jsonc
cp AGENTS.md ~/.config/opencode/AGENTS.md
cp -R agents ~/.config/opencode/agents
cp -R skills ~/.config/opencode/skills
```

On Windows, copy the same files into the opencode configuration directory under your user profile.

#### 3. Minimal `opencode.jsonc`

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "snapshot": false,
  "default_agent": "auto-flash",
  "instructions": [
    "AGENTS.md"
  ],
  "skills": {
    "paths": [
      "~/.config/opencode/skills"
    ]
  },
  "agent": {
    "plan": {
      "disable": true
    }
  },
  "mcp": {},
  "provider": {}
}
```

#### 4. Restart opencode

opencode loads config, agents, skills, and instructions at startup. After changing `opencode.jsonc`, `AGENTS.md`, files under `agents/`, or any `SKILL.md`, quit and restart opencode. Running sessions do not hot-reload these rules.

## 中文

### 亮点

- 默认轻量主控：`auto-flash` 为明确任务选择最短可靠路径。
- 复杂任务升级：多阶段、高风险或阻塞任务由 `auto-max` 接管唯一主控权。
- 单主控纪律：每轮任务只有一个主控，不并行争夺编排权。
- `build` 是唯一执行单元：读取当前文件、最小修改、自检验证。
- `qa` 独立验证；`code-reviewer` 独立审查。
- `ui-operator` 只在明确需要时处理真实浏览器/UI/E2E 路径。
- skills 按任务对象触发，不按上下文长度或笼统复杂度触发。
- 高风险边界明确：`.git`、provider/auth/model/API key、生产、部署、plugins/MCP、破坏性数据操作和 GitHub 写操作。

### 为什么存在

多数 agent 配置容易走向两个极端：简单任务被重流程拖慢，复杂任务又被单轮局部补丁草率处理，缺少独立证据。本套配置让快路径保持快速，同时把升级、验证、审查和安全边界显式化。

### 一眼看懂

```text
用户任务
   |
   v
auto-flash  -- 明确 + 有边界 --> build --> 自检 --> 交付
   |
   +-- 事实不足 -------------> researcher
   +-- 路线/范围不清 --------> decision-planner
   +-- 独立验证 -------------> qa
   +-- 独立审查 -------------> code-reviewer
   +-- 真实 UI/E2E ---------> ui-operator
   +-- 复杂/高风险 ----------> auto-max
   +-- 反复失败 -------------> reflector

auto-max --> 规划 --> 调研 --> 实现 --> QA --> 审查 --> 可选 UI/E2E --> 门禁交付
```

### 架构

仓库结构：

```text
opencode.jsonc
AGENTS.md
agents/
  auto-flash.md
  auto-max.md
  build.md
  decision-planner.md
  researcher.md
  qa.md
  code-reviewer.md
  ui-operator.md
  reflector.md
skills/
  <skill-name>/SKILL.md
```

控制模型：

```text
主控层
  auto-flash：默认轻量主控
  auto-max：复杂任务的项目级主控

专项层
  build：实现
  researcher：只读事实定位
  decision-planner：只读规划
  qa：独立验证
  code-reviewer：独立审查
  ui-operator：真实 UI/E2E 操作
  reflector：只读失败反思

Skill 层
  仅在任务对象匹配 skill 领域时加载
```

核心原则：

- 每轮任务只有一个主控。
- 简单任务保持轻量。
- 复杂任务升级，不盲目局部修补。
- 实现、验证、审查、规划、调研和 UI 操作分离。
- 修改、验证、审查前读取当前最新文件。
- 交付基于证据，不靠口头断言。

### Agent 角色

| Agent | 角色 | 输出 |
| --- | --- | --- |
| `auto-flash` | 明确中低复杂度任务的默认轻量主控 | 路由、分派、简洁最终交付 |
| `auto-max` | 复杂、多阶段、高风险或阻塞任务的唯一项目级主控 | 阶段计划、状态记录、门禁、最终交付 |
| `build` | 代码、配置、脚本、agent、skill、测试和文档修改的唯一执行单元 | 最小修改和聚焦自检 |
| `decision-planner` | 只读路线、边界、优先级、阶段和验证参谋 | 执行边界、停止条件、门禁建议 |
| `researcher` | 只读文件、配置、依赖、调用链和证据定位 | 带来源的当前事实 |
| `qa` | 独立验证单元 | 带命令或证据的 PASS / FAIL / BLOCKED / NOT_COVERED |
| `code-reviewer` | 独立风险审查单元 | 需求匹配、回归风险、边界、安全、测试缺口 |
| `ui-operator` | 真实 UI/E2E 操作单元 | 浏览器路径、截图、console/network 或 E2E 证据 |
| `reflector` | 连续失败或重复错误时的只读失败反思单元 | 临时 context_injection（最多 3 条，不持久化，不重置失败轮次） |

### 任务流程

`auto-flash` 是默认入口。除非任务本身需要升级，否则保持最短可靠路径。

```text
用户任务
  |
  v
auto-flash：判断目标、范围、风险和事实缺口
  |
  +-- 目标明确 + 边界清晰 ------------------------> build
  |                                                   |
  |                                                   v
  |                                               交付摘要
  |
  +-- 事实不足 ------------------------------------> researcher
  +-- 路线/范围/优先级不清 ------------------------> decision-planner
  +-- 需要独立验证 --------------------------------> qa
  +-- 需要独立风险审查 ----------------------------> code-reviewer
  +-- 需要真实 UI/浏览器/E2E 证据 -----------------> ui-operator
  +-- 复杂/高风险/多阶段/阻塞 ---------------------> auto-max
  +-- 反复失败 / 同类错误 -----------------------> reflector
```

默认路径刻意保持轻量：`auto-flash -> build -> 自检 -> 交付`。只有需要必要证据、规划、审查或 UI/E2E 覆盖时，才使用专项 agent。

### Auto-Max 项目级流程

当单轮轻量闭环会掩盖风险时使用 `auto-max`：范围过宽、多个依赖阶段、高风险操作、成功标准不清、反复失败，或交付门禁要求独立 QA/review。

```text
auto-flash 发现升级信号
  |
  v
auto-max 接管唯一主控权
  |
  v
decision-planner：阶段、边界、门禁、停止条件
  |
  v
researcher：当前事实、调用链、依赖、配置证据
  |
  v
build：在批准阶段内做最小实现
  |
  v
qa：按需独立验证
  |
  v
code-reviewer：独立审查需求和回归风险
  |
  +-- 需要 UI/E2E --> ui-operator：真实浏览器证据
  |
  v
阶段门禁：通过、重排、失败回流或停止
  |
  v
最终交付：修改、读取、验证、审查、阻塞、残余风险
```

| 阶段 | 负责 | 门禁 |
| --- | --- | --- |
| 升级 | `auto-flash` -> `auto-max` | `auto-max` 接受唯一主控，并记录升级原因。 |
| 规划 | `decision-planner` | 范围、成功标准、允许修改、验证层级和停止条件可执行。 |
| 调研 | `researcher` | 事实缺口已补齐，或作为阻塞报告。 |
| 实现 | `build` | 已读取最新文件，只修改批准文件。 |
| 验证 | `qa` | 独立覆盖要求验证，或如实标记 NOT_COVERED / BLOCKED。 |
| 审查 | `code-reviewer` | 阻塞性需求、回归、安全或过度修改风险已回流。 |
| UI/E2E | `ui-operator` | 所需浏览器/UI/E2E 证据已捕获，或带原因阻塞。 |
| 交付 | `auto-max` | 所有门禁关闭，或残余风险明确。 |

状态记录保持简洁：目标、范围、禁止范围、当前阶段、负责角色、已读文件、已改文件、命令、产物、决策、假设、阻塞、失败轮次和残余 NOT_COVERED 项。

### 路由判断

| 信号 | 路由 | 目的 |
| --- | --- | --- |
| 目标明确、范围窄、中低风险 | `auto-flash -> build` | 做最小正确修改并验证。 |
| 缺少文件、依赖、配置、调用链或证据事实 | `researcher` | 只读补事实，不改文件。 |
| 范围、路线、优先级、阶段边界或停止条件不清 | `decision-planner` | 定义安全执行边界。 |
| 代码/配置/脚本/agent/skill/测试/文档修改 | `build` | 在批准边界内实现。 |
| 需要独立测试/构建/typecheck/静态证据 | `qa` | 不复用 `build` 结论，独立验证。 |
| 需要需求、回归、边界、安全或过度修改审查 | `code-reviewer` | 只读审查风险。 |
| 需要浏览器交互、截图、真实 UI 路径或 E2E | `ui-operator` | 收集真实 UI/E2E 证据。 |
| 复杂、高风险、多阶段、反复失败或重门禁任务 | `auto-max` | 统筹阶段、专项 agent、QA/review 和重排。 |
| 反复失败、同类错误或多 agent 结论冲突 | `reflector` | 输出临时 context_injection，不重置失败轮次。 |

### 审查与 QA 模型

`build` 自检是必要的，但不能覆盖非平凡风险。它只能证明实现闭环没有明显损坏，不能替代独立验证或审查。

| 层级 | 负责 | 检查内容 | 输出 |
| --- | --- | --- | --- |
| 实现自检 | `build` | 最新文件读取、最小 diff、引用、语法/静态结构、聚焦验证 | PASS / FAIL / BLOCKED / NOT_COVERED |
| 独立验证 | `qa` | 测试、构建、typecheck、复现、集成路径或指定验证层级 | 基于证据的 PASS / FAIL / BLOCKED / NOT_COVERED |
| 独立审查 | `code-reviewer` | 需求匹配、回归风险、边界条件、测试缺口、安全/数据风险、过度修改 | 阻塞与非阻塞发现 |
| UI/E2E 证据 | `ui-operator` | 真实页面路径、浏览器操作、截图、必要 console/network | UI/E2E 结果和产物 |

失败处理：

1. 分类失败：事实缺口、路线错误、实现缺陷、验证环境、审查风险、UI/E2E 行为、需求冲突或高风险边界。
2. 回流给能解决问题的角色。
3. 反复失败时先调用 `reflector` 输出临时 `context_injection` 再重试；`reflector` 不重置失败轮次。
4. 只基于当前文件状态重试，不回滚 snapshot。
5. 三轮修复/验证失败后停止，报告证据、阻塞、残余风险和建议接手对象。

### 交付报告

最终交付应简洁且可审计：

- 修改文件：文件、操作、目的。
- 最新读取：修改/审查前读取的文件、范围、依赖、调用路径或产物。
- 修改摘要：每个改动解决什么问题，是否保持最小范围。
- 验证记录：层级、命令或方法、输出摘要、PASS / FAIL / BLOCKED / NOT_COVERED。
- 审查记录：已使用的 QA/review/UI 证据，或未覆盖原因。
- 失败回环：失败尝试、修复轮次、当前状态、剩余阻塞。
- 边界说明：确认范围、安全规则和高风险边界已遵守。
- 残余风险：仍未验证的内容，以及必要时建议谁接手。

### Skills

Skills 是领域工具，不是复杂度标签。只有任务对象匹配触发条件时才加载。

示例：

- 修改 opencode 配置、`AGENTS.md`、权限、plugins 或 MCP -> `customize-opencode`。
- 创建或修改 agent 文件 -> `opencode-agent-designer`。
- 治理 skills 目录 -> `opencode-skill-designer`。
- 创建单个 skill -> `skill-creator`。
- 安装给定 skill -> `skill-installer`。
- 根因未知或行为失败 -> `diagnose`。
- 已知行为的测试先行 -> `tdd-workflow`。
- 原始 CSV/Excel/JSONL/TXT 或 pandas 数据处理 -> `data-processing`。
- BERT、文本匹配、Cross-Encoder、hard negative、训练/评估 -> `nlp-modeling`。
- Docker、服务、日志、健康检查、部署/服务器运维 -> `deploy-ops`。
- GitHub 平台对象 -> `gh-ops`。
- 长期技术记忆 -> `memory`。
- 非技术日常记忆 -> `daily-memory`。

provider/auth/model/API key 属于高风险边界。不要提交或发布真实 API key。

### 必要 Skills

| Skill | 使用场景 | 安全说明 |
| --- | --- | --- |
| `customize-opencode` | opencode 配置、`AGENTS.md`、plugins、MCP、权限 schema | 修改配置加载期文件后需要重启 opencode。 |
| `opencode-agent-designer` | 创建、修改或审计 agent | 不用于 provider/auth/model 工作。 |
| `opencode-skill-designer` | skills 目录扫描、审计、注册、路由、重叠治理 | 不用于创建单个具体 skill。 |
| `opencode-model-provider` | provider/auth/model/API key/能力/variant 工作 | 需要明确确认；不得暴露真实 key。 |
| `skill-creator` | 创建或更新单个 skill | 能收窄已有 skill 时，不创建重叠 skill。 |
| `skill-installer` | 从给定 repo/path/URL 安装 skill | 使用下载/API 方法；不操作 `.git`。 |
| `diagnose` | 根因未知、行为异常、测试失败、异常、flaky、回归 | 先复现和取证，再修复。 |
| `tdd-workflow` | 测试先行、已知行为或 red-green-refactor | 根因未知时先用 `diagnose`。 |
| `data-processing` | 原始数据清洗、转换、采样、切分、标签、pandas | 用户数据按敏感信息处理。 |
| `nlp-modeling` | NLP 建模、BERT、文本匹配、Cross-Encoder、训练/评估 | 原始表格清洗不使用它，除非服务训练设计。 |
| `codebase-architecture` | 既有架构、模块边界、耦合、重构/可测试性分析 | 架构分析不等于授权大范围重构。 |
| `design-grill` | 压测 PRD、计划、设计、功能想法、模糊需求 | 一次只问一个关键问题。 |
| `deploy-ops` | Docker、服务日志、健康检查、部署配置、服务器操作 | 生产/部署变更需要确认。 |
| `gh-ops` | GitHub issue、PR、release、triage、仓库搜索 | GitHub 写操作需确认；不碰 `.git`。 |
| `prototype` | 抛弃式原型、UI mock、状态机 sandbox、快速实验 | 不用于生产实现。 |
| `handoff` | 给其他 agent 或未来会话压缩当前状态 | 需要脱敏；不是长期记忆。 |
| `memory` | 长期技术决策、项目状态、偏好、已确认根因 | 隐私敏感；只保存有价值且非敏感上下文。 |
| `daily-memory` | 非技术日常、想法感受、人际关系、健康、家庭 | 隐私敏感；不要用于代码/项目记忆。 |

### Skill 路由说明

- skills 按任务对象和领域匹配触发，不按上下文长度、笼统复杂度或自动模式触发。
- 复杂任务仍要匹配具体对象：诊断、TDD、数据、建模、部署、GitHub、架构、设计、原型、交接、记忆或日常记忆。
- provider/auth/API key 工作需要明确确认，且不得发布真实 key。
- GitHub 写操作需要明确确认，且不得操作 `.git`。
- 部署和生产/服务操作需要明确确认。
- `memory` 和 `daily-memory` 都是隐私敏感能力，必须分开使用。

### 安全边界

这套配置默认保守：

- 不操作 `.git`。
- 未明确确认，不删除、移动、重命名或破坏性迁移用户数据。
- 不做文件层回滚，不用旧 snapshot 覆盖当前文件。
- 不启动持久后台服务。
- 未确认，不修改生产服务、部署状态、provider/auth/model/API key、MCP/plugin 高风险配置或 GitHub 对象。
- 未明确允许，不运行 format、fix、snapshot、golden、fixture 更新或其他会写入的验证命令。
- 不提交真实 API key、私有 memory、私有 daily-memory 数据、secrets、tokens 或本地私有配置。

### 质量门禁

验证层级：

- L0：语法、导入、配置格式、frontmatter、Markdown 结构、代码块闭合、锚点可读性和静态可读性。
- L1：相关单测、lint、typecheck、最小脚本或最小样本验证。
- L2：功能路径、集成路径、关键调用链、数据流或回归路径验证。
- L3：UI/E2E、训练 dry-run、部署 dry-run、服务健康检查或专项验证。

失败回环：

1. 分类失败。
2. 只在批准边界内修复。
3. 基于当前文件状态重新验证。
4. 三轮修复/验证失败后停止，报告证据、阻塞、残余风险和建议接手对象。

### 使用方法

#### 1. 保持预期结构

```text
opencode.jsonc
AGENTS.md
agents/
  *.md
skills/
  */SKILL.md
```

#### 2. 复制到 opencode 配置目录

```bash
mkdir -p ~/.config/opencode
cp opencode.jsonc ~/.config/opencode/opencode.jsonc
cp AGENTS.md ~/.config/opencode/AGENTS.md
cp -R agents ~/.config/opencode/agents
cp -R skills ~/.config/opencode/skills
```

Windows 下复制到当前用户的 opencode 配置目录即可。

#### 3. 最小 `opencode.jsonc`

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "snapshot": false,
  "default_agent": "auto-flash",
  "instructions": [
    "AGENTS.md"
  ],
  "skills": {
    "paths": [
      "~/.config/opencode/skills"
    ]
  },
  "agent": {
    "plan": {
      "disable": true
    }
  },
  "mcp": {},
  "provider": {}
}
```

#### 4. 重启 opencode

opencode 在启动时加载配置、agents、skills 和 instructions。修改 `opencode.jsonc`、`AGENTS.md`、`agents/` 下文件或任意 `SKILL.md` 后，需要退出并重启 opencode。当前运行中的会话不会热加载这些规则。
