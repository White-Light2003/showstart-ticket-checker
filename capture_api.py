#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用浏览器捕获秀动API请求，对比分析必需参数
"""
import os
import sys
import json
import time
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def capture_api_request():
    """使用浏览器捕获API请求"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver.webdriver.chrome import ChromeDriverManager

    print("启动浏览器捕获API请求...")
    print("请在浏览器中访问秀动活动页面，登录后按回车继续")
    print()

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    local_driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
    if os.path.exists(local_driver):
        service = Service(local_driver)
    else:
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=options)

    # 注入脚本监听fetch
    driver.execute_script("""
    window.__apiCalls = [];
    window.__originalFetch = window.fetch;
    window.fetch = async function(url, options) {
        if (url.includes('/wap/activity/V2/ticket/list')) {
            console.log('API Call Detected:', url);
            console.log('Options:', JSON.stringify(options));
            window.__apiCalls.push({
                url: url,
                options: options,
                timestamp: Date.now()
            });
        }
        return window.__originalFetch(url, options);
    };
    console.log('API监听已启动');
    """)

    input("\n请在浏览器中访问任意活动的票务页面（如 https://www.showstart.com/activity/295821）\n登录后按回车继续...")

    # 获取捕获的请求
    api_calls = driver.execute_script("return window.__apiCalls || []")

    driver.quit()

    if api_calls:
        print("\n" + "=" * 60)
        print("捕获到的API请求：")
        print("=" * 60)
        for i, call in enumerate(api_calls):
            print(f"\n请求 {i+1}:")
            print(f"URL: {call['url']}")
            print(f"Options: {json.dumps(call['options'], indent=2, ensure_ascii=False)}")
    else:
        print("\n未捕获到API请求，请确保访问了正确的页面")

    return api_calls

def compare_with_our_request():
    """对比我们的请求和真实请求"""
    print("\n" + "=" * 60)
    print("我们的请求参数：")
    print("=" * 60)

    config_path = os.path.join(os.path.expanduser('~'), '.showstart_checker', 'tokens.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            tokens = json.load(f)

        event_id = "295821"
        url_path = '/wap/activity/V2/ticket/list'
        full_url = 'https://wap.showstart.com/v3' + url_path

        body_dict = {
            'activityId': str(event_id),
            'coupon': '',
            'st_flpv': tokens.get('st_flpv', ''),
            'sign': tokens.get('sign', ''),
            'trackPath': ''
        }

        print(f"URL: {full_url}")
        print(f"Body: {json.dumps(body_dict, separators=(',', ':'), ensure_ascii=False)}")
        print(f"Headers:")
        print(f"  CUSAT: {tokens.get('accessToken', '')[:20]}...")
        print(f"  CUSUT: {tokens.get('sign', '')[:20]}...")
        print(f"  CUSIT: {tokens.get('idToken', '')[:20]}...")
        print(f"  CUSID: {tokens.get('userId', '')}")
        print(f"  CDEVICENO: {tokens.get('token', '')[:20]}...")

if __name__ == "__main__":
    print("=" * 60)
    print("API请求捕获工具")
    print("=" * 60)
    print()
    print("此工具会打开浏览器，请手动访问秀动活动的票务页面")
    print("脚本会捕获实际的API请求，便于对比分析")
    print()

    capture_api_request()
    compare_with_our_request()