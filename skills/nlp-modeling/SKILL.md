---
name: nlp-modeling
description: Use when working on NLP model training, objectives, evaluation, BERT pretraining, text matching, sentence pair classification, Cross-Encoder architectures, hard-negative mining, or fine-tuning workflows. Use data-processing for raw table/JSONL cleaning, conversion, and splitting unless directly tied to training design.
---

# NLP Modeling

Use this skill for BERT-style pretraining and sentence-pair modeling work. Keep changes task-specific: data pipeline, objective, model head, training loop, evaluation, or inference.

## Choose The Track

- **BERT pretraining**: MLM, NSP/SOP, whole word masking, custom pretraining objectives, corpus packing, checkpoint schedules.
- **Text matching**: dataset preparation, label design, hard negative mining, augmentation, thresholding, metrics.
- **Cross-Encoder**: text pair classification/scoring where both inputs are concatenated and cross-attend in one encoder.

## BERT Pretraining Defaults

- MLM: mask 15% tokens; 80% `[MASK]`, 10% random, 10% unchanged; predict original tokens.
- NSP is optional; prefer SOP when sentence-order discrimination matters.
- Pipeline: raw text -> sentence split -> tokenize -> packed instances with `[SEP]`.
- Sequence length: phase 1 at 128 tokens, phase 2 at 512 tokens when reproducing BERT-style schedules.
- Duplicate factor: 5-10 for different masks per instance.
- Optimizer: AdamW, lr around `1e-4`, weight decay `0.01`, warmup then linear decay.
- Exclude bias and LayerNorm from weight decay.
- Use mixed precision when available; save model and optimizer state for resumption.

## Text Matching Workflow

- Data format: `text_a<TAB>text_b<TAB>label` unless the project already defines another schema.
- Label types: binary match/no-match, multi-class match categories, or regression similarity score.
- Check label balance first; use weighted loss, sampling, or threshold calibration for imbalance.
- Mine hard negatives from lexically or embedding-similar non-matches, preferably from the same domain.
- Add hard negatives progressively; start with random/easy negatives if training is unstable.
- Augment positives cautiously with paraphrases; avoid augmentations that change semantic equivalence.
- Evaluate with Accuracy, Precision, Recall, F1, AUC-PR/AUC-ROC, confusion matrix, and threshold sweep.

## Cross-Encoder Pattern

Use a Cross-Encoder when pairwise accuracy matters more than embedding retrieval speed.

```python
class CrossEncoder(nn.Module):
    def __init__(self, encoder, hidden_size, num_labels):
        super().__init__()
        self.encoder = encoder
        self.classifier = nn.Linear(hidden_size, num_labels)

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )
        pooled = outputs[1]
        return self.classifier(pooled)
```

- Input: concatenate `text_a [SEP] text_b`; use `token_type_ids` when supported.
- Loss: `BCEWithLogitsLoss` for binary, `CrossEntropyLoss` for multi-class, `MSELoss` for regression.
- Fine-tuning lr: usually `1e-5` to `3e-5`; batch size commonly 16-32 per GPU.
- Max sequence length: 256-512 depending on truncation risk and memory.
- Inference is O(number of pairs); use a bi-encoder first if large-scale retrieval is required.

## 二次确认（输出前必须执行）

- 反查代码完整性：训练/评估/推理流程是否一致，输入输出维度是否匹配，优化器参数和 loss 函数是否正确。
- 重新审视配置：超参数是否在安全区间，数据集路径、标签定义和切分逻辑是否有误。
- 确认可复现：随机种子是否固定，checkpoint 保存和加载路径是否明确。

## Common Pitfalls

- Surface-form leakage: shared tokens do not imply a match.
- Weak labels: noisy positives/negatives can dominate small datasets.
- Bad negatives: random negatives make metrics look good but fail in production.
- Truncation bias: one side may be silently cut off; inspect pair length distributions.
- Threshold drift: calibrate on validation data from the target deployment distribution.
