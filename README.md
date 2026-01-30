

<div align="center">
    
# 雨云自动签到（青龙面板版）
    
[![GitHub stars](https://img.shields.io/github/stars/你的用户名/Rainyun-QingLong?style=flat-square)](https://github.com/你的用户名/Rainyun-QingLong/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/你的用户名/Rainyun-QingLong?style=flat-square)](https://github.com/你的用户名/Rainyun-QingLong/network)
[![GitHub issues](https://img.shields.io/github/issues/你的用户名/Rainyun-QingLong?style=flat-square)](https://github.com/你的用户名/Rainyun-QingLong/issues)
[![GitHub license](https://img.shields.io/github/license/你的用户名/Rainyun-QingLong?style=flat-square)](https://github.com/你的用户名/Rainyun-QingLong/blob/main/LICENSE)
    
**本文档由AI生成，如有错误请反馈**
    
**支持多账号管理、验证码识别、服务器自动续费，专为青龙面板优化**

[快速开始](#快速开始) • [配置说明](#环境变量详解) • [常见问题](#常见问题) • [更新日志](#更新日志)

</div>

---

## ✨ 功能特性


### 🎯 核心功能
- ✅ 多账号轮询签到
- ✅ 智能验证码识别
- ✅ 账号级续费开关
- ✅ 服务器到期监控



### 🛡️ 安全保障
- ✅ 积分余额保护
- ✅ 通知推送汇总
- ✅ 执行结果统计
- ✅ 错误自动重试


---

## 🚀 快速开始

### 步骤 1：安装依赖

在青龙面板容器终端执行：

```bash
# 安装 Chrome 和 ChromeDriver
apt update && apt install -y chromium-driver

# 安装 Python 依赖
pip3 install selenium opencv-python-headless ddddocr requests
```
<img width="492" height="174" alt="image" src="https://github.com/user-attachments/assets/30c17b4d-a001-40da-b6b9-007460b68e39" />
<img width="522" height="376" alt="image" src="https://github.com/user-attachments/assets/79d163a2-b528-4afd-a31e-a373ded6a7b8" />
<img width="521" height="162" alt="image" src="https://github.com/user-attachments/assets/0b00dd28-f5c3-45f8-a018-5cbff8c6c40e" />

> 💡 **提示**：如果安装失败，请检查网络连接或使用国内镜像源

### 步骤 2：部署脚本（二选一）

#### 方式 A：订阅模式（推荐）

<details>
<summary>点击展开配置步骤</summary>

1. 进入青龙面板 → **订阅管理** → **创建订阅**

2. 填写订阅配置：

| 字段 | 填写内容 |
|------|---------|
| 名称 | `雨云签到` |
| 链接 | `https://github.com/你的用户名/Rainyun-QingLong.git` |
| 白名单 | `main` |
| 定时规则 | `0 2 * * *`（每天凌晨2点更新） |
| 分支 | `main` |

3. 保存后点击 **运行** 拉取脚本

4. **定时任务会自动创建**，无需手动添加

</details>

#### 方式 B：手动上传

<details>
<summary>点击展开上传步骤</summary>

1. 下载所有脚本文件到本地

2. 上传到青龙面板脚本目录：`/ql/scripts/RainYun/`

```
/ql/scripts/
└── RainYun/
    ├── stealth.min.js        # 反检测脚本
    ├── main.py               # 主入口
    ├── config.py
    ├── account_parser.py
    ├── api_client.py
    ├── server_manager.py
    └── captcha.py
```

3. **手动创建定时任务**：
   - 命令：`task RainYun/main.py`
   - 定时：`0 9 * * *`（每天9点）

</details>

> 📥 **stealth.min.js 下载**：[点击下载](https://raw.githubusercontent.com/berstend/puppeteer-extra/master/packages/puppeteer-extra-plugin-stealth/evasions/stealth.min.js)

### 步骤 3：配置环境变量

**相关说明请查看 [环境变量详解]**

进入青龙面板 → **环境变量** → **新建**

#### 必填项

```bash
# 变量名
RAINYUN_ACCOUNT

# 变量值（支持多账号）
[["账号1","密码1","true","api_key1"],["账号2","密码2","false"]]
```

**参数说明：**

| 位置 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 1 | ✅ | 雨云账号 | `user@qq.com` |
| 2 | ✅ | 密码 | `your_password` |
| 3 | ❌ | 自动续费 | `true` / `false`（默认 false） |
| 4 | ❌ | API Key | 雨云后台获取（不续费可留空） |

**配置示例：**

<details>
<summary>单账号启用续费</summary>

```bash
RAINYUN_ACCOUNT=[["user@qq.com","password123","true","ryapi_xxxxxxxx"]]
```

</details>

<details>
<summary>多账号部分续费</summary>

```bash
RAINYUN_ACCOUNT=[["user1@qq.com","pwd1","true","key1"],["user2@qq.com","pwd2","false"]]
```

</details>

<details>
<summary>仅签到不续费</summary>

```bash
RAINYUN_ACCOUNT=[["user@qq.com","password"]]
```

</details>

#### 可选项（高级配置）

```bash
# 变量名
RAINYUN_CONFIG

# 变量值（JSON格式）
{"captcha_retry_limit":-1,"renew_threshold_days":5}
```

<details>
<summary>完整配置参数</summary>

```json
{
  "timeout": 20,
  "max_delay": 5,
  "captcha_retry_limit": 10,
  "similarity_threshold": 0.4,
  "renew_days": 7,
  "renew_threshold_days": 3,
  "min_points_reserve": 5000,
  "stealth_js_path": "./stealth.min.js"
}
```

</details>

### 步骤 4：配置通知（可选）

青龙面板通知由系统统一管理，配置一次全局生效。

**配置路径：** 青龙面板 → **配置文件** → **config.sh**

**常用通知渠道：**

<details>
<summary>Server酱（推荐）</summary>

```bash
## Server酱
export PUSH_KEY="SCT******"
```

获取 SendKey：https://sct.ftqq.com/

</details>

<details>
<summary>企业微信机器人</summary>

```bash
## 企业微信机器人
export QYWX_KEY="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=******"
```

</details>

<details>
<summary>Telegram Bot</summary>

```bash
## Telegram
export TG_BOT_TOKEN="123456:ABC-DEF******"
export TG_USER_ID="123456789"
```

</details>

<details>
<summary>钉钉机器人</summary>

```bash
## 钉钉机器人
export DD_BOT_TOKEN="你的token"
export DD_BOT_SECRET="你的secret"  # 可选
```

</details>

<details>
<summary>Bark（iOS）</summary>

```bash
## Bark
export BARK_PUSH="https://api.day.app/你的key/"
```

</details>

<details>
<summary>PushPlus</summary>

```bash
## PushPlus
export PUSH_PLUS_TOKEN="你的token"
```

</details>

> 📖 **详细教程**：自行搜索「青龙面板通知配置」

---

## ⚙️ 环境变量详解

### RAINYUN_ACCOUNT（必填）

**格式：** JSON 数组，每个账号一个子数组

```bash
[["账号","密码","续费开关","API Key"],["账号2","密码2"]]
```

**完整参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| 账号 | String | ✅ | - | 雨云登录邮箱/手机号 |
| 密码 | String | ✅ | - | 雨云登录密码 |
| 续费开关 | Boolean | ❌ | `false` | `true` 启用 / `false` 禁用 |
| API Key | String | ❌ | `""` | 雨云 API 密钥（续费必需） |

### RAINYUN_CONFIG（可选）

**格式：** JSON 对象

**所有参数及默认值：**

<table>
<thead>
<tr>
<th>参数名</th>
<th>默认值</th>
<th>说明</th>
</tr>
</thead>
<tbody>
<tr><td colspan="3"><strong>基础配置</strong></td></tr>
<tr>
<td><code>timeout</code></td>
<td>20</td>
<td>页面加载超时（秒）</td>
</tr>
<tr>
<td><code>max_delay</code></td>
<td>5</td>
<td>账号间最大随机延时（分钟）</td>
</tr>
<tr><td colspan="3"><strong>验证码配置</strong></td></tr>
<tr>
<td><code>captcha_retry_limit</code></td>
<td>10</td>
<td>验证码重试次数（<code>-1</code>=无限重试）</td>
</tr>
<tr>
<td><code>similarity_threshold</code></td>
<td>0.4</td>
<td>验证码相似度阈值（0-1）</td>
</tr>
<tr><td colspan="3"><strong>下载配置</strong></td></tr>
<tr>
<td><code>download_max_retries</code></td>
<td>3</td>
<td>图片下载重试次数</td>
</tr>
<tr>
<td><code>download_retry_delay</code></td>
<td>2</td>
<td>下载重试间隔（秒）</td>
</tr>
<tr>
<td><code>download_timeout</code></td>
<td>10</td>
<td>下载超时（秒）</td>
</tr>
<tr><td colspan="3"><strong>续费配置</strong></td></tr>
<tr>
<td><code>renew_days</code></td>
<td>7</td>
<td>续费天数</td>
</tr>
<tr>
<td><code>renew_threshold_days</code></td>
<td>3</td>
<td>剩余天数≤此值时触发续费</td>
</tr>
<tr>
<td><code>min_points_reserve</code></td>
<td>5000</td>
<td>最低保留积分（续费后余额需≥此值）</td>
</tr>
<tr><td colspan="3"><strong>其他配置</strong></td></tr>
<tr>
<td><code>points_to_cny_rate</code></td>
<td>2000</td>
<td>积分兑换比率（2000分=1元）</td>
</tr>
<tr>
<td><code>stealth_js_path</code></td>
<td>./stealth.min.js</td>
<td>反检测脚本路径（相对/绝对路径）</td>
</tr>
</tbody>
</table>

**常用配置示例：**

```bash
# 验证码无限重试 + 提前5天续费
{"captcha_retry_limit":-1,"renew_threshold_days":5}

# 低配服务器延长超时
{"timeout":30,"download_timeout":15}

# 保守策略保留1万积分
{"min_points_reserve":10000}
```

---

## 💰 自动续费说明

### 获取 API Key

1. 登录 [雨云后台](https://app.rainyun.com/)
2. 进入 **用户中心** → **API 密钥**
3. **创建新密钥** 并复制

### 续费策略

| 项目 | 说明 |
|------|------|
| **触发条件** | 剩余天数 ≤ `renew_threshold_days`（默认3天） |
| **续费天数** | `renew_days`（默认7天） |
| **积分保护** | 续费后余额 ≥ `min_points_reserve`（默认5000） |
| **控制粒度** | 账号级独立开关 |

### 续费成本参考

| 续费天数 | 所需积分 | 约需签到 |
|---------|---------|---------|
| 7 天 | 2258 | 5 天 |
| 31 天 | 10000 | 20 天 |

> ⚠️ **注意**：签到每天约 500 积分，请确保积分充足

---

## 📊 通知报告示例

<details>
<summary>点击查看示例</summary>

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

</details>

---

## ❓ 常见问题

<details>
<summary><strong>Q: 验证码识别率低怎么办？</strong></summary>

**方案 1：降低相似度阈值**
```bash
RAINYUN_CONFIG={"similarity_threshold":0.3}
```

**方案 2：启用无限重试**
```bash
RAINYUN_CONFIG={"captcha_retry_limit":-1}
```

</details>

<details>
<summary><strong>Q: 如何关闭某个账号的自动续费？</strong></summary>

修改第3个参数为 `false`：

```bash
# 原配置
RAINYUN_ACCOUNT=[["user@qq.com","pwd","true","key"]]

# 修改后
RAINYUN_ACCOUNT=[["user@qq.com","pwd","false","key"]]
```

</details>

<details>
<summary><strong>Q: 积分充足但续费失败？</strong></summary>

**检查以下几点：**

1. 续费后剩余积分是否 ≥ `min_points_reserve`（默认5000）
2. API Key 是否有效（尝试重新生成）
3. 服务器是否已到期（到期后无法续费）
4. 查看日志中的具体错误信息

</details>

<details>
<summary><strong>Q: 通知没有收到？</strong></summary>

**排查步骤：**

1. 检查 `config.sh` 中环境变量名是否正确（区分大小写）
2. 确认 Token/Key 是否有效
3. 重启青龙面板容器：`docker restart qinglong`
4. 查看脚本执行日志是否有报错
5. 在青龙面板 **系统通知** 中测试通知是否正常

</details>

<details>
<summary><strong>Q: ChromeDriver 安装失败？</strong></summary>

**手动安装：**

```bash
# 方法 1
apt update && apt install -y chromium chromium-driver

# 方法 2（如果上面失败）
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
```

</details>

<details>
<summary><strong>Q: 如何修改 stealth.min.js 路径？</strong></summary>

在 `RAINYUN_CONFIG` 中配置：

```bash
# 相对路径（相对于 main.py）
RAINYUN_CONFIG={"stealth_js_path":"./stealth.min.js"}

# 绝对路径
RAINYUN_CONFIG={"stealth_js_path":"/ql/scripts/RainYun/stealth.min.js"}
```

</details>

<details>
<summary><strong>Q: 多账号会同时执行吗？</strong></summary>

**不会**。账号是串行处理的：

- 每个账号前有随机延时（0-5分钟，可配置）
- 账号之间间隔 3-6 秒
- 避免触发平台风控

</details>

<details>
<summary><strong>Q: 订阅拉取失败？</strong></summary>

**常见原因：**

1. **仓库地址错误**：确保以 `.git` 结尾
2. **网络问题**：使用国内镜像加速
   ```
   https://ghproxy.com/https://github.com/你的用户名/Rainyun-QingLong.git
   ```
3. **私有仓库**：需要配置 Personal Access Token

</details>

<details>
<summary><strong>Q: 订阅后创建了多个任务？</strong></summary>

**解决方案：**

1. 编辑订阅配置
2. **白名单** 填写：`main`
3. 删除多余任务
4. 重新拉取订阅

</details>

---

## 📁 文件结构

```
RainYun/
├── 📄 stealth.min.js       # 反检测脚本（支持自定义路径）
├── 🐍 main.py              # 主入口，流程编排
├── ⚙️ config.py            # 配置管理，解析环境变量
├── 👤 account_parser.py    # 账号解析，多账号配置
├── 🌐 api_client.py        # API客户端，封装雨云API
├── 🖥️ server_manager.py    # 服务器管理，自动续费逻辑
└── 🎯 captcha.py           # 验证码处理，图像识别
```

---

## 📝 更新日志

### v2.0.0 (2026-01-30)

<div style="background: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50;">

**🎉 重大更新**

本版本由 AI 全程开发，作者进行错误修正和优化

- ✅ 多账号管理，每个账号独立配置续费开关
- ✅ 验证码识别优化，支持自定义重试次数（含无限重试）
- ✅ 服务器自动续费，账号级精细控制
- ✅ 积分余额保护，避免积分耗尽
- ✅ 多渠道通知推送，执行结果汇总报告
- ✅ 支持相对路径配置 stealth.min.js
- ⚠️ 稳定性持续优化中

</div>

### v1.0.0 (2026-01-26)

- ✅ 多账号轮询签到
- ✅ 容器环境迁移至青龙面板

---

## 🙏 致谢

### 项目演进

<table>
<thead>
<tr>
<th width="15%">版本</th>
<th width="20%">作者</th>
<th width="35%">仓库</th>
<th width="30%">贡献</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">原版</td>
<td align="center">SerendipityR</td>
<td><a href="https://github.com/SerendipityR-2022/Rainyun-Qiandao">Rainyun-Qiandao</a></td>
<td>初始 Python 版本</td>
</tr>
<tr>
<td align="center">二改</td>
<td align="center">fatekey</td>
<td><a href="https://github.com/fatekey/Rainyun-Qiandao">Rainyun-Qiandao</a></td>
<td>Docker 化改造</td>
</tr>
<tr>
<td align="center">三改</td>
<td align="center">Jielumoon</td>
<td><a href="https://github.com/Jielumoon/Rainyun-Qiandao">Rainyun-Qiandao</a></td>
<td>稳定性优化 + 自动续费</td>
</tr>
<tr>
<td align="center">本版本</td>
<td align="center">你的用户名</td>
<td>本仓库</td>
<td>青龙面板适配 + 多账号管理</td>
</tr>
</tbody>
</table>

### 特别感谢

感谢所有为本项目提供帮助和建议的开发者 ❤️

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源

```
MIT License

Copyright (c) 2026 你的用户名

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## ⚠️ 免责声明

<div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">

**重要提示**

- 本项目仅供 **学习交流** 使用
- 请勿用于 **商业用途**
- 使用本脚本所产生的 **一切后果** 由使用者自行承担
- 作者不对任何损失或法律问题负责

</div>

---

## 💬 问题反馈

如果遇到问题或有建议，欢迎：

- 📮 提交 [Issue](https://github.com/LMTXQ/Rainyun-QingLong/issues)
- 🔀 提交 [Pull Request](https://github.com/LMTXQ/Rainyun-QingLong/pulls)
- 💬 Linux.DO私信 [Discussions](https://linux.do/u/t_acgn/summary)

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

Made with ❤️ by [LMTXQ](https://github.com/LMTXQ)

</div>


