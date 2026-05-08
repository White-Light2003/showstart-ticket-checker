import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

if len(sys.argv) < 2:
    event_id = input("请输入演出ID: ")
else:
    event_id = sys.argv[1]

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=414,736')

driver = webdriver.Chrome(options=options)

url = f"https://wap.showstart.com/event/{event_id}"

print(f"正在打开页面: {url}")
driver.get(url)
time.sleep(3)

print("\n请在浏览器中完成登录...")
print("登录完成后，手动点击'立即购票'按钮...")
print("看到票种信息后，按回车继续...")

try:
    import msvcrt
    msvcrt.getch()
except:
    input()

print("\n" + "="*60)
print("页面HTML片段（前8000字符）:")
print("="*60)

page_html = driver.page_source
print(page_html[:8000])

print("\n" + "="*60)
print("查找包含'票'和价格的行:")
print("="*60)

lines = page_html.split('\n')
for i, line in enumerate(lines):
    if '票' in line and ('¥' in line or 'price' in line.lower() or re.search(r'\d{3,4}', line)):
        print(f"行{i}: {line.strip()[:200]}")

print("\n" + "="*60)
print("查找所有价格（3-4位数字）:")
print("="*60)
prices = re.findall(r'¥(\d{3,4})', page_html)
print(f"找到价格: {prices}")

print("\n调试完成，3秒后自动关闭...")
time.sleep(3)
driver.quit()
