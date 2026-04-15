# wechat-reader 技术说明

## 为什么这个方案能工作

微信公众号文章页面是服务端渲染（SSR），HTML 里包含完整正文。不需要 JavaScript 执行，只需要：
1. 正确的 UA（移动端微信）
2. 能到达微信服务器的网络路径（上游代理）

### 关键 DOM 结构

```html
<h1 class="rich_media_title" id="activity-name">标题</h1>
<a id="js_name">公众号名称</a>
<em id="publish_time">2024-01-01</em>
<div id="js_content">正文 HTML...</div>
```

### 请求参数

| 参数 | 值 | 说明 |
|---|---|---|
| User-Agent | MicroMessenger/8.0.42.2440 | 微信移动端 UA，绕过桌面端内容差异 |
| Proxy | YOUR_PROXY_HERE:3128 | 上游代理（根据环境配置） |
| Referer | mp.weixin.qq.com | 防盗链 Referer |
| Timeout | 20s | 微信服务器偶尔慢 |

## 已测试的成功场景

- 普通公众号文章（图文混排）✅
- 含代码块的技术文章 ✅
- 长文（9000+ 字符）✅

## 已知失败场景

| 场景 | 表现 | 根因 |
|---|---|---|
| 付费文章 | 未找到 #js_content | 正文被付费墙隐藏 |
| 仅粉丝可见 | 未找到 #js_content | 同上 |
| 高频请求触发验证 | "环境异常" / "请在微信客户端打开" | IP 被限频 |
| 已删除文章 | HTTP 404 或空内容 | 文章下架 |

## 为什么放弃其他方案

| 方案 | 失败原因 |
|---|---|
| Jina reader | 返回空/Parameter error，微信被 Jina 反爬 |
| camoufox | 需要 libgtk-3，沙箱无 sudo 权限 |
| requests 直连 | 沙箱出口 IP 被微信封锁 |
| playwright | 同 camoufox，依赖 GTK |

## 图片处理说明

微信图片使用防盗链（检查 Referer），markdownify 提取后图片 src 无法直接访问。
当前输出为空 `![]()` 占位，是已知限制。
如需图片，建议用户自行在微信客户端保存。
