#!/usr/bin/env python3
"""
wechat-reader: 微信公众号文章抓取脚本
用法: python3 fetch_article.py <URL> [--output-format markdown|json]
"""

import sys
import re
import json
import argparse
import httpx
from markdownify import markdownify

# 上游代理（沙箱环境）
PROXY = "http://YOUR_PROXY_HERE:3128"

# 微信移动端 UA（必须用移动端 UA，否则返回内容不同）
WEIXIN_UA = (
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 "
    "MicroMessenger/8.0.42.2440(0x28002A37) NetType/WIFI Language/zh_CN"
)

HEADERS = {
    "User-Agent": WEIXIN_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://mp.weixin.qq.com/",
}


def fetch(url: str) -> dict:
    """抓取微信公众号文章，返回结构化结果"""
    transport = httpx.HTTPTransport(proxy=PROXY)
    with httpx.Client(transport=transport, headers=HEADERS, timeout=20, follow_redirects=True) as client:
        resp = client.get(url)

    if resp.status_code != 200:
        return {"success": False, "error": f"HTTP {resp.status_code}"}

    html = resp.text

    # 人机验证检测
    if "请在微信客户端打开链接" in html or "环境异常" in html:
        return {"success": False, "error": "触发人机验证，无法在沙箱读取"}

    # 提取标题
    title_match = re.search(r'id="activity-name"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not title_match:
        # 备用：从 <title> 提取
        title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else "未知标题"

    # 提取作者
    author_match = re.search(r'id="js_name"[^>]*>(.*?)</a>', html, re.DOTALL)
    author = re.sub(r'<[^>]+>', '', author_match.group(1)).strip() if author_match else ""

    # 提取发布时间
    pub_time_match = re.search(r'id="publish_time"[^>]*>(.*?)</em>', html, re.DOTALL)
    pub_time = pub_time_match.group(1).strip() if pub_time_match else ""

    # 提取正文（#js_content）
    content_match = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*(?:<!--|<div|$)', html, re.DOTALL)
    if not content_match:
        # 宽松匹配
        content_match = re.search(r'id="js_content"[^>]*>(.*)', html, re.DOTALL)

    if not content_match:
        return {"success": False, "error": "未找到文章正文（#js_content），可能是付费/限阅内容"}

    raw_content = content_match.group(1)
    # 转 Markdown，清理多余空行
    md_content = re.sub(r'\n{3,}', '\n\n', markdownify(raw_content, heading_style="ATX").strip())

    return {
        "success": True,
        "title": title,
        "author": author,
        "pub_time": pub_time,
        "url": url,
        "content": md_content,
        "char_count": len(md_content),
    }


def main():
    parser = argparse.ArgumentParser(description="微信公众号文章抓取")
    parser.add_argument("url", help="微信文章 URL（mp.weixin.qq.com/s/...）")
    parser.add_argument("--output-format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    if "mp.weixin.qq.com" not in args.url:
        print("❌ 仅支持 mp.weixin.qq.com 域名的文章链接", file=sys.stderr)
        sys.exit(1)

    result = fetch(args.url)

    if not result["success"]:
        print(f"❌ 抓取失败: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Markdown 格式输出
        lines = [
            f"# {result['title']}",
            "",
        ]
        if result["author"]:
            lines.append(f"**来源**：{result['author']}")
        if result["pub_time"]:
            lines.append(f"**发布时间**：{result['pub_time']}")
        lines.extend(["", "---", "", result["content"]])
        print("\n".join(lines))


if __name__ == "__main__":
    main()
