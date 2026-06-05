---
name: diagnose
description: "Use when root cause is unknown for hard bugs, failing tests, broken behavior, exceptions, flaky failures, or performance regressions. Reproduce, rank hypotheses, gather evidence, and act within the current agent permission boundary; read-only roles only reproduce and collect root-cause evidence, not fixes."
---

# Diagnose

用于困难 bug、失败测试、异常、性能回退和不稳定行为。核心是先建立快速、确定的反馈信号，再修复。

## Workflow

1. **反馈环**：先找最小可重复验证方式：单测、脚本、最小输入、日志断言、接口请求或浏览器复现。
2. **复现**：记录实际结果、期望结果、触发条件和最小复现步骤。不能复现时先缩小输入和环境差异。
3. **假设**：列 3-5 个可证伪假设，按可能性和验证成本排序。
4. **插桩**：一次只验证一个变量。日志要带唯一前缀，避免污染正式输出。
5. **修复**：先让反馈环从失败变通过，再考虑重构。不要边修边扩大范围。
6. **回归测试**：在正确边界补测试或复现脚本，确认同类问题不再发生。
7. **清理**：只删除本次任务创建的临时日志、debug 文件和试验代码；对已有排障资料只报告建议，不擅自删除。

## Rules

- 先证据，后结论；不要凭感觉改代码。
- 版本差异由用户提供或通过文件内容对比分析，不依赖外部版本管理操作。
- 强自动模式可自主推进；强手动模式只给定位、修改片段和原因。
- 修复越小越好，避免借调试机会重构无关代码。
- 多组件问题先在组件边界加诊断信号，确认数据在哪一层断掉，再修复。
- 连续 3 次修复失败就停止试错，重新质疑架构、假设或问题分解，不做第 4 次盲修。

## Output

- 复现方式。
- 根因结论和证据。
- 修改点。
- 验证命令与结果。
- 残余风险。

## 二次确认

- 反查根因是否由证据支持。
- 反查修复是否只覆盖目标问题。
- 重新运行或说明无法运行的验证项。
