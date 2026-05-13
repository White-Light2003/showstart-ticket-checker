#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""捕获真实API请求的完整参数"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def capture_real_request():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    
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
    
    # 打开演出详情页面
    event_id = "295821"
    driver.get(f"https://wap.showstart.com/event/detail?activityId={event_id}")
    
    print("请在浏览器中打开开发者工具 (F12)")
    print("1. 切换到 Network (网络) 标签")
    print("2. 点击页面上任意购票/买票按钮")
    print("3. 找到 wap/activity/V2/ticket/list 请求")
    print("4. 查看该请求的:")
    print("   - Request Headers (请求头)")
    print("   - Request Payload (请求体)")
    print("5. 将这些信息复制给我")
    
    input("\n准备好后按回车继续...")
    
    # 获取当前页面的所有请求记录
    print("\n" + "="*80)
    print("分析当前页面的JavaScript环境...")
    print("="*80)
    
    # 检查页面中是否有现成的API调用代码
    js_check = """
        // 检查页面中可能存在的API相关代码
        var result = {
            'hasST': typeof window.ST !== 'undefined',
            'hasConfig': typeof window.config !== 'undefined',
            'hasJQuery': typeof window.$ !== 'undefined',
            'hasaxios': typeof window.axios !== 'undefined',
            'hasVue': typeof window.Vue !== 'undefined'
        };
        
        // 获取所有localStorage
        result.localStorage = {};
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            try {
                result.localStorage[key] = JSON.parse(localStorage.getItem(key));
            } catch(e) {
                result.localStorage[key] = localStorage.getItem(key);
            }
        }
        
        // 检查sessionStorage
        result.sessionStorage = {};
        for (var i = 0; i < sessionStorage.length; i++) {
            var key = sessionStorage.key(i);
            try {
                result.sessionStorage[key] = JSON.parse(sessionStorage.getItem(key));
            } catch(e) {
                result.sessionStorage[key] = sessionStorage.getItem(key);
            }
        }
        
        return JSON.stringify(result, null, 2);
    """
    
    page_info = driver.execute_script(js_check)
    print("\n[页面环境信息]")
    print(page_info)
    
    # 尝试各种可能的请求格式
    print("\n" + "="*80)
    print("尝试不同的请求格式...")
    print("="*80)
    
    # 测试不同的参数组合
    test_cases = [
        {
            "name": "基础参数",
            "body": {
                "activityId": event_id,
                "coupon": "",
                "st_flpv": "",
                "sign": "",
                "trackPath": ""
            }
        },
        {
            "name": "添加deviceType和channel",
            "body": {
                "activityId": event_id,
                "coupon": "",
                "st_flpv": "",
                "sign": "",
                "trackPath": "",
                "deviceType": "H5",
                "channel": "H5"
            }
        },
        {
            "name": "完整参数(来自userInfo)",
            "body": {
                "activityId": event_id,
                "coupon": "",
                "st_flpv": "",
                "sign": "",
                "trackPath": "",
                "deviceType": "H5",
                "channel": "H5",
                "terminal": "wap",
                "appId": "wap",
                "version": "997",
                "userId": "",
                "idToken": ""
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n[测试: {test['name']}]")
        
        # 先获取最新的token
        js_test = f"""
            var body = {json.dumps(test['body'])};
            
            // 填充实际值
            body.st_flpv = localStorage.getItem('st_flpv') || '';
            body.sign = localStorage.getItem('sign') || '';
            
            var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
            var userInfo = JSON.parse(userInfoStr);
            if (userInfo.data) {{
                body.userId = userInfo.data.userId;
                body.idToken = userInfo.data.idtoken || localStorage.getItem('idToken') || '';
            }}
            
            var accessToken = localStorage.getItem('accessToken') || '';
            var idToken = localStorage.getItem('idToken') || '';
            var token = localStorage.getItem('token') || '';
            
            console.log('Request body:', JSON.stringify(body));
            
            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('CTERMINAL', 'wap');
            xhr.setRequestHeader('CSAPPID', 'wap');
            xhr.setRequestHeader('CVERSION', '997');
            xhr.setRequestHeader('CUSAT', accessToken);
            xhr.setRequestHeader('CUSUT', body.sign);
            xhr.setRequestHeader('CUSIT', idToken);
            xhr.setRequestHeader('CUSID', body.userId ? body.userId.toString() : '');
            xhr.setRequestHeader('CDEVICENO', token);
            xhr.setRequestHeader('st_flpv', body.st_flpv);
            xhr.withCredentials = true;
            
            xhr.send(JSON.stringify(body));
            
            console.log('Response:', xhr.responseText);
            return JSON.stringify({{
                'test': '{test['name']}',
                'status': xhr.status,
                'response': xhr.responseText,
                'body': JSON.stringify(body)
            }});
        """
        
        result = driver.execute_script(js_test)
        try:
            result_json = json.loads(result)
            print(f"  状态: {result_json['status']}")
            print(f"  响应: {result_json['response'][:100]}...")
        except:
            print(f"  结果: {result[:200]}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    capture_real_request()