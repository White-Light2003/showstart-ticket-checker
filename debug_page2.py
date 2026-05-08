import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

print("正在打开页面...")
driver.get("https://www.showstart.com/event/295821")
time.sleep(5)

print("\n页面标题:", driver.title)
print("当前URL:", driver.current_url)

html = driver.page_source

import re

print("\n--- 搜索价格 ---")
prices = re.findall(r'[¥¥](\d{3,4})', html)
print(f"找到价格: {prices}")

print("\n--- 搜索所有数字 ---")
nums = re.findall(r'\d{3,4}', html)
print(f"找到数字: {nums[:20]}")

print("\n--- 搜索关键字 ---")
keywords = ['票', 'ticket', 'price', 'stock', '剩余']
for kw in keywords:
    count = html.lower().count(kw.lower())
    print(f"'{kw}' 出现 {count} 次")

driver.quit()
print("\n调试完成!")
