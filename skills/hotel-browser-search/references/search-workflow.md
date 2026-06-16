# 酒店搜索工作流

## 搜索引擎选择策略

### 可用性分级

基于实际测试，搜索引擎可用性排序：

| 优先级 | 引擎 | 稳定性 | 备注 |
|--------|------|--------|------|
| P0 | cn.bing.com (国际版 ensearch=1) | 中 | 结果可能被中文内容污染，需验证 |
| P1 | cn.bing.com (国内版 ensearch=0) | 中 | 同上 |
| P2 | www.bing.com (cc=us, mkt=en-US) | 低 | 仍可能路由到中文内容 |
| P3 | DuckDuckGo /html/ | 低 | 经常传输错误 |
| P3 | Google / Google HK | 极低 | 几乎总是传输错误 |
| P4 | Brave / Startpage / Yahoo / Qwant / Ecosia | 极低 | 几乎不可用 |
| P5 | WolframAlpha | — | 仅数学/知识类查询，对酒店无效 |

### 搜索引擎使用规则

1. Bing 返回结果必须人工校验是否与 query 相关（常见漂移：搜索酒店返回飞书/抖音/1688）
2. 不要对 Google 系引擎抱期望，直接跳过或做为最后尝试
3. Bing query 中避免使用中文引号、特殊符号，可能导致结果漂移
4. 未获取互联网实时最新数据时，禁止做酒店/房型/重复判断

## OTA 平台直搜策略（主路径）

搜索引擎不可靠时，**直接构造目标 OTA 平台的搜索/详情页 URL**：

### 国际 OTA

| 平台 | URL 模式 | 封锁风险 |
|------|----------|----------|
| Trip.com | `/hotels/{city}-hotel-detail-{id}/{slug}/` | 低 |
| TripAdvisor | `/Hotel_Review-g{geo}-d{id}-Reviews-{slug}.html` | 高 (403) |
| Booking.com | `/hotel/{country}/{slug}.html` | 中 |
| Agoda | `/{slug}/hotel/{city}-{country}.html` | 中 |
| Expedia | `/Hotel-Search?destination={name}` | 高 (429) |
| Airbnb | `/s/{location}/homes?query={name}` | 低 |

### 印尼本地 OTA

| 平台 | URL 模式 | 备注 |
|------|----------|------|
| tiket.com | `/hotel/search?q={name}` | 评价数据丰富 |
| Traveloka | `/hotel/indonesia/{slug}-{id}` | 封锁率高 (403)，可从摘要提取 |
| Travelio | `/en/search?q={name}` | 公寓为主 |
| Pegipegi | `/hotel/search/?q={name}` | 不稳定 |
| OYO | `/search?location={city}&query={name}` | 封锁率高 |
| RedDoorz | `/en-id/hotel/search?q={name}` | 封锁率高 (404) |

### URL 构造技巧

1. Trip.com slug 格式：`{name}` 转 `-` 分隔全小写
2. TripAdvisor geo ID 需从搜索获取，不能直接猜测
3. 不同国家/语言版本的 TripAdvisor 可能返回不同结果，可尝试 `.co.uk`、`.sg`、`.com.my` 等

## 搜索策略决策树

```
用户需求
├─ 已知具体酒店名
│   ├─ 直接构造 OTA 详情页 URL → 命中 → 采集
│   └─ 未命中 → cn.bing.com 搜索 → 获取 OTA 链接 → 采集
├─ 模糊酒店名/关键词
│   ├─ cn.bing.com 搜索 → 提取 OTA 链接列表 → 逐个采集
│   └─ 同时尝试 tiket.com 站内搜索
└─ 需要发现同楼竞品/关联酒店
    └─ cn.bing.com 搜索 "{楼宇名} {城市}" 收集所有结果
```

## 信息采集清单

对每个酒店/房源，必须采集以下字段（尽可能完整）：

| 字段 | 优先级 | 常见来源 |
|------|--------|----------|
| 电话号码 | 🔴 必采 | Trip.com、tiket.com、OTA 列表页 |
| 地址 | 🔴 必采 | OTA 详情页、Bing 搜索结果摘要 |
| 坐标（经纬度） | 🔴 必采 | OTA 详情页、Bing Maps |
| 管理公司/品牌 | 🟡 重要 | 酒店名称中提取、Instagram |
| 评分 + 评价数 | 🟡 重要 | 各 OTA 分别采集，区分平台 |
| 房型 + 价格 | 🟢 辅助 | OTA 详情页 |
| 设施列表 | 🟢 辅助 | OTA 详情页 |
| 父酒店 ID | 🟢 辅助 | 数据库字段 |

## 信息可信度标注规范

每条采集到的信息必须标注：

```
值: "{地址}"
URL/页面: {平台搜索页或详情页URL}
可信度: L1
获取时间: {YYYY-MM-DD HH:mm}
```

冲突时采用多方交叉验证：至少 2 个独立来源一致才视为强线索；电话、地址、坐标仍不能单独作为重复酒店结论。
