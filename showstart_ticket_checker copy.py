import time
import subprocess
from datetime import datetime
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ShowstartTicketChecker:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.price_tiers = [880, 780, 580, 480, 380, 280]
        self.driver = None

    def _init_driver(self):
        """初始化Chrome驱动"""
        if self.driver:
            return

        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=414,896')
        options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')

        self.driver = webdriver.Chrome(options=options)

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
        print("\n⏳ 请在弹出的浏览器窗口中完成登录操作")
        print("   1. 输入手机号并获取验证码")
        print("   2. 输入验证码并勾选同意协议")
        print("   3. 点击'立即登录'")
        print("\n登录成功后，请回到命令行按回车键继续...")
        input()

    def get_ticket_page(self, event_id: str, require_login: bool = True) -> bool:
        """打开票务页面"""
        self._init_driver()

        if require_login:
            self.driver.get(f"https://wap.showstart.com/event/{event_id}")
            time.sleep(3)
            self.wait_for_login()

        url = f"https://wap.showstart.com/event/{event_id}"

        try:
            self.driver.get(url)
            time.sleep(3)

            try:
                buy_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "购票") or contains(text(), "立即购票") or contains(text(), "预约")]'))
                )
                buy_btn.click()
                time.sleep(3)
                print("[OK] 已点击购票/预约按钮")
            except Exception as e:
                try:
                    btns = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.btn'))
                    )
                    for btn in btns:
                        text = btn.text.strip()
                        if '购票' in text or '预约' in text:
                            btn.click()
                            time.sleep(3)
                            print(f"[OK] 已点击'{text}'按钮")
                            break
                    else:
                        raise Exception("未找到包含购票文本的按钮")
                except Exception as e2:
                    try:
                        btns = self.driver.find_elements(By.CSS_SELECTOR, '.btn')
                        if len(btns) >= 2:
                            btns[1].click()
                            time.sleep(3)
                            print("[OK] 已点击第二个btn按钮（立即购票）")
                        else:
                            raise Exception("btn按钮数量不足")
                    except Exception as e3:
                        print(f"[WARN] 未找到购票按钮，尝试直接解析页面: {e3}")

            return True
        except Exception as e:
            print(f"[ERR] 打开页面失败: {e}")
            return False

    def parse_tickets(self, debug=False) -> List[Dict]:
        """解析页面中的票务信息 - 动态获取实际票种"""
        time.sleep(2)
        page_html = self.driver.page_source
        import re

        # 使用JavaScript获取页面上的所有文本内容
        all_text = self.driver.execute_script(
            "return document.body.innerText || document.documentElement.innerText;"
        )
        
        # 调试输出
        if debug:
            print("\n" + "="*60)
            print("调试：页面文本中包含'票'和价格的片段:")
            print("="*60)
            
            # 查找所有价格
            prices = re.findall(r'[¥¥](\d{3,4})', all_text)
            print(f"找到的价格: {prices}")
            
            # 查找包含"票"的文本
            ticket_names = re.findall(r'([^\s]{2,20}?票)', all_text)
            print(f"找到的票种名称: {ticket_names}")
            
            # 查找票和价格相邻的情况
            lines = all_text.split('\n')
            for line in lines[:50]:
                if '票' in line and ('¥' in line or re.search(r'\d{3,4}', line)):
                    print(f"{line.strip()[:150]}")
            
            print("="*60 + "\n")

        # 从文本中提取票种和价格
        found_tickets = {}
        
        # 支持多种价格符号
        price_symbols = r'[¥¥$\uFFE5]'
        
        # 模式1：票种名称 价格（更严格）
        patterns = [
            rf'([^\s]{2,20}?票)\s*{price_symbols}(\d{{3,4}})',
            rf'{price_symbols}(\d{{3,4}})\s*([^\s]{2,20}?票)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, all_text)
            for match in matches:
                if len(match) == 2:
                    if '票' in match[0]:
                        name, price_str = match[0], match[1]
                    else:
                        price_str, name = match[0], match[1]
                    
                    price_int = int(price_str) if price_str.isdigit() else int(''.join(filter(str.isdigit, price_str)))
                    # 严格限制价格范围：100-1000元
                    if 100 <= price_int <= 1000 and name.strip():
                        clean_name = re.sub(r'^[\s¥¥$\uFFE5\d]+', '', name.strip())
                        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
                        if clean_name and price_int not in found_tickets:
                            found_tickets[price_int] = {
                                'price': price_int,
                                'name': clean_name if clean_name else f'{price_int}元票',
                                'remaining': 0,
                                'status': '售罄'
                            }

        # 额外尝试：直接从页面HTML中查找价格（更严格）
        if len(found_tickets) < 2:
            # 查找数字价格，必须跟在价格符号或price关键字后面
            all_prices = []
            
            # 从price关键字后找
            price_matches = re.findall(r'(?:price|Price|PRICE)\s*[=:]\s*["\']?(\d{3,4})', page_html)
            all_prices.extend(price_matches)
            
            # 从JSON格式中找
            json_prices = re.findall(r'"price"\s*:\s*(\d{3,4})', page_html)
            all_prices.extend(json_prices)
            
            # 从¥符号后找
            yen_prices = re.findall(r'[¥¥]\s*(\d{3,4})', page_html)
            all_prices.extend(yen_prices)
            
            for p in all_prices:
                price_int = int(p)
                # 严格限制价格范围
                if 100 <= price_int <= 1000 and price_int not in found_tickets:
                    found_tickets[price_int] = {
                        'price': price_int,
                        'name': f'{price_int}元票',
                        'remaining': 0,
                        'status': '售罄'
                    }

        # 如果通过文本没找到，尝试通过HTML元素
        if not found_tickets:
            try:
                elements = self.driver.find_elements(By.XPATH, '//*[contains(text(), "票")]')
                for elem in elements:
                    text = elem.text.strip()
                    if text and '票' in text:
                        # 从元素附近找价格
                        price_match = re.search(r'[¥¥](\d{3,4})', text)
                        if price_match:
                            price_int = int(price_match.group(1))
                            name = re.search(r'([^\s]{2,20}?票)', text)
                            name = name.group(1) if name else f'{price_int}元票'
                            if 100 <= price_int <= 3000 and price_int not in found_tickets:
                                found_tickets[price_int] = {
                                    'price': price_int,
                                    'name': name,
                                    'remaining': 0,
                                    'status': '售罄'
                                }
            except Exception as e:
                print(f"通过元素查找失败: {e}")

        # 判断状态
        if '票已售罄' in all_text or '已售罄' in all_text:
            # 简单处理：如果有"售罄"文字，检查每个价格附近是否有
            for price in list(found_tickets.keys()):
                price_str = str(price)
                # 在文本中查找价格和售罄的位置
                price_pos = all_text.find(price_str)
                sold_out_pos = all_text.find('票已售罄')
                
                if price_pos != -1 and sold_out_pos != -1:
                    # 如果售罄在价格附近，认为是售罄
                    if abs(price_pos - sold_out_pos) < 1000:
                        found_tickets[price]['status'] = '售罄'
                    else:
                        found_tickets[price]['status'] = '有票'
                else:
                    found_tickets[price]['status'] = '有票'
        else:
            for price in found_tickets:
                found_tickets[price]['status'] = '有票'

        # 如果还是没找到，用价格列表作为默认
        if not found_tickets:
            prices = re.findall(r'[¥¥](\d{3,4})', all_text)
            for p in prices:
                price_int = int(p)
                if 100 <= price_int <= 3000:
                    if price_int not in found_tickets:
                        found_tickets[price_int] = {
                            'price': price_int,
                            'name': f'{price_int}元票',
                            'remaining': 0,
                            'status': '售罄'
                        }

        results = sorted(found_tickets.values(), key=lambda x: x['price'], reverse=True)

        if not results:
            print("[WARN] 未能在页面中找到票种信息，请检查页面是否正确加载")
            print("[INFO] 提示：如果只看到部分票种，可能是账号未实名认证导致的权限限制")
            print("   请使用已实名认证的账号登录后重试")

        return results

    def check_tickets(self, event_id: str, debug=False) -> Optional[List[Dict]]:
        """检查余票"""
        if not self.get_ticket_page(event_id):
            return None

        return self.parse_tickets(debug=debug)

    def display_tickets(self, results: List[Dict], event_name: str = "演出"):
        """显示余票查询结果"""
        print("\n" + "=" * 60)
        print(f"🎵 {event_name}")
        print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        for ticket in results:
            price = ticket['price']
            status = ticket['status']
            remaining = ticket['remaining']
            name = ticket['name']

            if status == '有票':
                status_display = f"[OK] 有票 (剩余 {remaining} 张)"
            elif status == '售罄':
                status_display = "[NO] 售罄"
            else:
                status_display = "[--] 不存在"

            print(f"  {price:>4}元档 | {name:<15} | {status_display}")

        available_tickets = [t for t in results if t['status'] == '有票']
        print("-" * 60)
        if available_tickets:
            print(f"[INFO] 当前有 {len(available_tickets)} 个票价档次有余票")
        else:
            print("[INFO] 目前所有档次均无余票")
        print("=" * 60)

    def monitor_tickets(self, event_id: str, event_name: str = "演出", interval: int = 30, duration: int = 3600):
        """持续监控余票状态"""
        print(f"\n🔄 开始监控 {event_name} 的余票情况...")
        print(f"   监控间隔: {interval}秒 | 总监控时长: {duration}秒")
        print("   按 Ctrl+C 停止监控\n")

        start_time = time.time()
        last_status = {}
        first_check = True

        try:
            while time.time() - start_time < duration:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 正在检查余票...")

                if not self.get_ticket_page(event_id, require_login=first_check):
                    print("[ERR] 页面加载失败，等待重试...")
                    time.sleep(interval)
                    continue

                first_check = False

                results = self.parse_tickets()
                self.display_tickets(results, event_name)

                for ticket in results:
                    price = ticket['price']
                    status = ticket['status']
                    remaining = ticket['remaining']

                    if price in last_status:
                        prev_status = last_status[price]
                        if prev_status['status'] != status or prev_status['remaining'] != remaining:
                            if status == '有票' and prev_status['status'] != '有票':
                                print(f"\n[ALERT] 【重要提醒】{price}元档有票了！剩余 {remaining} 张\n")
                            elif status == '有票' and remaining > prev_status['remaining']:
                                print(f"\n[INFO] 【提醒】{price}元档余票增加：{prev_status['remaining']} -> {remaining}\n")
                            elif status == '售罄' and prev_status['status'] == '有票':
                                print(f"\n[WARN] 【提醒】{price}元档售罄了！\n")

                    last_status[price] = {'status': status, 'remaining': remaining}

                elapsed = int(time.time() - start_time)
                remaining_time = duration - elapsed
                if remaining_time > interval:
                    print(f"⏳ 下次刷新: {interval}秒后 (剩余监控时间: {remaining_time}秒)")
                    time.sleep(interval)
                else:
                    break

        except KeyboardInterrupt:
            print("\n\n[INFO] 监控已停止")
        finally:
            self._close_driver()

    def __del__(self):
        self._close_driver()


def find_chrome_path():
    """查找Chrome路径"""
    import os
    paths = [
        os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def main():
    checker = ShowstartTicketChecker(headless=False)

    print("\n" + "=" * 60)
    print("[音乐] 秀动余票查询工具 v2.0 (Selenium版)")
    print("=" * 60)

    event_id = input("\n请输入演出ID (如 295821): ").strip()

    if not event_id:
        print("[ERR] 演出ID不能为空")
        return

    print("\n请选择操作：")
    print("  1. 查询一次余票")
    print("  2. 持续监控余票 (变化时提醒)")
    print("  3. 退出\n")

    choice = input("请输入选项 (1-3): ").strip()

    event_name = input("请输入演出名称（用于显示，可跳过）: ").strip() or "未知演出"

    if choice == '1':
        print("\n[INFO] 正在查询，请稍候...")
        results = checker.check_tickets(event_id, debug=True)

        if results:
            checker.display_tickets(results, event_name)
            print("\n按回车键退出...")
            input()
        else:
            print("\n[ERR] 查询失败，请检查演出ID是否正确")
            print("按回车键退出...")
            input()

    elif choice == '2':
        interval = input("刷新间隔（秒，默认30）: ").strip()
        interval = int(interval) if interval.isdigit() else 30

        duration = input("监控时长（秒，默认3600=1小时）: ").strip()
        duration = int(duration) if duration.isdigit() else 3600

        checker.monitor_tickets(event_id, event_name, interval=interval, duration=duration)

    elif choice == '3':
        print("\n[INFO] 再见！")
    else:
        print("\n[ERR] 无效选项")

    checker._close_driver()


if __name__ == "__main__":
    main()
