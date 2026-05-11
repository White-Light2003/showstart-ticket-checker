#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试修改后的API请求"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_request():
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
    
    # 测试请求（使用修改后的代码逻辑）
    event_id = "295821"
    
    js_code = f"""
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : (localStorage.getItem('userId') || '');
        var st_flpv = localStorage.getItem('st_flpv') || '';
        
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
            trackPath: '',
            deviceType: 'H5',
            channel: 'H5',
            terminal: 'wap',
            appId: 'wap',
            version: '997'
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
                'st_flpv': st_flpv,
                'CRTRACEID': traceId
            }},
            body: body,
            credentials: 'include'
        }}).then(function(r) {{ return r.text(); }}).then(function(d) {{ result = d; }});
        
        var start = Date.now();
        while (result === '' && Date.now() - start < 5000) {{}}
        
        return result;
    """
    
    print("\n" + "="*80)
    print("API请求测试结果:")
    print("="*80)
    
    result = driver.execute_script(js_code)
    print(f"响应: {result}")
    
    # 解析响应
    try:
        result_json = json.loads(result)
        print(f"\n状态码: {result_json.get('code', 'N/A')}")
        print(f"成功: {result_json.get('success', 'N/A')}")
        print(f"消息: {result_json.get('msg', 'N/A')}")
        if 'data' in result_json:
            print(f"数据: {json.dumps(result_json['data'], indent=2, ensure_ascii=False)[:500]}...")
    except:
        print("\n无法解析响应JSON")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    test_api_request()