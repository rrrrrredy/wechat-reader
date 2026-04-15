---
name: wechat-reader
version: 1.0.0
description: "读取微信公众号文章全文并转为 Markdown。输入任意 mp.weixin.qq.com 链接，自动抓取标题、作者、发布时间和正文。触发词：读这篇公众号、公众号文章、微信文章、微信公众号链接、mp.weixin.qq.com、读取公众号内容、公众号全文。不适用：需要登录/付费/限阅的内容；非微信公众号链接（用 web-access 处理其他网页）。"
tags: [wechat, 公众号, article, markdown, reader]
---

# wechat-reader v1.0.0

## 首次使用

首次使用前请运行依赖检测脚本：
```bash
bash scripts/setup.sh
```
> Agent 会在首次触发时自动执行此脚本，通常无需手动操作。

读取微信公众号文章全文，输出结构化 Markdown。

---

## 快速使用

**输入**：任意 `mp.weixin.qq.com/s/...` 链接  
**输出**：标题 + 作者 + 发布时间 + 正文（Markdown）

**执行命令**：
```bash
python3 $CLAUDE_SKILL_DIR/scripts/fetch_article.py "<URL>"
```

**JSON 格式输出**（适合程序处理）：
```bash
python3 $CLAUDE_SKILL_DIR/scripts/fetch_article.py "<URL>" --output-format json
```

---

## 工作流

```
Step 1: 确认 URL 是 mp.weixin.qq.com 域名
  → 非该域名：告知用户改用 web-access skill

Step 2: 执行抓取
  → python3 $CLAUDE_SKILL_DIR/scripts/fetch_article.py "<URL>"

Step 3: 检查结果
  → ✅ 成功：直接输出 Markdown 内容给用户
  → ❌ 人机验证：告知用户"该文章触发了微信人机验证，建议用手机直接打开"
  → ❌ 未找到正文：告知用户"可能是付费/限阅文章，无法抓取"
  → ❌ 其他错误：见 Gotchas
```

---

## Gotchas

⚠️ **Jina reader 对微信完全无效** — `r.jina.ai/mp.weixin.qq.com/...` 返回空或 Parameter error，不要尝试  
⚠️ **camoufox 在沙箱不可用** — 缺 libgtk-3，需要 sudo 安装，当前沙箱无权限  
⚠️ **必须用移动端微信 UA** — 桌面 UA 会被微信识别并返回不同页面结构，导致解析失败  
⚠️ **必须走上游代理** — 沙箱直连被微信服务器拒绝；代理地址：`YOUR_PROXY:3128`（根据部署环境配置）  
⚠️ **付费/限阅/仅粉丝可见内容无法抓取** — 返回"未找到正文"，是预期行为，非 bug  
⚠️ **图片不会下载** — Markdown 中图片是空 `![]()` 占位，这是预期行为（微信图片有防盗链）  

---

## Hard Stop

同一 URL 抓取失败超过 **2 次**：立即停止，不再尝试。  
输出：失败原因 + 建议用户在手机微信直接打开。  
**禁止**：尝试其他代理、修改 UA、循环重试。

---

## 环境要求

| 依赖 | 说明 |
|---|---|
| `httpx` | Python HTTP 客户端，通常已安装 |
| `markdownify` | HTML→Markdown，通常已安装 |
| 上游代理 | 根据部署环境配置代理地址 |

检查依赖：
```bash
python3 -c "import httpx, markdownify; print('依赖正常')"
```

---

## 参考

- 详细技术说明：`$CLAUDE_SKILL_DIR/references/technical-notes.md`
- 沙箱代理配置：`TOOLS.md`（微信公众号章节）

---

## Changelog

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.0.0 | 2026-04-09 | 初版：httpx + 微信 UA + 上游代理，经真实 URL 验证 |
