#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""捕获浏览器的真实API请求"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def capture_request():
    """使用浏览器捕获API请求"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

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
            console.log('=== API请求捕获 ===');
            console.log('URL:', url);
            console.log('Headers:', JSON.stringify(options.headers || {}));
            console.log('Body:', typeof options.body === 'string' ? options.body : JSON.stringify(options.body));
            
            window.__capturedRequests.push({
                url: url,
                headers: Object.fromEntries(options.headers || {}),
                body: typeof options.body === 'string' ? options.body : JSON.stringify(options.body),
                timestamp: Date.now()
            });
        }
        return window.__originalFetch(url, options);
    };
    console.log('API请求拦截已启动');
    """)

    # 访问活动页面
    driver.get("https://www.showstart.com/activity/295821")

    input("\n请在浏览器中完成登录，然后打开开发者工具查看Network\n找到包含'ticket/list'的请求后按回车继续...")

    # 获取捕获的请求
    captured = driver.execute_script("return window.__capturedRequests || []")
    
    driver.quit()

    if captured:
        print("\n" + "="*70)
        print("捕获到的API请求详情：")
        print("="*70)
        
        for i, req in enumerate(captured):
            print(f"\n[请求 {i+1}]")
            print(f"URL: {req['url']}")
            print("\n请求头:")
            for k, v in req['headers'].items():
                if k.lower() in ['cusat', 'cusut', 'cusit', 'cusid', 'cdeviceno', 'crpsign', 'crtraceid']:
                    print(f"  {k}: {v[:30]}...")
                else:
                    print(f"  {k}: {v}")
            
            print("\n请求体:")
            try:
                body = json.loads(req['body'])
                print(json.dumps(body, indent=2, ensure_ascii=False))
            except:
                print(req['body'])
    else:
        print("\n未捕获到API请求")

if __name__ == "__main__":
    capture_request()