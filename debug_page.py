from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

print("正在打开页面...")
driver.get("https://www.showstart.com/event/detail/295821")
time.sleep(5)

print("\n" + "="*60)
print("页面标题:", driver.title)
print("="*60)

print("\n正在搜索页面中的票务相关内容...")

html = driver.page_source

import re

print("\n--- 搜索价格相关 (¥ 或 price) ---")
price_matches = re.findall(r'[¥¥]?\d{3,4}元?|price["\s:]+(\d+)', html)
print(f"找到 {len(price_matches)} 处: {price_matches[:20]}")

print("\n--- 搜索剩余票数相关 ---")
stock_matches = re.findall(r'剩余\s*(\d+)|stock["\s:]+(\d+)|库存[：:]\s*(\d+)', html)
print(f"找到 {len(stock_matches)} 处: {stock_matches[:20]}")

print("\n--- 搜索可能的class名称 ---")
class_matches = re.findall(r'class="([^"]*(?:ticket|票|price|price|remain|stock)[^"]*)"', html, re.IGNORECASE)
print(f"找到 {len(class_matches)} 个相关class: {class_matches[:20]}")

print("\n--- 搜索票档/票种相关文字 ---")
ticket_text = re.findall(r'[^<>]*(?:票档|票种|票价|档位)[^<>]*', html)
print(f"找到 {len(ticket_text)} 处: {ticket_text[:10]}")

print("\n--- 打印页面中包含数字的行 ---")
lines_with_numbers = [line.strip() for line in html.split('\n') if re.search(r'\d{3,4}', line) and len(line.strip()) < 200]
for line in lines_with_numbers[:30]:
    print(line)

driver.quit()
print("\n调试完成!")
