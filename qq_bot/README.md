# 秀动余票查询 QQ 机器人

基于 NoneBot2 + go-cqhttp 的秀动余票查询机器人，支持群聊和私聊。

## 功能特点

- 🔍 实时查询秀动演出余票
- 📊 显示各票档价格和剩余情况
- 💡 智能提示抢票建议
- 🤖 支持群聊和私聊

## 目录结构

```
qq_bot/
├── bot.py                      # NoneBot2 启动文件
├── nonebot2.toml              # NoneBot2 配置文件
├── .env                       # 环境变量配置
├── requirements.txt           # Python 依赖
├── 启动机器人.bat             # Windows 启动脚本
├── go-cqhttp_guide.md         # go-cqhttp 配置指南
└── plugins/
    └── showstart_ticket.py    # 秀动余票查询插件
```

## 部署步骤

### 1. 配置 go-cqhttp

参考 [go-cqhttp_guide.md](go-cqhttp_guide.md) 完成以下步骤：

1. 下载 go-cqhttp v1.2.0
2. 解压到任意目录
3. 运行并选择 `3` (反向 WebSocket)
4. 修改 `config.yml` 配置文件
5. 启动并扫码登录

### 2. 安装 Python 依赖

```bash
cd qq_bot
pip install -r requirements.txt
```

### 3. 修改配置

编辑 `.env` 文件：

```env
BOT_NICKNAME=秀动余票Bot
BOT_ADMIN=你的QQ号
CQHTTP_WS_URL=ws://127.0.0.1:8080/onebot/v11/ws
DEBUG=false
```

编辑 `nonebot2.toml` 中的 URL 与 go-cqhttp 的 `universal` 配置保持一致。

### 4. 启动机器人

Windows 用户双击 `启动机器人.bat`，或运行：

```bash
python bot.py
```

## 使用方法

### 机器人命令

| 命令 | 说明 | 示例 |
|------|------|------|
| 查票 | 查询演出余票 | 查票 295821 |
| 帮助 | 显示帮助信息 | 帮助 |
| 状态 | 查看运行状态 | 状态 |

### 查询示例

```
查票 295821
```

返回示例：
```
🎵 演出 295821
查询时间: 2026-05-02 15:30:00
------------------------------
🎫 ¥880 | ✅ 有票
🎫 ¥780 | ✅ 有票
🎫 ¥580 | ❌ 售罄
🎫 ¥480 | ✅ 有票
🎫 ¥380 | ❌ 售罄
🎫 ¥280 | ✅ 有票
------------------------------
📊 当前 4/6 个档位有余票

💡 提示: 有余票的档位建议尽快下单购买！
```

### 演出ID获取方法

1. 打开秀动APP或网页
2. 进入演出页面
3. 查看网址，例如：
   `https://www.showstart.com/event/295821`
4. 最后六位数字 `295821` 就是演出ID

## 注意事项

- ⚠️ go-cqhttp 和 NoneBot2 需要同时运行
- ⚠️ 首次使用需要扫码登录秀动账号
- ⚠️ 余票信息实时变化，以实际购买为准
- ⚠️ 热门演出建议看到有票就立即购买

## 常见问题

### Q: 提示"未登录"怎么办？
A: 首次使用需要手动登录秀动账号。机器人启动后会自动打开浏览器窗口进行登录。

### Q: 查询显示"未查询到票务信息"？
A: 请检查演出ID是否正确，确保是6位数字。

### Q: go-cqhttp 一直显示连接中？
A: 检查 go-cqhttp 的 `config.yml` 中 `universal` URL 是否与 `nonebot2.toml` 中的 `url` 一致。

## 技术栈

- **框架**: NoneBot2
- **协议端**: go-cqhttp (OneBot v11)
- **浏览器自动化**: Selenium + Chrome WebDriver
- **语言**: Python 3.8+
