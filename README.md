# opencode-agents-flow

An opencode agents/skills/rules suite that stays light by default, escalates only when needed, and keeps implementation, QA, review, and UI/E2E evidence separate. State is split across decision (in-context), progress (TodoWrite), and persistence (`.kiro-state/`), with the controller as the single writer.

## English

### Highlights

- Lightweight by default: `auto-flash` picks the shortest reliable path; `auto-max` takes sole control for complex/high-risk/multi-stage work.
- Role separation: `build` is the only execution unit; `qa` / `code-reviewer` / `ui-operator` are independent and never replace each other.
- Three-layer state: Long Task State (decision, in-context) + TodoWrite (progress, in-session) + `.kiro-state/` (persistence, on-disk, project-scoped).
- Single-writer state machine: only the controller writes `.kiro-state/`; subagents return evidence and let the controller persist.
- Disk is truth, state is navigation: file mtime is a soft signal; the actual file content on disk is the only ground truth.
- Qualitative failure loop: rerouting requires repeated `failure_type` / route / assumption with no substantial progress, not a fixed loop count.
- Milestone-amortized validation: `build` self-check (L0/L1) advances within a milestone; `qa` + `code-reviewer` run in batch at milestone boundaries — amortization, not gate downgrade.
- Layered write authority: controller may Write/Edit `.kiro-state/` directly; all business files still go through `build` → `qa` → `code-reviewer` → controller delivery.

## Table of Contents

- [English](#english)
  - [Highlights](#highlights)
  - [Comparison with mainstream multi-agent frameworks](#comparison-with-mainstream-multi-agent-frameworks)
  - [At a glance](#at-a-glance)
  - [Repository layout](#repository-layout)
  - [Agent roles](#agent-roles)
  - [Three-layer state](#three-layer-state)
  - [.kiro-state/ subsystem](#kiro-state-subsystem)
  - [Failure loop](#failure-loop)
  - [Progress vs risk](#progress-vs-risk)
  - [Skills](#skills)
  - [Safety boundaries](#safety-boundaries)
  - [Quality gates](#quality-gates)
  - [Usage](#usage)
- [中文](#中文)
  - [亮点](#亮点)
  - [与主流多 agent 框架的差异](#与主流多-agent-框架的差异)
  - [一眼看懂](#一眼看懂)
  - [仓库结构](#仓库结构)
  - [Agent 角色](#agent-角色)
  - [三层状态](#三层状态)
  - [.kiro-state/ 子系统](#kiro-state-子系统)
  - [失败回环](#失败回环)
  - [进度风险二分](#进度风险二分)
  - [Skills](#skills-1)
  - [安全边界](#安全边界)
  - [质量门禁](#质量门禁)
  - [使用方法](#使用方法)

### Comparison with mainstream multi-agent frameworks

| Dimension | LangGraph / AutoGen / CrewAI etc. | flow |
| --- | --- | --- |
| Default path | Full graph / round-robin / sequential pipeline | Shortest reliable path; escalate only when needed |
| Validation independence | Tool calls inside the same loop | `qa` / `code-reviewer` hold independent frontmatter permissions; never reuse `build` conclusions |
| Failure handling | Retry policy / chat-loop | Qualitative `failure_type` + `reflector` `context_injection` (max 3) |
| State persistence | Whole-graph checkpoint / chat history | Three-layer split (decision + progress + `.kiro-state/`) with single-writer controller |
| Audit trail | Runtime logs | Plain-text snapshot + append-only log under `.kiro-state/` |

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
   +-- complex/high-risk -------> auto-max (ownership transfer)
   +-- repeated failures -------> reflector

auto-max --> plan --> research --> build --> qa --> review --> optional UI/E2E --> gated delivery
```

L0 exceptions only: pure answers, read-only analysis, version/path queries, explicit tiny demos. Otherwise **every formal file change goes through `build` → `qa` → `code-reviewer` → controller delivery**.

### Repository layout

```text
opencode.jsonc           # Engine permission matrix
AGENTS.md                # Trunk rules (single file, includes skill routing and state subsystem)
agents/*.md              # 9 agents: auto-flash / auto-max / build / decision-planner /
                         #           researcher / qa / code-reviewer / ui-operator / reflector
skills/*/SKILL.md        # Domain skills
.kiro-state/             # Per-project runtime state, generated under user projects (not shipped with this repo)
```

### Agent roles

| Agent | Role | Verdict vocabulary |
| --- | --- | --- |
| `auto-flash` | Default lightweight controller | Route, dispatch, compact delivery |
| `auto-max` | Project-level orchestration controller | Phase plan, state, gates, final delivery |
| `build` | Only execution unit | `PASS / FAIL / BLOCKED / NOT_COVERED` |
| `decision-planner` | Read-only planning advisor | Boundary, stop conditions, gate suggestions |
| `researcher` | Read-only fact finder | Sourced current facts |
| `qa` | Independent validation | `PASS / FAIL / BLOCKED / NOT_COVERED` |
| `code-reviewer` | Independent risk review | `PASS / LIMITED_PASS / NEEDS_FIX / BLOCKED` |
| `ui-operator` | Real UI/E2E | Browser path, screenshots, console/network |
| `reflector` | Failure reflection (bash all-deny) | Up to 3 `context_injection`, not persisted |

Only `auto-flash` / `auto-max` are controllers. Every other agent has `task: deny`, preventing lateral scheduling. Verdict vocabularies are not interchangeable.

### Three-layer state

Long tasks separate decision, progress, and persistence. Each layer has a distinct owner, reader, and lifecycle.

| Layer | Owner | Content | Lifecycle |
| --- | --- | --- | --- |
| Decision (Long Task State) | Controller injects into subagent prompt | `objective`, `completion_definition`, `non_negotiables`, `allowed_scope`, `forbidden_scope`, `current_phase`, `quality_gates`, `done`, `not_covered`, `blocked`, `next_action` | In-context only |
| Progress (TodoWrite) | Controller holds and drives | Hierarchical todo tree with status `pending` / `in_progress` / `completed` / `cancelled` | In-session only |
| Persistence (`.kiro-state/`) | Controller-only, via Write/Edit tools | Snapshot fields + append-only log; `INDEX.md` + `tasks/<id>.md` | On-disk, project-scoped |

Subagents run as independent sessions and cannot see TodoWrite. They consume the injected Long Task State, return evidence, and let the controller persist. After any new session or context compaction, the controller re-reads current files; the disk is the source of truth.

### .kiro-state/ subsystem

`.kiro-state/` is the persistence layer for long-task state and processing log. Project-scoped, naturally isolated, travels with the repository.

- Location: `<workdir>/.kiro-state/`. `INDEX.md` indexes all tasks (one row per task, scanned once at session start to locate `active` tasks). Each `tasks/<id>.md` has a snapshot region (overwritable) and an append-only log region.
- Flush triggers: milestone boundaries, before high-risk operations, and on substantive state change. Each flush also appends one log entry.
- Write implementation: Write/Edit tools only. Bash redirection is forbidden because it bypasses permission audit. Append uses "Read existing → append → Write overwrite".
- Direct-write authority: only `auto-flash` / `auto-max` write `.kiro-state/`, and only for state and log files. This is the single exemption from the `build` → `qa` → `code-reviewer` chain. Business files (code, config, agent, skill, formal docs) still go through the chain.
- Legacy projects: a project without `.kiro-state/` is fine. Recovery degrades silently and does not raise errors.

### Failure loop

Classified by `failure_type` (transient / logic / route / fact gap / requirement conflict / high-risk boundary) and routed accordingly. Whether to reroute depends on substantial progress, not a fixed count:

```text
progress_made = whether this round produced (new fact ∪ scope reduction ∪ excluded route ∪ new testable hypothesis)
```

A different angle producing real movement keeps going; the same approach repeating in place triggers `reflector` → `decision-planner` reroute. `context_injection` is capped at 3 items, scoped to the current task, never persisted, and never overrides the user goal / `AGENTS.md` / current file facts / high-risk boundaries. Failure records are written into `.kiro-state` `failure_record` (`failure_type` / attempted rounds / excluded routes) to prevent cross-session repetition.

### Progress vs risk

Ask only on risk, never on progress. Once goals and boundaries are clear, in-bounds advancement is fully automatic; passing a gate auto-advances. There is no task-level "max N steps"; self-continuation runs until `completion_definition` is met or a hard risk boundary is hit.

Hard risk boundaries (immediate stop): irreversible operations, production changes, deletion of user data, privilege escalation, `provider/auth/model/API Key`, GitHub mutation, real requirement conflicts with no default, repeated failures still not converging after rerouting.

### Skills

Triggered by task object, not by context length or general complexity. Full routing table in `AGENTS.md` §6.

- opencode self-governance: `customize-opencode` / `opencode-agent-designer` / `opencode-skill-designer` / `opencode-model-provider` / `skill-creator` / `skill-installer`
- Engineering methodology: `design-grill` / `codebase-architecture` / `diagnose` / `tdd-workflow` / `prototype` / `handoff` / `memory` / `daily-memory`
- NLP / data / deploy / GitHub: `nlp-modeling` / `data-processing` / `deploy-ops` / `gh-ops`

### Safety boundaries

- Never operate on `.git` (hard ban, zero exception).
- Without confirmation: never delete/migrate user data; never roll back at the file level; never overwrite current files with old snapshots.
- Without confirmation: never touch production, deployment, `provider/auth/model/API Key`, MCP/plugin high-risk changes, or GitHub mutating actions.
- Never bypass permissions via shell launchers (`cmd / powershell / pwsh / bash / sh`), chained pipes, redirection, `python -c`, `node -e`, or `Invoke-Expression`.
- Never run `--fix` / `--write` / `--snapshot-update` / format / golden / fixture-update commands unless explicitly allowed.
- Never commit real API keys, private memory, secrets, or tokens.

### Quality gates

- L0: syntax, config format, frontmatter, Markdown structure, static readability.
- L1: focused unit tests, lint, typecheck, minimal sample validation.
- L2: functional path, key call chain, regression path.
- L3: UI/E2E, training dry-run, deployment dry-run, service health check.

Except L0, every formal change goes through `build` → `qa` → `code-reviewer` → delivery. QA and code-reviewer must independently read current files and provide evidence; do not reuse `build` conclusions. Mark NOT_COVERED when uncovered; mark BLOCKED on missing environment/permission. **Never fake PASS.** Inside a milestone, `build` self-check (L0/L1) is enough to advance; at milestone boundaries `qa` + `code-reviewer` run in batch — this is amortization, not gate downgrade.

### Usage

```bash
mkdir -p ~/.config/opencode
cp opencode.jsonc ~/.config/opencode/opencode.jsonc
cp AGENTS.md ~/.config/opencode/AGENTS.md
cp -R agents ~/.config/opencode/agents
cp -R skills ~/.config/opencode/skills
```

On Windows, copy into `%USERPROFILE%\.config\opencode\`. The block below is a minimal subset; the full deny matrix is in the repo root `opencode.jsonc`.

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "snapshot": false,
  "default_agent": "auto-flash",
  "instructions": ["AGENTS.md"],
  "skills": { "paths": ["~/.config/opencode/skills"] },
  "agent": { "plan": { "disable": true } },
  "permission": {
    "bash": {
      "*": "ask",
      "cmd": "deny", "cmd.exe": "deny",
      "powershell": "deny", "powershell.exe": "deny",
      "pwsh": "deny", "bash": "deny", "sh": "deny",
      "python -c *": "deny", "node -e *": "deny",
      "Invoke-Expression *": "deny", "iex *": "deny",
      "git *": "deny", "git.exe *": "deny",
      "rm *": "deny", "del *": "deny", "Remove-Item *": "deny", "Rename-Item *": "deny",
      "*;*": "deny", "*&&*": "deny", "*|*": "deny", "*>*": "deny",
      "*$(*": "deny", "*`*": "deny",
      "*--fix": "deny", "*--write*": "deny", "*--snapshot-update*": "deny", "ruff format*": "deny"
    }
  }
}
```

The full version (all deny/ask/allow rules) is in the repo root. `agent.plan.disable=true` only disables the opencode built-in plan agent; it does not affect `decision-planner`.

After modifying `opencode.jsonc` / `AGENTS.md` / `agents/` / `SKILL.md`, **restart opencode**. Running sessions do not hot-reload.

## 中文

### 亮点

- 默认轻量：`auto-flash` 给明确任务选最短可靠路径；复杂、高风险、多阶段任务才升级 `auto-max` 接管唯一主控权。
- 角色分离：`build` 是唯一执行单元；`qa` / `code-reviewer` / `ui-operator` 各自独立，不互相替代。
- 三层状态：决策层 Long Task State（上下文注入）+ 进度层 TodoWrite（会话内）+ 持久层 `.kiro-state/`（落盘，跟项目走）。
- 单写者状态机：只有主控写 `.kiro-state/`，子 agent 只回传证据，由主控持久化。
- 磁盘是真相，状态是导航：mtime 只是软信号，磁盘文件实际内容才是判定依据。
- 失败回环按质性判断：同类 `failure_type` / 路线 / 假设无实质进展才换路，不靠固定轮数。
- 里程碑摊销验证：里程碑内 `build` 自测（L0/L1）即可推进，里程碑边界批量上 `qa` + `code-reviewer`——这是摊销，不是降门禁。
- 写入分层：主控可用 Write/Edit 直写 `.kiro-state/`，业务文件仍走 `build` → `qa` → `code-reviewer` → 主控交付。

### 与主流多 agent 框架的差异

| 维度 | LangGraph / AutoGen / CrewAI 等 | flow |
| --- | --- | --- |
| 默认路径 | 全图 / 轮询 / 顺序流水线 | 最短可靠路径，复杂度升高才升级 |
| 验证独立性 | 同一循环内的工具调用 | `qa` / `code-reviewer` 独立 frontmatter 权限，不复用 build 结论 |
| 失败处理 | 重试策略 / chat-loop | 质性 `failure_type` + `reflector` 临时 `context_injection`（≤3 条） |
| 状态持久化 | 整图 checkpoint / 聊天历史 | 三层分离（决策 + 进度 + `.kiro-state/`）+ 单写者主控 |
| 审计轨迹 | 运行时日志 | `.kiro-state/` 下的纯文本快照 + 只追加日志 |

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
   +-- 复杂/高风险 ----------> auto-max（主控权移交）
   +-- 反复失败 -------------> reflector

auto-max --> 规划 --> 调研 --> 实现 --> QA --> 审查 --> 可选 UI/E2E --> 门禁交付
```

L0 例外仅限：纯回答、只读分析、版本/路径查询、用户明确极小 demo。除此之外，**任何正式文件修改必须 `build` → `qa` → `code-reviewer` → 主控交付**。

### 仓库结构

```text
opencode.jsonc           # 引擎层权限矩阵
AGENTS.md                # 主干规则（单文件，含 skill 路由与状态子系统）
agents/*.md              # 9 个 agent：auto-flash / auto-max / build / decision-planner /
                         #              researcher / qa / code-reviewer / ui-operator / reflector
skills/*/SKILL.md        # 领域 skills
.kiro-state/             # 项目运行时状态，在用户项目中生成（不随本仓库分发）
```

### Agent 角色

| Agent | 角色 | 输出枚举 |
| --- | --- | --- |
| `auto-flash` | 默认轻量主控 | 路由、分派、简洁交付 |
| `auto-max` | 项目级深度编排主控 | 阶段计划、状态、门禁、最终交付 |
| `build` | 唯一执行单元 | `PASS / FAIL / BLOCKED / NOT_COVERED` |
| `decision-planner` | 只读规划参谋 | 边界、停止条件、门禁建议 |
| `researcher` | 只读事实定位 | 带来源的当前事实 |
| `qa` | 独立验证 | `PASS / FAIL / BLOCKED / NOT_COVERED` |
| `code-reviewer` | 独立风险审查 | `PASS / LIMITED_PASS / NEEDS_FIX / BLOCKED` |
| `ui-operator` | 真实 UI/E2E | 浏览器路径、截图、console/network 证据 |
| `reflector` | 失败反思（bash 全 deny） | ≤3 条临时 `context_injection`，不持久化 |

主控只有 `auto-flash` / `auto-max`；其他 agent `task: deny` 锁死，不能横向调度。结论词表互不通用。

### 三层状态

长任务分离决策、进度和持久三层，三层不重复，各自有独立的写入者、读取者和生命周期。

| 层级 | 写入者 | 内容 | 生命周期 |
| --- | --- | --- | --- |
| 决策层（Long Task State） | 主控注入子 agent prompt | `objective`、`completion_definition`、`non_negotiables`、`allowed_scope`、`forbidden_scope`、`current_phase`、`quality_gates`、`done`、`not_covered`、`blocked`、`next_action` | 仅在上下文 |
| 进度层（TodoWrite） | 主控持有并驱动 | 分层 todo 树，状态 `pending` / `in_progress` / `completed` / `cancelled` | 仅在会话内 |
| 持久层（`.kiro-state/`） | 仅主控通过 Write/Edit 工具写 | 快照字段 + 只追加日志；`INDEX.md` + `tasks/<id>.md` | 落盘，跟项目走 |

子 agent 是独立子会话，看不到 TodoWrite。它们消费注入的 Long Task State、回传证据，由主控负责持久化。任何新会话或上下文压缩后，主控按需读磁盘最新代码，以磁盘实际内容为准。

### .kiro-state/ 子系统

`.kiro-state/` 是长任务状态与处理日志的持久层，跟项目走，天然隔离。

- 位置：`<工作目录>/.kiro-state/`。`INDEX.md` 索引所有任务（一行一任务，会话开始时扫一次定位 `active` 任务）；每个 `tasks/<id>.md` = 快照区（可覆盖）+ 处理日志区（只追加）。
- 刷盘时机：里程碑边界、重大风险操作前、状态实质变化时；每次刷盘同时追加一条日志。
- 写实现：仅 Write/Edit 工具；禁止 bash 重定向（绕过权限审计）；日志追加用"Read 现有 → 追加 → Write 覆盖"。
- 主控可直写豁免：仅 `auto-flash` / `auto-max` 直写 `.kiro-state/`，且仅限状态与日志文件。这是 `build` → `qa` → `code-reviewer` 链的唯一豁免；业务文件（代码、配置、agent、skill、正式文档）仍走完整链路。
- 老项目兼容：项目无 `.kiro-state/` 时优雅空转，不报错。

### 失败回环

按 `failure_type` 分类（瞬态 / 逻辑 / 路线 / 事实缺口 / 需求冲突 / 高风险边界）路由到对应角色。是否换路看"有无实质进展"，不靠固定轮数：

```text
progress_made = 本轮是否带来 (新事实 ∪ 缩小范围 ∪ 排除错误路径 ∪ 新可检验假设)
```

只要不同思路真在推进就继续；只有重复同一套路且原地打转才触发 `reflector` → `decision-planner` 换路。`context_injection` ≤ 3 条，仅当前任务有效，不持久化，不能覆盖用户目标 / `AGENTS.md` / 当前文件事实 / 高风险边界。失败记录写入 `.kiro-state` 的 `failure_record` 字段（`failure_type` / 已试轮次 / 已排除路线），防跨会话重复踩坑。

### 进度风险二分

只在风险上问，不在进度上问。任务边界确定后，安全范围内推进动作全自动，过门禁即自动进下一节，禁止在进度上问"要不要继续"。任务级别无"最多 N 步"上限，自我续跑直到 `completion_definition` 满足或命中风险硬边界。

风险硬边界（即时停问）：不可逆操作、生产变更、删除用户数据、权限越界、`provider/auth/model/API Key`、GitHub mutating、需求实质冲突且无默认方案、同类错误换路后仍不收敛。

### Skills

按任务对象触发，不按上下文长度或笼统复杂度触发。完整路由表见 `AGENTS.md` §6。

- opencode 自治：`customize-opencode` / `opencode-agent-designer` / `opencode-skill-designer` / `opencode-model-provider` / `skill-creator` / `skill-installer`
- 工程方法：`design-grill` / `codebase-architecture` / `diagnose` / `tdd-workflow` / `prototype` / `handoff` / `memory` / `daily-memory`
- NLP / 数据 / 部署 / GitHub：`nlp-modeling` / `data-processing` / `deploy-ops` / `gh-ops`

### 安全边界

- 不操作 `.git`（硬性禁令，零例外）。
- 未确认不删除/迁移用户数据，不文件层回滚，不用旧 snapshot 覆盖当前文件。
- 未确认不动生产服务、部署、`provider/auth/model/API Key`、MCP/plugin 高风险变更、GitHub 写操作。
- 不通过 shell launcher（`cmd / powershell / pwsh / bash / sh`）、串联管道、重定向、`python -c`、`node -e`、`Invoke-Expression` 绕过权限。
- 未明确允许，不运行 `--fix` / `--write` / `--snapshot-update` / format / golden / fixture 更新等会写入的命令。
- 不提交真实 API key、私有 memory、secrets、tokens。

### 质量门禁

- L0：语法、配置格式、frontmatter、Markdown 结构、静态可读性。
- L1：相关单测、lint、typecheck、最小样本验证。
- L2：功能路径、关键调用链、回归路径。
- L3：UI/E2E、训练 dry-run、部署 dry-run、服务健康检查。

除 L0 例外，正式文件修改必须 `build` → `qa` → `code-reviewer` → 交付。QA 和 code-reviewer 必须独立读最新文件并给证据，不复用 build 结论。未覆盖写 NOT_COVERED；环境/权限不足写 BLOCKED；**不得伪造 PASS**。里程碑内 `build` 自测（L0/L1）即可推进，里程碑边界批量上 `qa` + `code-reviewer`——这是摊销，不是降门禁。

### 使用方法

```bash
mkdir -p ~/.config/opencode
cp opencode.jsonc ~/.config/opencode/opencode.jsonc
cp AGENTS.md ~/.config/opencode/AGENTS.md
cp -R agents ~/.config/opencode/agents
cp -R skills ~/.config/opencode/skills
```

Windows 复制到 `%USERPROFILE%\.config\opencode\` 即可。下面是最小可用子集；完整 deny 矩阵见仓库根 `opencode.jsonc`。

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "snapshot": false,
  "default_agent": "auto-flash",
  "instructions": ["AGENTS.md"],
  "skills": { "paths": ["~/.config/opencode/skills"] },
  "agent": { "plan": { "disable": true } },
  "permission": {
    "bash": {
      "*": "ask",
      "cmd": "deny", "cmd.exe": "deny",
      "powershell": "deny", "powershell.exe": "deny",
      "pwsh": "deny", "bash": "deny", "sh": "deny",
      "python -c *": "deny", "node -e *": "deny",
      "Invoke-Expression *": "deny", "iex *": "deny",
      "git *": "deny", "git.exe *": "deny",
      "rm *": "deny", "del *": "deny", "Remove-Item *": "deny", "Rename-Item *": "deny",
      "*;*": "deny", "*&&*": "deny", "*|*": "deny", "*>*": "deny",
      "*$(*": "deny", "*`*": "deny",
      "*--fix": "deny", "*--write*": "deny", "*--snapshot-update*": "deny", "ruff format*": "deny"
    }
  }
}
```

完整版（含全部 deny/ask/allow 矩阵）见仓库根目录 `opencode.jsonc`。`agent.plan.disable=true` 仅禁用 opencode 内置 plan agent，不影响 `decision-planner`。

修改 `opencode.jsonc` / `AGENTS.md` / `agents/` / `SKILL.md` 后**必须重启 opencode**，运行中的会话不会热加载。
