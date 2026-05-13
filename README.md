# Showstart Ticket Checker 秀动余票查询器

秀动余票监控工具 - 自动化监控秀动演出回流票，支持QQ群推送和微信提醒。

## 功能特点

- 🔍 实时监控秀动演出余票
- 📱 微信推送提醒（通过PushPlus）
- 💬 QQ群推送提醒（通过NapCat）
- 🤖 AI生成推送文案（DeepSeek）
- ⏰ 定时任务（每日21:00自动关闭、维护提醒等）
- 🌙 后台运行和防睡眠支持

## 环境要求

- Python 3.8+
- Chrome浏览器
- NapCat（用于QQ机器人推送）
- PushPlus Token（用于微信推送，可选）
- DeepSeek API Key（用于AI文案生成，可选）

## 配置说明

在运行前，请在 `showstart_ticket_checker.py` 中配置以下内容：

```python
# NapCat 配置
NAPCAT_HTTP_URL = "http://localhost:3000"  # NapCat 服务地址

# PushPlus 配置（用于微信推送）
PUSHPLUS_TOKEN = "your_pushplus_token"

# DeepSeek 配置（用于AI文案生成）
DEEPSEEK_API_KEY = "your_deepseek_api_key"
```

## 使用方法

1. 安装依赖：
```bash
pip install selenium requests webdriver-manager pygame
```

2. 配置NapCat服务

3. 运行脚本（脚本密码见Admin Password文件）：
```bash
python showstart_ticket_checker.py
```

4. 选择操作模式：
   - 模式1：单次查询
   - 模式2：持续监控余票（QQ推送+声音提醒）
   - 模式3：持续监控余票（QQ推送+手机推送+系统提醒）

## 免责声明

本工具仅用于学习交流，请勿用于商业用途或违规操作。使用本工具产生的任何问题由使用者自行承担。

## License

MIT License
