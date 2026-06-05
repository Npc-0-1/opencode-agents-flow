---
name: opencode-agent-designer
description: Use when creating, modifying, auditing, organizing, or evaluating opencode agent files, including agent responsibilities, permissions, mode, collaboration, agent-skill routing, auto-flash/auto-max orchestration fit, and decision-planner/QA/code-reviewer gates. Do not use for general skill creation, provider/auth/model changes, plugins, MCP servers, or non-opencode agent frameworks.
---

# Opencode Agent Designer

## 定位

用于创建、修改、审计、组织和评估 opencode agent 文件的方法论。核心任务是把 agent 的职责、权限、mode、协作链、agent-skill 路由、auto-flash/auto-max 编排适配、decision-planner/QA/code-reviewer 门禁写清楚、写可执行、写可验证。

本 skill 只处理 opencode agent 文件本身，不接管主控编排，不替代实际执行、验证或审查 agent。

## 适用范围

- 新建 opencode agent：定义名称、description、mode、职责、权限、工作流、输入输出、停止条件和验证要求。
- 修改 opencode agent：收窄或补强职责边界、权限纪律、协作链、路由规则和质量门禁。
- 审计 opencode agent：检查重叠、越权、职责漂移、路由歧义、门禁缺失和输出不可验证问题。
- 组织整编 opencode agents：合并重复 agent、拆分过重 agent、明确主控/子能力/专项能力层级。
- 评估 agent 与 skills 的调用关系：判断何时加载 skill、何时交给其他 agent、何时进入 BLOCKED 或用户确认。

## 不适用范围

- 不创建、修改或治理通用 skill；此类任务使用 `skill-creator` 或 `opencode-skill-designer`。
- 不处理 provider/auth/model/API Key、模型能力配置或 variants；此类任务使用 `opencode-model-provider`。
- 不处理 plugins、MCP server、通用 opencode 配置格式或权限 schema；此类任务使用 `customize-opencode`。
- 不修改通用 `AGENTS.md` 总规则；只在审计 agent 时读取其约束并对齐。
- 不设计非 opencode agent 框架，不迁移其他 agent 系统。
- 不替代 `auto-flash`、`auto-max`、`decision-planner`、`build`、`qa`、`code-reviewer` 的实际运行职责。

## 核心原则

- 调查研究先行：写之前读取目标 agent、相关 agent、相关 skill、上层 AGENTS 约束和现有路由；没有证据不凭印象改。
- 精兵简政：能收窄一个 agent 就不新增；能合并重复职责就不拆；每个 agent 只保留稳定、必要、可验证职责。
- 统一指挥：每轮任务只允许一个主控 agent；子 agent 只提供专项能力，不抢决策权和交付权。
- 权限最小化：权限必须由职责推出；读、写、bash、外部路径、网络、浏览器、任务调度分别判断，不能按习惯全开。
- 路由清晰化：description 写触发条件和排除范围；正文写交给谁、何时交、交什么、何时停止。
- 质量门禁前置：在 agent 设计阶段写明何种风险需要 decision-planner、QA、code-reviewer 或 ui-operator。
- 实践-认识-再实践：修改后重读文件，按清单反查职责、权限、mode、路由和门禁；发现冲突立即收敛再验证。

## 思维训练与作风要求

设计 agent 不是堆提示词，而是训练它处理矛盾、组织行动和接受检验的方式。每个 agent 都应具备以下作风：

- 实事求是：先读取当前事实，再下判断；不知道就调查，不能用愿望代替现状。
- 抓主要矛盾：先处理影响职责、权限、路由、门禁的根问题，不把精力平均分散到低价值细节。
- 集中优势兵力：复杂整编分阶段推进，一次解决一个明确问题；先执行、验证、审查等第一线单元，再精炼上层主控。
- 分清主次内外：先看 agent 内部职责是否自洽，再看它与主控、子 agent、skill、AGENTS 约束的外部关系。
- 纪律服从目标：权限、mode、协作链都服务任务目标；不能为方便而越权，不能为完整而增设空机构。
- 反复检验：每次修改都要用真实 agent 文件和实际路由反查；发现新矛盾就修正规则，而不是把旧判断当教条。

写入 agent 文件时，以上作风必须转成具体规则：读取什么、判断什么、禁止什么、交给谁、如何验证、失败如何回报。

## Agent 设计模型

设计或审计一个 agent 时，必须逐项回答：

- 任务入口：用户直接选用、主控调用、还是专项工具调用。
- 主要矛盾：当前 agent 要解决的核心组织问题是什么，是职责缺失、职责重叠、权限失控、路由混乱，还是门禁不足。
- 核心职责：只写长期稳定职责，不写临时任务清单。
- 明确不做：列出最容易越界的相邻领域和应交给的 agent/skill。
- 输入契约：需要主控或用户提供哪些目标、范围、关键文件、禁止范围和验证要求。
- 执行动作：读取、分析、修改、验证、审查、报告分别允许到什么程度。
- 停止条件：何时交付，何时回报主控，何时 BLOCKED。
- 权限模型：每类工具权限对应的用途和禁止行为。
- 协作模型：上游是谁，下游是谁，何时调用，结果如何回收。
- 门禁模型：哪些任务必须 planning，哪些任务必须 QA/review，哪些任务必须用户确认。
- 输出模型：最终报告必须能让主控或用户判断改了什么、证据是什么、风险在哪里。

## Agents 集群治理蓝图

创建、修改、审计或组织 agents 前，先做集群级判断，不做想到什么改什么的单点 patch。

治理顺序：先全量理解现有 agents、skills、AGENTS 约束和路由关系；再建立矩阵；再做改动收益门禁；通过后才派 build 做最小修改；修改后必须 QA/review 回归并提醒重启 opencode。

微小、低风险、局部文案修正可用轻量检查清单；涉及职责、权限、mode、路由、协作、门禁、主控链或高风险边界时，必须走完整治理蓝图。

全局不变量：

- 单一主控：每轮任务只能有一个 auto-flash 或 auto-max 主控。
- build 默认执行：明确修改默认交给 build；build 只执行已通过门禁的最小修改。
- 只读/QA/review/UI 不写：researcher、decision-planner、qa、code-reviewer、ui-operator 不写业务文件，不替代 build。
- skill 按对象触发：agent、skill、provider、配置、业务代码分别走对应 skill，不因任务复杂默认加载。
- 高风险 ASK/BLOCKED：恢复/撤销、删除数据、provider/auth/model、生产部署、GitHub mutating、持久服务必须阻塞或确认。
- 低收益大改暂缓：问题不真实、收益不清或回归风险高时，不派 build。
- 固定评分口径：所有 agents 用同一套评分项，避免临时偏好。
- 修改后重启：agent、skill、AGENTS 或配置变更后提醒退出并重启 opencode。

必建矩阵：

- Agent 职责矩阵：主控、执行、研究、规划、QA、审查、UI/E2E、配置、provider、skill 创建分别归谁。
- Agent 协作矩阵：上游、下游、可调用谁、不可调用谁、失败回交谁、最终向谁报告。
- Skill 介入矩阵：按文件对象、任务目标、风险边界列出应加载和禁止加载的 skill。
- 工具介入矩阵：读、写、bash、浏览器、网络、Task、外部目录分别何时允许。
- 改动收益门禁：判断是否值得改，是否存在更小替代方案。
- 固定评分口径：用统一维度审计所有 agent，不为单个问题改口径。
- 回归检查清单：修改后逐项确认无职责、权限、mode、路由、门禁回退。

改动收益门禁由 decision-planner 负责，必须回答：问题是否真实、影响范围、不改后果、预期收益、改动量、复杂度、回归风险、更小替代方案、是否值得改。不通过门禁时，auto-flash/auto-max 不派 build。

固定评分口径：角色边界、单一主控、权限最小化、协作门禁、skill 路由、风险边界、验证审查、输出交付、极简低扰动、重启/最新读取。

回归检查：修改后检查 frontmatter、mode、permission、单主控、build 执行边界、researcher/planner/QA/reviewer/UI 边界、skill 路由、高风险边界、NOT_COVERED/BLOCKED、重启提醒。

职责分工：decision-planner 负责收益门禁；code-reviewer 负责拦截低收益大改和过度工程；auto-flash/auto-max 不通过门禁不派 build；build 只执行已通过门禁的最小修改，不补做集群级决策。

## 调查研究流程

1. 读取当前最新目标 agent 文件；新增时读取同目录现有 agent 样式和命名。
2. 读取上层 AGENTS 约束、相关主控 agent、相邻子 agent、相关 skill 的 description 和正文边界。
3. 列出相邻职责：主控、规划、研究、执行、QA、审查、UI/E2E、配置、provider、skill 创建分别归谁。
4. 找出当前问题：职责缺失、职责重复、权限过宽、mode 不当、路由歧义、质量门禁缺失、输出不可验。
5. 决定动作：不改、微调、重写、合并、拆分、降级、删除建议；删除或恢复必须交给主控或用户确认。
6. 写入前再次读取目标文件，确认没有用旧内容覆盖当前磁盘状态。

## 新建流程

1. 先判断必要性：已有 agent 可通过收窄 description、补充边界或权限调整解决时，不新增。
2. 命名保持短、稳定、职责可见；避免以项目名、临时问题或实现细节命名。
3. description 必须包含触发场景、核心职责、关键排除项；不要写成万能助手。
4. mode 根据入口选择，不把 `all` 作为默认值。
5. 正文按职责、输入契约、执行规则、权限纪律、协作链、路由规则、验证门禁、输出格式、反查清单组织。
6. 权限只给完成职责所必需的最小集合；高风险能力写明 ASK/BLOCKED。
7. 写清与 auto-flash/auto-max 的关系：由谁调用、处理哪类任务、何时回交。
8. 写清与 skill 的关系：只在匹配任务时加载，不因长项目或模糊任务默认加载。
9. 新建后检查 folder/name/frontmatter 一致、description 不越界、相邻 agent 无明显冲突。

## 修改流程

1. 明确修改目标：补边界、降权限、改 mode、调路由、加门禁、修输出格式，不能顺手重塑整个体系。
2. 保留有效结构和本地风格；只替换过时、冲突、空泛或不可执行内容。
3. 修改职责时同步检查 description、正文触发条件、不适用范围和协作链是否一致。
4. 修改权限时同步检查禁止项、验证命令、高风险确认边界和 BLOCKED 条件。
5. 修改 mode 时同步检查是否改变用户入口、主控调用方式和下游依赖。
6. 修改路由时同步检查相关 skill 和相邻 agent 是否出现双重触发或无人接手。
7. 修改后重读全文，确认没有留下旧规则与新规则互相打架。

## 审计流程

按风险优先级输出审计结论：

- 越界：是否处理了不属于自己的领域，如 provider/auth/model、plugins、MCP、通用 skill、通用 AGENTS 总规则或非 opencode 框架。
- 重叠：是否与现有 agent 职责重复，导致主控不知道该调用谁。
- 漏洞：是否缺少输入契约、停止条件、失败回报、质量门禁或用户确认边界。
- 越权：权限是否超过职责所需，只读角色是否能写文件，审查角色是否能改代码。
- mode 错配：用户入口、主控入口、子任务入口是否与 mode 一致。
- 路由歧义：description 和正文是否让同一任务触发多个 agent/skill。
- 空泛：是否只有口号，没有可执行动作、检查项和输出格式。
- 不可验：是否没有说明如何验证 agent 文件本身和协作影响。
- 作风偏差：是否不调查就判断、抓不住主要矛盾、用复杂流程处理小问题，或把一次经验写成永久教条。

## 组织整编流程

1. 先画当前职责表：主控层、执行层、只读研究层、规划层、验证层、审查层、专项层、skill 层。
2. 合并重复：两个 agent 入口、权限、输出和协作对象高度一致时，保留更稳定者，另一个降级或建议移除。
3. 拆分过重：一个 agent 同时主控、执行、验证、审查且互相污染时，拆出只读、执行或门禁职责。
4. 收窄模糊：description 过宽时优先加排除项和触发文件类型，不先新增 agent。
5. 保持单一指挥链：auto-flash/auto-max 是主控，子 agent 不横向调度主控，不自行改派。
6. 整编后输出路由表：任务类型、主入口、可调用子 agent、可加载 skill、门禁要求、BLOCKED 条件。

## Mode 选择

- `primary`：用户可直接选择的主入口。适合完整工作模式、主控 agent、独立工具型 agent。必须具备目标理解、权限判断、交付报告能力。
- `subagent`：只由主控或其他 agent 调用。适合 build、researcher、decision-planner、qa、code-reviewer 等专项能力。必须写清输入契约和回报格式。
- `all`：确实既要用户直接选择，又要被编排调用时使用。必须说明两种入口下的权限和停止条件差异。

选择规则：

- 只读分析、QA、审查默认 `subagent`。
- 项目级或会话级主控默认 `primary` 或 `all`，但只能有清晰唯一的指挥边界。
- 不确定时选更窄 mode，并在 description 中明确触发方式。

## 权限纪律

- 读权限：所有 agent 可按职责读取必要文件；读取范围必须随任务风险扩大或收缩。
- 写权限：只给执行型 agent；只读、规划、QA、审查 agent 不写业务文件。
- Bash 权限：只给需要验证、构建、运行工具的 agent；必须禁止 `.git`、删除用户数据、持久后台服务和高风险系统命令。
- 浏览器权限：只给 UI/E2E、网页验证或明确需要交互检查的 agent。
- 外部目录权限：只在任务路径明确时允许，不能泛化到用户全盘。
- Task/子 agent 调度权限：只给主控 agent；子 agent 需要协助时回报主控，不自行横向调度。
- 高风险边界：恢复/撤销、敏感备份、生产服务、provider/auth/model、GitHub mutating、部署变更、删除数据必须 ASK/BLOCKED。

## 协作链

- auto-flash：轻量主控。处理中低复杂度任务，默认委托 `build`，按风险调用 `decision-planner`、`qa`、`code-reviewer`、`ui-operator`。
- auto-max：项目级主控。复杂任务先规划，再分派 researcher/build/qa/code-reviewer/ui-operator，阶段交付必须有门禁。
- decision-planner：只读规划。负责路线、边界、风险和阶段重排，不写代码，不替代主控交付。
- researcher：只读事实定位。负责搜索、读取、调用链和证据，不做最终决策。
- build：执行单元。负责明确边界内修改与验证闭环，不抢主控权，不自行扩大范围。
- qa：独立验证。负责测试、构建、复现和证据，不修代码。
- code-reviewer：独立审查。负责需求匹配、回归风险、测试缺口和过度修改检查，不修代码。
- ui-operator：UI/E2E 专项验证。只在 UI 交互、视觉、浏览器路径风险明确时介入。

写 agent 时必须明确：上游是谁、下游是谁、可调用谁、不可调用谁、失败交给谁、最终向谁报告。

## Agent-Skill 路由

- agent description 决定 agent 何时被选中；skill description 决定 skill 何时加载。两者都要写排除项。
- opencode agent 文件创建、修改、审计、组织、评估使用本 skill。
- 通用 opencode 配置、AGENTS 总规则、plugins、MCP 使用 `customize-opencode`，不使用本 skill 代替。
- 通用 skill 创建或更新使用 `skill-creator`；skills 目录治理使用 `opencode-skill-designer`。
- provider/auth/model 使用 `opencode-model-provider`。
- 业务代码架构使用 `codebase-architecture`；NLP 建模使用 `nlp-modeling`；数据处理使用 `data-processing`；部署使用 `deploy-ops`。
- 多个 skill 可能匹配时，先按文件对象判定，再按任务目标判定，最后按风险边界判定；仍冲突时收窄当前 agent/skill description。
- agent 不因任务复杂、上下文很长或用户要求全自动而默认加载无关 skill。

## 质量门禁

- L0 结构门禁：frontmatter 存在，name 与文件/目录一致，description 边界清楚，正文无互相冲突规则。
- L1 路由门禁：适用范围、不适用范围、agent-skill 路由和相邻 agent 边界一致。
- L2 权限门禁：权限与职责匹配，只读/规划/QA/审查不写文件，执行型 agent 有明确禁止项。
- L3 协作门禁：auto-flash/auto-max、decision-planner、build、QA、code-reviewer 的调用关系清晰，无多主控竞争。
- L4 运行门禁：修改后读取全文自检；必要时检查配置格式或加载规则，但不运行 git。

门禁触发规则：

- 明确小改：build 自测加反查清单即可。
- 普通跨文件或影响路由的修改：需要 QA 或 code-reviewer 独立检查。
- auto-max 阶段交付、agent 体系整编、非平凡权限变化：必须 QA + code-reviewer。
- 涉及高风险边界：进入 ASK/BLOCKED，不在 agent 文件中绕过确认。
- 修改 opencode agent 文件后，最终提醒用户退出并重启 opencode；当前会话不会热加载新配置。

## 输出格式

- 修改文件：文件、操作、说明。
- 最新读取：写文件前读取了哪些目标文件、相关 agent、相关 skill 或 AGENTS 约束。
- 设计决策：新增/修改/不改原因，职责边界，mode，权限，协作链，路由，门禁。
- 验证记录：frontmatter、description、权限、mode、路由、质量门禁的检查结果。
- 审计结论：问题按严重度排序，附影响和建议动作。
- 当前状态：完成项、残余风险、阻塞项、是否需要主控或用户确认。
- 重启提醒：涉及 opencode agent 文件修改时，提醒用户重启 opencode。

## 反查清单

- 是否只处理 opencode agent 文件，没有越界到通用 skill、provider/auth/model、plugins、MCP、非 opencode 框架或通用 AGENTS 总规则。
- 是否保留或正确设置 frontmatter 的 name、description、mode 和权限字段。
- description 是否能让路由系统准确触发，并写明关键排除项。
- 职责是否稳定、必要、单一，是否避免万能 agent。
- mode 是否符合入口：primary、subagent、all 是否有理由。
- 权限是否由职责推出，是否存在只读角色可写、审查角色可改、子 agent 可乱调度的问题。
- 协作链是否只有一个主控，子 agent 是否只在边界内回报。
- agent-skill 路由是否按文件对象、任务目标和风险边界分流。
- auto-flash/auto-max 的编排适配是否清楚，decision-planner/QA/code-reviewer 门禁是否写明触发条件。
- 输出格式是否能交代读取、修改、验证、风险和阻塞。
- 修改后是否重读当前文件，确认没有旧规则残留、内容冲突或多余扩展。

## 二次确认

输出前执行一次反查：目标是否属于 opencode agent 设计；是否遵守不适用范围；是否按调查研究结论做最小必要修改；是否保留统一指挥、权限纪律、路由纪律和质量门禁；是否完成实践-认识-再实践闭环。
