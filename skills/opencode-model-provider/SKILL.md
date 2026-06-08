---
name: opencode-model-provider
description: Use when adding, deleting, renaming, or modifying custom model providers in opencode. Covers opencode.jsonc provider entries, auth.json API key management, model capability config, variants, and troubleshooting. Do NOT use for non-provider config changes.
---

# Provider 配置与管理

## 文件分工

| 文件 | 存什么 |
|------|--------|
| `~/.config/opencode/opencode.jsonc` | provider 定义（SDK、baseURL、models、options） |
| `~/.local/share/opencode/auth.json` | provider 的 API key（通用安全建议） |

当前个人配置按 AGENTS.md 允许 `provider.*.options.apiKey` 明文保存；除非用户明确要求，不主动迁移、不作为风险项、不输出具体 key。通用场景仍建议优先使用环境变量、文件引用或 auth.json 管理凭证。

## 高风险门禁

- 读取配置、定位 provider/auth/model/API key 问题、排查模型不可用等只读操作可自动进行。
- 写入、删除、重命名、迁移 provider、key、auth、model、default model 或 variants 前，必须取得用户明确授权。
- 不得输出、复述、记录完整 API key；涉及 key 时只描述位置、引用方式或是否存在。
- 当前个人配置允许 `provider.*.options.apiKey` 明文保存；除非用户明确要求，不主动迁移。

---

## 新增自定义供应商

### 1. 选 SDK（npm 包）

按当前个人配置和实际 provider 文档决定 `npm`。除非用户明确要求，不主动补 npm；只有 provider 实际不显示、模型不可用或 SDK 选择错误时，再检查 npm 包是否正确。

如果同一个 provider 下需要不同 SDK，可以**按模型覆盖 npm**：

```jsonc
"models": {
  "chat-model": {
    "name": "chat-model"
  },
  "responses-model": {
    "name": "responses-model",
    "provider": { "npm": "@ai-sdk/example" }
  }
}
```

### 2. 在 opencode.jsonc 添加 provider（完整范例）

```jsonc
"provider": {
  "my-provider": {
    "name": "my-provider",
    "npm": "@ai-sdk/example",
    "options": {
      "baseURL": "https://api.example.com/v1",
      "apiKey": "{env:MY_PROVIDER_KEY}",
      "headers": {
        "X-Custom-Header": "value"
      },
      "timeout": 300000,
      "chunkTimeout": 30000
    },
    "models": {
      "model-id": {
        "name": "model-id",
        "reasoning": true,
        "tool_call": true,
        "temperature": true,
        "modalities": {
          "input": ["text", "image"],
          "output": ["text"]
        },
        "limit": {
          "context": 400000,
          "output": 128000
        }
      }
    }
  }
}
```

### 3. 各字段说明

#### Provider 级字段

| 字段 | 必需 | 说明 |
|------|:----:|------|
| `name` | 否 | UI 显示名，与 key 一致即可 |
| `npm` | 否 | AI SDK 包，按当前个人配置和 provider 文档配置 |
| `options.baseURL` | 是 | API 端点 URL |
| `options.apiKey` | 否 | API key。支持 `{env:VAR}` 引用环境变量、`{file:path}` 引用文件 |
| `options.headers` | 否 | 自定义请求头，每个请求都带上 |
| `options.timeout` | 否 | 请求总超时(ms)，默认 300000（5分钟），设为 `false` 禁用 |
| `options.chunkTimeout` | 否 | SSE 流式块间隔超时(ms)，超时则中止 |
| `options.setCacheKey` | 否 | 强制启用 promptCacheKey（默认 false） |

#### 模型级字段

| 字段 | 含义 | 可选值 |
|------|------|--------|
| `name` | UI 中的模型显示名 | 字符串 |
| `reasoning` | 是否支持深度推理 | `true` / `false` |
| `tool_call` | 是否支持工具调用 | `true` / `false` |
| `temperature` | 是否支持温度参数 | `true` / `false` |
| `modalities.input` | 支持输入模态 | `["text","image","audio","video","pdf"]` 子集 |
| `modalities.output` | 支持输出模态 | 同上 |
| `limit.context` | 最大上下文 token 数 | 数字 |
| `limit.output` | 最大输出 token 数 | 数字 |
| `limit.input` | 最大输入 token 数 | 数字 |

### 4. 设置默认模型

```jsonc
"model": "my-provider/model-id"
```

加载优先级：
1. `--model` CLI 参数（`-m`）
2. `opencode.jsonc` 中的 `model` 字段
3. 上次使用的模型
4. 内部默认值

### 5. 添加 API key（二选一）

**方式 A — opencode TUI 命令**
```
/connect
```
选 Other → 输入 provider ID → 粘贴 key。

**方式 B — 直接写 auth.json**

文件格式：
```json
"my-provider": {
  "type": "api",
  "key": "..."
}
```

### 6. 重启 opencode

配置只在启动时加载一次，改完必须重启。

---

## 删除自定义供应商

1. 从 `opencode.jsonc` 的 `"provider"` 对象里删除对应 key
2. 从 `~/.local/share/opencode/auth.json` 删除对应 key
3. 如果旧名在 `disabled_providers` 中，也需删除
4. 重启 opencode

---

## 重命名供应商

三步：
1. `opencode.jsonc` 中 provider key 改为新名称
2. `auth.json` 中对应 key 改为新名称
3. `disabled_providers` 中删除旧名（如有）

---

## 禁用而不删除

```jsonc
"disabled_providers": ["provider-name"]
```

provider 定义和 key 都保留，但 `/models` 中不显示。移除数组元素后恢复。

**注意**：`disabled_providers` 优先级高于 `enabled_providers`。若 provider 同时出现在两个列表中，以 disabled 为准。

---

## 使用 enabled_providers 白名单

只允许少数 provider 时用白名单比逐个禁用更干净：

```jsonc
"enabled_providers": ["provider-a", "provider-b"]
```

---

## Variants（模型变体）

同一个模型可以配置多个参数预设，在 `/models` 中按 `model:variant` 选择。

**内置变体**（部分 provider）：
- Anthropic：`high`（默认高 thinking）、`max`（最高 thinking）
- Google：`low` / `high`

**自定义变体**：

```jsonc
"models": {
  "gpt-5.5": {
    "variants": {
      "fast": {
        "reasoningEffort": "low",
        "textVerbosity": "low"
      },
      "deep": {
        "reasoningEffort": "high",
        "textVerbosity": "low",
        "reasoningSummary": "auto"
      }
    }
  }
}
```

选择方式：`/models` → `gpt-5.5:fast` 或 `gpt-5.5:deep`。

---

## 全局模型 options 覆盖

可对特定 provider 下的特定模型设置全局推理参数：

```jsonc
"provider-name": {
  "models": {
    "model-id": {
      "options": {
        "reasoningEffort": "high",
        "textVerbosity": "low",
        "reasoningSummary": "auto",
        "include": ["reasoning.encrypted_content"]
      }
    }
  }
}
```

---

## 变量替换

`opencode.jsonc` 支持两种变量语法：

```jsonc
// 环境变量
"apiKey": "{env:MY_API_KEY}"

// 文件内容（适合敏感信息）
"apiKey": "{file:~/.secrets/provider-key}"
```

文件路径可以是相对路径（相对 config 目录）或绝对路径。

---

## 快速检查

```bash
# 在 opencode 内验证
/models               # 看完整 provider/model 列表

# 检查凭证
# 凭证文件路径（Windows）：
# C:\Users\<用户名>\.local\share\opencode\auth.json
```

---

## 常见问题

- **Model not allowed for this plan**
  不是配置问题，是 API key 套餐不支持该模型。换模型或升级套餐。

- **Provider 不出现**
  当前个人配置不主动补 npm；只有 provider 实际不显示、模型不可用或 SDK 选择错误时，再检查 npm 包是否正确、baseURL 是否正确、auth.json 中 key 存在且 id 匹配。

- **重命名后不可用**
  检查 `disabled_providers` 是否还引用了旧名。

- **401 Unauthorized**
  检查 auth.json 中 key 是否正确、是否过期。

- **工具调用（tool_call）失败**
  检查模型是否天然支持 tool calling；如果是本地/Ollama 模型，尝试增大 `num_ctx`（16k-32k）。
