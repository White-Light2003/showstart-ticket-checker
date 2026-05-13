#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取真实API请求参数"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_real_request_params():
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
    
    # 打开演出详情页面
    event_id = "295821"
    driver.get(f"https://wap.showstart.com/pages/activity/detail/detail?activityId={event_id}")
    
    print("="*80)
    print("🎯 获取真实API请求参数指南")
    print("="*80)
    print("")
    print("请按照以下步骤操作:")
    print("")
    print("1. 🔐 登录您的秀动账号")
    print("2. 🛠️ 打开浏览器开发者工具 (按 F12)")
    print("3. 🔄 切换到 'Network' (网络) 标签")
    print("4. 🎫 点击页面上的 '立即购票' 按钮")
    print("5. 🔍 在网络请求列表中搜索 'ticket/list'")
    print("6. 📋 找到请求后，右键点击 -> Copy -> Copy as cURL")
    print("7. 📧 将复制的内容粘贴到这里:")
    print("")
    print("="*80)
    
    # 让用户输入cURL内容
    curl_content = input("请粘贴cURL内容: ")
    
    print("\n" + "="*80)
    print("分析cURL内容...")
    print("="*80)
    
    # 解析cURL内容
    if curl_content:
        # 提取URL
        url_start = curl_content.find("'https://") + 1
        url_end = curl_content.find("'", url_start)
        if url_start > 0 and url_end > url_start:
            url = curl_content[url_start:url_end]
            print(f"\n📡 请求URL: {url}")
        
        # 提取请求体
        body_start = curl_content.find("--data-raw '") + len("--data-raw '")
        body_end = curl_content.rfind("'")
        if body_start > len("--data-raw '") and body_end > body_start:
            body = curl_content[body_start:body_end]
            print(f"\n📝 请求体: {body}")
        
        # 提取请求头
        print("\n📄 请求头:")
        import re
        headers = re.findall(r"-H '([^']+)'", curl_content)
        for header in headers:
            print(f"  {header}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    get_real_request_params()