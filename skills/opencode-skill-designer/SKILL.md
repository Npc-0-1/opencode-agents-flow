---
name: opencode-skill-designer
description: "Use when scanning, detecting, evaluating, organizing, or governing the opencode skills directory. Triggers on: 扫描 skills、检测空壳 skill、路由一致性检查、未注册 skill、skill 职责重叠、description 触发质量评估、skill 目录治理。Do not use for: individual skill creation methodology (use skill-creator), agent governance (use opencode-agent-designer), opencode config format (use customize-opencode), or provider/auth/model/API Key changes."
---

# Opencode Skill Designer

## 定位

用于扫描、检测、评估、整理和治理 opencode skills 目录。聚焦 skills 目录健康度、AGENTS.md 路由一致性、skill 职责边界和 description 触发质量，不涉及单个 skill 的具体创建方法论。

## 触发条件

- 扫描 skills 目录、检测空壳 skill（目录存在但无 SKILL.md）。
- 检查 AGENTS.md 路由 ↔ 实际 skill 文件一致性。
- 识别未注册 skill（有 SKILL.md 但 AGENTS.md 无对应路由条目）。
- 评估 skill 职责重叠、合并或拆分必要性。
- 评估 skill description 触发描述是否清晰准确。
- 判断是否需要新增 skill 还是修改/合并已有 skill。

## 不做什么

- 不替代 `skill-creator` 做单个 skill 的具体创建方法论（frontmatter 格式、资源组织）。
- 不替代 `opencode-agent-designer` 做 agents 体系治理。
- 不替代 `customize-opencode` 做 opencode 配置格式校验或 AGENTS.md 总规则修改。
- 不处理 provider、auth、model、API Key。

## 工作流

1. 读取 AGENTS.md skill 使用规则段落和 skills 目录结构。
2. 明确本轮任务：扫描/检测、路由审计、职责评估还是新增/修改决策。
3. 按任务类型执行对应检查（见下方各节）。
4. 输出结构化审计结论，只做最小必要修改建议。
5. 新增或修改 skill 时走质量门禁（见质量门禁节）。
6. 修改 skill 文件或 AGENTS.md 后必须提醒重启 opencode。

## 新增/修改 skill 必要性判断

- 已有 skill 可通过小幅 description 或内容调整满足时，不新增 skill。
- 职责与现有 skill 高度重叠、触发歧义、收益低时，默认不新增，优先合并或收窄。
- 只有职责稳定、触发明确、与已有 skill 无重叠、能降低路由歧义时才新增。

## 空壳检测

扫描 skills 目录下每个子目录：
- 有目录但无 `SKILL.md`：标记为空壳，报告目录名和建议（补建或删除）。
- `SKILL.md` 存在但 frontmatter 缺少 `name` 或 `description`：标记为不完整。
- `name` 字段与目录名不一致：标记为命名冲突。

## 路由一致性检查

对比 AGENTS.md `Skill 使用规则` 与 skills 目录实际内容：
- AGENTS.md 有路由条目但 skills 目录无对应 `SKILL.md`：标记为缺失 skill（注意系统内置 skill 如 `customize-opencode` 无本地目录属正常）。
- skills 目录有 `SKILL.md` 但 AGENTS.md 无路由条目：标记为未注册 skill，建议补充路由或评估是否需要注册。
- 路由条目的 name 与 SKILL.md frontmatter name 不一致：标记为命名不一致。

## skill 职责评估

- 列出各 skill 的核心职责关键词，交叉比对重叠度。
- 两个 skill 触发条件高度重叠（>50% 关键词重叠）：标记为候选合并，给出合并/收窄建议。
- 存在职责空缺（某类任务无 skill 覆盖）：标记为候选新增，说明空缺范围。

## description 触发质量评估

对每个 skill 的 description 检查：
- 是否包含明确触发关键词（动词 + 名词，如"扫描 skills 目录"而非"用于 skill 相关工作"）。
- 是否包含排除范围（Do not use for...），避免与相邻 skill 歧义。
- 是否过于宽泛（可能误触发）或过于狭窄（漏触发）。
- 给出具体改写建议，不自动修改。

## 质量门禁

- 新增或修改 skill 文件、AGENTS.md 路由条目，必须经过 `decision-planner` 必要性决策、`build` 实现验证闭环（最多 3 轮）、`qa` 独立验证、`code-reviewer` 审查。
- QA 和 code-reviewer 必须独立给出依据，不复用实现者结论。
- 门禁失败时基于当前文件状态继续分析，不用旧内容覆盖当前文件。
- 修改 skill 文件或 AGENTS.md 后，必须提醒用户退出并重启 opencode；当前会话不会热加载新配置。

## 输出格式

- 变更清单：文件、操作、说明。
- 读取记录：读取了哪些 skill 文件、AGENTS.md 段落和目录结构。
- 审计结论：空壳列表、路由缺失/未注册/命名冲突列表、职责重叠列表、description 质量问题列表。
- 新增/修改决策：必要性判断结果、建议操作和优先级。
- 验证记录：frontmatter 完整性、name/folder 一致性、路由覆盖、门禁通过状态。
- 当前状态：已完成内容、残余风险、阻塞项和下一步。
- 重启提醒：涉及 skill 文件或 AGENTS.md 修改时，提醒用户退出并重启 opencode。

## 二次确认

输出前重新检查：目标是否属于 skills 目录治理；是否越界到单个 skill 创建方法论、agent 治理、opencode 配置或 provider/auth/model；是否存在多余修改建议或遗漏路由条目；门禁记录是否完整。
