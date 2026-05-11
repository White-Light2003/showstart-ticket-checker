#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""捕获并复制浏览器的真实API请求"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def capture_and_replay():
    """捕获浏览器请求并重放"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import requests

    print("启动浏览器捕获API请求...")

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

    # 注入请求拦截脚本
    driver.execute_script("""
    window.__capturedRequests = [];
    window.__originalFetch = window.fetch;
    window.fetch = async function(url, options) {
        if (url.includes('/ticket/list')) {
            var headersObj = {};
            if (options.headers) {
                options.headers.forEach(function(value, key) {
                    headersObj[key] = value;
                });
            }
            window.__capturedRequests.push({
                url: url,
                headers: headersObj,
                body: typeof options.body === 'string' ? options.body : JSON.stringify(options.body),
                method: options.method || 'GET'
            });
        }
        return window.__originalFetch(url, options);
    };
    console.log('API拦截已启动');
    """)

    # 访问活动页面
    driver.get("https://www.showstart.com/activity/295821")

    input("\n请登录并刷新页面，然后按回车继续...")

    # 获取捕获的请求
    captured = driver.execute_script("return window.__capturedRequests || []")
    
    driver.quit()

    if captured:
        print(f"\n捕获到 {len(captured)} 个请求")
        
        # 选择第一个ticket/list请求
        ticket_req = None
        for req in captured:
            if '/ticket/list' in req['url']:
                ticket_req = req
                break

        if ticket_req:
            print("\n" + "="*70)
            print("捕获到的ticket/list请求:")
            print("="*70)
            print(f"URL: {ticket_req['url']}")
            print("\n请求头:")
            for k, v in ticket_req['headers'].items():
                print(f"  {k}: {v}")
            print(f"\n请求体: {ticket_req['body']}")

            # 保存到文件
            with open('captured_request.json', 'w', encoding='utf-8') as f:
                json.dump(ticket_req, f, indent=2, ensure_ascii=False)
            print("\n✅ 请求已保存到 captured_request.json")

            # 尝试重放请求
            print("\n" + "="*70)
            print("尝试重放捕获的请求...")
            print("="*70)
            try:
                resp = requests.post(
                    ticket_req['url'],
                    data=ticket_req['body'],
                    headers=ticket_req['headers'],
                    timeout=15
                )
                print(f"HTTP状态: {resp.status_code}")
                print(f"响应: {resp.text}")
            except Exception as e:
                print(f"重放失败: {e}")
        else:
            print("未找到ticket/list请求")
    else:
        print("未捕获到任何请求")

if __name__ == "__main__":
    capture_and_replay()