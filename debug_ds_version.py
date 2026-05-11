#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试DS版本问题"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chrome_driver():
    """测试Chrome驱动是否正常"""
    print("=" * 60)
    print("测试1: 检查Chrome浏览器")
    print("=" * 60)

    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if os.path.exists(chrome_path):
        print(f"[OK] Chrome路径存在: {chrome_path}")
    else:
        print(f"[FAIL] Chrome路径不存在: {chrome_path}")
        alternative_paths = [
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ]
        for path in alternative_paths:
            if os.path.exists(path):
                print(f"[OK] 找到替代Chrome: {path}")
                break
        else:
            print("[FAIL] 无法找到Chrome浏览器")

    print("\n" + "=" * 60)
    print("测试2: 检查ChromeDriver")
    print("=" * 60)

    local_driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
    if os.path.exists(local_driver):
        print(f"[OK] 本地chromedriver存在: {local_driver}")
    else:
        print(f"[FAIL] 本地chromedriver不存在: {local_driver}")

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("[OK] webdriver-manager已安装")
    except ImportError:
        print("[FAIL] webdriver-manager未安装")

    print("\n" + "=" * 60)
    print("测试3: 尝试初始化Chrome驱动")
    print("=" * 60)

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        if os.path.exists(local_driver):
            service = Service(local_driver)
            print(f"使用本地chromedriver: {local_driver}")
        else:
            driver_path = ChromeDriverManager().install()
            service = Service(driver_path)
            print(f"使用webdriver-manager下载的chromedriver: {driver_path}")

        print("正在创建Chrome驱动...")
        driver = webdriver.Chrome(service=service, options=options)
        print("[OK] Chrome驱动创建成功!")

        print("\n正在访问秀动网站...")
        driver.get("https://www.showstart.com")
        print(f"[OK] 页面标题: {driver.title}")
        print(f"[OK] 当前URL: {driver.current_url}")

        driver.quit()
        print("\n[OK] 浏览器测试完成!")

    except Exception as e:
        print(f"[FAIL] Chrome驱动初始化失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("测试4: API请求测试")
    print("=" * 60)

    config_path = os.path.join(os.path.expanduser('~'), '.showstart_checker', 'tokens.json')
    if os.path.exists(config_path):
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            tokens = json.load(f)
        print(f"[OK] 找到tokens配置: {list(tokens.keys())}")
        print(f"   - accessToken: {tokens.get('accessToken', '')[:20]}...")
        print(f"   - sign: {tokens.get('sign', '')[:20]}...")
        print(f"   - idToken: {tokens.get('idToken', '')[:20]}...")
        print(f"   - userId: {tokens.get('userId', '')}")
        print(f"   - token: {tokens.get('token', '')[:20]}...")
    else:
        print(f"[FAIL] tokens配置文件不存在: {config_path}")
        print("请先运行get_tokens.py获取token")

if __name__ == "__main__":
    test_chrome_driver()