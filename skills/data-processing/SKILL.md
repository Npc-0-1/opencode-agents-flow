---
name: data-processing
description: Use when cleaning, converting, splitting, sampling, or checking raw CSV, Excel, JSONL, TXT, pandas datasets, labels, class balance, encoding issues, or NLP/text-matching data files. Use nlp-modeling for training objectives, hard-negative strategy, evaluation, and modeling.
---

# Data Processing

用于数据清洗、格式转换、数据集检查和 NLP/Text Matching 数据准备。

## Workflow

1. 先确认输入文件、输出目标、字段含义和标签规则。
2. 读取少量样本和字段统计，优先检查编码、空值、重复、异常长度。
3. 修改前记录总行数、唯一键数量、标签分布和缺失值数量。
4. 处理后再次统计，保证行数变化、标签变化和过滤规则可解释。
5. 不静默覆盖原始数据，默认输出新文件或要求用户确认覆盖。

## Defaults

- 编码优先尝试 `utf-8`、`utf-8-sig`，中文历史数据再尝试 `gbk`。
- CSV/Excel 处理优先使用 `pandas`，大文件再考虑分块读取。
- 数据切分默认固定随机种子，保持可复现。
- 文本匹配数据默认检查 `text_a`、`text_b`、`label` 三类核心字段。
- 二分类标签必须检查正负样本比例，极端不均衡时先报告再处理。

## 二次确认（输出前必须执行）

- 反查处理前后统计是否一致：行数变化是否可解释，去重/过滤/切分逻辑是否正确。
- 重新审视输出文件：读取少量样本确认格式、编码、字段和标签是否符合预期。
- 确认无静默破坏：原始文件未被覆盖，异常样本和丢弃原因已记录。

## Output Report

- 输入文件和输出文件。
- 处理规则和过滤条件。
- 处理前后行数、空值、重复、标签分布。
- 发现的异常样本和潜在风险。
- 后续训练或评估建议。
