#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速获取秀动token
"""
import time
import json
import os
from datetime import datetime

def main():
    print("=" * 50)
    print("秀动Token获取工具")
    print("=" * 50)
    print()
    print("即将打开浏览器，请在浏览器中登录")
    print("登录成功后，按回车键继续")
    print()
    
    # 使用Selenium启动浏览器
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.showstart.com")
    
    input("登录成功后，请按回车键继续...")
    
    # 获取所有token，包括从userInfo中解析userId
    tokens = driver.execute_script("""
        var userInfoStr = localStorage.getItem('userInfo') || '{}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        return {
            accessToken: localStorage.getItem('accessToken') || '',
            sign: localStorage.getItem('sign') || '',
            idToken: localStorage.getItem('idToken') || '',
            token: localStorage.getItem('token') || '',
            st_flpv: localStorage.getItem('st_flpv') || '',
            userId: userId || localStorage.getItem('userId') || ''
        };
    """)
    
    driver.quit()
    
    print()
    print("=" * 50)
    print("获取到的Token：")
    print("=" * 50)
    print(f"accessToken: {tokens['accessToken'][:30]}..." if tokens['accessToken'] else "accessToken: 未获取")
    print(f"sign: {tokens['sign'][:30]}..." if tokens['sign'] else "sign: 未获取")
    print(f"idToken: {tokens['idToken'][:30]}..." if tokens['idToken'] else "idToken: 未获取")
    print(f"token: {tokens['token'][:30]}..." if tokens['token'] else "token: 未获取")
    print(f"st_flpv: {tokens['st_flpv'][:30]}..." if tokens['st_flpv'] else "st_flpv: 未获取")
    print(f"userId: {tokens['userId']}")
    print("=" * 50)
    
    # 保存到config.json
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"✅ Token已保存到: {config_path}")
    
    # 也保存到~/.showstart_checker/tokens.json
    config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
    os.makedirs(config_dir, exist_ok=True)
    tokens_path = os.path.join(config_dir, 'tokens.json')
    with open(tokens_path, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Token已保存到: {tokens_path}")
    print()
    print("现在你可以运行主程序了！")

if __name__ == "__main__":
    main()
