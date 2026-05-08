import nonebot
from nonebot import on_command, on_message, on_regex
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot.permission import GROUP_ADMIN, GROUP_MEMBER, PRIVATE_FRIEND
from nonebot.typing import T_State
import re
import time
import json
import os
from datetime import datetime
from typing import List, Dict

try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from showstart_ticket_checker import ShowstartTicketChecker
except ImportError:
    from showstart_ticket_checker import ShowstartTicketChecker


class QQShowstartBot:
    def __init__(self):
        self.checker = ShowstartTicketChecker(headless=True)
        self.price_tiers = [880, 780, 580, 480, 380, 280]

    def format_ticket_message(self, tickets: List[Dict], event_id: str) -> str:
        """格式化票务信息为 QQ 消息"""
        if not tickets:
            return f"🎵 演出 {event_id}\n\n未查询到票务信息\n\n请检查演出ID是否正确"

        available = [t for t in tickets if t['status'] == '有票']

        msg = f"🎵 演出 {event_id}\n"
        msg += f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        msg += "-" * 30 + "\n"

        for ticket in tickets:
            status = "✅ 有票" if ticket['status'] == '有票' else "❌ 售罄"
            emoji = "🎫" if ticket['status'] == '有票' else "🚫"
            msg += f"{emoji} ¥{ticket['price']} | {status}\n"

        msg += "-" * 30 + "\n"
        msg += f"📊 当前 {len(available)}/{len(tickets)} 个档位有余票\n\n"

        if available:
            msg += "💡 提示: 有余票的档位建议尽快下单购买！\n"
        else:
            msg += "💡 提示: 所有票档已售罄，可以关注回流票或等待下一场\n"

        return msg

    def check_and_login(self) -> bool:
        """检查登录状态并自动登录"""
        if self.checker.check_login_status():
            return True

        try:
            self.checker._init_driver()
            self.checker.wait_for_login()
            self.checker.save_tokens_after_login()
            return True
        except Exception as e:
            print(f"[ERROR] 登录失败: {e}")
            return False

    def query_tickets(self, event_id: str) -> str:
        """查询演出余票"""
        try:
            tickets = self.checker.check_tickets(event_id)
            return self.format_ticket_message(tickets, event_id)
        except Exception as e:
            return f"❌ 查询失败: {str(e)}\n\n请稍后重试或联系管理员"


bot_instance = QQShowstartBot()

查票 = on_command("查票", aliases={"查余票", "票", "余票"}, priority=5)
帮助 = on_command("帮助", aliases={"help", "使用说明"}, priority=5)
状态 = on_command("状态", aliases={"登录状态", "bot状态"}, priority=5)


@查票.handle()
async def handle_query(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()

    if not args:
        await 查票.finish("📝 使用方法:\n\n查票 <演出ID>\n\n例如: 查票 295821\n\n演出ID获取方法:\n打开秀动APP或网页，点击演出，网址栏最后六位数就是演出ID")

    event_id = args.split()[0] if args.split() else args

    if not event_id.isdigit() or len(event_id) < 6:
        await 查票.finish("❌ 演出ID格式错误\n\n演出ID应该是6位数字\n\n例如: 查票 295821")

    await 查票.send("🔍 正在查询，请稍候...")

    try:
        tickets = bot_instance.checker.check_tickets(event_id)
        msg = bot_instance.format_ticket_message(tickets, event_id)
        await 查票.finish(msg)
    except Exception as e:
        await 查票.finish(f"❌ 查询失败: {str(e)}\n\n请稍后重试")


@帮助.handle()
async def handle_help(bot: Bot, event: Event, state: T_State):
    help_msg = """
🎵 秀动余票查询机器人使用说明

📌 主要命令:
  查票 <演出ID>  - 查询指定演出的余票
  帮助           - 显示本帮助信息
  状态           - 查看机器人运行状态

📝 演出ID获取方法:
  1. 打开秀动APP或网页
  2. 进入想要查询的演出页面
  3. 查看网址，例如:
     https://www.showstart.com/event/295821
     其中最后六位 295821 就是演出ID

💡 示例:
  查票 295821

⚠️ 注意:
  - 余票信息实时变化，以实际购买时为准
  - 有票建议尽快下单，热门演出售罄很快
  - 所有票档售罄后可关注回流票

🎸 祝你抢票成功！
"""
    await 帮助.finish(help_msg.strip())


@状态.handle()
async def handle_status(bot: Bot, event: Event, state: T_State):
    is_logged_in = bot_instance.checker.check_login_status()

    status_msg = "🔧 机器人状态\n\n"
    status_msg += f"📌 登录状态: {'✅ 已登录' if is_logged_in else '❌ 未登录'}\n"
    status_msg += f"🕐 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    status_msg += f"🌐 协议端: go-cqhttp\n"
    status_msg += f"🤖 框架: NoneBot2\n"

    if not is_logged_in:
        status_msg += "\n⚠️ 当前未登录，部分演出可能无法查询\n"
        status_msg += "请联系管理员进行登录"

    await 状态.finish(status_msg)
