#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""深度调试：尝试多种参数组合"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def deep_debug():
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
    driver.get("https://wap.showstart.com/pages/activity/detail/detail?activityId=295821")
    
    input("请登录后按回车继续...")
    
    # 测试多种参数组合
    event_id = "295821"
    
    # 获取所有必要参数
    get_params_js = """
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        var st_flpv = userInfo.data && userInfo.data.st_flpv ? userInfo.data.st_flpv : (localStorage.getItem('st_flpv') || '');
        var uniqueCode = userInfo.data ? userInfo.data.uniqueCode : '';
        
        return JSON.stringify({
            accessToken: accessToken,
            sign: sign,
            idToken: idToken,
            token: token,
            userId: userId,
            st_flpv: st_flpv,
            uniqueCode: uniqueCode
        });
    """
    
    params = json.loads(driver.execute_script(get_params_js))
    print("\n" + "="*80)
    print("获取到的参数:")
    print("="*80)
    for k, v in params.items():
        print(f"  {k}: {v}")
    
    # 测试1: 仅基础参数
    print("\n" + "="*80)
    print("测试1: 仅基础参数")
    print("="*80)
    
    test1_js = f"""
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: '{params['st_flpv']}',
            sign: '{params['sign']}',
            trackPath: ''
        }});
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.withCredentials = true;
        xhr.send(body);
        
        return xhr.responseText;
    """
    
    result1 = driver.execute_script(test1_js)
    print(f"响应: {result1}")
    
    # 测试2: 添加userId和idToken
    print("\n" + "="*80)
    print("测试2: 添加userId和idToken")
    print("="*80)
    
    test2_js = f"""
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: '{params['st_flpv']}',
            sign: '{params['sign']}',
            trackPath: '',
            userId: {params['userId']},
            idToken: '{params['idToken']}'
        }});
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.withCredentials = true;
        xhr.send(body);
        
        return xhr.responseText;
    """
    
    result2 = driver.execute_script(test2_js)
    print(f"响应: {result2}")
    
    # 测试3: 添加所有请求头
    print("\n" + "="*80)
    print("测试3: 添加所有请求头")
    print("="*80)
    
    test3_js = f"""
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: '{params['st_flpv']}',
            sign: '{params['sign']}',
            trackPath: '',
            userId: {params['userId']},
            idToken: '{params['idToken']}',
            deviceType: 'H5',
            channel: 'H5',
            terminal: 'wap',
            appId: 'wap',
            version: '997'
        }});
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('CTERMINAL', 'wap');
        xhr.setRequestHeader('CSAPPID', 'wap');
        xhr.setRequestHeader('CVERSION', '997');
        xhr.setRequestHeader('CUSAT', '{params['accessToken']}');
        xhr.setRequestHeader('CUSUT', '{params['sign']}');
        xhr.setRequestHeader('CUSIT', '{params['idToken']}');
        xhr.setRequestHeader('CUSID', '{params['userId']}');
        xhr.setRequestHeader('CDEVICENO', '{params['token']}');
        xhr.setRequestHeader('st_flpv', '{params['st_flpv']}');
        xhr.setRequestHeader('Referer', 'https://wap.showstart.com/pages/activity/detail/detail?activityId={event_id}');
        xhr.setRequestHeader('Origin', 'https://wap.showstart.com');
        xhr.withCredentials = true;
        xhr.send(body);
        
        return xhr.responseText;
    """
    
    result3 = driver.execute_script(test3_js)
    print(f"响应: {result3}")
    
    # 测试4: 尝试不同的API端点
    print("\n" + "="*80)
    print("测试4: 尝试不同的API端点")
    print("="*80)
    
    endpoints = [
        'https://wap.showstart.com/v3/wap/activity/V2/ticket/list',
        'https://wap.showstart.com/api/wap/activity/V2/ticket/list',
        'https://www.showstart.com/v3/wap/activity/V2/ticket/list'
    ]
    
    for endpoint in endpoints:
        test4_js = f"""
            var body = JSON.stringify({{
                activityId: '{event_id}',
                coupon: '',
                st_flpv: '{params['st_flpv']}',
                sign: '{params['sign']}',
                trackPath: '',
                userId: {params['userId']},
                idToken: '{params['idToken']}'
            }});
            
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '{endpoint}', false);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.withCredentials = true;
            xhr.send(body);
            
            return '{{"endpoint": "{endpoint}", "status": ' + xhr.status + ', "response": ' + (xhr.responseText ? JSON.stringify(xhr.responseText) : '"empty"') + '}}';
        """
        
        result = driver.execute_script(test4_js)
        print(f"\n端点: {endpoint}")
        print(f"结果: {result}")
    
    # 测试5: 模拟真实页面的fetch请求
    print("\n" + "="*80)
    print("测试5: 模拟真实页面请求")
    print("="*80)
    
    test5_js = f"""
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: '{params['st_flpv']}',
            sign: '{params['sign']}',
            trackPath: '',
            userId: {params['userId']},
            idToken: '{params['idToken']}'
        }});
        
        console.log('Request body:', body);
        
        var result = '';
        fetch('/v3/wap/activity/V2/ticket/list', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'CTERMINAL': 'wap',
                'CSAPPID': 'wap',
                'CVERSION': '997',
                'CUSAT': '{params['accessToken']}',
                'CUSUT': '{params['sign']}',
                'CUSIT': '{params['idToken']}',
                'CUSID': '{params['userId']}',
                'CDEVICENO': '{params['token']}',
                'st_flpv': '{params['st_flpv']}'
            }},
            body: body,
            credentials: 'include'
        }}).then(function(r) {{ return r.text(); }}).then(function(d) {{ result = d; }});
        
        var start = Date.now();
        while (result === '' && Date.now() - start < 3000) {{}}
        
        return result;
    """
    
    result5 = driver.execute_script(test5_js)
    print(f"响应: {result5}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    deep_debug()