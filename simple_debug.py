#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单调试脚本：捕获真实API请求"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def simple_debug():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # 模拟移动端
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=options)
    
    # 打开秀动首页
    driver.get("https://wap.showstart.com")
    
    print("="*80)
    print("操作指南:")
    print("="*80)
    print("1. 在浏览器中登录您的秀动账号")
    print("2. 搜索演出并进入详情页")
    print("3. 打开浏览器开发者工具 (按 F12)")
    print("4. 切换到 Network (网络) 标签")
    print("5. 点击 '购票' 按钮")
    print("6. 在网络请求列表中找到包含 'ticket/list' 的请求")
    print("7. 右键点击该请求 -> Copy -> Copy as cURL")
    print("8. 将复制的内容粘贴到下面:")
    print("="*80)
    
    input("\n完成以上步骤后按回车继续...")
    
    # 获取当前页面的所有信息
    print("\n" + "="*80)
    print("获取当前页面信息...")
    print("="*80)
    
    # 获取localStorage
    storage = driver.execute_script("""
        var result = {};
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            result[key] = localStorage.getItem(key);
        }
        return JSON.stringify(result, null, 2);
    """)
    
    print("\n[localStorage内容]")
    print(storage)
    
    # 获取cookies
    cookies = driver.get_cookies()
    print("\n[cookies内容]")
    for cookie in cookies:
        print(f"  {cookie['name']}: {cookie['value']}")
    
    # 获取当前URL
    print(f"\n[当前页面URL]")
    print(f"  {driver.current_url}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    simple_debug()