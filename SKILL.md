---
name: 建站工作流
version: "10.1"
description: 电子制造B2B出口建站。一句话→完整内容蓝图→全站图片策略→10秒买家测试驱动设计迭代。纯静态HTML完整多页网站。
upstream: https://github.com/cpu152650311-coder/website-workflow
---

# 建站工作流 v10.1

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
      "display": "full-bleed"
    },
    {
      "id": "pcb-stackup-diagram",
      "role": "technical-diagram",
      "page": "/products/index.html", 
      "prompt": "Cross-section diagram showing PCB layer stackup...",
      "display": "inline-large"
    }
  ]
}
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
| **全幅 Hero** | hero-bg, sub-hero-bg | `object-fit:cover; object-position:center 30%` 上下留暗区 |
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

##### B2B 内容架构（每页必须承载）

| 页面 | 必须承载的业务内容 |
|------|-------------------|
| 首页 | Hero + 核心能力概述(3-4条) + 产品线预览 + 认证徽标条 + 产能数据亮点 + CTA |
| 关于页 | 工厂规模 + 产线设备 + QC流程 + 认证列表 + 出货能力 + 合作模式 |
| 产品/能力页 | 技术参数表 + 工艺能力清单 + 材料选项 + 品质标准 + 交期/MOQ + 应用领域 |
| 联系页 | 询盘表单 + 地址/联系方式 + 办公/工厂图 + FAQ |

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

**API 端点**：默认 `aihubmix.com`，不可达时自动回退 `api.inferera.com`。**不要用 `api.aihubmix.com`（已弃用）。**

**图片尺寸限制**：所有图片 `1024×1024`。

### 按角色分 Prompt 策略

不同图片角色用不同的 prompt 写法：

| 角色 | Prompt 重点 | 典型写法 |
|------|-----------|---------|
| hero-bg | 品类氛围 + 上半部留空给文字 | `atmospheric [品类] manufacturing environment, upper area clean for text overlay, [色彩方向] tones` |
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

GPT Image 2 API 可能返回两种格式：URL 或 Base64。脚本必须同时支持。

```python
import requests, base64, json
from pathlib import Path

def generate_image(prompt, api_key, quality='low'):
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'model': 'gpt-image-2', 'prompt': prompt, 'size': '1024x1024'}
    
    try:
        resp = requests.post('https://aihubmix.com/v1/images/generations', 
                            headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
    except:
        resp = requests.post('https://api.inferera.com/v1/images/generations',
                            headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
    
    data = resp.json()
    image_data = data['data'][0]
    
    if 'url' in image_data:
        return requests.get(image_data['url']).content
    elif 'b64_json' in image_data:
        return base64.b64decode(image_data['b64_json'])
    else:
        raise ValueError('No image data in response')
```

```bash
python gen-site-images.py --prompts image-strategy.json --out ./generated
```

**gen-site-images.py 获取方式**：通过 `skill_view(name='建站工作流', file_path='scripts/gen-site-images.py')` 获取源码，写入项目根目录再执行。

**追加图片**：
```bash
python gen-site-images.py --prompts supplement.json --out ./generated --manifest image-manifest.json
```

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

### Hero 设计原则

**文字可读性**：背景图上方透出图片内容、下方保证文字可读。渐变 overlay 顶部透明、底部加深：

```css
.hero{
  min-height:100vh;
  display:flex; align-items:flex-end;
}
.hero-overlay{
  background:linear-gradient(to bottom,
    rgba(bg,.15) 0%, rgba(bg,.30) 30%,
    rgba(bg,.60) 60%, rgba(bg,.88) 100%);
}
```

**图片构图配合文字位置**：文字居中→广角/平铺；文字靠左→图片主体偏右；文字靠下→图片上半部有内容。

---

## 错误恢复

| 阶段 | 失败 | 恢复 |
|------|------|------|
| Phase 0 | 品类不在知识库 | Agent 搜索补充该品类标准参数 |
| Phase 1 | 蓝图或文件不完整 | 主 Agent 补全 |
| Phase 2 | 生图失败 | 切换 `api.inferera.com` 回退 |
| Phase 2 | 400 Bad Request | 检查 `response_format` 参数（不支持）；检查端点（`aihubmix.com` 非 `api.aihubmix.com`） |
| Phase 2 | gen-site-images.py 不在磁盘 | `skill_view` 获取源码写入 |
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
