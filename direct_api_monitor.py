"""
秀动回流票监控 - 直接API方式（轻量级）
使用requests直接调用API，不依赖浏览器持续运行
"""
import requests
import json
import hashlib
import random
import time
import os
import sys
import logging
from datetime import datetime

# 日志文件路径
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f'monitor_{datetime.now().strftime("%Y%m%d")}.log')

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
    ]
)
logger = logging.getLogger('xiudong-monitor')


def log(msg):
    """打印日志，同时写入文件"""
    logger.info(msg)
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode('utf-8', errors='replace').decode('ascii', errors='replace'), flush=True)


class DirectAPIMonitor:
    def __init__(self, config=None):
        self.config = config or {}
        self.last_status = {}
        self.session = requests.Session()
        self.session.trust_env = False  # 禁用代理

    def _generate_crtraceid(self):
        """生成CRTRACEID"""
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        return ''.join(random.choice(chars) for _ in range(32)) + str(int(time.time() * 1000))

    def _generate_crpsign(self, body_str, url_path, trace_id):
        """生成CRPSIGN签名"""
        R = (self.config['accessToken'] + self.config['sign'] + self.config['idToken'] +
             self.config['userId'] + 'wap' + self.config['token'] + body_str + url_path + '997' + 'wap' + trace_id)
        return hashlib.md5(R.encode('utf-8')).hexdigest()

    def _refresh_token(self):
        """刷新token"""
        from token_refresher import refresh_tokens

        log(f"[{datetime.now()}] 刷新token...")
        updated = refresh_tokens(self.config)

        if updated:
            self.config = updated
            log(f"[{datetime.now()}] Token刷新成功")
            return True
        else:
            log(f"[{datetime.now()}] Token刷新失败")
            return False

    def get_ticket_list(self, activity_id):
        """获取票档列表"""
        url_path = '/wap/activity/V2/ticket/list'
        full_url = 'https://wap.showstart.com/v3' + url_path

        data = {
            "activityId": str(activity_id),
            "coupon": "",
            "st_flpv": self.config['st_flpv'],
            "sign": self.config['sign'],
            "trackPath": ""
        }
        body_str = json.dumps(data, separators=(',', ':'))

        crtraceid = self._generate_crtraceid()
        crpsign = self._generate_crpsign(body_str, url_path, crtraceid)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Origin': 'https://wap.showstart.com',
            'Referer': f'https://wap.showstart.com/pages/activity/detail/detail?activityId={activity_id}',
            'Content-Type': 'application/json',
            'CTERMINAL': 'wap',
            'CSAPPID': 'wap',
            'CVERSION': '997',
            'CUSNAME': 'nil',
            'CSOURCEPATH': '',
            'CTRACKPATH': '',
            'CUSAT': self.config['accessToken'],
            'CUSUT': self.config['sign'],
            'CUSIT': self.config['idToken'],
            'CUSID': self.config['userId'],
            'CDEVICENO': self.config['token'],
            'CUUSERREF': self.config['token'],
            'st_flpv': self.config['st_flpv'],
            'CRPSIGN': crpsign,
            'CRTRACEID': crtraceid,
            'CDEVICEINFO': '%7B%22vendorName%22:%22%22,%22deviceMode%22:%22PC%22,%22deviceName%22:%22%22,%22systemName%22:%22windows%22,%22systemVersion%22:%2210%20x64%22,%22cpuMode%22:%22%20%22,%22cpuCores%22:%22%22,%22cpuArch%22:%22%22,%22memerySize%22:%22%22,%22diskSize%22:%22%22,%22network%22:%224G%22,%22resolution%22:%221536*864%22,%22pixelResolution%22:%22%22%7D',
        }

        try:
            logger.debug(f"API请求: {full_url}")
            logger.debug(f"accessToken: {self.config['accessToken'][:20]}...")
            logger.debug(f"CRPSIGN: {crpsign}")

            resp = self.session.post(full_url, data=body_str, headers=headers, timeout=15)

            logger.debug(f"HTTP状态: {resp.status_code}")
            logger.debug(f"响应内容: {resp.text[:500]}")

            if resp.status_code == 200:
                result = resp.json()
                api_status = result.get('status')
                api_msg = result.get('msg', '')
                logger.info(f"API返回: status={api_status}, msg={api_msg}")
                if api_status != 200:
                    logger.warning(f"API业务错误: status={api_status}, msg={api_msg}, state={result.get('state')}")
                return result
            else:
                log(f"[{datetime.now()}] HTTP错误: {resp.status_code}")
                logger.error(f"HTTP错误: {resp.status_code}, 响应: {resp.text[:300]}")
                return None
        except Exception as e:
            log(f"[{datetime.now()}] 请求异常: {e}")
            logger.exception("请求异常详情")
            return None

    def get_ticket_status(self, activity_id):
        """获取票档状态"""
        data = self.get_ticket_list(activity_id)
        if data and data.get('status') == 200:
            return self._parse_tickets(data)
        elif data:
            msg = data.get('msg', '未知错误')
            code = data.get('status', 'N/A')
            log(f"[{datetime.now()}] API错误 [{code}]: {msg}")
        else:
            log(f"[{datetime.now()}] 网络请求失败，请检查网络连接")
        return None

    def _parse_tickets(self, data):
        """解析票档数据"""
        tickets = []
        result = data.get('result', [])
        if result and len(result) > 0:
            session_info = result[0]
            ticket_price_list = session_info.get('ticketPriceList', [])
            for price_group in ticket_price_list:
                ticket_list = price_group.get('ticketList', [])
                for ticket in ticket_list:
                    tickets.append({
                        'id': ticket.get('ticketId'),
                        'name': ticket.get('ticketType'),
                        'price': ticket.get('sellingPrice'),
                        'stock': ticket.get('remainTicket', 0),
                        'total': ticket.get('ticketNum', 0),
                        'saleStatus': ticket.get('saleStatus'),
                        'sellOver': ticket.get('sellOver', False),
                    })
        return tickets

    def check_stock_change(self, activity_id):
        """检测库存变化"""
        current = self.get_ticket_status(activity_id)
        if current is None:
            return None

        last = self.last_status.get(activity_id, [])
        changes = []

        for ticket in current:
            last_ticket = next((t for t in last if t['id'] == ticket['id']), None)
            if last_ticket:
                if ticket['stock'] > last_ticket['stock']:
                    changes.append({
                        'ticket': ticket,
                        'type': 'increase',
                        'diff': ticket['stock'] - last_ticket['stock']
                    })
                if last_ticket.get('sellOver') and not ticket.get('sellOver'):
                    changes.append({
                        'ticket': ticket,
                        'type': 'available',
                        'diff': ticket['stock']
                    })

        self.last_status[activity_id] = current
        return changes

    def monitor_loop(self, activity_id, interval=30, callback=None):
        """持续监控"""
        log(f"[{datetime.now()}] 开始监控演出: {activity_id}")
        log(f"[{datetime.now()}] 检查间隔: {interval}秒")
        log(f"[{datetime.now()}] 按 Ctrl+C 停止监控")
        print()

        # 首次刷新token
        if not self._refresh_token():
            log(f"[{datetime.now()}] Token刷新失败，请重新登录")
            return

        check_count = 0
        token_refresh_count = 0

        try:
            while True:
                check_count += 1
                log(f"[{datetime.now()}] 第{check_count}次检查...")

                try:
                    changes = self.check_stock_change(activity_id)

                    if changes is None:
                        log(f"[{datetime.now()}] 获取数据失败，尝试刷新token...")
                        if self._refresh_token():
                            time.sleep(2)
                            changes = self.check_stock_change(activity_id)

                    if changes is None:
                        log(f"[{datetime.now()}] 获取数据仍然失败，等待下次重试...")
                    elif changes:
                        for change in changes:
                            if change['type'] == 'increase':
                                msg = f"发现回流票! {change['ticket']['name']} +{change['diff']}张 (库存: {change['ticket']['stock']})"
                            else:
                                msg = f"票档恢复! {change['ticket']['name']} 现有{change['diff']}张"
                            log(f"[{datetime.now()}] !!! {msg}")
                            if callback:
                                callback(msg)
                    else:
                        tickets = self.last_status.get(activity_id, [])
                        stock_parts = []
                        for t in tickets:
                            if t.get('sellOver'):
                                stock_parts.append(f"{t['name']}:售罄")
                            else:
                                stock_parts.append(f"{t['name']}:{t['stock']}张")
                        stock_info = ', '.join(stock_parts)
                        log(f"[{datetime.now()}] 无变化 [{stock_info}]")

                    # 每10次检查刷新一次token
                    token_refresh_count += 1
                    if token_refresh_count >= 10:
                        self._refresh_token()
                        token_refresh_count = 0

                except Exception as e:
                    log(f"[{datetime.now()}] 监控异常: {e}")

                log(f"[{datetime.now()}] 等待{interval}秒后进行下次检查...")
                time.sleep(interval)

        except KeyboardInterrupt:
            log(f"\n[{datetime.now()}] 监控已停止")


# 主程序
if __name__ == '__main__':
    import sys

    # 读取配置
    config = None
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            pass

    if not config or not config.get('accessToken'):
        log("未找到有效配置，请先运行登录获取Token")
        exit(1)

    # 解析参数
    interval = 30
    activity_id = '295821'

    for arg in sys.argv[1:]:
        if arg.isdigit():
            interval = int(arg)
        elif arg.startswith('--id='):
            activity_id = arg.split('=')[1]

    monitor = DirectAPIMonitor(config)

    try:
        monitor.monitor_loop(activity_id, interval)
    except KeyboardInterrupt:
        log(f"\n[{datetime.now()}] 监控已停止")
