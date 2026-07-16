---
name: 建站工作流
version: "10.3"
description: 电子制造B2B出口建站。一句话→完整内容蓝图→全站图片策略→10秒买家测试驱动设计迭代。纯静态HTML完整多页网站。v10.3 移除固定板块模板，Agent自主决策首页结构。
upstream: https://github.com/cpu152650311-coder/website-workflow
---

# 建站工作流 v10.3

> **v10.3**：**移除固定板块模板**——首页不再强制 10 板块结构，Agent 根据买方角色扫描路径自主决定板块数量、类型、顺序。**废除 hero 硬编码 prompt 模板**（禁止 "dark navy"、"electric blue" 等固定颜色），Hero 构图策略改为品牌人格驱动选择矩阵（微距/广角/抽象/工作室 4 方向）。唯一硬性约束：板块类型重叠率 < 50%（连续站点间）。
> **v10.2**：Hero 居中布局默认 + `::before` 遮罩模式、首页图片密度标准（10-12 张 / 9-10 板块）、Hero 生图 prompt 升级为高端产品微距摄影策略、能力卡片/应用方案网格/全幅数据条/垂直流程列表等新组件模式。
> **v10.1**：ENV 凭据自动管理、部署后 CDN 缓存破坏、弹窗双栏组件模板、批量替换安全规则。
> **v10.0**：新增 Phase 0 一句话内容展开、全站图片角色策略（28+张/站）、方形图片展示规则、10秒买家测试驱动设计迭代循环。Phase 4 从单向检查升级为循环验证。
> **v9.0**：品类细分+品牌人格三轴+差异化防收敛
> **v8.4-8.5**：Hero 沉浸式布局、CTA 按钮可见性陷阱、生图双格式支持、B2B UX 规则、部署后验证。

Agent 在 Phase 1 **自主进行设计决策**，无需加载外部技能。

## 核心理念

```
用户: "做个PCB外贸站，叫华兴电路"
  │
  ▼
Phase 0  一句话 → 完整 B2B 内容蓝图
  │ 模型知识库自动填充：产品参数/认证/交期/MOQ/产能/工艺
  │ 全部按深圳电子制造最高标准展开
  ▼
Phase 1  设计决策 + 全站图片策略
  │ 每页每 section 预先分配图片角色
  │ 品类细分 → 品牌人格三轴 → 差异化防收敛
  ▼
Phase 2  全站生图（28-35 张，<$0.21）
  │ 不同角色用不同 prompt 策略
  ▼
Phase 3  逐页编码
  ▼
Phase 4  10秒买家测试 ←──┐
  │ 不通过 → 缺什么视觉模块？   │ 设计迭代循环
  │ → Phase 2 补图 → Phase 3 补模块 ──┘
  ▼
Phase 5  子 Agent 独立验收（含买家视角）
  ▼
Phase 6  Wrangler → Cloudflare Pages 部署
  ▼
  🚀 上线
```

## 流程（7 Phase）

```
Phase 0  主 Agent → 一句话展开为内容蓝图
         └─ content-blueprint.md（产品参数/认证/交期/产能/工艺/信任信号）

Phase 1  主 Agent → 设计 + 骨架 + 图片策略
         ├─ design-blueprint.md（品类+人格+差异化）
         ├─ design-tokens.css
         ├─ index.html
         ├─ blocks/*.html
         ├─ image-strategy.json（全站图片角色分配 + prompt）
         ├─ image-brief.html
         ├─ acceptance-criteria.json
         └─ reveal.js

Phase 2  GPT Image 2 → /generated/*.webp（全站图片，28-35 张）
         └─ python gen-site-images.py --prompts image-strategy.json --out ./generated

Phase 3  主 Agent → 逐页编码（每页嵌入对应图片）

Phase 4  主 Agent → 10 秒买家测试 + 设计迭代
         ├─ 每页模拟海外采购经理 10 秒扫描
         ├─ PASS → 继续 Phase 5
         └─ FAIL → 补图(Phase 2) → 补模块(Phase 3) → 重测

Phase 5  子 Agent → 独立验收（技术+买家双视角）

Phase 6  Wrangler → Cloudflare Pages 部署
```

---

## 环境准备（首次建站）

Agent 在开始建站前自动处理凭据和环境，不依赖用户手动配置。

### 自动创建 .env

从用户系统环境或已有凭据文件中读取，写入项目 `.env`：

```bash
CLOUDFLARE_API_TOKEN=<从 ~/.claude/.env 或用户环境读取>
CLOUDFLARE_ACCOUNT_ID=<从 ~/.claude/.env 或用户环境读取>
AIHUBMIX_API_KEY=<从 ~/.claude/.env 或用户环境读取>
```

**规则**：
- 优先从 `~/.claude/.env` 读取（用户全局凭据存储）
- 其次从当前 shell 环境变量读取
- 如果都找不到，提示用户提供并写入 `.env`
- `.env` 写入后立即创建 `.gitignore`

### 自动创建 .gitignore

```gitignore
.env
.wrangler/
node_modules/
```

**原则**：凭据文件不入库、Wrangler 缓存不入库。Agent 每次部署前自动 `source .env` 或 `export $(grep -v '^#' .env | xargs)` 加载凭据，无需用户手动操作。

---

## Phase 0 — 一句话展开为内容蓝图

用户只需给：**品类 + 品牌名**。Agent 按深圳电子制造出口最高标准自动填充所有内容。

### 自动展开规则

Agent 根据品类从模型知识库自动填充以下字段，**不询问用户、不等待厂商资料**：

| 字段 | 填充策略 | 示例（PCB） |
|------|---------|-----------|
| 产品参数 | 该品类全球最高工艺标准 | 2-32层、HDI任意层、3/3mil线宽线距、阻抗±5% |
| 认证体系 | 该品类必备+加分认证 | ISO 9001, ISO 14001, IATF 16949, UL, RoHS, REACH |
| 产能数据 | 深圳中型工厂标准 | 月产80,000㎡、8条SMT线、24h加急打样 |
| 交期 | 行业标准最优档 | 常规5-7天、打样3天、加急24h |
| MOQ/样品 | 最有竞争力的条款 | MOQ 1pcs起、免费打样、样品3天 |
| 工艺能力 | 该品类完整工艺链 | 沉金/OSP/沉银/沉锡、FR-4/Rogers/铝基/陶瓷基 |
| 品质控制 | 标准QC体系 | IQC→IPQC→OQC、AOI自动检测、飞针测试、阻抗测试 |
| 应用领域 | 该品类典型下游 | 汽车电子、医疗设备、工业控制、消费电子、通信 |

**输出文件**：`content-blueprint.md`，包含完整的业务内容字段，Phase 1 设计时直接引用。

### 为什么可以这样做

- 深圳电子制造在每个品类都是全球供应链顶端，模型知识库对该品类的最高标准有完整知识
- 厂商认证不会差（深圳出口导向的筛选门槛）
- 真实客户信息后期替换即可，AI 先填充最优标准
- 厂商确认时只需微调数字，不需要从零写

---

## Phase 1 — 设计 + 图片策略

### 步骤

#### 1. 品类细分 → 视觉线索

从 brief 提取具体产品品类，映射视觉线索（非固定配色，是意象方向）：

| 品类 | 视觉意象 | 典型色彩方向 |
|------|---------|:--:|
| PCB/PCBA/SMT | 电路、精密、层叠 | 深绿/金/铜 |
| LED/照明 | 光效、色温、光束 | 暗底+暖光 |
| 电池/储能/电源 | 能量、安全、耐用 | 蓝/绿/银 |
| IoT/无线/模块 | 连接、网络、微型 | 白/蓝/灰 |
| 医疗电子 | 洁净、精密、信任 | 白/蓝/淡灰 |
| IC/半导体/芯片 | 微观、极致精密 | 黑/金/银 |
| 显示屏/LCD/OLED | 色彩、清晰、薄 | 黑/白+鲜艳点缀 |
| 充电桩/新能源 | 未来、速度、户外 | 深蓝/绿/橙 |
| 工业控制/机箱 | 坚固、散热、规模 | 炭灰/橙/蓝 |
| 线缆/连接器 | 秩序、传输、精密 | 灰/蓝/铜 |
| 传感器/器件 | 感应、微型、智能 | 白/蓝/绿 |

Agent 根据 brief 选择最接近的品类，提取视觉意象。跨品类（如"PCBA+医疗"）则融合两个方向的意象。

#### 2. 品牌人格 → 设计基调

在以下三轴上定位品牌人格，每个轴选一端：

```
技术先锋型 ←————————————————→ 可靠传统型
（大胆配色/不对称/动效）       （稳重视觉/对称/克制）

高端精密型 ←————————————————→ 规模产能型
（留白多/字少图大/金属色）     （信息密度高/表格/产品阵列）

国际通路型 ←————————————————→ 工厂直营型
（英文优先/简洁/信任信号）     （中英双语/车间实景/认证墙）
```

三轴组合（如「技术+高端+国际」vs「传统+规模+工厂」）产出完全不同的设计基调。Agent 必须在 design-blueprint.md 中明确写出三轴定位。

#### 3. 设计差异化 → 防收敛

同一品类、同一人格容易产出相似设计。Agent 必须主动做以下差异化决策（至少 3 项）：

- [ ] 主色：从品类色彩方向中选**一个非默认**的（如 PCB 不选深绿而选铜金为主、绿为辅）
- [ ] 布局系统：首页首个 section 的类型与上一个站点不同（全屏图 / 图文分屏 / 卡片网格 / 大标题居中）
- [ ] 字体个性：标题字体在 serif/sans/mono 之间切换感受
- [ ] 密度节奏：内容密度在「稀疏留白」与「信息密集」之间制造差异
- [ ] CTA 策略：弹窗/页尾表单/浮动按钮/内联 CTA，切换主要询盘入口形式
- [ ] Hero 构图：产品特写/车间广角/抽象科技纹理/地理网络，使用不同视觉母题

**差异化检查**：如果连续两个站点的差异化项重叠 ≥2 项，第三个站点必须强制使用不同的选项。

#### 4. 全站图片策略规划

**核心原则：GPT Image 2 生成 1024×1024 图片极便宜（$0.006/张），应在全站广泛使用。不要把生图限定在产品照片上。**

Agent 遍历每个页面的每个 section，分配图片角色。输出 `image-strategy.json`：

```json
{
  "images": [
    {
      "id": "hero-bg",
      "role": "hero-bg",
      "page": "/index.html",
      "prompt": "PCB manufacturing facility with automated production lines...",
      "display": "full-bleed",
      "reference": ""
    },
    {
      "id": "product-angle-45",
      "role": "product-showcase",
      "page": "/products/index.html",
      "prompt": "Same PCB product, 45-degree angle view, clean studio lighting...",
      "display": "inline-large",
      "reference": "https://example.com/product-front.webp"
    },
    {
      "id": "pcb-stackup-diagram",
      "role": "technical-diagram",
      "page": "/products/index.html", 
      "prompt": "Cross-section diagram showing PCB layer stackup...",
      "display": "inline-large"
    }
  ],
  "meta": {
    "referenceBaseUrl": "https://original-site.com"
  }
}
```

> **`reference` 字段说明**：当 `reference` 存在时，Phase 2 使用图生图（edits 端点），参考图引导生成匹配产品外观/品牌风格。`reference` 为空或不存在时，使用纯文本生图。
> **`meta.referenceBaseUrl`**：相对路径的基准 URL。例如 `reference: "/images/product.webp"` + `referenceBaseUrl: "https://example.com"` → 实际下载 `https://example.com/images/product.webp`。

```

##### 图片角色类型

| 角色 | 用途 | 每站用量 | Prompt 策略 |
|------|------|:--:|------|
| **hero-bg** | 首页 Hero 全幅背景 | 1 | 品类氛围 + 空间留白给文字 |
| **sub-hero-bg** | 子页面 Hero 背景 | 4-5 | 该页面主题场景，每页不同 |
| **product-showcase** | 产品线/能力展示 | 3-5 | 多对象排列展示产品线 |
| **technical-diagram** | 技术原理/结构图 | 3-5 | 截面/层叠/原理示意 |
| **process-flow** | 生产/工艺流程 | 1-2 | 步骤可视化，从原料到出货 |
| **concept-scene** | 应用场景/行业方案 | 3-4 | 产品在终端设备中的效果 |
| **texture-bg** | 卡片/区域背景纹理 | 3-5 | 低对比度抽象纹理 |
| **comparison-chart** | 材料/工艺对比 | 1-2 | 左右对比或表格可视化 |
| **stats-bg** | 数据展示区背景 | 1-2 | 与品类相关的抽象意象 |
| **cta-bg** | CTA 卡片背景图 | 2-3 | 品牌氛围，不抢按钮注意力 |
| **blog-cover** | 博客文章封面 | 按需 | 由 blog-workflow 生成 |

**总量：每站 25-35 张，成本 $0.15-0.21。**

##### 图片展示规则（1024×1024 方形格式）

GPT Image 2 固定输出 1024×1024。方形图在网页中有特定的适用场景：

| 展示方式 | 适用角色 | CSS 要点 |
|---------|---------|---------|
| **全幅 Hero** | hero-bg, sub-hero-bg | `object-fit:cover; object-position:center 30%`；**默认居中文字**（`align-items:center;text-align:center`），通过 `::before{background:rgba(0,0,0,0.45)}` 叠加暗色遮罩保证白色文字可读性 |
| **图文分屏等高** | product-showcase, concept-scene | `align-items:stretch` + img `position:absolute;inset:0;object-fit:cover` |
| **大尺寸内联图** | technical-diagram, process-flow | 占内容区 60-80% 宽度，居中，圆角 |
| **卡片缩略** | blog-cover, product-showcase | `aspect-ratio:1/1` 或 `aspect-ratio:4/3`（裁切上下） |
| **背景纹理** | texture-bg, stats-bg, cta-bg | `::before{opacity:.25-.35}` 低透明度叠加 |
| **对比展示** | comparison-chart | 两张并排或上下排列 |

**禁止**：方形图缩放到小于 200px 宽度（失去细节）、用作 icon/徽章、用在 nav/header 微型位置。

#### 5. 完整页面规划（必须包含）

- 首页 (index.html)
- 关于页 (/about/index.html)
- 产品/能力页（按品类选 `/products/` 或 `/capabilities/`）
- 联系页 (/contact/index.html)
- 博客预留 (/blog/index.html)
- 根据品类添加行业相关页面

##### B2B 内容架构（每页必须承载的业务信息）

以下为每页**必须覆盖的信息维度**，Agent 根据买方角色和品类自主决定以何种板块形式呈现。**不设固定板块模板。**

| 页面 | 必须覆盖的信息维度 | 板块决策权 |
|------|-------------------|:--:|
| 首页 | ① 我是谁（品类+定位，1秒识别） ② 我提供什么能力/产品（至少 2 个维度展示） ③ 凭什么信我（认证/产能/品质至少 2 个信任信号） ④ 我服务过哪些场景（应用案例） ⑤ 怎么联系（CTA） | Agent 自主决定板块数量、类型、顺序 |
| 关于页 | 工厂规模 + 产线设备 + QC流程 + 认证列表 + 出货能力 + 合作模式 | Agent 自主组织 |
| 产品/能力页 | 技术参数表 + 工艺能力清单 + 材料选项 + 品质标准 + 交期/MOQ + 应用领域 | Agent 自主组织 |
| 联系页 | 询盘表单 + 地址/联系方式 + 办公/工厂图 + FAQ | Agent 自主组织 |

**Agent 决策原则**：
- 首页板块数量**不设下限和上限**。信息维度覆盖全即可，板块可合并（如认证+数据合并为一个信任信号区）或拆分（如产品线分两个独立的图文分屏）
- 板块类型根据**买方角色扫描路径**选择：技术采购偏好数据表格/参数对比，品牌采购偏好大图/场景展示，工厂直采偏好认证墙/产能实拍
- 关于页、产品页、联系页的信息维度必须覆盖，但排版方式由 Agent 根据品类和品牌人格自主决定

**内容标准**：全部按深圳电子制造出口最高标准填充。产品参数用技术指标，不写空洞形容词。一个海外采购经理读完任何一页，10秒内能判断「这个工厂能做我的单」。

#### 6. 执行产出

写 `design-tokens.css` → 写 `index.html` → 提取 `blocks/*.html` → 生成 `image-strategy.json` → 生成 `image-brief.html` → 生成 `acceptance-criteria.json`

**design-blueprint.md 字段**：
- CATEGORY — 品类细分 + 视觉意象
- BRAND PERSONALITY — 三轴定位（技术/高端/国际 各轴明确选边）
- DESIGN DIFFERENTIATORS — 差异化决策记录（≥3 项）
- COLOR PALETTE — 完整色彩系统（含差异化理由）
- TYPOGRAPHY — 字体系统
- PAGE COLLECTION — 所有页面列表（必须 ≥5 个页面）
- IMAGE STRATEGY — 图片角色总数 + 每页分布
- BLOCK MANIFEST — 可复用区块
- IMAGE DIRECTION — 图片风格指导

**关键原则**：
- 创建**完整多页网站**，不是单页landing page
- 每个页面都有独立内容和完整结构
- 导航链接指向真实页面，不是锚点
- blocks 是参考模板，执行时可调整 DOM 和布局
- 所有文件在主 Agent 的连续上下文中产出，保持设计一致性

### 博客框架预留

Phase 3 完成后，`/blog/index.html` 只是一个空框架。**Agent 必须在建站工作流完成后提示用户执行博客工作流**，或者在 Phase 5 验收中加入博客配图检查。

```html
<!-- /blog/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>博客 | {brand}</title>
  <link rel="stylesheet" href="../design-tokens.css">
</head>
<body>
  <main>
    <h1>博客</h1>
    <p>博客内容即将上线。</p>
    <!-- blog-workflow 将在此生成文章列表 -->
  </main>
</body>
</html>
```

### 联系表单简化

**字段**：name, email, message（无 product、phone、company）

```html
<form action="/inquiry" method="POST" class="contact-form">
  <label>姓名 <input type="text" name="name" required></label>
  <label>邮箱 <input type="email" name="email" required></label>
  <label>留言 <textarea name="message" required></textarea></label>
  <button type="submit">发送</button>
</form>
```

**action**：`/inquiry`（如果有 inquiry-workflow 部署），否则 `action="https://formsubmit.co/{email}"` 兜底。

---

## Phase 2 — 全站生图

模型：**GPT Image 2**，三档质量可选：

| 质量 | 单价（1024×1024） | 适用 |
|------|:-----------------:|------|
| `low` | **$0.006** | 全站所有图片（效果足够好） |
| `medium` | $0.053 | 不稳定，避免使用 |
| `high` | $0.211 | 仅交付级精修 |

**默认全部用 `low`**。成本极低，不要省。

**API 端点**：`api.inferera.com`（已验证稳定可用）。`aihubmix.com` 已确认超时不可用，不再尝试。

**文本生图端点**：`https://api.inferera.com/v1/images/generations`
**图生图端点**：`https://api.inferera.com/v1/images/edits`（当 `image-strategy.json` 中指定了 `reference` 字段时自动使用，见下方"图生图模式"）

**图片尺寸限制**：所有图片 `1024×1024`。

### 按角色分 Prompt 策略

不同图片角色用不同的 prompt 写法：

| 角色 | Prompt 重点 | 构建原则 |
|------|-----------|---------|
| hero-bg | **由 design-blueprint.md 的品牌人格三轴决定构图策略**。Agent 从以下方向中自主选择（不限于一种）：<br>• 高端精密型 → 产品微距特写，浅景深，电影级布光<br>• 规模产能型 → 广角车间/产线实景，纵深构图<br>• 技术先锋型 → 抽象科技视觉，几何纹理，大胆配色<br>• 可靠传统型 → 稳重产品摆拍，工作室布光，干净背景<br>**禁止在 prompt 中硬编码固定颜色**（如 "dark navy"、"electric blue"）。颜色描述必须从 design-blueprint.md 的 COLOR PALETTE 中提取。上半部或文字区域留空（配合 Hero 文字位置） | Agent 根据品牌人格选择构图策略 → 从 COLOR PALETTE 提取颜色描述 → 组装 prompt。不使用固定模板。 |
| sub-hero-bg | 页面主题场景 | `[主题] in [品类] context, professional B2B photography style` |
| product-showcase | 产品线多对象排列 | `range of [产品类型] displayed showing product line diversity, [品类视觉意象]` |
| technical-diagram | 结构/原理示意 | `technical cross-section diagram of [具体技术], clean vector style, labeled layers, [品类视觉意象]` |
| process-flow | 流程步骤 | `manufacturing process flow from raw material to finished [产品], sequential steps visualized` |
| concept-scene | 应用场景 | `[产品] installed in [应用终端], professional setting, showing integration` |
| texture-bg | 抽象纹理 | `abstract [品类视觉意象] texture, subtle, low contrast, suitable as background overlay` |
| comparison-chart | 对比可视化 | `side by side comparison of [材料A] vs [材料B], visual differences highlighted` |
| stats-bg | 数据氛围 | `[品类] industry abstract background with subtle geometric patterns, dark/light per site theme` |
| cta-bg | 品牌氛围 | `[品牌名] brand atmosphere, [品类视觉意象], space for text and button overlay` |

**Prompt 通用规则**：
- 所有 prompt 包含 `no people faces, no text, no logos`
- 匹配 design-blueprint.md 中的色彩方向
- 构图配合该 section 的文字位置（见 Phase 1 步骤 4 的展示规则）

### 生图脚本

`gen-site-images.py` 已内置文本生图和图生图自动切换。脚本源码通过 `skill_view(name='建站工作流', file_path='scripts/gen-site-images.py')` 获取，写入项目根目录再执行。

```bash
# 全量生成（自动检测 reference 字段，切换 text-to-image / image-to-image）
python gen-site-images.py --prompts image-strategy.json --out ./generated

# 追加图片（Phase 4 迭代补图）
python gen-site-images.py --prompts supplement.json --out ./generated --manifest image-manifest.json

# 高质量模式（交付级精修）
python gen-site-images.py --prompts image-strategy.json --out ./generated --quality high

# 断点续传
python gen-site-images.py --prompts image-strategy.json --out ./generated --start-from 15
```

### 图生图模式（Image-to-Image）

当 `image-strategy.json` 中的图片条目包含 `reference` 字段时，脚本自动切换到图生图模式。参考图片可以是：

- **绝对 URL**：`"reference": "https://example.com/images/product.webp"`
- **相对路径 + baseUrl**：`"reference": "/images/product.webp"` + `meta.referenceBaseUrl`
- **本地路径**：`"reference": "./reference-images/product.webp"`

**图生图 API 格式**：
```json
{
  "model": "gpt-image-2",
  "prompt": "Same product, different angle...",
  "images": [{"image_url": "data:image/webp;base64,..."}],
  "size": "1024x1024"
}
```

> **踩坑经验**：`images` 参数必须是对象数组 `[{"image_url": "data:..."}]`，**不是**纯 base64 字符串，**不是** `{url: ...}` 对象，**不是** `{type: "image_url", ...}` Chat Completions 格式。

**适合用图生图的角色**：
| 角色 | 推荐度 | 原因 |
|------|:--:|------|
| product-showcase | **强烈推荐** | 参考图确保产品外观一致性 |
| concept-scene | **推荐** | 参考图帮产品融入场景 |
| hero-bg | 可选 | 有特定产品主视觉时 |
| cta-bg | 可选 | 品牌氛围参考 |

**不适合**用图生图的角色：technical-diagram、process-flow、texture-bg、comparison-chart（纯文本生成效果已足够好）。

### 产品多角度/多场景生成（`gen-product-shots.py`）

独立脚本，用于「提供产品图 → 自动生成不同角度/场景/光线」的需求：

```bash
# 快速模式：用预设模板
python gen-product-shots.py --reference ./product.webp \
    --angles front,45deg,side --scenes studio,office --out ./shots

# 查看所有预设
python gen-product-shots.py --list-presets

# 完整配置模式
python gen-product-shots.py --config product-shots.json --out ./shots
```

**预设角度**：front, 45deg, side, back, topdown, macro
**预设场景**：studio, office, hotel, retail, industrial, outdoor
**预设光线**：daylight, softbox, rim, ambient

脚本源码通过 `skill_view(name='建站工作流', file_path='scripts/gen-product-shots.py')` 获取。

---

## Phase 3 — 逐页编码

主 Agent 直接写所有页面：
1. Read image-strategy.json → 了解每页每 section 的图片分配
2. Read 所需的 blocks 和 design-tokens.css
3. Write 完整 HTML 文件，按策略嵌入对应图片

### 页面路由：目录路由（零重定向）

```
/about/index.html
/products/index.html  或 /capabilities/index.html
/contact/index.html
/blog/index.html
```

Cloudflare Pages 原生支持 `/about` → `/about/index.html`，无需 `_redirects`。

### 页面规划原则

- 每个主要 section 都有对应的独立页面
- 导航链接指向真实页面，不是锚点
- 每个页面都有完整的 HTML 结构和内容
- 页面数量 ≥ 5 个（首页 + 4 个子页面）
- 每页按 Phase 1 的 B2B 内容架构填充业务内容
- 图片按 image-strategy.json 的角色分配嵌入对应 section

### 方形图片嵌入模式

| 展示方式 | HTML/CSS |
|---------|---------|
| 全幅 Hero | `<img class="hero-img">` + `object-fit:cover` |
| 图文分屏等高 | grid `align-items:stretch` + img `position:absolute;inset:0;object-fit:cover` |
| 大尺寸内联 | `<img>` 宽度 60-80%，居中，`border-radius:var(--radius-lg)` |
| 背景纹理 | `::before{background:url(...);opacity:.3}` |
| 卡片缩略 | `aspect-ratio:4/3` + `object-fit:cover`（裁切上下） |

**CSS 布局陷阱**：用 CSS `order` 代替 `direction:rtl`：

```css
.media-split.reversed .media-text { order: 1; }
.media-split.reversed .media-img { order: 2; }
@media(max-width:768px) {
  .media-split.reversed .media-text,
  .media-split.reversed .media-img { order: 0; }
}
```

### SVG 图标精灵模式（推荐）

```html
<svg xmlns="http://www.w3.org/2000/svg" style="display:none;position:absolute;width:0;height:0">
  <symbol id="icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
    <path d="M5 13l4 4L19 7"/>
  </symbol>
</svg>
<svg width="24" height="24" style="color:var(--accent)"><use href="#icon-check"/></svg>
```

---

## Phase 4 — 10 秒买家测试 + 设计迭代循环

### 主 Agent 逐页执行 10 秒买家测试

模拟**海外采购经理**视角，每页自问：

```
1. 这页讲的是什么？（1 秒）
2. 这个工厂能做什么？（3 秒）—— 产品/工艺/产能
3. 为什么选他们？（3 秒）—— 认证/品质/交期/差异化
4. 下一步怎么联系？（1 秒）—— CTA 是否可见
5. 还有什么疑问没回答？（2 秒）—— 缺失的关键信息
```

**PASS 标准**：5 个问题全部能在页面内找到答案。答案必须**可见**（不是藏在折叠区、不是需要推理）。

**FAIL 处理**：

```
10 秒测试 FAIL
  │
  ├─ 缺内容？→ 回到 Phase 0 补内容字段 → Phase 3 补页面模块
  │
  ├─ 缺视觉？→ 确定需要的图片角色 → Phase 2 补生图 → Phase 3 嵌入
  │   常见缺失：
  │   · 技术原理没图 → technical-diagram
  │   · 工艺流程纯文字 → process-flow
  │   · 产品太抽象 → product-showcase 或 concept-scene
  │   · 数据区太干 → stats-bg 或 texture-bg
  │   · CTA 区域视觉弱 → cta-bg
  │
  └─ 设计问题？→ 调整布局/对比度/信息层级 → 重测

补图用追加模式：
python gen-site-images.py --prompts supplement.json --out ./generated --manifest image-manifest.json
```

**迭代上限**：最多 2 轮。2 轮后仍有 FAIL → 记录到 acceptance-criteria.json，Phase 5 由子 Agent 独立判断是否可接受。

### Cross-check 技术层

1. `<img src>` 匹配 image-manifest.json
2. 所有图片为本地 `.webp`
3. 零外部资源
4. JS `forEach(el => obs.observe(el))` 模式
5. 每页 ≥1 个真实 CTA
6. 内容图业务相关性
7. 博客框架存在（`/blog/index.html`）
8. 联系表单仅 name/email/message

### Cross-check 设计层

- [ ] Hero 标题 ≤ 2 行，副文简洁有力
- [ ] Hero 元素 ≤ 4 个
- [ ] 色彩一致性：一页一强调色
- [ ] 按钮对比度 WCAG AA
- [ ] 每页布局家族 ≥ 4 种不同 pattern

---

## Phase 5 — 子 Agent 独立验收

**主 Agent 调用 `delegate_task` 起独立子 Agent 做验收**，不调外部模型：

```
delegate_task(
  goal="你是建站验收专家。验收 {项目目录} 的 acceptance-criteria.json。逐项检查并输出 reports/acceptance-report.md。",
  context="""
项目目录：{绝对路径}
验收标准文件：acceptance-criteria.json

=== 技术检查 ===
1. 零 CDN（无 fonts.googleapis / unsplash / picsum / 外部 CDN）
2. body 内容 ≥ 500 字符
3. 所有 JS 使用 forEach(el => obs.observe(el)) 模式
4. 图片引用匹配 image-manifest.json
5. 所有图片为本地 WebP 格式
6. /blog/index.html 存在
7. 联系表单仅含 name/email/message
8. 导航链接可点击、无死链
9. 每页 title/description/OG 唯一不重复

=== 买家视角检查 ===
10. 首页：10秒内能否判断工厂品类+核心能力？
11. 产品页：技术参数是否具体（有数字，非空洞形容词）？
12. 关于页：认证/产能/QC流程是否可见？
13. 全站：CTA 按钮是否在每个页面都可见可达？
14. 全站：信任信号（认证/产能数据/工艺描述）是否充分？
15. 全站：图片是否承担了视觉传达角色（非纯装饰）？

输出格式：Markdown，每项 PASS/FAIL + 具体问题位置 + 建议修复方式。
""",
  toolsets=["file", "terminal", "search"]
)
```

子 Agent 独立上下文、独立判断。验收报告出来后主 Agent 修复 FAIL 项再部署。

---

## Phase 6 — 部署

### Wrangler 部署

```bash
npx wrangler pages deploy . --project-name=<project-name> --commit-dirty=true --branch=main
```

### Cloudflare Pages 部署

**环境变量加载**：
```bash
# 从项目 .env 自动加载（Agent 自动执行）
export $(grep -v '^#' .env | xargs)
# 或从全局凭据文件
export CLOUDFLARE_API_TOKEN=$(grep CLOUDFLARE_API_TOKEN ~/.claude/.env | cut -d= -f2)
export CLOUDFLARE_ACCOUNT_ID=$(grep CLOUDFLARE_ACCOUNT_ID ~/.claude/.env | cut -d= -f2)
```

**首次部署**：
```bash
echo "<project-name>" | npx wrangler pages project create <project-name> --production-branch=main
npx wrangler pages deploy . --project-name=<project-name> --commit-dirty=true --branch=main
```

**后续部署**：
```bash
npx wrangler pages deploy . --project-name=<project-name> --commit-dirty=true --branch=main
```

### CDN 缓存破坏

每次部署后，CDN 可能继续提供旧版本的 CSS/JS。Agent 必须执行以下至少一项：

**策略 A（推荐）：版本号**
在 HTML 中的 `<link>` 和 `<script>` 标签追加版本查询参数：
```html
<link rel="stylesheet" href="/design-tokens.css?v=2">
```
每次修改 CSS/JS 后，递增版本号。Agent 部署前自动扫描并更新。

**策略 B：Purge Cache API**
部署后调用 Cloudflare API 清除全站缓存：
```bash
# 获取 Zone ID
ZONE_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones?name=<domain>" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | python3 -c "import sys,json;print(json.load(sys.stdin)['result'][0]['id'])")

# 清除缓存
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"purge_everything":true}'
```

**原则**：CSS/JS 文件名不变时，CDN 按 hash 判断未变更而继续提供旧版本。版本号或 purge 二选一，版本号更轻量可靠。

### 部署后验证

```bash
# 1. 检查 wrangler 输出：确认 "Uploaded N files" > 0
# 2. 验证生产域名内容已更新
curl -s "https://<project>.pages.dev/" | grep <expected-new-content>
# 3. CSS 规则验证：检查关键样式是否正确加载
curl -s "https://<project>.pages.dev/design-tokens.css?v=N" | grep <expected-css-rule>
# 4. 如果仍显示旧内容：检查 CDN 缓存
#    - 自定义域名可能缓存旧版本：对比 pages.dev 预览域名 vs 生产域名
#    - 如果 pages.dev 正确但生产域名错误 → CDN 缓存问题，执行 Purge Cache
#    - 如果两者都错误 → 部署未生效，检查 wrangler 输出
```

> **踩坑经验**：部署输出 "Uploaded 0 files" 可能意味着所有文件被误判为已上传（hash 匹配旧版本），但实际上 CDN 提供的是更早的缓存版本。如果本地文件与云端内容不一致，先 touch 文件再部署，或清除 `.wrangler/cache` 目录。

## 硬约束（10 条）

| # | 规则 |
|---|------|
| 1 | **零 CDN**。系统字体 + 本地图片 |
| 2 | **JS: `forEach(el => obs.observe(el))`** 模式 |
| 3 | **图片 ID 可追溯** |
| 4 | **内容图禁图标冒充** |
| 5 | **CI 图禁建筑外观/假公司名/Logo** |
| 6 | **网站禁具体人物** |
| 7 | **Phase 4 图片引用 cross-check** |
| 8 | **每页 ≥1 个真实 CTA** |
| 9 | **内容图必须传达业务信息** |
| 10 | **完整多页网站：≥5个页面，导航指向真实页面** |

---

## 组件样式架构

**所有共享组件样式必须写在 `design-tokens.css` 中，禁止只写在 index.html 内嵌 `<style>` 里。**

```
design-tokens.css     ← CSS 变量 + Reset + Utility + 所有共享组件样式 + 响应式
index.html            ← 无内嵌 <style>（页面特有样式极少）
子页面                 ← <style> 仅包含页面特有样式
```

写 `design-tokens.css` 时一次到位，包含完整的共享组件样式，不要先写 token 再在 index.html 里补组件样式。

---

## UX 规则

### B2B 询盘弹窗（Modal Inquiry）

CTA 按钮触发 modal 弹窗表单，不跳转打断浏览：

**推荐：双栏布局（图片面板 + 表单面板）**

```html
<div class="modal-overlay" id="inquiryModal" onclick="if(event.target===this)closeModal()">
  <div class="modal-dialog">
    <button class="modal-close" onclick="closeModal()">&times;</button>
    <div class="modal-image-panel">
      <img src="/generated/modal-inquiry.webp" alt="">
      <div class="modal-image-overlay"></div>
      <div class="modal-image-text">
        <div class="mi-label">BRAND NAME</div>
        <div class="mi-value">核心卖点 · 认证信息 · <strong>高亮项</strong></div>
      </div>
    </div>
    <div class="modal-form-panel">
      <h2>询盘表单</h2>
      <p class="mf-subtitle">简短引导文案。突出免费/快速/专业。</p>
      <form action="https://formsubmit.co/{email}" method="POST">...</form>
    </div>
  </div>
</div>
```

**CSS 关键规则**（写入 design-tokens.css）：
- `.modal-dialog`：`display:grid; grid-template-columns:1fr 1fr; max-width:760px; max-height:92vh; overflow:hidden` — 双栏均分
- `.modal-image-panel`：`position:relative; overflow:hidden; min-height:100%` — 图片撑满左侧
- `.modal-image-panel img`：`position:absolute; inset:0; width:100%; height:100%; object-fit:cover` — 图片裁剪铺满
- `.modal-image-overlay`：`position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0.8) 100%)` — 渐变遮罩保证文字可读
- `.modal-image-text`：底部定位，品牌名 + 卖点，适配品牌色强调
- `.modal-form-panel`：`padding:var(--space-lg) var(--space-md); display:flex; flex-direction:column; justify-content:center` — 垂直居中，紧凑 padding 避免滚动条
- 移动端 `@media(max-width:640px)`：恢复单栏 `grid-template-columns:1fr; max-width:420px`，图片面板限高 160-200px

**设计原则**：
- 左侧图片面板用品牌氛围图或产品展示图，传达品牌调性
- 表单面板紧凑排版，桌面端不应出现滚动条
- 关闭按钮置于右上角，`z-index:10` 覆盖图片面板
- 表单字段：Name + Email + Message（3 字段，不贪多）
- FormSubmit.co 或等效后端兜底

### 弹窗图片生成

弹窗左侧图片推荐用生图 API 生成，prompt 方向：
- **产品展示型**：「人手捧高端产品展示，第一人称视角，品牌氛围光，匹配站点配色」
- **品牌氛围型**：「品类抽象纹理，品牌色渐变，留空间给文字叠加」

图片尺寸 1024×1024，`object-fit:cover` 自动适配。

> **踩坑经验**：单栏弹窗（480px 居中）在高信息密度下显得拥挤且缺乏品牌感。双栏布局（760px）同时展示品牌视觉和表单，转化更好。关键是控制表单面板高度，避免桌面端出现右侧滚动条。

### 子页面 Hero

每个子页面用 `.sub-hero`：背景图 + dark overlay + 标题/副标题。每页配不同的背景图（见 Phase 1 图片策略的 sub-hero-bg）。

### CTA 卡片

CTA 卡片叠加低透明度背景纹理增加层次感：

```css
.cta-card{position:relative;overflow:hidden}
.cta-card::before{content:'';position:absolute;inset:0;
  background:url(/generated/cta-bg.webp) center/cover no-repeat;
  opacity:.33;z-index:0}
.cta-card::after{content:'';position:absolute;z-index:1}
.cta-card>*{position:relative;z-index:2}
```

CTA 卡片应出现在：首页、产品页、关于页、博客列表页、每篇博客文章底部。

> **踩坑经验：CTA 按钮可见性陷阱** — 深色 CTA 卡片会导致按钮文字融入背景。必须在 design-tokens.css 中显式覆盖按钮颜色，确保对比度达标。

### 导航与锚点

- Footer 链接必须指向独立页面，**禁止** `#anchor` 定位链接
- 不适合做独立页面的内容，从 footer 删除，不要用锚点凑数

### 博客文章卡片

博客列表中的卡片必须是 `<a>` 链接（指向 `/blog/slug.html`）。每篇文章卡片应有封面缩略图（`.blog-card-img`）。

### Hero 设计最佳实践

#### 默认布局：居中（推荐）

经过多个实战站点验证，**居中 Hero 布局是 B2B 电子制造站最稳妥的默认选择**：

```css
.hero{
  position:relative;
  min-height:100vh;
  display:flex;align-items:center;  /* 垂直居中，非 flex-end */
  padding:var(--space-5xl) 0;
  background:#0a0f1a;  /* 深色兜底，与图片色调融合 */
  overflow:hidden;
}
.hero::before{
  content:'';position:absolute;inset:0;
  background:rgba(0,0,0,0.45);  /* 单一暗色遮罩，非复杂渐变 */
  z-index:1;
}
.hero-img{
  position:absolute;inset:0;
  width:100%;height:100%;
  object-fit:cover;object-position:center 30%;
  z-index:0;
}
.hero-content{
  position:relative;z-index:2;
  width:100%;text-align:center;  /* 文字水平居中 */
}
.hero-content .container{max-width:860px}  /* 收窄文字宽度保证可读性 */
.hero-content .section-label{
  background:rgba(21,101,208,0.25);  /* 品牌色半透明标签 */
  color:var(--accent-glow);
  margin-left:auto;margin-right:auto;  /* 居中 */
}
.hero-content h1{
  font-size:clamp(2.5rem,5vw,4rem);
  line-height:1.1;
  color:#fff;
}
.hero-content h1 span{color:var(--accent-glow)}  /* 关键词品牌色高亮 */
.hero-content .hero-sub{
  font-size:var(--text-lg);
  color:rgba(255,255,255,0.8);
  margin:0 auto var(--space-xl);
  max-width:600px;  /* 副标题收窄 */
  line-height:1.6;
}
.hero-buttons{
  display:flex;gap:var(--space-md);
  flex-wrap:wrap;justify-content:center;
}
.hero-stats{
  display:flex;gap:var(--space-3xl);justify-content:center;
  margin-top:var(--space-3xl);
  padding-top:var(--space-xl);
  border-top:1px solid rgba(255,255,255,0.12);
}
.hero-stat-value{font-size:var(--text-3xl);font-weight:700;color:#fff;line-height:1}
.hero-stat-label{font-size:var(--text-sm);color:rgba(255,255,255,0.7);margin-top:4px}

@media(max-width:768px){
  .hero-stats{flex-wrap:wrap;gap:var(--space-xl)}
  .hero-buttons{flex-direction:column}
}
```

**关键设计决策**（与旧版的区别）：
- `align-items:center` 替代 `align-items:flex-end` → 文字在视口垂直居中
- `::before{background:rgba(0,0,0,0.45)}` 替代复杂渐变色 overlay → 更干净、暗度均匀
- `text-align:center` + `margin:0 auto` → 所有文字/按钮/数据条水平居中
- 标题用 `<span>` 包裹关键词并以 `--accent-glow` 高亮 → 视觉焦点

#### 备选布局：靠下（适合车间广角图）

如果 Hero 图是车间广角（非产品微距），可将文字靠下放置：

```css
.hero{align-items:flex-end;padding-bottom:var(--space-4xl)}
.hero::before{
  background:linear-gradient(to bottom,
    rgba(0,0,0,0.15) 0%,rgba(0,0,0,0.30) 30%,
    rgba(0,0,0,0.60) 60%,rgba(0,0,0,0.88) 100%);
}
```

**适用条件**：背景图为广角车间/工厂实景（非微距产品特写），上半部有内容需要透出时。

#### Hero 背景图 Prompt 策略

Hero 背景图是整站第一印象。**不存在「唯一正确」的策略**——构图方向由 design-blueprint.md 的品牌人格三轴决定。

**策略选择矩阵**（Agent 根据品牌人格选择）：

| 品牌人格 | 推荐构图策略 | Prompt 关键词方向 |
|---------|------------|-----------------|
| 高端精密型 | 产品微距特写 | macro photography, extreme close-up, shallow depth of field, cinematic lighting, [品牌色] background with [金属色] rim light |
| 规模产能型 | 广角产线实景 | wide shot, automated production line, clean factory floor, natural daylight, depth and scale |
| 技术先锋型 | 抽象科技视觉 | geometric patterns, [品牌色] glow, futuristic, dark gradient, light trails |
| 可靠传统型 | 工作室产品摆拍 | studio lighting, clean white/neutral background, product hero shot, soft shadows, commercial photography |

**颜色规则**：prompt 中的颜色描述必须从 design-blueprint.md 的 COLOR PALETTE 提取，**禁止使用固定颜色名**（如 "dark navy"、"electric blue"、"golden"）。

**通用规则**（所有策略）：
- 包含文字区域留空指令（配合 Hero 文字位置：`upper portion clean for centered text` 或 `left side clear for text overlay`）
- 包含 `no people faces, no text, no logos`
- 构图配合该站 Hero 的文字布局（居中 / 左对齐 / 底部对齐）

#### Hero 图片迭代流程

如果 Hero 图效果不理想，**分析根因后生成 3 个跨策略变体**（不要在同一策略内微调）：

1. **分析失败原因**：构图问题 / 色调问题 / 质感问题 / 策略选择错误（如用微距策略做规模产能型站点）
2. **生成 3 个差异化变体**——从上述策略选择矩阵中选 **3 个不同方向**（如微距 + 广角 + 抽象，而非 3 个微距变体）
3. 并行生成，让用户选择
4. 保留最佳版本，另外 2 张降级为 sub-hero-bg 或 cta-bg
5. 3 张都不满意 → 品类视觉方向可能选错了，回到 Phase 1 步骤 1 重新审视

> **踩坑经验**：Whale PCBA 项目经过 3 轮 Hero 迭代（抽象蓝色 → 暗沉工厂 → 金色 ENIG PCB 微距），最终发现「高端产品微距摄影」prompt 策略比「工厂环境」策略效果好得多——但这**不代表每站都用微距**。一个主打产能规模的工厂站，广角产线实景比产品微距更有说服力。**策略服务于品牌人格，不是反过来。**

### 首页板块编排：Agent 自主决策

#### 核心原则

首页是整站视觉密度最高的页面。B2B 采购经理扫描首页时，每向下滚动一次应看到新的内容。但**板块数量、类型、顺序、组合方式由 Agent 根据买方角色和品类自主决定**，不设固定模板。

#### 唯一的硬性约束：结构差异化检查

为保证连续站点不趋同，Agent 必须在 `design-blueprint.md` 中记录首页板块结构，并与上一站点对比：

**板块类型重叠率 < 50%**（基于板块的功能角色分类）：
- 同一板块角色（如"图文分屏"、"卡片网格"、"数据条"、"流程展示"、"大图+大字"等）在连续两个站点中重复出现不超过半数
- 板块**顺序**应有变化（如上一站 Hero→卡片→图文→CTA，本站可以 Hero→大图展示→数据→卡片→CTA）

**不限制的内容**（Agent 自由发挥）：
- 首页板块总数（5 个或 12 个都可以，只要信息维度覆盖全）
- 每个板块的具体视觉呈现方式（卡片/表格/图文分屏/全幅图/轮播/时间线…任选）
- 图片使用数量（按需，不设下限和上限）
- 板块间的视觉分隔方式（背景色切换/图片/留白/分割线/装饰元素）
- CSS 组件样式（每次建站根据设计基调重新设计，不复用固定组件模板）

#### 设计节奏指南（非强制）

板块之间的视觉节奏建议遵循「密度交替」原则：密集信息板块与呼吸感板块交替出现，避免连续高密度导致疲劳。Agent 在设计完首页后自检：滚动首页时是否有「轻重交替」的节奏感。

> **踩坑经验**：Whale PCBA 初版首页只有 7 个板块 + 3 张图，用户反馈「首页图片太少了，多一些板块」。从 3 张图扩展到 12 张图、7 板块扩展到 10 板块后，首页的视觉说服力显著提升。但这**不代表每站都需要 10 个板块**——关键在于每个板块是否承担了独特的说服功能。合并功能重叠的板块比堆砌数量更重要。

---

## 错误恢复

| 阶段 | 失败 | 恢复 |
|------|------|------|
| Phase 0 | 品类不在知识库 | Agent 搜索补充该品类标准参数 |
| Phase 1 | 蓝图或文件不完整 | 主 Agent 补全 |
| Phase 2 | 生图失败 | 检查网络连接和 API Key；确认 `api.inferera.com` 可达 |
| Phase 2 | edits 端点 400 | 检查 `images` 是否为对象数组 `[{"image_url":"data:..."}]`，非纯字符串或 `{url:...}` |
| Phase 2 | 参考图片下载失败 | 检查 `reference` URL 可访问性；本地路径是否相对于 `meta.referenceBaseUrl` 正确；回退到纯文本生图 |
| Phase 2 | aihubmix.com 超时 | 已默认使用 `api.inferera.com`，不再出现此错误 |
| Phase 2 | gen-site-images.py 不在磁盘 | `skill_view` 获取源码写入 |
| Phase 2 | 图生图图片过大(>5MB) | 脚本会警告，建议先压缩参考图到 1024x1024 以内 |
| Phase 3 | 子页面格式混乱 | 检查共享组件样式是否在 design-tokens.css |
| Phase 3 | 单页失败 | 主 Agent 重写该页 |
| Phase 3 | `execute_code` 内 write_file 未生效 | **严重陷阱**：`execute_code` 的 `write_file` 可能静默失败。修改文件必须用顶层工具直接调用 |
| Phase 4 | 10秒测试 FAIL | 补图→补模块→重测（最多2轮） |
| Phase 4 | Cross-check 失败 | 主 Agent 针对性修复 |
| Phase 5 | 验收 FAIL | 主 Agent 修复 → 重新 delegate_task |
| Phase 6 | Pages 项目不存在 | `wrangler pages project create` → deploy |
| Phase 6 | 部署显示 "Uploaded 0 files" | 常见于 `execute_code` write 静默失败，`grep` 确认文件包含新内容 |
| Phase 6 | 生产域名显示旧内容 | CDN 缓存延迟，sleep 5-10s 后重试 |
| Phase 6 | 部署后 CSS 不生效 | CDN 缓存了旧版本 CSS：对比 pages.dev 预览 URL 与自定义域名的 CSS 内容，如不一致则 purge cache 或递增版本号 |
| 通用 | 批量替换破坏特殊字符 | `@`、`$` 等字符在 Perl/sed 中可能被当作变量/正则元字符。优先用 `sed` 字面量模式（`s|literal|replacement|g`），避免 Perl `-0pe` 中大段带特殊字符的替换。修改后立即 `grep` 验证关键字段（如邮箱地址）是否完整 |

---

## 依赖的 API 与环境变量

| 阶段 | API | 环境变量 | 状态 |
|------|-----|----------|:--:|
| Phase 2 | AIHubMix → GPT Image 2 | `AIHUBMIX_API_KEY` | ✅ |
| Phase 6 | Cloudflare Pages | `CLOUDFLARE_API_TOKEN` + `_ACCOUNT_ID` | ✅ |

Python 依赖: `requests`。CLI: `wrangler`。
