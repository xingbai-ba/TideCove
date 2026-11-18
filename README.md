# TideCove × TideGleam

**一个只属于你自己的 AI 私聊。**

手机上一对一聊天，数据全在你电脑上，不经过任何第三方 IM。

---

## 两个东西

| | 是什么 | 在哪 |
|---|---|---|
| **TideGleam** | 电脑端的服务端，接 AI、管会话、存数据 | `TideGleam.exe`（Windows，双击即用） |
| **TideCove** | 手机端的聊天窗口 | `TideCove.apk`（Android 7.0+） |

一句话：**TideGleam 是大脑，TideCove 是嘴和耳朵。**

---

## 下载

去 [Releases](../../releases) 拿最新版：

- `TideGleam.exe` —— 电脑端服务（约 90 MB，自带 Node 运行时，**不用装任何依赖**）
- `TideCove.apk` —— 手机端（51 KB）
- `使用说明.txt` —— 三步上手

---

## 三步就能用

1. 电脑上双击 **启动.bat**（或直接跑 `TideGleam.exe`）
2. 几秒后会自动弹出配对页面，上面有**服务器地址**和**配对码**
3. 手机装 `TideCove.apk`，填地址和配对码，连上

---

## 能力边界

**TideGleam 已经全了**：完整 OneBot 11 协议（60+ action）、文字/图片/语音、主动推送、会话自愈。

**TideCove 是 1.0 基础版**：文字、图片（AI 能看懂）、语音输入。语音回复、文件、群聊在做了。

---

## 它不做什么

- **不经过任何第三方服务器**：消息从手机直接到你电脑
- **不收集数据**：聊天记录只在 `TideGleam\data\` 里
- **不联网初始化**：装完就能用，不需要注册账号
- **不依赖云端**：电脑关机就断，这是设计不是 bug

---

## 前提

电脑上要跑着 **DeepSeek Harness**（DSH）。TideGleam 会自动探测它的端口，探测不到就在 `config.json` 里手动指定：

```json
{ "dshUrl": "http://127.0.0.1:50052" }
```

---

## 已知限制

- 消息提示音在部分手机 WebView 上不响（系统 autoplay 策略）
- 同一时间只能连一台手机
- 本版不含长期记忆/数据库（上下文由 DSH 会话管理）
- 公网地址用 cloudflared 隧道时，每次重启都会变

---

## OneBot 接入（可选）

TideGleam 同时是一个 OneBot 11 服务端，外部机器人框架可以接进来：

```bash
# HTTP
curl -X POST http://127.0.0.1:8080/onebot/v11/send_private_msg \
  -d '{"message":"你好","user_id":10001}'

# WebSocket
ws://127.0.0.1:8080/onebot/v11/ws
```

只支持私聊；群、文件、好友关系链相关 action 会返回 `retcode 1404`。

---

## 关于源码

**本仓库只放交付物和文档，不放核心代码。**

服务端逻辑已编译进 `TideGleam.exe`（Node SEA + minify），前端页面随服务端分发。

想改自己的版本，可以基于公开的接口文档自己实现。

---

## 许可

仅供个人使用。不提供任何担保。
