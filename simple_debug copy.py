import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

event_id = input("请输入演出ID: ")
url = f"https://wap.showstart.com/event/{event_id}"

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

chrome_driver_paths = [
    'chromedriver.exe',
    'C:\\chromedriver\\chromedriver.exe',
    'C:\\Program Files\\chromedriver\\chromedriver.exe',
    'C:\\Users\\35184\\Documents\\trae_projects\\dmt\\chromedriver.exe'
]

driver = None
for path in chrome_driver_paths:
    if os.path.exists(path):
        try:
            service = Service(path)
            driver = webdriver.Chrome(service=service, options=options)
            print(f"使用ChromeDriver: {path}")
            break
        except Exception as e:
            print(f"尝试 {path} 失败: {e}")

if not driver:
    print("未找到ChromeDriver，尝试默认路径...")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"无法启动Chrome: {e}")
        print("请确保ChromeDriver已安装并在PATH中")
        exit(1)

print(f"正在打开: {url}")
driver.get(url)

time.sleep(3)

print("\n当前URL:", driver.current_url)
print("页面标题:", driver.title)

html = driver.page_source
print(f"\n页面内容长度: {len(html)} 字符")

lines = html.split('\n')
ticket_lines = [line.strip() for line in lines if '票' in line and len(line.strip()) < 300]

print(f"\n包含'票'的行数: {len(ticket_lines)}")
for i, line in enumerate(ticket_lines[:20]):
    print(f"{i+1}. {line[:150]}")

print("\n按回车退出...")
input()
driver.quit()
