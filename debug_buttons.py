import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=414,896')
options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')

driver = webdriver.Chrome(options=options)

print("正在打开页面...")
driver.get("https://wap.showstart.com/event/295821")
time.sleep(5)

print("\n" + "="*60)
print("页面元素分析")
print("="*60)

print("\n--- 查找所有div元素 ---")
divs = driver.find_elements(By.TAG_NAME, 'div')
print(f"找到 {len(divs)} 个div元素")

print("\n--- 查找包含'购票'文本的元素 ---")
elements = driver.find_elements(By.XPATH, '//*[contains(text(), "购票")]')
print(f"找到 {len(elements)} 个包含'购票'的元素:")
for i, elem in enumerate(elements):
    text = elem.text.strip()
    tag = elem.tag_name
    cls = elem.get_attribute('class')
    print(f"  {i+1}. {tag}: '{text}' - class: {cls}")

print("\n--- 查找带有onclick的元素 ---")
onclick_elements = driver.find_elements(By.XPATH, '//*[@onclick]')
print(f"找到 {len(onclick_elements)} 个带onclick的元素")

print("\n--- 查找class包含btn或button的元素 ---")
btn_elements = driver.find_elements(By.CSS_SELECTOR, '[class*="btn"], [class*="button"], [class*="Button"]')
print(f"找到 {len(btn_elements)} 个按钮样式元素:")
for i, elem in enumerate(btn_elements[:10]):
    text = elem.text.strip()[:30]
    cls = elem.get_attribute('class')[:50]
    print(f"  {i+1}. '{text}' - class: {cls}")

print("\n--- 打印页面源码片段（包含购票的行）---")
html = driver.page_source
lines = html.split('\n')
print("包含'购票'的行:")
for line in lines:
    if '购票' in line and len(line) < 200:
        print(line.strip())

driver.quit()
print("\n调试完成!")
