#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""详细调试浏览器API请求"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_browser_api():
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
    driver.get("https://wap.showstart.com")
    
    input("请登录后按回车继续...")
    
    # 获取所有localStorage值
    js_get_storage = """
        var result = {};
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            result[key] = localStorage.getItem(key);
        }
        return JSON.stringify(result);
    """
    
    storage_str = driver.execute_script(js_get_storage)
    print("\n" + "="*80)
    print("浏览器localStorage内容:")
    print("="*80)
    import json
    storage = json.loads(storage_str)
    for key, value in storage.items():
        if isinstance(value, str) and len(value) > 50:
            print(f"  {key}: {value[:50]}... (长度: {len(value)})")
        else:
            print(f"  {key}: {value}")
    
    # 测试API请求
    event_id = "295821"
    js_test_api = f"""
        // 获取所有必要的token
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : (localStorage.getItem('userId') || '');
        var st_flpv = localStorage.getItem('st_flpv') || '';
        
        console.log('accessToken:', accessToken ? '有值' : '空');
        console.log('sign:', sign ? '有值' : '空');
        console.log('idToken:', idToken ? '有值' : '空');
        console.log('token:', token ? '有值' : '空');
        console.log('userId:', userId ? '有值' : '空');
        console.log('st_flpv:', st_flpv ? '有值' : '空');
        
        // 生成traceId
        var chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        var randomStr = '';
        for (var i = 0; i < 32; i++) {{
            randomStr += chars[Math.floor(Math.random() * chars.length)];
        }}
        var traceId = randomStr + Date.now();
        
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: st_flpv,
            sign: sign,
            trackPath: ''
        }});
        
        console.log('body:', body);
        
        // 使用fetch API发送请求，观察真实的错误
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        
        xhr.send(body);
        return xhr.responseText;
    """
    
    print("\n" + "="*80)
    print("简化API请求测试（仅基础头）:")
    print("="*80)
    result = driver.execute_script(js_test_api)
    print(f"响应: {result}")
    
    input("\n请在浏览器开发者工具中查看Network请求，找到正确的请求参数后按回车退出...")
    driver.quit()

if __name__ == "__main__":
    debug_browser_api()