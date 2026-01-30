
# 雨云自动签到（青龙面板版）

本文档由 AI 自动生成，如有错误，请反馈

支持多账号管理、验证码识别、服务器自动续费，专为青龙面板优化。

## 功能特性

- ✅ 多账号轮询签到（每个账号独立配置）
- ✅ 智能验证码识别（支持自定义重试次数）
- ✅ 账号级自动续费开关（灵活控制每个账号是否续费）
- ✅ 服务器到期监控（剩余天数低于阈值自动续费）
- ✅ 积分余额保护（续费后保留最低积分储备）
- ✅ 多渠道通知推送（接入青龙面板自身通知模块）
- ✅ 执行结果汇总报告（统计成功/失败/积分变化）

## 快速开始

### 1. 安装依赖

在青龙面板服务器或容器终端执行：

```bash
# 安装 Chrome 和 ChromeDriver
apt update && apt install -y chromium-driver

# 安装 Python 依赖
pip3 install selenium opencv-python-headless ddddocr requests
```

### 2. 上传文件

将以下文件上传到青龙脚本目录（通常是 `/ql/scripts/QianDao/RainYun/`）：

```
/ql/scripts/
├── QianDao/
│   ├── stealth.min.js          # 反检测脚本
│   └── RainYun/
│       ├── main.py             # 主入口
│       ├── config.py           # 配置管理
│       ├── account_parser.py   # 账号解析
│       ├── api_client.py       # API客户端
│       ├── server_manager.py   # 服务器管理
│       └── captcha.py          # 验证码处理
```

> 📥 **stealth.min.js 下载地址**：  
> https://raw.githubusercontent.com/berstend/puppeteer-extra/master/packages/puppeteer-extra-plugin-stealth/evasions/stealth.min.js

### 3. 配置环境变量

在青龙面板「环境变量」中添加：

#### 基础配置（必填）

```bash
# 账号配置（必填）
RAINYUN_ACCOUNT=[["账号1","密码1","true","api_key1"],["账号2","密码2","false"]]
```

**格式说明：**
- 第1个参数：雨云账号（邮箱/手机号）
- 第2个参数：密码
- 第3个参数：是否启用自动续费（`true`/`false`）
- 第4个参数：API Key（可选，不续费可留空）

**简化格式（不启用续费）：**
```bash
RAINYUN_ACCOUNT=[["账号1","密码1"],["账号2","密码2"]]
```

#### 高级配置（可选）

```bash
# JSON 格式配置（所有参数可选，未设置则使用默认值）
RAINYUN_CONFIG={"timeout":20,"captcha_retry_limit":10,"renew_threshold_days":3}
```

### 4. 创建定时任务

在青龙面板「定时任务」中添加：

- **名称**：雨云自动签到
- **命令**：`task QianDao/RainYun/main.py`[ 路径可修改 ]
- **定时规则**：`0 9 * * *`（每天9点执行）

## 环境变量详解

### 基础配置（RAINYUN_ACCOUNT）

| 参数位置 | 必填 | 说明 | 示例 |
|---------|------|------|------|
| 第1个参数 | ✅ | 雨云账号 | `user@example.com` |
| 第2个参数 | ✅ | 密码 | `your_password` |
| 第3个参数 | ❌ | 自动续费开关 | `true` / `false`（默认 false） |
| 第4个参数 | ❌ | API Key | 从雨云后台获取（不续费可留空） |

**配置示例：**

```bash
# 示例1：单账号，启用续费
RAINYUN_ACCOUNT=[["user@qq.com","password123","true","ryapi_xxxxxxxx"]]

# 示例2：多账号，部分启用续费
RAINYUN_ACCOUNT=[["user1@qq.com","pwd1","true","key1"],["user2@qq.com","pwd2","false"]]

# 示例3：仅签到，不续费
RAINYUN_ACCOUNT=[["user@qq.com","password"]]
```

### 高级配置（RAINYUN_CONFIG）

JSON 格式，所有参数可选：

```json
{
  "timeout": 20,
  "max_delay": 5,
  "captcha_retry_limit": 10,
  "similarity_threshold": 0.4,
  "download_max_retries": 3,
  "download_retry_delay": 2,
  "download_timeout": 10,
  "api_base_url": "https://api.v2.rainyun.com",
  "api_request_timeout": 10,
  "api_max_retries": 3,
  "api_retry_delay": 2,
  "renew_days": 7,
  "renew_threshold_days": 3,
  "min_points_reserve": 5000,
  "points_to_cny_rate": 2000,
  "stealth_js_path": "./stealth.min.js"
}
```

#### 参数说明

| 参数名 | 默认值 | 说明 |
|--------|--------|------|
| `timeout` | 20 | 页面加载超时（秒） |
| `max_delay` | 5 | 最大随机延时（分钟） |
| `captcha_retry_limit` | 10 | 验证码重试次数（-1=无限重试） |
| `similarity_threshold` | 0.4 | 验证码相似度阈值（0-1） |
| `download_max_retries` | 3 | 图片下载重试次数 |
| `download_retry_delay` | 2 | 下载重试间隔（秒） |
| `download_timeout` | 10 | 下载超时（秒） |
| `api_base_url` | https://api.v2.rainyun.com | API 基础地址 |
| `api_request_timeout` | 10 | API 请求超时（秒） |
| `api_max_retries` | 3 | API 重试次数 |
| `api_retry_delay` | 2 | API 重试间隔（秒） |
| `renew_days` | 7 | 续费天数 |
| `renew_threshold_days` | 3 | 续费阈值（剩余N天时触发） |
| `min_points_reserve` | 5000 | 最低保留积分（续费后保留） |
| `points_to_cny_rate` | 2000 | 积分兑换比率（2000分=1元） |
| `stealth_js_path` | ../stealth.min.js | 反检测脚本相对路径 |

**常用配置示例：**

```bash
# 验证码无限重试，剩余5天时续费
RAINYUN_CONFIG={"captcha_retry_limit":-1,"renew_threshold_days":5}

# 低配服务器，延长超时时间
RAINYUN_CONFIG={"timeout":30,"download_timeout":15}

# 保守续费策略，保留1万积分
RAINYUN_CONFIG={"min_points_reserve":10000}
```

## 通知配置

青龙面板支持多种通知渠道，配置后自动生效。

### Server酱（推荐）

最简单的通知方式，微信接收。

1. 访问 https://sct.ftqq.com/
2. 微信扫码登录
3. 复制你的 SendKey
4. 在青龙面板添加环境变量：

```bash
# 变量名
PUSH_KEY

# 变量值
SCT******（你的SendKey）
```

### 企业微信机器人

1. 企业微信群聊 → 右键 → 添加群机器人
2. 复制 Webhook 地址
3. 在青龙面板添加环境变量：

```bash
# 变量名
QYWX_KEY

# 变量值
https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=******
```

### 钉钉机器人

```bash
# Bot Token
DD_BOT_TOKEN
你的token

# 如果设置了加签
DD_BOT_SECRET
你的secret
```

### Telegram Bot

```bash
# Bot Token
TG_BOT_TOKEN
123456:ABC-DEF******

# 用户ID
TG_USER_ID
123456789
```

### Bark（iOS推送）

```bash
# 变量名
BARK_PUSH

# 变量值
https://api.day.app/你的key/
```

### PushPlus（推送加）

```bash
# 变量名
PUSH_PLUS_TOKEN

# 变量值
你的token
```

> 💡 **提示**：配置任意一种通知方式即可，脚本会自动调用青龙面板的 `notify.py` 发送通知。

## 自动续费说明

### 获取 API Key

1. 登录雨云后台
2. 进入「用户中心」→「API 密钥」
3. 创建新密钥并复制

### 续费策略

- **触发条件**：服务器剩余天数 ≤ `renew_threshold_days`（默认3天）
- **续费天数**：默认7天（2258积分）
- **积分保护**：续费后剩余积分 ≥ `min_points_reserve`（默认5000）
- **白名单模式**：账号级控制，仅启用续费的账号会执行

### 续费成本参考

| 续费天数 | 所需积分 | 签到天数 |
|---------|---------|---------|
| 7 天 | 2258 | 约 5 天 |
| 31 天 | 10000 | 约 20 天 |

> ⚠️ **注意**：签到每天约 500 积分，请确保积分充足后再启用自动续费。

## 通知报告示例

执行完成后会收到类似以下的汇总报告：

```
============================================================
📊 雨云签到任务执行报告
============================================================

📈 总体统计:
  总账号数: 2
  ✅ 成功: 2
  ❌ 失败: 0

💰 积分统计:
  签到前总积分: 25000
  签到后总积分: 25500
  本次获得: 500 分
  约合人民币: 12.75 元

📋 各账号详情:
------------------------------------------------------------

【账号 1】 user1@qq.com
  状态: ✅ 成功
  积分: 12000 → 12250 (+250)
  自动续费: ✅ 已启用
    续费: 1台成功, 0台跳过, 0台失败

【账号 2】 user2@qq.com
  状态: ✅ 成功
  积分: 13000 → 13250 (+250)
  自动续费: ⏭️  未启用

============================================================
📅 执行时间: 2026-01-30 09:00:00
============================================================
```

## 常见问题

### Q: 验证码识别率低怎么办？

**A:** 有两种解决方案：

1. 降低相似度阈值：
```bash
RAINYUN_CONFIG={"similarity_threshold":0.3}
```

2. 启用无限重试（直到成功）：
```bash
RAINYUN_CONFIG={"captcha_retry_limit":-1}
```

### Q: 如何关闭某个账号的自动续费？

**A:** 修改账号配置的第3个参数为 `false`：

```bash
# 原配置
RAINYUN_ACCOUNT=[["user@qq.com","pwd","true","key"]]

# 修改后
RAINYUN_ACCOUNT=[["user@qq.com","pwd","false","key"]]
```

### Q: 积分充足但续费失败？

**A:** 检查以下几点：

1. 续费后剩余积分是否 ≥ `min_points_reserve`（默认5000）
2. API Key 是否有效（重新生成试试）
3. 服务器是否已到期（到期后无法续费）

### Q: 通知没有收到？

**A:** 排查步骤：

1. 检查环境变量名是否正确（区分大小写）
2. Token/Key 是否有效（重新获取）
3. 青龙面板是否重启（修改环境变量后建议重启）
4. 查看脚本日志是否有报错

### Q: ChromeDriver 安装失败？

**A:** 手动安装：

```bash
apt update
apt install -y chromium chromium-driver
```

### Q: 如何修改 stealth.min.js 路径？

**A:** 在 `RAINYUN_CONFIG` 中配置相对路径或绝对路径：

```bash
# 相对路径（相对于 main.py）
RAINYUN_CONFIG={"stealth_js_path":"../stealth.min.js"}

# 绝对路径
RAINYUN_CONFIG={"stealth_js_path":"/ql/scripts/QianDao/stealth.min.js"}
```

### Q: 多账号是否会并发执行？

**A:** 不会，为了避免触发风控，账号是串行处理的，每个账号之间有 3-6 秒随机间隔，且账号本身也有随机等待时间（可配置），多个账号执行间隔完全可以自定义。

## 文件结构

```
 RainYun/
    ├── stealth.min.js       # 反检测脚本（支持自定义路径）
    ├── main.py             # 主入口，负责流程编排
    ├── config.py           # 配置管理，解析环境变量
    ├── account_parser.py   # 账号解析，支持多账号配置
    ├── api_client.py       # API客户端，封装雨云API调用
    ├── server_manager.py   # 服务器管理，自动续费逻辑
    └── captcha.py          # 验证码处理，图像识别和点击
```

## 更新日志

### v2.0.0 (2026-01-30)
- V2.0.0 基于上一版本交由 AI 全程开发，作者仅在其基础上进行部分错误修正和优化（开发时间甚至没有半小时）
 - V2.0.0 稳定性不做保证，后续有bug慢慢修
- ✅ 多账号管理，支持每个账号独立配置续费
- ✅ 验证码识别，支持自定义重试次数和无限重试
- ✅ 服务器自动续费，账号级开关控制
- ✅ 积分余额保护，避免积分耗尽
- ✅ 多渠道通知推送，汇总报告
- ✅ 支持相对路径配置 stealth.min.js

### v1.0.0 (2026-01-26)
- ✅ 多账号轮询签到
- ✅ 由容器迁移至青龙面板运行

## 致谢

本项目首次发布基于以下仓库二次开发：

| 版本 | 作者 | 仓库 | 说明 |
|------|------|------|------|
| 原版 | SerendipityR | [Rainyun-Qiandao](https://github.com/SerendipityR-2022/Rainyun-Qiandao) | 初始 Python 版本 |
| 二改 | fatekey | [Rainyun-Qiandao](https://github.com/fatekey/Rainyun-Qiandao) | Docker 化改造 |
| 三改 | 本项目 | - | 青龙面板适配 + 多账号管理 + 自动续费 |

后续更新中参考Copy的部分仓库：

| 作者 | 仓库 | 说明 |
|------|------|------|
| Jielumoon | [Rainyun-Qiandao](https://github.com/Jielumoon/Rainyun-Qiandao) | Docker 化改造三改 ——稳定性优化 + 自动续费 |

## License

MIT License

---

**⚠️ 免责声明**

本项目仅供学习交流使用，请勿用于商业用途。使用本脚本所产生的一切后果由使用者自行承担。

