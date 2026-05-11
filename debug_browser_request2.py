#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""详细调试浏览器API请求 - 使用fetch API"""
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
    
    # 测试使用fetch API发送请求，包含完整头
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
        
        console.log('accessToken:', accessToken);
        console.log('sign:', sign);
        console.log('idToken:', idToken);
        console.log('token:', token);
        console.log('userId:', userId);
        console.log('st_flpv:', st_flpv);
        
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
        
        // 使用fetch发送请求（异步）
        var result = {{}};
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
        }}).then(function(response) {{
            return response.text();
        }}).then(function(data) {{
            console.log('Response:', data);
            window.__debug_result = data;
        }}).catch(function(error) {{
            console.error('Error:', error);
            window.__debug_result = 'Error: ' + error;
        }});
        
        // 等待请求完成
        setTimeout(function() {{}}, 3000);
        return '请在浏览器控制台查看结果';
    """
    
    print("\n" + "="*80)
    print("使用fetch API测试（完整头）:")
    print("="*80)
    result = driver.execute_script(js_test_api)
    print(f"提示: {result}")
    
    # 等待一下然后获取结果
    import time
    time.sleep(3)
    
    # 尝试获取结果
    result = driver.execute_script("return window.__debug_result || '未获取到结果';")
    print(f"\n响应结果: {result}")
    
    input("\n请打开浏览器开发者工具(F12)查看Network面板，分析真实请求后按回车退出...")
    driver.quit()

if __name__ == "__main__":
    debug_browser_api()