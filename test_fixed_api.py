#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试修复后的API请求"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_fixed_api():
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
    print("获取到的凭证信息:")
    print("="*80)
    
    user_info_str = storage.get('userInfo', '{}')
    try:
        user_info = json.loads(user_info_str)
        user_id = user_info.get('data', {}).get('userId', '')
        print(f"userId (数字): {user_id}")
        print(f"userId (字符串): {str(user_id)}")
    except:
        user_id = ''
    
    print(f"accessToken: {storage.get('accessToken', '')[:30]}...")
    print(f"sign: {storage.get('sign', '')[:30]}...")
    print(f"idToken: {storage.get('idToken', '')[:30]}...")
    print(f"token: {storage.get('token', '')[:30]}...")
    print(f"st_flpv: {storage.get('st_flpv', '')[:30]}...")
    
    # 测试请求（使用修复后的代码逻辑）
    event_id = "295821"
    
    js_code = f"""
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
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
            version: '997',
            userId: userId.toString(),
            idToken: idToken
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
        xhr.setRequestHeader('CUSID', userId.toString());
        xhr.setRequestHeader('CDEVICENO', token);
        xhr.setRequestHeader('st_flpv', st_flpv);
        xhr.setRequestHeader('CRTRACEID', traceId);
        xhr.withCredentials = true;
        
        xhr.send(body);
        
        return xhr.responseText;
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
        print(f"状态: {result_json.get('state', 'N/A')}")
        if 'data' in result_json:
            data = result_json['data']
            print(f"\n数据类型: {type(data)}")
            if isinstance(data, dict):
                print(f"数据键: {list(data.keys())}")
                if 'ticketList' in data:
                    print(f"票档数量: {len(data['ticketList'])}")
                    for t in data['ticketList'][:3]:
                        print(f"  - {t.get('ticketName', t.get('name', ''))}: ¥{t.get('price', 0)}")
            elif isinstance(data, list):
                print(f"数据长度: {len(data)}")
    except Exception as e:
        print(f"\n解析JSON失败: {e}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    test_fixed_api()