---
name: prototype
description: "Do not use for formal product implementation, production hardening, deployment, or complex engineering. Use when the user wants a throwaway prototype, UI mock, state-machine sandbox, quick design experiment, or says prototype this, try a few designs, sanity-check logic, or let me play with it."
---

# Prototype

用于抛弃式原型。原型的价值是回答问题，不是成为正式代码。

## Choose Mode

- **Logic prototype**：状态机、业务规则、数据转换、算法流程。优先写一个可运行脚本或终端交互。
- **UI prototype**：界面布局、交互方案、视觉对比。做多个明显不同版本，并提供简单切换方式。

## Rules

- 从一开始标记为 throwaway。
- 一个命令即可运行。
- 不接入真实生产数据，不写持久化，除非用户明确要求。
- 不做打磨、认证、部署、复杂工程化。
- 回答完问题后：删除原型，或把有效部分吸收到正式实现。
- 用户未明确全自动修改时，只给创建位置、代码片段和运行命令。

## Local Path

需要生成临时代码时，优先放到用户测试代码路径或系统临时目录。任务结束后询问是否清理本批次测试代码。

## Output

- 原型要验证的问题。
- 运行方式。
- 观察到的结论。
- 可吸收进正式代码的部分。
- 应删除的临时文件。

## 二次确认

- 确认原型没有被当作正式架构扩展。
- 确认没有引入生产依赖或持久化副作用。
- 确认结论已记录，临时代码可删除。
