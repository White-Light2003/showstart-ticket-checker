#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""详细调试API请求参数"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_api_params():
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
    
    # 获取所有信息
    print("\n" + "="*80)
    print("获取浏览器中的所有信息...")
    print("="*80)
    
    # 获取localStorage
    storage = driver.execute_script("""
        var result = {};
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            result[key] = localStorage.getItem(key);
        }
        return JSON.stringify(result);
    """)
    storage = json.loads(storage)
    
    print("\n[localStorage]")
    for k, v in sorted(storage.items()):
        if isinstance(v, str) and len(v) > 50:
            print(f"  {k}: {v[:50]}... (长度: {len(v)})")
        else:
            print(f"  {k}: {v}")
    
    # 获取userInfo详情
    print("\n[userInfo详情]")
    user_info_str = storage.get('userInfo', '{}')
    try:
        user_info = json.loads(user_info_str)
        print(f"  完整内容: {json.dumps(user_info, indent=2, ensure_ascii=False)}")
    except:
        print(f"  解析失败: {user_info_str[:100]}...")
    
    # 获取cookie
    print("\n[cookies]")
    cookies = driver.get_cookies()
    for cookie in cookies:
        print(f"  {cookie['name']}: {cookie['value'][:50]}...")
    
    # 测试各种参数组合
    event_id = "295821"
    
    print("\n" + "="*80)
    print("测试API请求参数...")
    print("="*80)
    
    # 测试1: 使用所有可用参数
    js_test1 = f"""
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : (localStorage.getItem('userId') || '');
        var st_flpv = localStorage.getItem('st_flpv') || '';
        
        console.log('accessToken:', accessToken);
        console.log('sign:', sign);
        console.log('idToken:', idToken);
        console.log('token:', token);
        console.log('userId:', userId);
        console.log('st_flpv:', st_flpv);
        
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: st_flpv,
            sign: sign,
            trackPath: '',
            deviceType: 'H5',
            channel: 'H5',
            terminal: 'wap',
            appId: 'wap',
            version: '997',
            userId: userId
        }});
        
        console.log('Request body:', body);
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('CTERMINAL', 'wap');
        xhr.setRequestHeader('CSAPPID', 'wap');
        xhr.setRequestHeader('CVERSION', '997');
        xhr.setRequestHeader('CUSAT', accessToken);
        xhr.setRequestHeader('CUSUT', sign);
        xhr.setRequestHeader('CUSIT', idToken);
        xhr.setRequestHeader('CUSID', userId);
        xhr.setRequestHeader('CDEVICENO', token);
        xhr.setRequestHeader('st_flpv', st_flpv);
        xhr.withCredentials = true;
        
        xhr.send(body);
        
        console.log('Response status:', xhr.status);
        console.log('Response:', xhr.responseText);
        
        return xhr.responseText;
    """
    
    result1 = driver.execute_script(js_test1)
    print(f"\n测试1响应: {result1}")
    
    # 测试2: 尝试不同的API端点
    print("\n" + "="*80)
    print("测试不同API端点...")
    print("="*80)
    
    endpoints = [
        'https://wap.showstart.com/v3/wap/activity/V2/ticket/list',
        'https://www.showstart.com/v3/wap/activity/V2/ticket/list',
        'https://wap.showstart.com/v3/activity/V2/ticket/list'
    ]
    
    for endpoint in endpoints:
        js_test = f"""
            var accessToken = localStorage.getItem('accessToken') || '';
            var sign = localStorage.getItem('sign') || '';
            var idToken = localStorage.getItem('idToken') || '';
            var token = localStorage.getItem('token') || '';
            var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
            var userInfo = JSON.parse(userInfoStr);
            var userId = userInfo.data ? userInfo.data.userId : '';
            var st_flpv = localStorage.getItem('st_flpv') || '';
            
            var body = JSON.stringify({{
                activityId: '{event_id}',
                coupon: '',
                st_flpv: st_flpv,
                sign: sign,
                trackPath: ''
            }});
            
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '{endpoint}', false);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('CTERMINAL', 'wap');
            xhr.setRequestHeader('CSAPPID', 'wap');
            xhr.setRequestHeader('CVERSION', '997');
            xhr.setRequestHeader('CUSAT', accessToken);
            xhr.setRequestHeader('CUSUT', sign);
            xhr.setRequestHeader('CUSIT', idToken);
            xhr.setRequestHeader('CUSID', userId);
            xhr.setRequestHeader('CDEVICENO', token);
            xhr.withCredentials = true;
            
            xhr.send(body);
            return '{{"endpoint": "{endpoint}", "status": ' + xhr.status + ', "response": ' + (xhr.responseText || '"empty"') + '}}';
        """
        
        result = driver.execute_script(js_test)
        print(f"\n端点: {endpoint}")
        print(f"响应: {result}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    debug_api_params()