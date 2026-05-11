#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单测试浏览器API请求"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_browser_api():
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
    
    # 先打开首页登录
    driver.get("https://wap.showstart.com")
    
    input("请登录后按回车继续...")
    
    # 获取localStorage中的值
    storage = driver.execute_script("""
        var result = {};
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            result[key] = localStorage.getItem(key);
        }
        return JSON.stringify(result);
    """)
    storage = json.loads(storage)
    
    print("\n" + "="*80)
    print("localStorage内容:")
    print("="*80)
    for k, v in storage.items():
        if isinstance(v, str) and len(v) > 30:
            print(f"  {k}: {v[:30]}...")
        else:
            print(f"  {k}: {v}")
    
    # 测试请求
    event_id = "295821"
    
    # 方法1：使用fetch API，让浏览器自动处理cookie
    print("\n" + "="*80)
    print("方法1: 使用fetch API发送请求")
    print("="*80)
    
    js_code = f"""
        var st_flpv = localStorage.getItem('st_flpv') || '';
        var sign = localStorage.getItem('sign') || '';
        
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: st_flpv,
            sign: sign,
            trackPath: ''
        }});
        
        console.log('Request body:', body);
        
        var result = '';
        fetch('https://wap.showstart.com/v3/wap/activity/V2/ticket/list', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'CTERMINAL': 'wap',
                'CSAPPID': 'wap',
                'CVERSION': '997'
            }},
            body: body,
            credentials: 'include'
        }}).then(function(r) {{ return r.text(); }}).then(function(d) {{ result = d; }});
        
        // 等待
        var start = Date.now();
        while (result === '' && Date.now() - start < 3000) {{}}
        
        return result;
    """
    
    result = driver.execute_script(js_code)
    print(f"响应: {result}")
    
    # 方法2：使用完整的请求头
    print("\n" + "="*80)
    print("方法2: 使用完整请求头")
    print("="*80)
    
    js_code2 = f"""
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        var st_flpv = localStorage.getItem('st_flpv') || '';
        
        console.log('accessToken:', accessToken);
        console.log('sign:', sign);
        console.log('idToken:', idToken);
        console.log('token:', token);
        console.log('userId:', userId);
        
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: st_flpv,
            sign: sign,
            trackPath: '',
            deviceType: 'H5'
        }});
        
        var result = '';
        fetch('https://wap.showstart.com/v3/wap/activity/V2/ticket/list', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'CTERMINAL': 'wap',
                'CSAPPID': 'wap',
                'CVERSION': '997',
                'CUSAT': accessToken,
                'CUSUT': sign,
                'CUSIT': idToken,
                'CUSID': userId,
                'CDEVICENO': token,
                'st_flpv': st_flpv
            }},
            body: body,
            credentials: 'include'
        }}).then(function(r) {{ return r.text(); }}).then(function(d) {{ result = d; }});
        
        var start = Date.now();
        while (result === '' && Date.now() - start < 3000) {{}}
        
        return result;
    """
    
    result2 = driver.execute_script(js_code2)
    print(f"响应: {result2}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    test_browser_api()