#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""详细调试浏览器API请求 - 打开演出页面"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_browser_api():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--auto-open-devtools-for-tabs')
    
    # 模拟移动端
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=options)
    
    # 先打开首页登录
    driver.get("https://wap.showstart.com")
    
    input("请登录后按回车继续...")
    
    # 打开一个演出页面
    event_id = "295821"
    driver.get(f"https://wap.showstart.com/event/detail?activityId={event_id}")
    
    print("\n" + "="*80)
    print("请打开浏览器开发者工具(F12) -> Network面板")
    print("刷新页面后，查找包含 'ticket/list' 的POST请求")
    print("查看该请求的Headers和Request Payload")
    print("="*80)
    
    input("\n请分析完真实请求后按回车退出...")
    driver.quit()

if __name__ == "__main__":
    debug_browser_api()