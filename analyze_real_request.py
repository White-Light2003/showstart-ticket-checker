#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析浏览器中的真实API请求"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def analyze_real_request():
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
    event_id = "295821"
    driver.get(f"https://wap.showstart.com/event/detail?activityId={event_id}")
    
    input("请登录并在浏览器中点击购票按钮，然后按回车继续...")
    
    # 等待页面加载
    time.sleep(3)
    
    # 尝试获取页面中的JavaScript变量和函数
    print("\n" + "="*80)
    print("分析页面中的JavaScript环境...")
    print("="*80)
    
    # 获取页面中定义的所有函数和变量
    js_analyze = """
        // 获取所有全局变量
        var result = {};
        
        // 检查常见的API配置变量
        var commonVars = ['ST', 'config', 'token', 'accessToken', 'sign', 'idToken', 'userId', 'st_flpv'];
        for (var i = 0; i < commonVars.length; i++) {
            var name = commonVars[i];
            if (window[name] !== undefined) {
                result[name] = typeof window[name] === 'string' && window[name].length > 50 ? window[name].substring(0, 50) + '...' : window[name];
            }
        }
        
        // 检查localStorage
        result.localStorage = {};
        for (var j = 0; j < localStorage.length; j++) {
            var key = localStorage.key(j);
            var value = localStorage.getItem(key);
            result.localStorage[key] = typeof value === 'string' && value.length > 50 ? value.substring(0, 50) + '...' : value;
        }
        
        return JSON.stringify(result);
    """
    
    result = driver.execute_script(js_analyze)
    result_json = json.loads(result)
    
    print("\n[全局变量]")
    for k, v in result_json.items():
        if k != 'localStorage':
            print(f"  {k}: {v}")
    
    print("\n[localStorage]")
    for k, v in sorted(result_json.get('localStorage', {}).items()):
        print(f"  {k}: {v}")
    
    # 尝试调用页面中的API函数
    print("\n" + "="*80)
    print("尝试调用页面中的API...")
    print("="*80)
    
    # 测试使用页面原有的方式发送请求
    js_test_page_api = f"""
        var activityId = '{event_id}';
        
        // 尝试获取页面中已有的API调用方式
        var result = '未找到页面API';
        
        // 检查是否有ST对象
        if (window.ST && window.ST.api) {{
            console.log('找到ST.api');
            result = '找到ST.api对象';
        }}
        
        // 检查是否有fetch或ajax函数
        if (window.$ && window.$.ajax) {{
            console.log('找到$.ajax');
            result = '找到$.ajax';
        }}
        
        return result;
    """
    
    api_result = driver.execute_script(js_test_page_api)
    print(f"\n页面API检测: {api_result}")
    
    # 测试完整的参数组合
    print("\n" + "="*80)
    print("测试完整参数组合...")
    print("="*80)
    
    js_full_test = f"""
        var activityId = '{event_id}';
        
        // 获取所有可能的参数
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        var st_flpv = localStorage.getItem('st_flpv') || '';
        var uniqueCode = userInfo.data ? userInfo.data.uniqueCode : '';
        
        console.log('userId类型:', typeof userId);
        console.log('userId值:', userId);
        
        // 构造请求体，确保userId是数字类型
        var body = JSON.stringify({{
            activityId: activityId,
            coupon: '',
            st_flpv: st_flpv,
            sign: sign,
            trackPath: '',
            deviceType: 'H5',
            channel: 'H5',
            terminal: 'wap',
            appId: 'wap',
            version: '997',
            userId: parseInt(userId) || userId,
            uniqueCode: uniqueCode,
            timestamp: Date.now()
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
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.withCredentials = true;
        
        xhr.send(body);
        
        console.log('Response:', xhr.responseText);
        return xhr.responseText;
    """
    
    full_result = driver.execute_script(js_full_test)
    print(f"\n完整参数测试响应: {full_result}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    analyze_real_request()