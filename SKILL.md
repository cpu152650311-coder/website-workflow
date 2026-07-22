---
name: 建站工作流
version: "11.1"
description: B2B外贸出口建站（通用）。一句话→完整页面树→SEO+安全基础设施→ui-ux-pro-max专业配色→Pinterest视觉参考→全站图片策略→AI去背Logo自动favicon→10秒买家测试→部署后审计。纯静态HTML多页站（30+页）。博客只需3篇。适用任意制造/贸易品类。
upstream: https://github.com/cpu152650311-coder/website-workflow
---

# 建站工作流 v11.1

> **v11.1**：**视觉设计专业化 + Logo自动化**。Phase 1B 整合 ui-ux-pro-max 获取专业配色/字体建议（161 调色板 + 57 字体配对），新增 Pinterest 视觉参考搜索获取品类真实 mood board。Logo 生成流程全自动：GPT Image 2 生图 → rembg AI 去背景 → Pillow 缩放 favicon 全尺寸。gen-site-images.py 新增 `--limit N` 参数支持样图阶段精确控制。Phase 0 研究增强：WebSearch + WebFetch 多维度搜索 + 竞品站信息架构分析。
> **v11**：**全历程经验编码**——基于 huaxingpcba.com（97页/449图/152提交）7轮对话实战经验重构。Phase 0 产出完整4层页面树（核心信任页+能力页+行业页+营销页，30+页）。Phase 1 新增SEO基础设施（JSON-LD/og/canonical/robots/sitemap/_headers）、CSS反模式黑名单（background简写/--cta-bg/direction:rtl/hover纯CSS导航）、CTA按钮硬规则、页面骨架模式库。Phase 2 质量硬阻止+零图片复用。Phase 3 新增404/Google Ads落地页模板、表单标准化。Phase 5 扩展SEO/安全/图片去重审计。Phase 7 全新：部署后线上验证。博客只需3篇（blog-workflow生成）。
> **v10.3**：移除固定板块模板，Agent自主决定首页板块结构。废除hero硬编码prompt模板，Hero构图策略改为品牌人格驱动选择矩阵。
> **v10.0-v10.2**：Phase 0一句话内容展开、全站图片角色策略、10秒买家测试驱动设计迭代、Hero居中布局、ENV凭据管理、CDN缓存破坏。
> **v8.4-v9.0**：品类细分+品牌人格三轴+差异化防收敛、Hero沉浸式布局、CTA按钮可见性陷阱、B2B UX规则。

## 核心理念

```
用户: "做个{品类}外贸站，叫{品牌名}"
  │
  ▼
Phase 0  Agent 多维度搜索（WebSearch+WebFetch+竞品站分析）→ 菜单勾选
  │ 🛑 用户确认菜单
  ▼
Phase 1A  Logo 生成（3-4 候选）→ 用户选定 → rembg AI去背景 → 自动转换 favicon
  │ 🛑 用户确认 Logo
  ▼
Phase 1B  ui-ux-pro-max 配色/字体建议 + Pinterest 视觉参考 → 用户选择
  │ 🛑 用户确认配色+字体
  ▼
Phase 1C  图片 prompt 审阅（5-8 个关键 prompt）→ 用户确认方向
  │ 🛑 用户确认 prompt
  ▼
Phase 2   样图生成（--limit 3）→ 展示 → 🛑 确认 → 全量生图
  │ quality 写死 low，零复用
  ▼
Phase 3   先做首页+2代表页 → 展示视觉一致性 → 🛑 确认 → 全量编码
  │ 含 404 / Google Ads 落地页模板
  ▼
Phase 4   10秒买家测试 ←──┐
  │ 不通过 → 补图(Phase 2) → 补模块(Phase 3) ──┘
  ▼
Phase 5   子 Agent 独立验收（SEO/安全/图片去重/买家视角）
  ▼
Phase 6   Wrangler → Cloudflare Pages 部署
  ▼
Phase 7   部署后线上验证（安全头/HTTP状态/sitemap/robots）
  ▼
  🚀 上线
```

## 流程（8 Phase + 确认点）

```
Phase 0  主 Agent → 多维度搜索（WebSearch+WebFetch+竞品站）+ 菜单勾选（🛑用户确认）
         ├─ content-blueprint.md（产品参数/认证/交期/产能/工艺/信任信号）
         └─ page-tree.json（4层页面树）

Phase 1A Agent → Logo 生成（3-4候选）+ rembg AI去背景 + Favicon 转换（🛑用户确认）
Phase 1B Agent → ui-ux-pro-max 配色/字体建议 + Pinterest 参考 + 设计基调（🛑用户确认）
Phase 1C Agent → 图片 prompt 审阅（5-8关键prompt）（🛑用户确认）
         ├─ design-blueprint.md（品类+人格+差异化）
         ├─ design-tokens.css
         ├─ index.html
         ├─ blocks/*.html
         ├─ image-strategy.json（零复用）
         ├─ acceptance-criteria.json
         ├─ _headers / robots.txt / sitemap.xml / llms.txt
         └─ generated/logo-transparent.png, favicon.ico, apple-touch-icon图标

Phase 2  GPT Image 2 → 样图 --limit 3 → 🛑确认 → 全量生图（quality 硬写死 low）
         └─ python gen-site-images.py --prompts image-strategy.json --out ./generated

Phase 3  主 Agent → 首页+2代表页 → 🛑确认视觉一致性 → 全量编码

Phase 4  主 Agent → 10 秒买家测试 + 设计迭代

Phase 5  子 Agent → 独立验收（技术+SEO+安全+买家双视角）

Phase 6  Wrangler → Cloudflare Pages 部署

Phase 7  主 Agent → 部署后线上验证 → deploy-report.md
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

## Phase 0 — 一句话展开为内容蓝图 + 菜单选择

用户只需给：**品类 + 品牌名**。

### 步骤 1：自动行业调研

Agent 收到品类名后，**立即自动执行多维度搜索**（不需用户提供资料）：

```
搜索策略（WebSearch + WebFetch 组合）：
1. WebSearch "{品类} product categories types classification"
   → 提取产品分类体系（一级/二级/三级）
2. WebSearch "{品类} manufacturing process quality standards certification"
   → 提取工艺能力、品质标准、行业认证
3. WebSearch "{品类} export B2B wholesale MOQ lead time"
   → 提取交期、MOQ、包装标准
4. WebSearch "{品类} applications industries downstream"
   → 提取下游应用行业
5. WebSearch "{品类} top manufacturers brands global"
   → 提取竞品站参考（了解行业视觉/内容标准）
6. WebFetch 竞品站首页 + 能力页（2-3 个站点）
   → 分析信息架构、常见板块、内容深度
```

**搜索工具**：
- `WebSearch`：覆盖搜索引擎获取行业信息、竞品站列表
- `WebFetch`：深入读取具体页面的信息架构和内容结构
- 模型知识库：补充搜索不到的专业技术参数

**信息校验**：跨 2-3 个来源交叉验证（如认证标准、交期等），避免单一来源偏差。

### 步骤 2：呈现菜单供用户选择

Agent 调研完后，将结果整理为菜单，**让用户勾选**，不替用户做决定：

```
📋 页面结构方案 — 请确认或调整：

一、能力分类（capabilities/）：
  根据调研，{品类} 通常分为以下子类：
  □ {子类A}
  □ {子类B}  
  □ {子类C}
  □ {子类D}
  □ 其他：___

二、行业应用（industries/）：
  该品类主要服务以下行业：
  □ {行业1}
  □ {行业2}
  □ {行业3}
  □ {行业4}
  □ 其他：___

三、Logo 方向：
  根据品牌名和品类，以下哪种风格合适？
  □ 抽象符号（几何图形/行业意象，无文字）
  □ 字母标（品牌首字母或缩写，极简 typography）
  □ 图形+文字组合（图标 + 品牌名）
  □ 纯文字标（定制字体，无图标）
  你的选择：___
  补充要求（可选）：{颜色偏好/避免元素/参考风格}

四、设计方向：
  品牌人格三轴定位（每轴选一端）：
  ① 技术先锋型 ←→ 可靠传统型
  ② 高端精密型 ←→ 规模产能型  
  ③ 国际通路型 ←→ 工厂直营型
  你的选择：___

五、核心信任页（以下为必需，不可跳过）：
  ☑ about ☑ factory ☑ quality ☑ shipping 
  ☑ faq ☑ how-it-works ☑ design-guides ☑ projects
  ☑ contact ☑ privacy ☑ terms ☑ 404
```

用户确认/调整后，Agent 产出 page-tree.json。

### 自动展开规则

Agent 根据品类从模型知识库自动填充以下字段，**不询问用户、不等待厂商资料**：

| 字段 | 填充策略 |
|------|---------|
| 产品参数 | 该品类全球最高工艺标准（搜索补充） |
| 认证体系 | 该品类必备+加分认证（搜索补充） |
| 产能数据 | 该品类中型工厂标准产能 |
| 交期/MOQ | 该品类标准最优档 |
| 工艺能力 | 该品类完整工艺链 |
| 品质控制 | 该品类标准QC流程 |
| 应用领域 | 该品类典型下游行业 |

**输出文件**：
- `content-blueprint.md`：完整的业务内容字段，Phase 1 设计时直接引用。
- `page-tree.json`：全站页面树（4层结构，30+页），每页分配独立标题/H1/描述/关键词/内容角度。

### 页面树规划（4 层结构）

Phase 0 不止填充业务参数，还要**产出完整页面树**。Agent 根据品类和行业自动展开以下 4 层：

#### 第 1 层：核心信任页（每个站必需，14 页）

```
index.html              → 首页
about/index.html        → 关于我们（规模/设备/团队）
factory/index.html      → 工厂实景（产线/设备/环境）
quality/index.html      → 品质控制（QC流程/检测设备/认证）
capabilities/index.html → 能力总览（hub页，链接子能力）
industries/index.html   → 行业方案（hub页，链接子行业）
shipping/index.html     → 物流出货（包装/时效/全球配送）
faq/index.html          → 常见问题（FAQPage JSON-LD）
how-it-works/index.html → 合作流程（询盘→打样→量产→出货）
design-guides/index.html → 设计指南（DFM/文件格式/参数推荐）
projects/index.html     → 案例展示（精选项目/客户评价）
quote/index.html        → 快速报价（计算器/表单）
contact/index.html      → 联系询盘（表单+地址+FAQ）
privacy/index.html      → 隐私政策
terms/index.html        → 服务条款
blog/index.html         → 博客列表（框架，文章由blog-workflow生成）
404.html                → 404错误页
```

#### 第 2 层：能力页（按品类自动展开，2-3 层深）

根节点 `capabilities/` 为 hub 页。Agent 根据 Phase 0 步骤 2 的用户选择拆分子能力，保持 2-3 层深度。

#### 第 3 层：行业页（从"应用领域"字段展开）

`industries/` 为 hub 页，从 Phase 0 步骤 2 的用户勾选展开：

每行业独立页包含：行业痛点 → 技术要求 → 我们的方案 → 相关认证 → 案例 → CTA。

#### 第 4 层：营销落地页

```
welcome/index.html     → Google Ads 独立着陆页
                         无 header/footer，noindex nofollow
                         内嵌 CSS，不依赖 design-tokens.css
```

**Agent 决策原则**：
- 核心信任页 14 页**必须全部创建**，不能省略
- 能力页按品类知识库展开，Agent 自主决定子页面数量和名称
- 行业页从"应用领域"字段自动映射，通常 6-8 页
- 全部页面规划写入 `page-tree.json`，每页预分配：标题/H1/meta description/关键词/内容角度/所需图片角色

### 为什么可以这样做

- 模型知识库对大多数制造品类的标准参数有完整知识
- 所有内容按该品类的行业最高标准展开
- 真实客户信息后期替换即可，AI 先填充最优标准
- 厂商确认时只需微调数字，不需要从零写

---

## Phase 1 — Logo + 设计确认 + 图片策略

Phase 1 分 3 步，**每步完成后暂停，等用户确认再继续**。

---

### Phase 1A：Logo 生成 + Favicon（透明背景）

Agent 根据 Phase 0 用户选择的 Logo 方向，写出 3-4 个 prompt 变体（同一方向的不同表现）。

**Logo prompt 关键规则**：所有 prompt 末尾自动追加 `isolated on pure white background, no shadows, clean edges`。白底/纯色底让 AI 背景移除（rembg）能精准抠图，产出透明背景 logo。

```bash
# 并行生成 3-4 个 logo 候选
python gen-site-images.py --prompts logo-variants.json --out ./generated --limit 4
```

> `logo-variants.json` 临时文件，包含 3-4 个同方向的 logo prompt 变体。质量硬写死 `low`。

生成后，**展示给用户选择**。用户选定一张后，转为 favicon 格式（**自动 AI 去背景**）：

```bash
python gen-favicon.py --source ./generated/{logo-id}.webp --out ./generated
```

> **gen-favicon.py 工作流程**（位于本技能 `scripts/` 目录）：
> 1. 读取源 logo 图片
> 2. **rembg AI 自动移除背景**（输出透明 PNG）
> 3. 保存 `logo-transparent.png`（透明背景，可直接用于 header/navbar）
> 4. Pillow 缩放生成 `favicon.ico`（16×16 + 32×32）、`apple-touch-icon.png`（180×180）、`icon-192.png`、`icon-512.png`
> 5. 打印 HTML `<link>` 标签
>
> **依赖**：rembg（`pip install rembg`）+ Pillow。如 rembg 未安装，脚本自动跳过去背步骤并输出 WARNING。
> **跳过去背**：`--no-remove-bg` 参数保留原始背景（如 logo 本身已是透明 PNG）。

**输出**：
| 文件 | 说明 |
|------|------|
| `generated/logo-raw.webp` | 原始生图（白底） |
| `generated/logo-transparent.png` | 去背后透明 PNG（**网站 header/navbar 用这个**） |
| `generated/favicon.ico` | 多尺寸 ICO（16×16 + 32×32） |
| `generated/apple-touch-icon.png` | iOS 桌面图标（180×180） |
| `generated/icon-192.png` | Android/Chrome 图标（192×192） |
| `generated/icon-512.png` | PWA 大图标（512×512） |

**HTML 引用**：
```html
<link rel="icon" type="image/x-icon" href="/generated/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/generated/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/generated/icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/generated/icon-512.png">
```

---

### Phase 1B：配色 + 字体 + 整体风格确认

Agent 提取该品类的视觉特征后，**先调用 ui-ux-pro-max 获取专业设计建议**，再呈现选项让用户选择。

#### 1. 获取专业设计系统建议（ui-ux-pro-max）

Agent 自动运行 ui-ux-pro-max 搜索，获取该品类的专业配色、字体、风格建议：

```bash
python skills/ui-ux-pro-max/scripts/search.py "{industry} {product_type} {keywords}" --design-system -f markdown
```

**搜索策略**：
- 从 Phase 0 的行业调研中提取关键词（品类 + 定位 + 风格倾向）
- 组合多维度关键词搜索：`"{品类} {行业} {风格关键词}"`
- 如搜索结果不理想，换关键词重试（如 `"industrial manufacturing B2B professional"` → `"precision engineering premium trust"`）

同时搜索配色和字体细节：
```bash
python skills/ui-ux-pro-max/scripts/search.py "{industry} {keywords}" --domain color
python skills/ui-ux-pro-max/scripts/search.py "{style_keywords}" --domain typography
python skills/ui-ux-pro-max/scripts/search.py "{style_name}" --domain prompt
```

> 不将 ui-ux-pro-max 的输出当作硬性规则，而是作为专业参考来辅助设计方案呈现。

#### 2. Pinterest 视觉参考采集

Agent 搜索 Pinterest 收集该品类/风格的参考情绪板（mood board），获取真实世界的设计灵感：

```
搜索关键词（WebSearch）：
- "pinterest {品类} website design inspiration"
- "pinterest {风格关键词} web design mood board"
- "pinterest B2B {品类} color palette"
```

**目的**：
- 了解该品类实际网站常用的视觉语言（颜色、排版、图片风格）
- 获取配色比例参考（主色/辅色/点缀色的实际使用比例）
- **不是复制**，而是确保设计方向符合该品类的视觉惯例

> Pinterest 无公开 API，通过 WebSearch + WebFetch 获取公开的 Pin/Board 截图和描述即可。

#### 3. 品类视觉线索（搜索驱动，非预设）

Agent 综合 ui-ux-pro-max 结果 + Pinterest 参考 + Phase 0 行业调研，提取该品类的视觉意象：

- 该品类的产品/材料/工艺的视觉特征是什么？
- Pinterest 上该品类标杆品牌的常用配色是什么？
- 该品类海外买家对视觉的期待是什么？

**禁止套用任何预设的品类→色彩映射表。** 每个站点都从零调研。

#### 4. 呈现配色方案（2-3 组）→ 用户选择

Agent 综合 ui-ux-pro-max color 搜索结果，设计 2-3 组不同的配色方案，每组包含：
- 主色 + 强调色 + 背景色 + 文字色（CSS 变量格式）
- 一句话描述色彩感受
- 标注灵感来源（如 "基于 ui-ux-pro-max: {palette_name}"）

```
🎨 请选择配色方案：

A. {方案名}（灵感：ui-ux-pro-max {palette_name}）
   主色: #XXXXXX | 强调: #XXXXXX | 背景: #XXXXXX | 文字: #XXXXXX
   感受：{一句话描述}

B. {方案名}（灵感：Pinterest {行业} mood board）
   主色: #XXXXXX | 强调: #XXXXXX | 背景: #XXXXXX | 文字: #XXXXXX
   感受：{一句话描述}

C. {方案名}（灵感：自定义）
   主色: #XXXXXX | 强调: #XXXXXX | 背景: #XXXXXX | 文字: #XXXXXX
   感受：{一句话描述}

你的选择：___
```

#### 5. 呈现字体方案 → 用户选择

Agent 参考 ui-ux-pro-max `--domain typography` 搜索结果，提供 3 组字体方案：

```
🔤 请选择字体方案（参考 ui-ux-pro-max 推荐，均为系统安全字体，零 CDN）：

A. 标题 sans-serif + 正文 sans-serif（现代/干净，推荐技术品类）
   {推荐组合名，如 "Inter + System UI"}

B. 标题 serif + 正文 sans-serif（传统/权威，推荐高端品类）
   {推荐组合名}

C. 标题 mono + 正文 sans-serif（技术/精密，推荐工业品类）
   {推荐组合名}

你的选择：___
```

#### 6. 品牌人格 → 设计基调

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

#### 7. 设计差异化 → 防收敛

同一品类、同一人格容易产出相似设计。Agent 必须主动做以下差异化决策（至少 3 项）：

- [ ] 主色：从该品类的常见色中选**一个非默认**的（如该品类主流用蓝色，则选其对比色或金属色为主）
- [ ] 布局系统：首页首个 section 的类型与上一个站点不同（全屏图 / 图文分屏 / 卡片网格 / 大标题居中）
- [ ] 字体个性：标题字体在 serif/sans/mono 之间切换感受
- [ ] 密度节奏：内容密度在「稀疏留白」与「信息密集」之间制造差异
- [ ] CTA 策略：弹窗/页尾表单/浮动按钮/内联 CTA，切换主要询盘入口形式
- [ ] Hero 构图：产品特写/车间广角/抽象科技纹理/地理网络，使用不同视觉母题

**差异化检查**：如果连续两个站点的差异化项重叠 ≥2 项，第三个站点必须强制使用不同的选项。

#### 8. 全站图片策略规划

**核心原则：GPT Image 2 生成 1024×1024 图片极便宜（$0.006/张），应在全站广泛使用。不要把生图限定在产品照片上。**

Agent 遍历每个页面的每个 section，分配图片角色。输出 `image-strategy.json`：

```json
{
  "images": [
    {
      "id": "hero-bg",
      "role": "hero-bg",
      "page": "/index.html",
      "prompt": "{品类} manufacturing facility with automated production lines, professional B2B photography...",
      "display": "full-bleed",
      "reference": ""
    },
    {
      "id": "product-angle-45",
      "role": "product-showcase",
      "page": "/products/index.html",
      "prompt": "Same {产品} product, 45-degree angle view, clean studio lighting...",
      "display": "inline-large",
      "reference": "https://example.com/product-front.webp"
    },
    {
      "id": "tech-diagram",
      "role": "technical-diagram",
      "page": "/products/index.html", 
      "prompt": "Technical diagram showing {该品类的核心技术概念} structure and composition...",
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

**总量：每站 50-80 张（30+页站点），成本 ~$0.30-0.48。**

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

#### 9. 完整页面规划（基于 page-tree.json）

Phase 0 已产出 `page-tree.json`（4 层页面树）。Phase 1 在此基础上的工作：

- 为每页分配图片角色（写入 image-strategy.json）
- 确定每页的板块组成（参考下方"页面骨架模式"）
- 每页预分配：标题/H1/meta description/og:title/og:description/og:image

##### 页面骨架模式（结构参考，非视觉模板）

以下为 B2B 外贸站的通用页面结构模式。Agent 在这些骨架基础上**自主设计视觉呈现**，不逐行复制。每种页面类型有不同的说服逻辑：

| 页面类型 | 骨架结构 | 说服逻辑 |
|----------|---------|---------|
| 首页 | Hero→Trust Bar→Capabilities→Stats→Process→CTA | 品类定位1秒→信任信号→能力展示→数据论证→流程→转化 |
| 能力 Hub | Hero→Category Cards Grid→Trust Strip→CTA | 分类导航→快速定位→信任→转化 |
| 能力详情 | Hero→Specs Table→Process Split→Comparison→Related Links→CTA | 技术参数→工艺能力→对比优势→相关能力→转化 |
| 行业 Hub | Hero→Industry Grid→Why Us→CTA | 行业覆盖→差异优势→转化 |
| 行业详情 | Hero→Pain Points→Tech Requirements→Our Solution→Certifications→Cases→CTA | 痛点共鸣→技术要求→方案呈现→证据→案例→转化 |
| 关于/工厂/质量 | Hero→Stats Bar→Content Split→Certification Wall→CTA | 数据先声→内容展开→认证墙→转化 |
| FAQ | Hero→Accordion List→CTA | 问题分组→点击展开→转化 |
| 联系 | Hero→Form+Info Split→Address→CTA | 表单优先→补充信息→转化 |
| How It Works | Hero→Step-by-Step Timeline→FAQ→CTA | 流程可视化→打消顾虑→转化 |
| Design Guides | Hero→Guide Cards Grid→DFM Checklist→CTA | 知识价值→实用工具→转化 |
| 博客列表 | Hero→Article Cards Grid→CTA | 内容索引→阅读引导→转化 |
| Google Ads 落地页 | 10段：Hero→Trust→Split×4→Form→FAQ→Sticky CTA | 每屏一个说服点→表单采集→移动端sticky CTA |

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

**内容标准**：全部按该品类出口最高标准填充。产品参数用技术指标，不写空洞形容词。一个海外采购经理读完任何一页，10秒内能判断「这个工厂能做我的单」。

#### 10. 执行产出

写 `design-tokens.css` → 写 `index.html` → 提取 `blocks/*.html` → 生成 `image-strategy.json` → 生成 `image-brief.html` → 生成 `acceptance-criteria.json`

**design-blueprint.md 字段**：
- CATEGORY — 品类细分 + 视觉意象
- BRAND PERSONALITY — 三轴定位（技术/高端/国际 各轴明确选边）
- DESIGN DIFFERENTIATORS — 差异化决策记录（≥3 项）
- COLOR PALETTE — 完整色彩系统（含差异化理由；标注 ui-ux-pro-max 参考源）
- TYPOGRAPHY — 字体系统（标注 ui-ux-pro-max 推荐组合）
- PAGE COLLECTION — 所有页面列表（必须 ≥5 个页面）
- IMAGE STRATEGY — 图片角色总数 + 每页分布
- BLOCK MANIFEST — 可复用区块
- IMAGE DIRECTION — 图片风格指导
- VISUAL REFERENCES — Pinterest 参考 mood board 链接 + ui-ux-pro-max 调色板名称

**关键原则**：
- 创建**完整多页网站**，不是单页landing page
- 每个页面都有独立内容和完整结构
- 导航链接指向真实页面，不是锚点
- blocks 是参考模板，执行时可调整 DOM 和布局
- 所有文件在主 Agent 的连续上下文中产出，保持设计一致性

### SEO 基础设施（每页强制）

Agent 在 Phase 1 为每个页面配置完整的 SEO 元数据。**不设手工修改——模板生成时自动填入。**

#### 每页 HTML Head 必须包含

```html
<title>{Page Title} | {Brand Name}</title>
<meta name="description" content="{页面独立描述，120-160字符}">
<meta property="og:title" content="{标题}">
<meta property="og:description" content="{描述}">
<meta property="og:image" content="https://{domain}/generated/{page-hero}.webp">
<meta property="og:url" content="https://{domain}/{page-path}/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://{domain}/{page-path}/">
```

#### JSON-LD 结构化数据（按页面类型）

| 页面类型 | JSON-LD 类型 | 位置 |
|----------|-------------|------|
| 首页 | `Organization` + `WebSite` | `<head>` |
| 关于/工厂/质量 | `Organization` | `<head>` |
| 能力/产品页 | `Service` | `<head>` |
| FAQ 页 | `FAQPage` | `<head>` |
| 博客文章 | `Article` | `<head>` |
| 面包屑（全局） | `BreadcrumbList` | `<head>` |

#### 基础设施文件（Phase 1 产出）

**`_headers`**（Cloudflare Pages 安全头）：
```
/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

**`robots.txt`**（允许搜索，阻止AI训练爬虫）：
```
User-agent: *
Allow: /
User-agent: GPTBot
Disallow: /
User-agent: Google-Extended
Disallow: /
User-agent: Bytespider
Disallow: /
Sitemap: https://{domain}/sitemap.xml
```

**`sitemap.xml`**：部署后生成，包含所有页面 `<url>` + `<lastmod>` + `<priority>`

**`llms.txt`**：AI 爬虫索引，列出所有页面 URL + 简短描述

### CSS 反模式黑名单（硬性禁止）

从实战踩坑提炼。Agent 写 CSS 时必须遵守：

| ❌ 禁止 | ✅ 正确做法 | 根因 |
|---------|-----------|------|
| `background: var(--bg)` | `background-color: var(--bg)` | CSS 简写重置 `background-image` 为 `none` |
| `--cta-bg: url(...)` CSS 变量传图 | `<img>` 标签或 `::before { background-image: url(...) }` 内联 | 变量是死代码；删除 `::before` 后卡片背景变成纯色 |
| `direction: rtl` 做图文左右互换 | CSS `order` 属性 | `rtl` 影响整个字方向，移动端不退 |
| 导航 `:hover` 纯 CSS 下拉 | JS `mouseenter`/`mouseleave` + `setTimeout(300ms)` | 无延迟瞬间消失，鼠标无法移入子菜单 |
| CTA 按钮 > 4 词 | 最多 "Get Quote" / "Send Inquiry" / "Request Sample" | 海外采购经理扫描时间1秒 |
| CTA 按钮前置 SVG 图标 | 纯文字按钮 | `#icon-mail` 暗示使用邮件客户端，增加视觉噪音 |
| 方形图 `<img>` 缩放到 < 200px | 换用 SVG 图标或裁切 aspect-ratio | 失去所有细节 |

### CTA 按钮硬规则（强制）

- **主 CTA 文字**：2-3 词（"Get Quote" / "Send Inquiry" / "Request Sample"）
- **副 CTA 文字**：1-2 词（"View Products" / "Learn More"）
- **禁止**：长句、图标前缀、email emoji
- **移动端**：底部 sticky CTA 条（`position:sticky; bottom:0`），确保拇指可达
- **每页 ≥ 1 个 CTA 按钮在首屏可见**（不滚动即可见）
- 按钮对比度 WCAG AA 级

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

### 联系表单标准化

**字段**：name, email, company（可选）, message — 共 3-4 字段

**action 固定**：`https://inquiry-proxy.workers.dev/`（Cloudflare Worker 中转）

**提交方式**：JS `fetch` POST JSON，不用浏览器原生 form submit：

```html
<form id="inquiryForm" class="contact-form">
  <label>Name <input type="text" name="name" required></label>
  <label>Email <input type="email" name="email" required></label>
  <label>Company <input type="text" name="company"></label>
  <label>Message <textarea name="message" required></textarea></label>
  <button type="submit">Send Inquiry</button>
</form>
<script>
document.getElementById('inquiryForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  const res = await fetch('https://inquiry-proxy.workers.dev/', {
    method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data)
  });
  if (res.ok) { /* toast success */ } else { /* toast error */ }
});
</script>
```

**成功/失败提示**：使用 toast 通知，不跳转页面。

---

### Phase 1C：图片 prompt 审阅（只审不生成）

Agent 完成 `image-strategy.json` 后，**不立即全量生图**。先提取 5-8 个关键图片的 prompt，展示给用户审阅方向：

```
🖼️ 图片 prompt 审阅（共 {N} 张，以下是关键图片的方向）：

1. hero-bg（首页 Hero）：
   "{prompt 前 120 字}..."
   方向：{微距/广角/抽象/工作室} — {原因}

2. sub-hero-bg（关于页 Hero）：
   ...

3. product-showcase（能力页展示）：
   ...

4. concept-scene（行业应用场景）：
   ...

5. cta-bg（CTA 背景纹理）：
   ...

6-8. （其余 {N-5} 张的方向概述...）

━━━━━━━━━━━━━━━━━━━━━
请确认：
□ 方向 OK，开始全量生成
□ 某几张需要调整（请指明）
□ 全部重新来
```

**用户确认后**才进入 Phase 2 全量生图。不做沉默批处理。

---

## Phase 2 — 全站生图

### 样图确认（先 3 张，再全量）

全量生成前，**先生成 3 张代表图**（hero + 1 个内页 sub-hero + 1 个 product-showcase），展示给用户确认视觉一致性：

```
python gen-site-images.py --prompts image-strategy.json --out ./generated --limit 3
```

用户确认后，全量生成：

```
python gen-site-images.py --prompts image-strategy.json --out ./generated
```

模型：**GPT Image 2**。质量**硬件级写死 `low`（$0.006/张）**——medium/high 在脚本中 4 层硬阻止（argparse choices → CLI 入口 guard → 逐图 JSON guard → API payload 硬编码），误用即 `sys.exit(1)` 中止。

> **质量说明**：low 和 high 对 B2B 网站图片无肉眼可见区别，差价 35 倍（$0.006 vs $0.211）。所有脚本均内置 quality guard，不需要 Agent 传 `--quality` 参数。

**API 端点**：`api.inferera.com`（已验证稳定可用）。

**文本生图端点**：`https://api.inferera.com/v1/images/generations`
**图生图端点**：`https://api.inferera.com/v1/images/edits`（当 `image-strategy.json` 中指定了 `reference` 字段时自动使用）

**图片尺寸限制**：所有图片 `1024×1024`。
**图生图超时**：300s（大尺寸参考图上传慢，120s 不够）。文本生图超时：90s。

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

### 零图片复用（硬性规则）

**同一图片文件禁止被 ≥2 个不同 `<img>` 标签引用。** 每个 content image 必须是唯一生成的。

- 每个 `image-strategy.json` 中的 `id` 必须唯一
- 每页的 hero / sub-hero / split-section / CTA 背景图全部使用不同文件
- **例外**：cta-bg 角色的纹理背景可在不同页面复用（仅限此角色）
- Phase 5 审计检测：同一文件被 ≥2 个 `<img>` 引用 → **FAIL**
- 踩坑：同一图片文件曾被 6 个页面复用、弹窗图被 5 个页面复用 → 强制重构，零复用规则由此而来

### 生图脚本

**生图脚本**：`gen-site-images.py` 和 `gen-product-shots.py`（位于本技能 `scripts/` 目录）。Agent 部署前通过 `skill_view` 获取脚本源码写入项目根目录。quality 硬写死 `low`，4 层 guard 阻止 medium/high，超时 300s（图生图）/ 90s（文本生图）。

```bash
# 全量生成（自动检测 reference 字段，切换 text-to-image / image-to-image）
python gen-site-images.py --prompts image-strategy.json --out ./generated

# 追加图片（Phase 4 迭代补图）
python gen-site-images.py --prompts supplement.json --out ./generated --manifest image-manifest.json
```

> ⛔ quality 硬件级锁死在 `low`（$0.006/张）。argparse `choices=['low']` → CLI guard `sys.exit(1)` → JSON payload 硬编码。不暴露 `--quality` 参数。
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

独立脚本（位于本技能 `scripts/` 目录），用于「提供产品图 → 自动生成不同角度/场景/光线」：

```bash
# 快速模式：用预设模板
python gen-product-shots.py --reference ./product.webp \
    --angles front,45deg,side --scenes studio,office --out ./shots

# 完整配置模式
python gen-product-shots.py --config product-shots.json --out ./shots
```

**预设角度**：front, 45deg, side, back, topdown, macro
**预设场景**：studio, office, hotel, retail, industrial, outdoor
**预设光线**：daylight, softbox, rim, ambient

> Agent 通过 `skill_view(name='建站工作流', file_path='scripts/gen-product-shots.py')` 获取脚本源码，写入项目根目录后执行。quality 已硬写死 `low`。

---

## Phase 3 — 逐页编码

### 先做 3 页展示，再全量

**首轮**：生成首页 + 1 个能力详情页 + 1 个行业页（3 页覆盖主要页面类型）

Agent 展示这 3 页的视觉一致性：
- 导航/Footer 是否统一？
- 色彩/字体/图片风格是否匹配？
- CTA 按钮位置和样式是否一致？

**用户确认后**，继续完成所有剩余页面。

主 Agent 逐页编码（基于 page-tree.json）：
1. Read image-strategy.json → 了解每页每 section 的图片分配
2. Read 所需的 blocks 和 design-tokens.css
3. Write 完整 HTML 文件，按策略嵌入对应图片

### 页面路由：目录路由（零重定向）

```
/about/index.html
/capabilities/index.html
/capabilities/{subcategory}/index.html
/industries/index.html
/contact/index.html
/blog/index.html
/factory/index.html
/quality/index.html
/shipping/index.html
/faq/index.html
/how-it-works/index.html
/design-guides/index.html
/privacy/index.html
/terms/index.html
/welcome/index.html
```

Cloudflare Pages 原生支持 `/about` → `/about/index.html`，无需 `_redirects`。

### 页面规划原则

- 基于 `page-tree.json` 创建所有页面，不遗漏
- 每个页面都有完整的 HTML 结构、独立 `<title>`、独立 `<meta description>`
- 导航链接指向真实页面，不是锚点
- 每页按 Phase 1 的 B2B 内容架构填充业务内容
- 图片按 image-strategy.json 的角色分配嵌入对应 section
- 每页嵌入 JSON-LD 结构化数据（按页面类型）

### 404 页面模板（强制）

```html
<!-- /404.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Not Found | {Brand Name}</title>
  <link rel="stylesheet" href="/design-tokens.css">
</head>
<body style="display:flex;align-items:center;justify-content:center;min-height:100vh;text-align:center">
  <main>
    <h1 style="font-size:6rem;font-weight:100;color:var(--accent)">404</h1>
    <p style="color:var(--text-secondary);margin:var(--space-md) 0">Page not found. The link may be broken or the page has been moved.</p>
    <a href="/" class="btn btn-primary">Back to Home</a>
  </main>
</body>
</html>
```

- 简洁居中，品牌色调，不需要图片

### Google Ads 落地页模板（`/welcome/`）

独立营销着陆页，用于 Google Ads 投放：

- `<meta name="robots" content="noindex, nofollow">` — 避免 SEO 重复内容惩罚
- **无 header/footer** — 不分散注意力，无导航跳出
- CSS 内嵌，**不依赖 design-tokens.css**（独立页面，css 变更不影响）
- 10 区段结构：Hero→Trust Bar→Capabilities→Quality Split→Product Split→Testing Split→Process→Testimonials→Form→FAQ→Final CTA
- **移动端 sticky CTA 条**（`position:sticky; bottom:0`）——手机用户拇指可达
- 表单提交到 `https://inquiry-proxy.workers.dev/`（与主站共用端点）
- 表单字段：name, email, company, message（添加 `source: "google-ads"` 隐藏字段追踪来源）

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
8. 联系表单仅 name/email/company/message（3-4字段）
9. 每页独立 `<title>` + `<meta description>` + `og:*` + `canonical`
10. CTA 按钮文字 ≤ 4 词，无前置图标
11. 每页首屏可见 CTA（不滚动即可见）
12. FAQ 页 items 可点击展开/折叠
13. 所有表格正确渲染（不是空白行）
14. 移动端 sticky CTA 条可见

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
7. 联系表单仅含 name/email/company/message（3-4字段）
8. 导航链接可点击、无死链
9. 每页 title/description/OG 唯一不重复

=== SEO 检查 ===
10. 每页有独立 `<title>` + `<meta description>`
11. 每页有完整 `og:title`, `og:description`, `og:image`, `og:url`
12. 每页有 `<link rel="canonical">`
13. 首页有 `Organization` JSON-LD
14. FAQ 页有 `FAQPage` JSON-LD（如有）
15. robots.txt 存在且阻止 AI 爬虫（GPTBot/Google-Extended/Bytespider）
16. sitemap.xml 存在且包含所有页面

=== 安全与规章检查 ===
17. `_headers` 文件存在：HSTS + X-Frame-Options + X-Content-Type + Referrer-Policy
18. 404.html 存在并返回正确内容
19. privacy/index.html 和 terms/index.html 存在

=== 图片去重检查 ===
20. 同一 generated/*.webp 文件不被 ≥2 个不同 `<img>` 引用（cta-bg 角色除外）
21. 所有 `<img src>` 指向本地 generated/*.webp（非外部 URL）

=== 买家视角检查 ===
22. 首页：10秒内能否判断工厂品类+核心能力？
23. 产品页：技术参数是否具体（有数字，非空洞形容词）？
24. 关于页：认证/产能/QC流程是否可见？
25. 全站：CTA 按钮是否在每个页面都可见可达？
26. 全站：信任信号（认证/产能数据/工艺描述）是否充分？
27. 全站：图片是否承担了视觉传达角色（非纯装饰）？
28. 全站：CTA 按钮文字 ≤ 4 词，无图标前缀

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

---

## Phase 7 — 部署后线上验证

Phase 6 部署完成后，Agent 在线上做最终审计：

```bash
# 1. 逐页 HTTP 200 检查（从 page-tree.json 遍历所有页面路径）
for page in $(cat page-tree.json | python3 -c "import sys,json;[print(p['path']) for p in json.load(sys.stdin)['pages']]"); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://<project>.pages.dev/${page}")
  echo "${code} ${page}"
done

# 2. 验证安全头
curl -sI "https://<project>.pages.dev/" | grep -i "strict-transport-security\|x-frame-options\|x-content-type"

# 3. 验证 robots.txt 和 sitemap.xml 可访问
curl -s "https://<project>.pages.dev/robots.txt" | head -5
curl -s "https://<project>.pages.dev/sitemap.xml" | head -5

# 4. 验证 404 页面返回 404 状态
curl -s -o /dev/null -w "%{http_code}" "https://<project>.pages.dev/nonexistent-page-xyz"
```

**输出 `deploy-report.md`**：
- 部署 URL（pages.dev + 自定义域名）
- 页面总数 / 图片总数
- HTTP 状态检查结果（全绿 / 有失败）
- 安全头测试通过项
- 已知问题 / 待办事项
- Google Search Console URL 提交状态（如已配置）

## 硬约束（12 条）

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
| 10 | **完整多页网站：≥30个页面（核心14页+能力子页+行业页），导航指向真实页面。404/隐私/条款必须存在。** |
| 11 | **零图片复用：同一 generated/*.webp 不被 ≥2 个不同 `<img>` 引用（cta-bg 角色除外）** |
| 12 | **质量 LOCKED LOW：gen-site-images.py & gen-product-shots.py quality 写死 low，4层硬阻止 medium/high，误用即 exit(1)** |

---

## 品牌命名与版权规范

- **禁止 `{brand}` 占位符残留** — 每页 title/og/copyright/JSON-LD 必须使用真实品牌名
- **版权区格式强制**：`© 2026 {Brand Name} — {City}, {Country}`（根据厂商实际所在地填写）
- **语言**：全站英文（国际 B2B 通路），除非厂商要求中英双语
- **品牌名 + 品类名**同时出现在 title 中，例：`{Brand Name} | Professional {Category}`（具体格式由 Agent 根据品类决定）

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

经过多个实战站点验证，**居中 Hero 布局是 B2B 制造出口站最稳妥的默认选择**：

```css
.hero{
  position:relative;
  min-height:100vh;
  display:flex;align-items:center;  /* 垂直居中，非 flex-end */
  padding:var(--space-5xl) 0;
  background:var(--bg-hero-fallback, #0a0f1a);  /* 兜底色在 design-tokens.css 中定义，与品牌色调匹配 */
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
  background:var(--accent-alpha, rgba(200,150,62,0.25));  /* 品牌色半透明，颜色来自 design-tokens.css */
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
| Phase 2 | 生图失败 | 切换 `api.inferera.com` 回退 |
| Phase 2 | edits 端点 400 | 检查 `images` 是否为对象数组 `[{"image_url":"data:..."}]`，非纯字符串或 `{url:...}` |
| Phase 2 | 参考图片下载失败 | 检查 `reference` URL 可访问性；本地路径是否相对于 `meta.referenceBaseUrl` 正确；回退到纯文本生图 |
| Phase 2 | 图生图图片过大(>5MB) | 脚本会警告，建议先压缩参考图到 1024x1024 以内 |
| Phase 2 | gen-site-images.py 不在磁盘 | Agent 通过 `skill_view` 获取脚本写入项目根目录 |
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
