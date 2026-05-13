#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接模拟页面上的真实请求"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def simulate_real_request():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
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
    driver.get(f"https://wap.showstart.com/pages/activity/detail/detail?activityId={event_id}")
    
    print("="*80)
    print("操作步骤:")
    print("="*80)
    print("1. 请先登录您的秀动账号")
    print("2. 打开浏览器开发者工具 (F12)")
    print("3. 切换到 Network (网络) 标签")
    print("4. 点击页面上的 '立即购票' 按钮")
    print("5. 在网络请求中找到 ticket/list 请求")
    print("6. 查看请求体和请求头")
    print("="*80)
    
    input("\n准备好后按回车继续...")
    
    # 等待用户点击购票按钮后，尝试获取页面中的API请求参数
    time.sleep(5)
    
    # 获取页面中使用的请求参数
    print("\n" + "="*80)
    print("分析页面中的请求参数...")
    print("="*80)
    
    # 尝试获取页面中定义的API配置
    analyze_js = """
        // 分析页面中的JavaScript环境
        var result = {};
        
        // 检查页面中是否有ST对象（秀动的API对象）
        if (window.ST) {
            result.ST_exists = true;
            result.ST_keys = Object.keys(window.ST);
        }
        
        // 检查是否有API配置
        if (window.ST && window.ST.config) {
            result.ST_config = window.ST.config;
        }
        
        // 检查是否有默认参数
        if (window.ST && window.ST.defaultParams) {
            result.ST_defaultParams = window.ST.defaultParams;
        }
        
        // 获取所有请求头
        result.headers = {};
        
        // 获取当前页面的userInfo
        var userInfoStr = localStorage.getItem('userInfo') || '{}';
        var userInfo = JSON.parse(userInfoStr);
        result.userInfo = userInfo;
        
        // 获取所有localStorage
        result.localStorage = {};
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            result.localStorage[key] = localStorage.getItem(key);
        }
        
        return JSON.stringify(result, null, 2);
    """
    
    page_info = driver.execute_script(analyze_js)
    print("\n[页面分析结果]")
    print(page_info)
    
    # 尝试直接调用页面的API方法
    print("\n" + "="*80)
    print("尝试调用页面API...")
    print("="*80)
    
    call_api_js = f"""
        var result = {{success: false}};
        
        // 尝试使用页面的API方法
        if (window.ST && window.ST.api) {{
            console.log('找到ST.api');
            
            // 尝试调用API
            window.ST.api.post('/wap/activity/V2/ticket/list', {{
                activityId: '{event_id}',
                coupon: '',
                sign: localStorage.getItem('sign') || '',
                st_flpv: (function() {{
                    var userInfo = JSON.parse(localStorage.getItem('userInfo') || '[]');
                    return userInfo.data && userInfo.data.st_flpv ? userInfo.data.st_flpv : localStorage.getItem('st_flpv');
                }})(),
                trackPath: ''
            }}, function(data) {{
                console.log('API响应:', data);
                result = {{success: true, data: data}};
            }}, function(error) {{
                console.log('API错误:', error);
                result = {{success: false, error: error}};
            }});
        }}
        
        // 等待响应
        var start = Date.now();
        while (!result.success && Date.now() - start < 3000) {{}}
        
        return JSON.stringify(result);
    """
    
    api_result = driver.execute_script(call_api_js)
    print(f"\n页面API调用结果: {api_result}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    simulate_real_request()