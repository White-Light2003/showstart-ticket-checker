import time
import subprocess
import ctypes
import traceback
import os
import requests
from datetime import datetime
from typing import List, Dict, Optional

NAPCAT_HTTP_URL = "http://127.0.0.1:3000"
PUSHPLUS_TOKEN = "775190c6be9f4d9fbdd397c509178e37"  # 在这里填写你的 PushPlus token
DEEPSEEK_API_KEY = "sk-455a13a9e56a4b969b06f477f7d8fce0"  # 在这里填写你的 DeepSeek API Key

# ChiliChill乐团歌词库
CHILICHILL_LYRICS = [
    "你的世界才不是mono~你的表演才不是solo~——ChiliChill《不安灵魂收容所》(改编版)","我时常对自己失望~没有一个超自信的理想~——ChiliChill《万一对了呢》","毕竟天总会放晴雨会停~——ChiliChill《五块钱的伞》","推开门🚪摆摆左手✋🏻转身右走🚶🏻‍♀️‍➡️——ChiliChill《辞职信》",
    "别转头🙂‍↔️撞进万万人潮之后👥——ChiliChill《辞职信》","哦也许吧🧐人总有逃不掉的痛😣——ChiliChill《辞职信》","哦也许吧🧐下个街口也没自由🤷🏻‍♀️——ChiliChill《辞职信》","风不风🌬️昨日种种📒甩甩袖口👋——ChiliChill《辞职信》",
    "流不流🌊明天以后🔜不再逗留🏃🏻‍♀️‍➡️——ChiliChill《辞职信》","哦也许吧🧐有种荒谬才是出口🚪——ChiliChill《辞职信》","那天晚上🌃做了个我从前不敢做的梦😴💭——ChiliChill《辞职信》","老板，来20串！——ChiliChill《饿魔少女》",
    "左牵黄，右擎苍，日行千里系沙袋~——ChiliChill《恋爱困难少女》","请你管好你自己~我不需要你的废话大道理~——ChiliChill《管好你自己》","等一个人来坐我的船~抚平我摇摇晃晃的不安~思绪不断~——ChiliChill《双人船》","我们都会拥有美好的未来~——ChiliChill《飞鸟说》",
    "你走吧~此去山遥路远~——ChiliChill《山遥路远》","不加糖，不加奶，放了几颗冰块的~Americano(啊美丽卡洛)——ChiliChill《啊！美丽卡洛》","泡上一杯咖啡，今晚继续熬夜~——ChiliChill《社畜少女》","我用世间最顺的笔尖~将我们的故事书写~——ChiliChill《芭蕉夜雨》",
    "一身素青纱，草柄当头花~——ChiliChill《下等马》","夏末秋初，第一场雨，混了5%的酒精~——ChiliChill《入秋的第一场雨真让人矫情》","Hakunama ta ta,my friend~——ChiliChill《提瓦特民谣》","这里最美丽的咒语——谢谢你和我也爱你（呐喊）！——ChiliChill《混入人类计划》",
    "如今我却想往回走~——ChiliChill《衡山路宛平路》","Itai Itai 明明忘了怎么突然清晰~——ChiliChill《难过233秒》","场灯灭~拉幕帘~起配乐~——ChiliChill《演》","你介绍给我的对象~现在还是八字没一撇~——ChiliChill《恋爱困难少男》",
    "或许你和我的缘分~并不值得三个铜板~——ChiliChill《橙子汽水》","可以撩我的心~别撩我的头发——ChiliChill《别动我头发》","今天到底是礼拜几~怎么就头晕脚无力~——ChiliChill《屑屑》","我的破木箱~装满枯萎的花~——ChiliChill《我不曾忘记》",
    "高举一面夜色~星空替你记得~究竟为了什么活着~——ChiliChill《启航的歌》","褪色的画面重叠~数着还没过完的日子入眠~—ChiliChill《时光盲盒》","等天黑~再过一夜~—ChiliChill《搬家前，短暂夜》","当你的天空突然下起了大雨，那是我在为你炸乌云~—ChiliChill《让风告诉你》",
    "Drop the beat~I feel~Like a rollercoaster going up and down~—ChiliChill《pinking》","Overtake~Step on the GAS~Dash like a vroom vroom vroom~—ChiliChill《都市不丽人》","摘一朵纯白色的花~塞西莉亚~塞西莉亚~—ChiliChill《别让我担心》",
    "告诉我~不想再继续~我的心就石沉大海~偏偏你~就是拖着不坦白~—ChiliChill《半梦》","我的悲伤~是水做的~是水做的~—ChiliChill《我的悲伤是水做的》","怎么不挽留~拦下~我的冲动~—ChiliChill《半醒》","你没喝完的无糖可乐~冰箱里还剩几瓶~全部丢出去~全部丢出去~换成我爱的雪碧~—ChiliChill《心碎烧酒》",
    "心在波比~震天动地~是我是你~不太确定~—ChiliChill《有线耳机》","高温缩减，长江中下游地带有大雨到暴雨~—ChiliChill《晚间天气预报》"
]

# 定时关闭任务配置
DAILY_SHUTDOWN_HOUR = 21  # 每天自动关闭时间（小时）
QQ_PUSH_END_DATE = datetime(2026, 6, 8, 0, 0, 0)  # QQ推送关闭日期
QQ_PUSH_NOTICE_DATES = [datetime(2026, 6, 4), datetime(2026, 6, 5), datetime(2026, 6, 6), datetime(2026, 6, 7)]  # 发送关闭通知的日期
QQ_PUSH_NOTICE_TIME = (22, 0)  # 关闭通知发送时间（小时，分钟）
QQ_PUSH_END_NOTICE_SENT = False  # 是否已发送6月8日零点关闭的通知
DAILY_SHUTDOWN_DONE = False  # 今日是否已执行每日关闭

# 新歌推广消息
NEW_SONG_PROMO_MSG = """🎵【新歌推送】🎵

ChiliChill乐团的新歌《辞职信》已于各大音乐平台上线！
请各位及时加入自己的歌单并开启单曲循环！🎶"""

def should_disable_qq_push() -> bool:
    """检查是否应该关闭QQ推送"""
    now = datetime.now()
    return now >= QQ_PUSH_END_DATE

def check_and_send_shutdown_notice():
    """检查并发送关闭通知"""
    global QQ_PUSH_END_NOTICE_SENT
    now = datetime.now()
    
    # 检查是否已过关闭时间
    if now >= QQ_PUSH_END_DATE:
        return False
    
    # 检查是否是发送通知的日期
    for notice_date in QQ_PUSH_NOTICE_DATES:
        if (now.year == notice_date.year and 
            now.month == notice_date.month and 
            now.day == notice_date.day and
            now.hour == QQ_PUSH_NOTICE_TIME[0] and 
            now.minute == QQ_PUSH_NOTICE_TIME[1]):
            return True
    
    return False

NAPCAT_HEARTBEAT_INTERVAL = 60  # 心跳检测间隔（秒）
last_heartbeat_time = 0
napcat_connected = True

def check_napcat_connection() -> bool:
    """检查 NapCat 服务是否正常连接"""
    global napcat_connected
    try:
        url = f"{NAPCAT_HTTP_URL}/_ping"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            napcat_connected = True
            return True
        else:
            napcat_connected = False
            return False
    except:
        napcat_connected = False
        return False

def napcat_heartbeat():
    """NapCat 心跳检测，定期检查连接状态"""
    global last_heartbeat_time, napcat_connected
    current_time = time.time()
    if current_time - last_heartbeat_time >= NAPCAT_HEARTBEAT_INTERVAL:
        last_heartbeat_time = current_time
        is_connected = check_napcat_connection()
        if not is_connected and napcat_connected:
            # 刚断开连接
            print("\n[WARNING] ❌ NapCat 连接断开！")
            send_phone_notification("⚠️ NapCat连接断开", "NapCat服务已断开连接！请检查NapCat是否正常运行或QQ是否在线！")
            show_system_notification("⚠️ NapCat连接断开", "NapCat服务已断开连接！\n\n请检查：\n• NapCat是否正常运行\n• QQ是否在线\n• 网络连接是否正常")
        elif is_connected and not napcat_connected:
            # 重新连接成功
            print("\n[INFO] ✅ NapCat 重新连接成功！")
            send_phone_notification("✅ NapCat已重新连接", "NapCat服务已重新连接成功！")
            show_system_notification("✅ NapCat已重新连接", "NapCat服务已重新连接成功！")

def generate_ticket_message(event_id: str, tickets: List[Dict]) -> str:
    """使用 DeepSeek AI 生成票务推送文案（支持有票和无票场景）"""
    if not DEEPSEEK_API_KEY:
        return ""
    
    available_tickets = [t for t in tickets if t['status'] == '有票']
    
    if available_tickets:
        ticket_info = "\n".join([f"- {t['price']}元 ({t['name']})" for t in available_tickets])
        prompt = f"""
        请帮我写一段吸引眼球的QQ群回流票推送文案，要求：
        
        演出ID: {event_id}
        
        有票档位：
        {ticket_info}
        
        要求：
        1. 使用表情符号和换行，让消息更生动
        2. 语气要兴奋、紧迫，营造抢购氛围
        3. 突出"回流票"、"手速"、"快抢"等关键词
        4. 结尾加上催促大家去秀动APP抢购的号召
        5. 不要超过4行
        """
    else:
        prompt = f"""
        请帮我写一段QQ群票务状态通知文案，当前演出暂无余票，要求：
        
        演出ID: {event_id}
        
        当前票档状态：全部售罄
        
        要求：
        1. 使用表情符号和换行，让消息更易读
        2. 语气要亲切、鼓励，不要让大家失望
        3. 提醒大家继续关注，回流票随时可能出现
        4. 可以加点幽默或可爱的表情让氛围轻松一些
        5. 不要超过3行
        """
    
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个专业的票务通知文案撰写助手，擅长用简短、有趣、吸引人的方式编写群消息。"},
                {"role": "user", "content": prompt.strip()}
            ],
            "max_tokens": 200,
            "temperature": 0.8
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        result = response.json()
        
        if result.get("choices"):
            message = result["choices"][0]["message"]["content"].strip()
            # 从歌词库中随机选择一句歌词添加到结尾
            import random
            lyrics = random.choice(CHILICHILL_LYRICS)
            message = f"{message}\n\n{lyrics}"
            print(f"[AI生成] ✅ 成功生成推送文案")
            return message
        else:
            print(f"[AI生成] ❌ 生成失败: {result.get('error', {}).get('message', '未知错误')}")
            return ""
    except Exception as e:
        print(f"[AI生成] ❌ 请求异常: {e}")
        return ""

def clean_message(message: str) -> str:
    """清洗消息内容，移除可能导致 NapCat 解析错误的特殊字符"""
    # 移除控制字符（保留换行和制表符）
    cleaned = ''.join(char for char in message if ord(char) >= 32 or char in '\n\t')
    # 限制消息长度
    if len(cleaned) > 2000:
        cleaned = cleaned[:2000] + "..."
    # 移除多余的换行和空格
    cleaned = '\n'.join(line.strip() for line in cleaned.split('\n') if line.strip())
    return cleaned

def send_to_qq_group(group_id: int, message: str, max_retries: int = 2) -> bool:
    """通过 NapCat HTTP API 发送消息到 QQ 群（支持重试）"""
    retry_delay = 2  # 重试间隔（秒）
    
    # 清洗消息，移除可能导致解析错误的特殊字符
    message = clean_message(message)
    
    for attempt in range(max_retries + 1):
        try:
            url = f"{NAPCAT_HTTP_URL}/send_group_msg"
            params = {
                "group_id": group_id,
                "message": message
            }
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            if result.get("retcode") == 0:
                print(f"[QQ推送] ✅ 消息已发送到群 {group_id}")
                return True
            else:
                if attempt < max_retries:
                    print(f"[QQ推送] ⚠️ 发送失败(尝试 {attempt+1}/{max_retries+1}): {result}，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    continue
                print(f"[QQ推送] ❌ 发送失败: {result}")
                return False
        except requests.exceptions.ConnectionError:
            if attempt < max_retries:
                print(f"[QQ推送] ⚠️ 连接失败(尝试 {attempt+1}/{max_retries+1})，{retry_delay}秒后重试...")
                time.sleep(retry_delay)
                continue
            print(f"[QQ推送] ❌ 连接失败：无法连接到 NapCat 服务")
            return False
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                print(f"[QQ推送] ⚠️ 连接超时(尝试 {attempt+1}/{max_retries+1})，{retry_delay}秒后重试...")
                time.sleep(retry_delay)
                continue
            print(f"[QQ推送] ❌ 连接超时：NapCat 服务无响应")
            return False
        except Exception as e:
            if attempt < max_retries:
                print(f"[QQ推送] ⚠️ 发送异常(尝试 {attempt+1}/{max_retries+1}): {e}，{retry_delay}秒后重试...")
                time.sleep(retry_delay)
                continue
            print(f"[QQ推送] ❌ 发送异常: {e}")
            return False

def show_system_notification(title: str, message: str):
    """显示系统弹窗提醒"""
    try:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x1000 | 0x40)  # MB_ICONWARNING | MB_TOPMOST
    except Exception as e:
        print(f"[提醒] 无法显示系统通知: {e}")

def send_phone_notification(title: str, content: str) -> bool:
    """通过 PushPlus 发送手机消息推送"""
    if not PUSHPLUS_TOKEN:
        print(f"[手机推送] ⚠️ 未配置 PushPlus token，跳过手机推送")
        return False
    
    try:
        url = "http://www.pushplus.plus/send"
        data = {
            "token": PUSHPLUS_TOKEN,
            "title": title,
            "content": content,
            "template": "txt"
        }
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        if result.get("code") == 200:
            print(f"[手机推送] ✅ 消息已发送到手机")
            return True
        else:
            print(f"[手机推送] ❌ 发送失败: {result.get('msg', '未知错误')}")
            return False
    except Exception as e:
        print(f"[手机推送] ❌ 发送异常: {e}")
        return False

def get_available_groups() -> List[int]:
    """获取Bot所在的群列表"""
    try:
        url = f"{NAPCAT_HTTP_URL}/get_group_list"
        response = requests.get(url, timeout=5)
        result = response.json()
        if result.get("retcode") == 0:
            groups = result.get("data", [])
            return [g["group_id"] for g in groups]
        return []
    except:
        return []

def select_target_groups() -> Optional[List[int]]:
    """让用户选择目标群（支持多选）"""
    groups = get_available_groups()
    if not groups:
        print("[QQ推送] ❌ 无法获取群列表，请确保 NapCat HTTP 服务正常运行")
        print("[QQ推送] 💡 提示：请先确认 NapCat 已登录并且在群中")
        return None

    print("\n" + "="*50)
    print("📋 Bot 所在群列表：")
    print("="*50)
    for i, gid in enumerate(groups, 1):
        print(f"  {i}. {gid}")
    print("="*50)
    print("\n💡 输入示例：")
    print("  • 单选：输入 1")
    print("  • 多选：输入 1,3,5（用逗号分隔）")
    print("  • 全选：输入 all")

    while True:
        choice = input("\n请选择要推送的群号：").strip()
        if not choice:
            print("输入不能为空，请重新输入")
            continue

        if choice.lower() == 'all':
            return groups

        try:
            if ',' in choice:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
            else:
                indices = [int(choice) - 1]

            selected = [groups[i] for i in indices if 0 <= i < len(groups)]
            if selected:
                return selected
            print("无效选择，请重新输入")
        except ValueError:
            print("请输入有效数字，用逗号分隔多选")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Windows API 防止电脑睡眠
try:
    kernel32 = ctypes.windll.kernel32
    EXECUTION_STATE = 0x80000003  # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED

    def prevent_sleep():
        kernel32.SetThreadExecutionState(EXECUTION_STATE)

    def allow_sleep():
        kernel32.SetThreadExecutionState(0)  # 恢复默认睡眠设置
except:
    def prevent_sleep():
        pass

    def allow_sleep():
        pass

class ShowstartTicketChecker:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.price_tiers = [880, 780, 580, 480, 380, 280]
        self.driver = None
        self.chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        self.tokens_set = False

    def _init_driver(self):
        """初始化Chrome驱动"""
        if self.driver:
            return

        options = Options()
        if self.headless:
            options.add_argument('--headless=new')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-notifications')
        options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        try:
            import os
            
            custom_driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
            
            if os.path.exists(custom_driver_path):
                service = Service(custom_driver_path)
            else:
                driver_path = ChromeDriverManager().install()
                import shutil
                shutil.copy(driver_path, custom_driver_path)
                service = Service(custom_driver_path)
            
            self.driver = webdriver.Chrome(service=service, options=options)
            
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en-US', 'en']});
                Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
                Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            """)
        except Exception as e:
            print(f"[ERROR] 浏览器启动失败: {e}")
            raise

    def _close_driver(self):
        """关闭驱动"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

    def wait_for_login(self):
        """等待用户手动登录"""
        print("\n请在浏览器窗口中完成后续的登录操作")
        print("注意：请使用已经在秀动账号实名认证后的手机号登录，否则票务信息加载不完整。")
        print("   1. 输入手机号并获取验证码")
        print("   2. 输入验证码并勾选同意协议")
        print("   3. 点击'立即登录'")
        print("\n登录成功后，请回到命令行按回车键继续...")
        input()

    def save_tokens_after_login(self):
        """登录后保存token到配置文件"""
        import json
        import os

        print("\n[INFO] 正在捕获登录凭证...")

        try:
            tokens = self.driver.execute_script("""
                return JSON.stringify({
                    'accessToken': localStorage.getItem('accessToken') || '',
                    'sign': localStorage.getItem('sign') || '',
                    'idToken': localStorage.getItem('idToken') || '',
                    'token': localStorage.getItem('token') || '',
                    'st_flpv': localStorage.getItem('st_flpv') || '',
                    'userId': localStorage.getItem('userId') || ''
                });
            """)

            if tokens:
                config = json.loads(tokens)

                if config.get('accessToken') and len(config['accessToken']) > 10:
                    config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
                    os.makedirs(config_dir, exist_ok=True)
                    config_path = os.path.join(config_dir, 'tokens.json')

                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2)

                    print("[SUCCESS] 登录凭证已保存")
                    self.tokens_set = True
                    return True
                else:
                    print("[WARNING] 未获取到有效的登录凭证")
                    return False
            else:
                print("[WARNING] 获取登录凭证失败")
                return False
        except Exception as e:
            print(f"[ERROR] 保存登录凭证失败: {e}")
            return False

    def load_tokens(self):
        """加载保存的token"""
        import json
        import os

        config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
        config_path = os.path.join(config_dir, 'tokens.json')

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config
            except:
                return None
        return None

    def set_tokens_to_browser(self):
        """将token设置到浏览器localStorage"""
        tokens = self.load_tokens()
        if not tokens:
            return False

        try:
            self._init_driver()
            self.driver.get("https://www.showstart.com")

            for key, value in tokens.items():
                if value:
                    self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")

            print("[INFO] 已加载保存的登录凭证")
            return True
        except Exception as e:
            print(f"[ERROR] 设置登录凭证失败: {e}")
            return False

    def check_login_status(self):
        """检查登录状态"""
        tokens = self.load_tokens()
        if tokens and tokens.get('accessToken'):
            return True
        return False

    def check_tickets(self, event_id: str) -> List[Dict]:
        """查询演出余票"""
        tokens = self.load_tokens()
        
        self._init_driver()

        try:
            if tokens and not self.tokens_set:
                self.driver.get("https://www.showstart.com")
                time.sleep(0.5)

                for key, value in tokens.items():
                    if value:
                        self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
                
                self.tokens_set = True

            url = f"https://www.showstart.com/event/{event_id}"
            self.driver.get(url)
            time.sleep(1.5)

            buy_buttons_xpath = [
                '//*[contains(text(), "立即购票")]',
                '//*[contains(text(), "购票")]',
                '//*[contains(text(), "预约")]',
                '//button[contains(text(), "购票") or contains(text(), "立即购票")]',
                '//div[contains(@class, "buy") or contains(@class, "ticket")]/button',
                '//*[@id="buyBtn"]',
                '//a[contains(text(), "购票") or contains(text(), "立即购票")]'
            ]

            clicked = False
            for xpath in buy_buttons_xpath:
                try:
                    buy_btn = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    buy_btn.click()
                    time.sleep(1.5)
                    clicked = True
                    break
                except TimeoutException:
                    continue
                except Exception:
                    continue

            return self._parse_tickets()
        except Exception as e:
            print(f"[ERROR] 查询失败: {e}")
            return []

    def _parse_tickets(self) -> List[Dict]:
        """解析票务信息"""
        import re

        all_text = self.driver.execute_script("return document.body.innerText || document.documentElement.innerText;")

        found_tickets = {}

        patterns = [
            r'(\d{3,4})\s*元',
            r'¥\s*(\d{3,4})',
            r'(\d{3,4})\s*元\s*票',
            r'票\s*(\d{3,4})',
            r'(\d{3,4})元\D',
            r'(\d{3,4})\s*[元块]',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, all_text)
            for match in matches:
                if isinstance(match, tuple):
                    price_str = match[0] if match else ''
                else:
                    price_str = match
                
                if price_str.isdigit():
                    price_int = int(price_str)
                    if 100 <= price_int <= 2000 and price_int not in found_tickets:
                        found_tickets[price_int] = {
                            'price': price_int,
                            'name': f'{price_int}元票',
                            'status': '有票'
                        }

        lines = all_text.split('\n')
        
        for price in found_tickets:
            price_str = str(price)
            for i, line in enumerate(lines):
                if price_str in line:
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 3)
                    context = '\n'.join(lines[context_start:context_end])
                    
                    if '票已售罄' in context or '已售罄' in context or '已售完' in context:
                        found_tickets[price]['status'] = '售罄'
                        break

        return sorted(found_tickets.values(), key=lambda x: x['price'], reverse=True)

    def run_diagnostics(self) -> Dict[str, Dict]:
        """系统自检，诊断潜在问题"""
        results = {}
        suggestions = {}

        print("\n" + "="*50)
        print("🔧 秀动余票查询工具 - 系统自检")
        print("="*50)

        results['chrome_driver'] = self._check_chrome_driver()
        results['network'] = self._check_network()
        results['website_access'] = self._check_website_access()
        results['selenium'] = self._check_selenium()

        print("\n" + "-"*50)
        print("📋 诊断结果汇总")
        print("-"*50)

        for check_name, result in results.items():
            status_icon = "✅" if result['status'] == 'pass' else ("⚠️" if result['status'] == 'warning' else "❌")
            print(f"{status_icon} {result['name']}: {result['message']}")

        print("\n" + "-"*50)
        print("💡 解决方案建议")
        print("-"*50)

        has_issues = False
        for check_name, result in results.items():
            if result['status'] != 'pass':
                has_issues = True
                print(f"\n📌 [{result['name']}]")
                for suggestion in result.get('suggestions', []):
                    print(f"   • {suggestion}")

        if not has_issues:
            print("🎉 所有检查项均通过！未发现问题。")

        print("\n" + "="*50)
        return results

    def _check_chrome_driver(self) -> Dict:
        """检查ChromeDriver"""
        result = {
            'name': 'ChromeDriver',
            'status': 'pass',
            'message': '正常',
            'suggestions': []
        }

        custom_driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')

        if os.path.exists(custom_driver_path):
            try:
                version_info = subprocess.run(
                    [custom_driver_path, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if version_info.returncode == 0:
                    result['message'] = f"本地版本 - {version_info.stdout.strip()}"
                else:
                    result['status'] = 'warning'
                    result['message'] = '版本可能不匹配'
                    result['suggestions'] = [
                        '当前chromedriver.exe可能与Chrome版本不匹配',
                        '建议删除本地chromedriver.exe，让脚本自动下载匹配版本'
                    ]
            except Exception as e:
                result['status'] = 'warning'
                result['message'] = f'本地驱动异常: {e}'
                result['suggestions'] = [
                    '删除当前chromedriver.exe',
                    '脚本将自动下载匹配版本'
                ]
        else:
            try:
                driver_path = ChromeDriverManager().install()
                if os.path.exists(driver_path):
                    result['message'] = '自动下载版本正常'
                else:
                    result['status'] = 'warning'
                    result['message'] = '驱动未找到'
                    result['suggestions'] = ['运行一次查询让脚本自动下载驱动']
            except Exception as e:
                result['status'] = 'error'
                result['message'] = f'驱动检查失败: {e}'
                result['suggestions'] = [
                    '网络问题导致无法下载驱动',
                    '请检查网络连接后重试'
                ]

        return result

    def _check_network(self) -> Dict:
        """检查网络连接"""
        result = {
            'name': '网络连接',
            'status': 'pass',
            'message': '正常',
            'suggestions': []
        }

        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            result['message'] = '网络连接正常'
        except OSInterrupt:
            result['status'] = 'error'
            result['message'] = '无法连接外网'
            result['suggestions'] = [
                '请检查网络连接',
                '确保电脑已连接到互联网',
                '尝试打开浏览器访问其他网站测试'
            ]

        return result

    def _check_website_access(self) -> Dict:
        """检查秀动网站可访问性"""
        result = {
            'name': '秀动网站访问',
            'status': 'pass',
            'message': '正常',
            'suggestions': []
        }

        try:
            import requests
            response = requests.get("https://www.showstart.com", timeout=10)
            if response.status_code == 200:
                result['message'] = '网站可正常访问'
            else:
                result['status'] = 'warning'
                result['message'] = f'网站返回状态码: {response.status_code}'
                result['suggestions'] = [
                    '秀动网站可能正在维护',
                    '稍后再试或联系秀动客服'
                ]
        except ImportError:
            result['status'] = 'warning'
            result['message'] = '无法验证（缺少requests库）'
            result['suggestions'] = [
                '网站应该可以访问',
                '如果实际访问有问题，请安装requests库: pip install requests'
            ]
        except Exception as e:
            result['status'] = 'error'
            result['message'] = f'网站无法访问: {e}'
            result['suggestions'] = [
                '秀动网站可能宕机或维护中',
                '稍后再试',
                '或检查网络代理设置'
            ]

        return result

    def _check_selenium(self) -> Dict:
        """检查Selenium环境"""
        result = {
            'name': 'Selenium环境',
            'status': 'pass',
            'message': '正常',
            'suggestions': []
        }

        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            result['message'] = 'Selenium库正常'
        except ImportError as e:
            result['status'] = 'error'
            result['message'] = f'Selenium库缺失: {e}'
            result['suggestions'] = [
                '请安装Selenium: pip install selenium',
                '请安装webdriver-manager: pip install webdriver-manager'
            ]

        return result

def play_notification_sound():
    """播放通知声音"""
    try:
        import winsound
        winsound.Beep(1000, 500)
        time.sleep(0.1)
        winsound.Beep(1200, 500)
        time.sleep(0.1)
        winsound.Beep(1000, 500)
    except:
        pass

def print_ticket_info(tickets: List[Dict], event_name: str = ""):
    """显示票务信息"""
    if not tickets:
        print("未查询到票务信息")
        return

    print(f"\n{'='*40}")
    if event_name:
        print(f"🎵 {event_name}")
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('-' * 40)

    for ticket in tickets:
        status = "有票" if ticket['status'] == '有票' else "售罄"
        print(f"  ¥{ticket['price']} | {ticket['name']} | {status}")

    available = [t for t in tickets if t['status'] == '有票']
    print('-' * 40)
    print(f"当前 {len(available)}/{len(tickets)} 个档位有余票")
    print('='*40)

def main():
    checker = ShowstartTicketChecker(headless=False)
    is_logged_in = checker.check_login_status()

    try:
        password = "Edgure2003"
        max_attempts = 3
        
        for attempt in range(max_attempts):
            input_pass = input("\n请输入管理员密码: ").strip()
            if input_pass == password:
                break
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"[ERROR] 密码错误，剩余尝试次数: {remaining}")
                else:
                    print("[ERROR] 密码错误次数过多，程序退出")
                    return
        
        while True:
            print("\n" + "="*70)
            print("秀动余票查询工具 v3.2|CopyRight 录音室楼下的白灯")
            print("本版本更新：1.增加了随机歌词库内的歌词")
            print("          2.增加了ChiliChill新歌《辞职信》的推广功能")
            print("          3.增加了脚本定时关闭功能")
            print("全群查秀动余票的唯一希望，每周三中午11:00-11:10脚本维护~")
            print("="*70)


            print("\n请选择操作：")
            print("  1. 查询一次余票")
            print("  2. 持续监控余票")
            print("  3. 持续监控余票 + QQ推送")
            print("  4. 故障诊断")
            print("  5. 退出\n")

            choice = input("请输入选项 (1/2/3/4/5): ").strip()

            if choice == '1':
                event_id = input("请输入演出ID（演出ID可从网址栏获取，如https://www.showstart.com/event/295821，其中最后六位数295821就是演出ID）: ").strip()
                if not event_id:
                    print("请输入有效的演出ID")
                    continue

                try:
                    print(f"\n[INFO] 正在查询该演出...")
                    tickets = checker.check_tickets(event_id)
                    
                    print_ticket_info(tickets, f"演出 {event_id}")
                    
                    if not tickets:
                        print("\n[INFO] 需要登录以查看更多票务信息")
                        checker.wait_for_login()
                        checker.save_tokens_after_login()
                        is_logged_in = True
                        print(f"\n[INFO] 登录成功，正在查询该演出的余票...")
                        tickets = checker.check_tickets(event_id)
                        print_ticket_info(tickets, f"演出 {event_id}")
                    
                    checker._close_driver()

                    input("\n按回车键继续...")
                except Exception as e:
                    print(f"\n[ERROR] 查询过程出错: {e}")
                    checker._close_driver()
                    input("\n按回车键继续...")

            elif choice == '2':
                event_id = input("请输入演出ID，演出ID可从网址栏获取，如https://www.showstart.com/event/295821，其中最后六位数295821就是演出ID: ").strip()
                if not event_id:
                    print("输错了呢，请检查后重新输入")
                    continue

                try:
                    print(f"\n[INFO] 正在查询该演出...")
                    tickets = checker.check_tickets(event_id)
                    
                    print_ticket_info(tickets, f"演出 {event_id}")
                    
                    if not tickets:
                        print("\n[INFO] 请登录查看更多票务信息")
                        checker.wait_for_login()
                        checker.save_tokens_after_login()
                        is_logged_in = True
                        print(f"\n[INFO] 登录成功，正在查询该演出的余票信息...")
                        tickets = checker.check_tickets(event_id)
                        print_ticket_info(tickets, f"演出 {event_id}")
                    
                    try:
                        interval = int(input("\n请输入查票间隔(秒，默认30): ").strip() or 30)
                    except ValueError:
                        interval = 30

                    print(f"\n[INFO] 开始监控该演出的余票情况，每 {interval} 秒检查一次...")
                    print("[INFO] 已启用防睡眠模式，电脑不会自动熄屏")
                    print("[INFO] 按 Ctrl+C 停止监控\n")

                    last_available_count = -1

                    while True:
                        try:
                            prevent_sleep()

                            tickets = checker.check_tickets(event_id)
                            
                            available_count = sum(1 for t in tickets if t['status'] == '有票')

                            current_time = datetime.now().strftime('%H:%M:%S')
                            current_timestamp = time.time()

                            if available_count > 0 and available_count != last_available_count:
                                print(f"\n[{current_time}] 🎉 检测到余票变化！")
                                print_ticket_info(tickets, f"演出 {event_id}")
                                play_notification_sound()
                                last_available_count = available_count
                            elif available_count > 0:
                                print(f"[{current_time}]  仍有余票 ({available_count}个档位)")
                                print_ticket_info(tickets, f"演出 {event_id}")
                            else:
                                print(f"[{current_time}]  暂无余票")
                                print_ticket_info(tickets, f"演出 {event_id}")

                            time.sleep(interval)
                        except KeyboardInterrupt:
                            print("\n[INFO] 监控已停止")
                            break
                        except Exception as e:
                            print(f"\n[ERROR] 监控过程出错: {e}")
                            print("[INFO] 等待5秒后继续监控...")
                            time.sleep(5)

                    allow_sleep()
                    checker._close_driver()
                    input("\n按回车键继续...")
                except Exception as e:
                    print(f"\n[ERROR] 监控初始化失败: {e}")
                    allow_sleep()
                    checker._close_driver()
                    input("\n按回车键继续...")

            elif choice == '3':
                event_id = input("请输入演出ID，演出ID可从网址栏获取，如https://www.showstart.com/event/295821，其中最后六位数295821就是演出ID: ").strip()
                if not event_id:
                    print("输错了呢，请检查后重新输入")
                    continue

                try:
                    print(f"\n[INFO] 正在查询该演出...")
                    tickets = checker.check_tickets(event_id)
                    
                    print_ticket_info(tickets, f"演出 {event_id}")
                    
                    if not tickets:
                        print("\n[INFO] 请登录查看更多票务信息")
                        checker.wait_for_login()
                        checker.save_tokens_after_login()
                        is_logged_in = True
                        print(f"\n[INFO] 登录成功，正在查询该演出的余票信息...")
                        tickets = checker.check_tickets(event_id)
                        print_ticket_info(tickets, f"演出 {event_id}")
                    
                    try:
                        interval = int(input("\n请输入查票间隔(秒，默认30): ").strip() or 30)
                    except ValueError:
                        interval = 30

                    target_groups = select_target_groups()
                    if not target_groups:
                        input("\n按回车键继续...")
                        continue

                    monitor_start_time = datetime.now().strftime('%H:%M:%S')
                    last_report_time_str = monitor_start_time
                    print(f"\n[INFO] 开始监控该演出的余票情况，每 {interval} 秒检查一次...")
                    print(f"[INFO] QQ推送目标群: {', '.join(str(g) for g in target_groups)}")
                    print("[INFO] 已启用防睡眠模式，电脑不会自动熄屏")
                    print("[INFO] 已启用后台运行模式，窗口将自动最小化")
                    print("[INFO] 按 Ctrl+C 停止监控\n")
                    
                    # 最小化浏览器窗口以实现后台运行
                    try:
                        checker.driver.minimize_window()
                    except:
                        pass
                    
                    start_msg = f"📢 秀动回流票监控已启动！\n📍 监控演出ID: {event_id}\n⏰ 监控时段: {monitor_start_time} 开始\n🔔 有回流票会第一时间通知大家！\n\n请保持关注，祝各位群友刷到回流票！🎫"
                    print(f"[QQ推送] 发送监控开始提醒:\n{start_msg}")
                    for tg in target_groups:
                        send_to_qq_group(tg, start_msg)
                    send_phone_notification("🎉 监控已启动", f"秀动回流票监控已开始!\n\n演出ID: {event_id}\n推送群数: {len(target_groups)}个\n间隔: {interval}秒")
                    show_system_notification("🎉 监控已启动", f"秀动回流票监控已开始!\n\n演出ID: {event_id}\n推送群数: {len(target_groups)}个\n间隔: {interval}秒")

                    last_available_count = -1
                    last_report_time = time.time()
                    report_interval = 300
                    has_shown_notification = False  # 是否已经显示过掉线提醒
                    maintenance_done_today = False  # 今日是否已执行维护关闭
                    confirm_count = 0  # 连续检测到有票的次数（用于双重确认）
                    CONFIRM_THRESHOLD = 2  # 需要连续检测几次有票才确认

                    try:
                        while True:
                            # 检查是否需要发送关闭通知
                            if check_and_send_shutdown_notice() and not QQ_PUSH_END_NOTICE_SENT:
                                shutdown_notice = "📢 【重要通知】📢\n\n由于该演出2026/6/7 19:00以后不再接受退票，23:00为最后一波回流票高峰，故于2026/6/8零点起正式关闭QQ群推送。\n\n请各位群友提前做好准备，祝大家都能抢到票！🎫"
                                print(f"[QQ推送] 发送关闭通知:\n{shutdown_notice}")
                                for tg in target_groups:
                                    send_to_qq_group(tg, shutdown_notice)
                                QQ_PUSH_END_NOTICE_SENT = True
                            
                            # 检查是否是周三上午10:57（维护时间前3分钟）
                            now = datetime.now()
                            if now.weekday() == 2 and now.hour == 10 and now.minute >= 57 and not maintenance_done_today:
                                print("\n[INFO] ⏰ 检测到每周三维护时间（11:00-11:10），即将自动关闭脚本进行维护...")
                                maintenance_msg = f"📢 秀动回流票监控即将暂停维护！\n⏰ 维护时间: {now.strftime('%Y-%m-%d')} 11:00 - 11:10\n🔧 每周例行维护更新，预计10分钟后恢复\n\n感谢大家的理解与支持！🙏"
                                print(f"[QQ推送] 发送维护提醒:\n{maintenance_msg}")
                                for tg in target_groups:
                                    send_to_qq_group(tg, maintenance_msg)
                                send_phone_notification("⏰ 维护提醒", f"秀动回流票监控即将暂停维护！\n\n维护时间: {now.strftime('%Y-%m-%d')} 11:00-11:10\n每周例行维护更新，预计10分钟后恢复！")
                                show_system_notification("⏰ 维护提醒", f"即将进行日常脚本维护（{now.strftime('%Y-%m-%d')} 11:00-11:10），脚本将自动关闭！")
                                maintenance_done_today = True
                                break
                            
                            # 检查是否是晚上9点（每日自动关闭）
                            if now.hour == DAILY_SHUTDOWN_HOUR and now.minute == 0 and not DAILY_SHUTDOWN_DONE:
                                print(f"\n[INFO] ⏰ 检测到每日关闭时间（{DAILY_SHUTDOWN_HOUR}:00），即将自动关闭脚本...")
                                shutdown_msg = f"📢 秀动回流票监控已结束！\n⏰ 今日监控到此结束\n感谢大家的关注，明天同一时间再见！👋"
                                print(f"[QQ推送] 发送关闭通知:\n{shutdown_msg}")
                                for tg in target_groups:
                                    send_to_qq_group(tg, shutdown_msg)
                                send_phone_notification("⏹️ 监控已结束", f"秀动回流票监控已结束!\n\n演出ID: {event_id}\n今日监控到此结束，明天见！")
                                show_system_notification("⏹️ 监控已结束", f"秀动回流票监控已结束!\n\n演出ID: {event_id}\n今日监控到此结束，明天见！")
                                DAILY_SHUTDOWN_DONE = True
                                break

                            # 心跳检测：定期检查 NapCat 连接状态
                            napcat_heartbeat()

                            try:
                                prevent_sleep()

                                tickets = checker.check_tickets(event_id)
                                
                                available_count = sum(1 for t in tickets if t['status'] == '有票')

                                current_time = datetime.now().strftime('%H:%M:%S')
                                current_timestamp = time.time()

                                if available_count > 0:
                                    # 双重确认机制：连续检测到有票才推送
                                    confirm_count += 1
                                    is_new_detection = confirm_count == CONFIRM_THRESHOLD
                                    
                                    if confirm_count < CONFIRM_THRESHOLD:
                                        # 正在确认中，只打印不推送
                                        print(f"\n[{current_time}] 🔍 检测到有票（确认中 {confirm_count}/{CONFIRM_THRESHOLD}）")
                                        print_ticket_info(tickets, f"演出 {event_id}")
                                    else:
                                        # 确认有票
                                        if is_new_detection:
                                            # 首次确认有票，发送推送
                                            print(f"\n[{current_time}] 🎉 确认有回流票！")
                                            available_tickets = [t for t in tickets if t['status'] == '有票']
                                            ticket_info = "\n".join([f"• {t['price']}元 - {t['name']}" for t in available_tickets])
                                            msg = generate_ticket_message(event_id, tickets)
                                            print(f"[QQ推送] 准备推送消息:\n{msg}")
                                            # 检查是否应该关闭QQ推送
                                            if should_disable_qq_push():
                                                print(f"[QQ推送] 已到关闭时间（2026/6/8 00:00），跳过QQ推送")
                                                all_success = True
                                            else:
                                                all_success = True
                                                for tg in target_groups:
                                                    success = send_to_qq_group(tg, msg)
                                                    if not success:
                                                        all_success = False
                                                for tg in target_groups:
                                                    send_to_qq_group(tg, NEW_SONG_PROMO_MSG)
                                            send_phone_notification(
                                                "🎉 检测到回流票！",
                                                f"演出ID: {event_id}\n\n有票档位：\n{ticket_info}\n\n快去秀动抢票！"
                                            )
                                            show_system_notification(
                                                "🎉 检测到回流票！",
                                                f"演出ID: {event_id}\n\n有票档位：\n{ticket_info}\n\n快去秀动抢票！"
                                            )
                                            if all_success:
                                                has_shown_notification = False
                                            else:
                                                if not has_shown_notification:
                                                    print(f"[警告] 部分群推送失败，可能已掉线！")
                                                    send_phone_notification(
                                                        "⚠️ QQ推送掉线提醒",
                                                        "部分群推送失败！\n\n可能原因：\n• NapCat服务已停止\n• QQ已掉线或被踢\n• 网络连接异常\n\n请检查NapCat和QQ状态！"
                                                    )
                                                    show_system_notification(
                                                            "⚠️ QQ推送掉线提醒",
                                                            "部分群推送失败！\n\n可能原因：\n• NapCat服务已停止\n• QQ已掉线或被踢\n• 网络连接异常\n\n请检查NapCat和QQ状态！"
                                                        )
                                                    has_shown_notification = True
                                        else:
                                            # 持续有票，定期推送
                                            print(f"\n[{current_time}]  仍有余票 ({available_count}个档位)")
                                            print_ticket_info(tickets, f"演出 {event_id}")
                                            if current_timestamp - last_report_time >= report_interval:
                                                msg = generate_ticket_message(event_id, tickets)
                                                print(f"[QQ推送] 准备推送消息:\n{msg}")
                                                # 检查是否应该关闭QQ推送
                                                if should_disable_qq_push():
                                                    print(f"[QQ推送] 已到关闭时间（2026/6/8 00:00），跳过QQ推送")
                                                    all_success = True
                                                else:
                                                    all_success = True
                                                    for tg in target_groups:
                                                        success = send_to_qq_group(tg, msg)
                                                        if not success:
                                                            all_success = False
                                                    for tg in target_groups:
                                                        send_to_qq_group(tg, NEW_SONG_PROMO_MSG)
                                                if all_success:
                                                    has_shown_notification = False
                                                else:
                                                    if not has_shown_notification:
                                                        print(f"[警告] 部分群推送失败，可能已掉线！")
                                                        send_phone_notification(
                                                                "⚠️ QQ推送掉线提醒",
                                                                "部分群推送失败！\n\n可能原因：\n• NapCat服务已停止\n• QQ已掉线或被踢\n• 网络连接异常\n\n请检查NapCat和QQ状态！"
                                                            )
                                                        show_system_notification(
                                                                "⚠️ QQ推送掉线提醒",
                                                                "部分群推送失败！\n\n可能原因：\n• NapCat服务已停止\n• QQ已掉线或被踢\n• 网络连接异常\n\n请检查NapCat和QQ状态！"
                                                            )
                                                        has_shown_notification = True
                                                last_report_time = current_timestamp
                                                last_report_time_str = current_time
                                    last_available_count = available_count
                                    if is_new_detection:
                                        last_report_time = current_timestamp
                                        last_report_time_str = current_time
                                else:
                                    # 无票，重置确认计数
                                    confirm_count = 0
                                    print(f"[{current_time}]  暂无余票")
                                    print_ticket_info(tickets, f"演出 {event_id}")
                                    if current_timestamp - last_report_time >= report_interval:
                                        msg = generate_ticket_message(event_id, tickets)
                                        print(f"[QQ推送] 准备推送消息:\n{msg}")
                                        # 检查是否应该关闭QQ推送
                                        if should_disable_qq_push():
                                            print(f"[QQ推送] 已到关闭时间（2026/6/8 00:00），跳过QQ推送")
                                            all_success = True
                                        else:
                                            all_success = True
                                            for tg in target_groups:
                                                success = send_to_qq_group(tg, msg)
                                                if not success:
                                                    all_success = False
                                            for tg in target_groups:
                                                send_to_qq_group(tg, NEW_SONG_PROMO_MSG)
                                        if all_success:
                                            has_shown_notification = False
                                        else:
                                            if not has_shown_notification:
                                                print(f"[警告] 部分群推送失败，可能已掉线！")
                                                send_phone_notification(
                                                    "⚠️ QQ推送掉线提醒",
                                                    "部分群推送失败！\n\n可能原因：\n• NapCat服务已停止\n• QQ已掉线或被踢\n• 网络连接异常\n\n请检查NapCat和QQ状态！"
                                                )
                                                show_system_notification(
                                                    "⚠️ QQ推送掉线提醒",
                                                    "部分群推送失败！\n\n可能原因：\n• NapCat服务已停止\n• QQ已掉线或被踢\n• 网络连接异常\n\n请检查NapCat和QQ状态！"
                                                )
                                                has_shown_notification = True
                                        last_report_time = current_timestamp
                                        last_report_time_str = current_time

                                time.sleep(interval)
                            except KeyboardInterrupt:
                                print("\n[INFO] 监控已停止")
                                break
                            except Exception as e:
                                print(f"\n[ERROR] 监控过程出错: {e}")
                                print("[INFO] 等待5秒后继续监控...")
                                time.sleep(5)
                    finally:
                        monitor_end_time = datetime.now().strftime('%H:%M:%S')
                        end_msg = f"📢 秀动回流票监控已结束！\n📍 监控演出ID: {event_id}\n⏰ 监控时段: {monitor_start_time} - {monitor_end_time}\n\n那我就先下线了，修复bug去啦！👋"
                        print(f"[QQ推送] 发送监控结束提醒:\n{end_msg}")
                        for tg in target_groups:
                            send_to_qq_group(tg, end_msg)
                        send_phone_notification("⏹️ 监控已结束", f"秀动回流票监控已结束!\n\n演出ID: {event_id}\n监控时段: {monitor_start_time} - {monitor_end_time}")
                        show_system_notification("⏹️ 监控已结束", f"秀动回流票监控已结束!\n\n演出ID: {event_id}\n监控时段: {monitor_start_time} - {monitor_end_time}")

                    allow_sleep()
                    checker._close_driver()
                    input("\n按回车键继续...")
                except Exception as e:
                    print(f"\n[ERROR] 监控初始化失败: {e}")
                    allow_sleep()
                    checker._close_driver()
                    input("\n按回车键继续...")

            elif choice == '4':
                print("\n[INFO] 正在启动系统诊断...")
                checker.run_diagnostics()
                input("\n按回车键继续...")

            elif choice == '5':
                print("感谢您的使用，祝您抢票成功，再见！")
                break

            else:
                print("无效选项，请重新输入")

    except Exception as e:
        print(f"\n[FATAL ERROR] 程序发生致命错误: {e}")
    finally:
        allow_sleep()
        checker._close_driver()
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()