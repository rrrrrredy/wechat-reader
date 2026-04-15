# wechat-reader

Read WeChat Official Account articles and convert to Markdown — no login required.

> OpenClaw Skill — works with [OpenClaw](https://github.com/openclaw/openclaw) AI agents

## What It Does

Takes any `mp.weixin.qq.com` article URL and extracts the full content as structured Markdown, including title, author, publish date, and body text. Uses `httpx` with mobile WeChat User-Agent and upstream proxy to fetch article HTML (server-side rendered, no browser needed), then converts to Markdown with `markdownify`.

## Quick Start

```bash
# Install via ClawHub (recommended)
openclaw skill install wechat-reader

# Or clone this repo
git clone https://github.com/rrrrrredy/wechat-reader.git ~/.openclaw/skills/wechat-reader

# Install dependencies
bash scripts/setup.sh
```

## Features

- **Full article extraction**: Title, author, publish date, and body text
- **Markdown output**: Clean, structured Markdown with proper headings and formatting
- **No browser needed**: Uses `httpx` HTTP client directly — WeChat articles are server-side rendered, no JavaScript execution required
- **Proxy support**: Built-in upstream proxy configuration for network access
- **No login required**: Works with public articles without authentication
- **Error resilience**: Timeout handling and fallback selectors
- **Image limitation**: Images are output as empty `![]()` placeholders — WeChat CDN uses anti-hotlinking, image URLs cannot be directly downloaded

## Usage

**触发词：**
- `读这篇公众号`、`公众号文章`、`微信文章`
- `微信公众号链接`、`mp.weixin.qq.com`
- `读取公众号内容`、`公众号全文`

**Example:**
```
"帮我读一下这篇公众号文章：https://mp.weixin.qq.com/s/xxxxx"
```

**不适用：** 需要登录/付费/限阅的内容；非微信公众号链接（用 web-access 处理其他网页）。

## Project Structure

```
wechat-reader/
├── SKILL.md                  # Main skill definition
├── scripts/
│   ├── setup.sh              # Dependency installer
│   └── fetch_article.py      # Article fetcher & converter
├── references/
│   └── technical-notes.md    # Implementation notes
└── .gitignore
```

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) agent runtime
- Python 3.8+
- `httpx` (HTTP client with proxy support)
- `markdownify` (HTML to Markdown)
- HTTP upstream proxy for WeChat server access (direct IP blocked)

## License

[MIT](LICENSE)
