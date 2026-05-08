import nonebot
from nonebot.adapters.cqhttp import CQHttp

# 初始化 NoneBot
nonebot.init()

# 使用 CQHttp 适配器（OneBot v11）
adapter = CQHttp(
    access_token="",
    websocket_url="ws://127.0.0.1:8080/onebot/v11/ws"
)

# 注册适配器
nonebot.get_driver().register_adapter(adapter)

# 加载插件
nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run()
