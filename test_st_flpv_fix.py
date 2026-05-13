#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试修复后的st_flpv参数"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_st_flpv_fix():
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
    
    input("请登录后按回车继续...")
    
    # 测试使用正确的st_flpv
    event_id = "295821"
    
    js_test = f"""
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        
        // 关键修复：优先使用userInfo中的st_flpv（与token相同）
        var st_flpv_from_userInfo = userInfo.data && userInfo.data.st_flpv ? userInfo.data.st_flpv : '';
        var st_flpv_from_localStorage = localStorage.getItem('st_flpv') || '';
        
        console.log('st_flpv (userInfo):', st_flpv_from_userInfo);
        console.log('st_flpv (localStorage):', st_flpv_from_localStorage);
        console.log('token:', token);
        console.log('是否相同:', st_flpv_from_userInfo === token);
        
        // 使用userInfo中的st_flpv
        var st_flpv = st_flpv_from_userInfo || st_flpv_from_localStorage;
        
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
        xhr.setRequestHeader('Referer', 'https://wap.showstart.com/');
        xhr.setRequestHeader('Origin', 'https://wap.showstart.com');
        xhr.withCredentials = true;
        
        xhr.send(body);
        
        console.log('Response:', xhr.responseText);
        return JSON.stringify({{
            status: xhr.status,
            response: xhr.responseText,
            st_flpv_used: st_flpv,
            st_flpv_userInfo: st_flpv_from_userInfo,
            st_flpv_localStorage: st_flpv_from_localStorage,
            token: token,
            same_as_token: st_flpv === token
        }});
    """
    
    print("\n" + "="*80)
    print("测试结果:")
    print("="*80)
    
    result = driver.execute_script(js_test)
    result_json = json.loads(result)
    
    print(f"使用的st_flpv: {result_json['st_flpv_used']}")
    print(f"userInfo中的st_flpv: {result_json['st_flpv_userInfo']}")
    print(f"localStorage中的st_flpv: {result_json['st_flpv_localStorage']}")
    print(f"token: {result_json['token']}")
    print(f"st_flpv与token是否相同: {result_json['same_as_token']}")
    print(f"\nHTTP状态: {result_json['status']}")
    print(f"响应: {result_json['response']}")
    
    # 解析响应
    try:
        response_data = json.loads(result_json['response'])
        print(f"\n解析结果:")
        print(f"  code: {response_data.get('code')}")
        print(f"  success: {response_data.get('success')}")
        print(f"  msg: {response_data.get('msg')}")
        print(f"  state: {response_data.get('state')}")
        if 'data' in response_data:
            print(f"  data类型: {type(response_data['data'])}")
    except:
        pass
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    test_st_flpv_fix()