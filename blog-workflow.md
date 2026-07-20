---
name: blog-workflow
version: "6.1"
description: B2B SEO 博客自动化。一句话→自动选题→深度内容(最高标准)→GPT Image 2全篇配图(5-8张/篇)→10秒读者测试+WAF兼容检查。电子制造出口专用。
upstream: https://github.com/cpu152650311-coder/website-workflow
---

# B2B SEO 博客自动化 v6.1

> **v6.1**：WAF 兼容性检查、生图 API 双格式容错（URL/Base64自动检测+超时重试）、部署后 CDN 缓存处理。
> **v6.0**：一句话选题展开(深圳电子制造最高标准)。全篇配图策略(5-8张/篇)。10秒读者测试+内容迭代。
> **v5.5**：封面+内容图双图策略
> **v5.4**：前置检查博客框架
> **v5.3**：Agent-only驱动, 意图导向SEO, 零硬编码模型

## 核心理念

```
用户: "给这个PCB站写博客"
         |
    +----+-----------------+
    |                      |
    v                      v
  读建站蓝图              自动填充内容
  (content-blueprint)     (深圳最高标准)
    |                      |
    +----------+-----------+
               |
    +----------+-----------+----------+----------+
    v          v           v          v          v
  选题展开   封面图    技术原理图   场景图    数据可视化
  (自动)   (1张)    (2-3张)     (1张)    (1-2张)
    |          |           |          |          |
    +----------+-----------+----------+----------+
               |
               v
          10秒读者测试
               |
               v
           部署+CTA
```

**核心原则**：
- SEO 是「意图导向」而非「词句导向」
- GPT Image 2 极便宜（$0.006/张），每篇文章大胆配图 5-8 张
- 内容按深圳电子制造最高标准自动填充（与建站工作流 Phase 0 一致）
- 纯 Agent 驱动，不指定模型，不固定格式

---

## Phase 0：了解站点 + 前置检查

Agent 进入站点项目目录，读取：

| 文件 | 用途 |
|------|------|
| `content-blueprint.md` | 产品参数/认证/产能/交期 — 博客内容的真实素材来源 |
| `design-blueprint.md` | 品类+品牌人格+色彩 — 决定配图风格 |
| `image-strategy.json` | 站点图片角色和风格 — 博客配图保持一致 |
| `design-tokens.css` | 品牌色/背景色/强调色 — 配图 prompt 的颜色约束 |
| 首页 | 品牌、行业、语气 |
| 导航结构 | 内链目标页面 |
| 已有博客 | 避免选题重复 |
| `wrangler.toml` | 部署配置 |

**前置检查**：
- 检查 `/blog/index.html` 是否存在
- **如果不存在** → 停止并告知用户：「站点无博客框架，请先运行建站工作流生成 `/blog/index.html`」

---

## Phase 1：一句话选题展开

### 自动选题生成

Agent 读 Phase 0 的站点数据，自动生成 1-2 篇选题。**不依赖用户给关键词**。

**选题来源（按优先级）**：

| 优先级 | 来源 | 示例（PCB站点） |
|:--:|------|------|
| 1 | 产品技术深度文 | "HDI任意层互连 vs 传统通孔：什么时候该升级" |
| 2 | 工艺/材料对比 | "沉金 vs OSP vs 沉银：不同应用选什么表面处理" |
| 3 | 行业应用方案 | "汽车电子PCB的5个可靠性要求" |
| 4 | 采购决策指南 | "中国PCB供应商评估清单：海外采购经理的10个检查点" |
| 5 | 热点关联（web_search辅助） | 新能源汽车对PCB的需求变化 |

**内容标准**：全部按深圳电子制造最高标准填充具体数据（与建站工作流 Phase 0 同源）。技术参数用数字，不写空洞形容词。

**选题约束**：
- 每篇选题必须基于站点的**实际品类和能力**（从 content-blueprint.md 提取）
- 不做泛行业通稿——PCB站不写"什么是PCB"，LED站不写"LED基础知识"
- 每篇选题回答一个**海外采购经理会搜索的实际问题**

**风格指令**：从风格池随机抽（≥5 个备选）。连续 3 次同一种 → 第 4 次强制排除。

---

## Phase 2：生成内容

Agent 用自己当前的模型直接生成博客。内容深度对标建站工作流 Phase 0 的自动填充标准。

### 内容约束

| 必须 | 禁止 |
|------|------|
| 具体技术数据（层数/线宽/材料/认证/交期） | 空洞形容词（"高质量""有竞争力"） |
| 内链到 2-3 个站点页面 | CDN 资源 / 框架标签 |
| 自然匹配搜索意图 | 关键词堆砌 / AI 机械腔调 |
| 每个 H2 的问题正文给出答案 | 泛行业通稿（"电子制造行业前景广阔"） |
| H2 用英文（B2B 出口买家搜英文） | 图片数/字数/段落数硬性规定 |

### 内容结构灵活性

Agent 自主决定文章结构。常见的有效结构：
- **技术深挖型**：问题→原理→对比→结论
- **采购指南型**：需求→评估维度→检查清单→推荐
- **应用方案型**：行业背景→技术挑战→解决方案→案例
- **工艺对比型**：场景→方案A vs 方案B→选型建议

**不强制任何结构。** Agent 根据选题类型选择最合适的。

---

## Phase 3：全篇配图

GPT Image 2 极便宜（$0.006/张），**每篇文章充分利用**，配图 5-8 张。质量写死 `low`，无参数暴露。使用独立脚本 `skills/ai-image-gen/scripts/gen-image.py`。

### 图片角色

| 角色 | 数量 | 用途 | Prompt 策略 |
|------|:--:|------|------|
| **cover** | 1 | 列表缩略图 + 文章 header 背景 | 文章主题氛围，匹配站点配色 |
| **hero-bg** | 1 | 文章顶部大图(sub-hero) | 与 cover 不同角度，留文字空间 |
| **technical-diagram** | 1-2 | 技术原理/结构示意 | 截面/对比/原理，从文章具体段落提取 |
| **process-illustration** | 0-1 | 工艺流程/步骤 | 步骤可视化 |
| **concept-scene** | 0-1 | 应用场景 | 产品在终端设备中的效果 |
| **data-viz** | 0-1 | 数据/对比可视化 | 表格数据转图形对比 |
| **cta-bg** | 1 | 文章底部 CTA 卡片背景 | 品牌氛围，不抢按钮 |
| **section-divider** | 0-1 | 长文分区装饰 | 低对比度抽象纹理 |

**总量：每篇 5-8 张，成本 $0.03-0.05。**

### Prompt 规则

- 所有 prompt 包含 `no people faces, no text, no logos`
- 封面和场景图匹配站点配色（从 design-tokens.css 提取品牌色）
- 技术图 prompt 从文章具体段落内容提取——「把这段文字描述的 XX 做成信息图」，不是通用描述
- 风格与建站工作流 image-strategy.json 保持一致

### API 调用与容错

生图 API 可能返回两种格式（URL 或 Base64），调用可能超时。代码必须同时处理：

```python
# 使用独立生图脚本 skills/ai-image-gen/scripts/gen-image.py
# quality 已写死 low，不暴露参数，无需手动指定
from openai import OpenAI
import base64, time, os

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

def generate_with_retry(prompt, max_retries=2, retry_delay=3):
    """生成图片，自动检测 URL/Base64 格式，支持重试。quality=low 写死。"""
    for attempt in range(max_retries + 1):
        try:
            resp = client.images.generate(
                model="gpt-image-2", prompt=prompt,
                n=1, size="1024x1024", quality="low"
            )
            data = resp.data[0]
            # 自动检测格式：优先 URL，回退 Base64
            if data.url:
                return {'format': 'url', 'data': data.url}
            elif data.b64_json:
                return {'format': 'b64_json', 'data': base64.b64decode(data.b64_json)}
            else:
                raise ValueError("Response has neither URL nor b64_json")
        except Exception as e:
            if attempt < max_retries:
                time.sleep(retry_delay)
                continue
            return None  # 所有重试失败，返回 None 触发降级

# 生成全部图片
for img in article_images:
    result = generate_with_retry(img["prompt"])
    if result:
        save_image(result, img["filename"])
    else:
        # 降级：跳过该图片，不阻塞部署
        print(f"SKIP: {img['id']} — API unavailable after retries, continuing without it")
```

**容错规则**：
- 最多重试 2 次，每次间隔 3 秒
- 同时处理 `url` 和 `b64_json` 两种响应格式（不做假设）
- API key 缺失或所有重试失败 → 跳过该图片，继续部署
- 跳过图片时在日志中标注，不静默丢失

> **踩坑经验**：生图 API 有时返回 URL 有时返回 Base64，客户端不能假设格式。超时是常见现象（网络波动或 API 负载），重试 1-2 次大概率成功。另外 `AIHUBMIX_API_KEY` 需确保 `.env` 中已配置（建站工作流会自动创建 `.env`，博客工作流复用它）。

### 方形图片在博客中的展示规则

1024×1024 图片在博客文章中的嵌入方式：

| 展示方式 | CSS 要点 |
|---------|---------|
| 文章 header 全幅 | `object-fit:cover; max-height:50vh` |
| 大尺寸内联(技术图) | 宽度 70-90%，居中，`border-radius:var(--radius-lg)` |
| 文字环绕(小场景图) | 宽度 40-50%，`float` 或 grid 侧放 |
| 全幅穿插(流程/数据图) | 宽度 100%，上下留白 |
| 卡片缩略(封面) | `aspect-ratio:4/3` + `object-fit:cover`（裁切上下） |
| 背景纹理(CTA区域) | `::before{opacity:.25-.35}` |
| 两张对比并排 | grid `1fr 1fr`，各 `aspect-ratio:1/1` |

**禁止**：图宽 < 200px、用作 icon、嵌入文字行内。

---

## Phase 4：10 秒读者测试 + WAF 兼容性检查

部署前逐篇执行，模拟**海外采购经理**视角：

```
1. 标题告诉了我什么？（2秒）—— 是否具体、是否有搜索价值
2. 这篇文章的核心洞察是什么？（3秒）—— 是否有我带走的知识点
3. 有具体数据和数字吗？（2秒）—— 还是空洞形容词
4. 图片传达了有用信息吗？（2秒）—— 还是纯装饰
5. 下一步是什么？（1秒）—— CTA 是否可见、内容是否引导行动
```

**PASS 标准**：5 个问题全部能找到答案。答案必须可见，不需要推理。

**FAIL 处理**：
- 缺数据 → 回 Phase 2 补具体技术数据
- 缺图 → 回 Phase 3 补对应角色的图片
- 标题弱 → 回 Phase 1 重新选题

### WAF 兼容性检查

CDN/WAF（如 Cloudflare）的安全规则可能将博客文章误判为恶意内容。部署前逐篇检查：

| 检查项 | 风险 | 处理 |
|--------|------|------|
| HTML 标签密度 | 连续 `<strong>`、`<p>`、`<li>` 嵌套过深可能触发 "HTML injection" 规则 | 稀释标签密度：插入图片、代码块、引用块打断纯标签序列 |
| 敏感字符串 | 文章中出现 `html`、`injection`、`script`、`spam`、`block` 等词可能触发关键词匹配 | 用自然语言改写，避免连续堆叠这些词；如无法避免，使用同义词替代 |
| 表单/链接密度 | 文章内过多 `<form>` 或外部链接被误判为 spam | 内链优先指向本站页面，外链 ≤3 个 |
| 特殊字符序列 | `<>` `{}` `[]` 等连续出现被误判为代码注入 | 技术文章中的代码块用 `<pre><code>` 包裹，不要裸写在 `<p>` 中 |

**检查方法**：部署后如果博客页面返回 WAF 拦截页面（而非 404/500），说明被安全规则误判。处理方法：
- Cloudflare：将安全级别从 "Medium" 降为 "Low"，或在 WAF 中为该路由添加 Skip 规则
- 或删除触发拦截的遗留 WAF 规则（旧规则常处于维护模式但仍然生效）

> **踩坑经验**：技术博客天然包含大量 HTML 标签和代码术语，容易触发 WAF 的 "Block spam pattern html injection" 类规则。表现是页面显示 "Sorry, you have been blocked" 而非正常内容。根因通常是旧的遗留 WAF 规则，删除或跳过即可。

---

## Phase 5：更新列表 + 部署

1. 更新 `/blog/index.html` 的文章列表
2. 每篇文章底部嵌入站点 CTA 卡片（复用站点 HTML）
3. `git commit` + `git push`
4. `wrangler pages deploy` 或 vercel deploy

### 部署后缓存处理

部署后 CSS/JS 可能被 CDN 缓存为旧版本，导致新样式不生效。

- **版本号策略**：如果博客页面引用了站点级 CSS（如 `../design-tokens.css`），确保 CSS 链接带版本参数（建站工作流会自动管理）
- **部署后验证**：打开新发布的博客页面，检查关键样式是否正确加载；如果样式异常，检查浏览器 DevTools 中 CSS 文件是否为最新版本
- **Purge Cache**：如确认 CDN 缓存了旧文件，调用 Cloudflare purge cache API 或通过 Dashboard 手动清除

> **详细流程**：CDN 缓存破坏的完整策略在建站工作流 Phase 6 中定义。博客工作流新增文章时，如果只改 HTML 不改 CSS，通常不需要额外处理缓存。但如果同时修改了站点 CSS，必须与建站工作流配合处理缓存。

---

## SEO 自检清单

```
P0（部署前实际抓取 <head> 验证）：
  [ ] <title> == 本文标题（≠ 首页标题）
  [ ] og:title/description/image/url/type 全部指向本文
  [ ] canonical 指向本文 URL
  [ ] JSON-LD BlogPosting
  [ ] 无死链

内容深度检查：
  [ ] 文章包含 ≥3 个具体技术数据点（数字，非形容词）
  [ ] 文章回答了一个采购经理会搜索的实际问题
  [ ] 每个 H2 的问题，正文都给出了回答

配图检查：
  [ ] 每篇文章配图 ≥5 张
  [ ] 封面图存在且匹配站点配色（不同文章不同封面，不共用）
  [ ] 技术图从文章具体段落提取（非通用图）

禁止项：
  X CDN 资源 / 框架标签 / 空洞形容词
  X 关键词堆砌 / AI 机械腔调
  X 泛行业通稿
  X 无具体数据的"高质量""有竞争力"
```

---

## 陷阱清单

1. **数据直接嵌入，不靠 JSON 引用** — 模型忽略间接引用
2. **不拆分策划和生成** — Agent 在一个上下文中一步到位
3. **不固定输出格式** — 先读站点格式再决定
4. **图片不阻塞部署** — API key 缺失或超时重试耗尽时跳过
5. **内容质量靠数据，不靠多模型** — 无数据 3/10，有数据 8+/10
6. **不定死数字** — 避免批量 AI 内容指纹
7. **随机风格必须真随机** — 连续 3 次同一种强制排除
8. **选题必须基于站点实际品类** — 不做泛行业通稿
9. **配图必须从文章具体段落提取 prompt** — 不做通用配图
10. **批量替换注意特殊字符** — `@`、`$` 等字符在 Perl/sed 替换中可能被转义或变量插值。优先用 `sed` 字面量模式，修改后立即 `grep` 验证关键字段（如邮箱地址）完整性
11. **生图 API 不假设返回格式** — 同时处理 `url` 和 `b64_json`，不假定只有一种

---

## 上游依赖

- 建站工作流（website-workflow）→ content-blueprint.md + design-blueprint.md + image-strategy.json
- 仓库: https://github.com/cpu152650311-coder/website-workflow
