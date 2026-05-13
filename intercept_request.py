#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自动拦截并分析真实的API请求"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def intercept_real_request():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
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
    
    # 打开秀动首页
    driver.get("https://wap.showstart.com")
    
    print("="*80)
    print("操作步骤:")
    print("="*80)
    print("1. 浏览器会打开秀动首页")
    print("2. 请先登录 (如果未登录)")
    print("3. 搜索您要查看的演出并进入详情页")
    print("4. 点击页面上的 '购票' 或 '买票' 按钮")
    print("5. 脚本会自动拦截并记录真实的API请求")
    print("6. 等待30秒后会自动分析")
    print("="*80)
    
    # 注入代码拦截XMLHttpRequest
    intercept_code = """
    window._realXHROpen = XMLHttpRequest.prototype.open;
    window._realXHRSend = XMLHttpRequest.prototype.send;
    window._interceptedRequests = [];
    
    XMLHttpRequest.prototype.open = function(method, url, async, user, pass) {
        this._method = method;
        this._url = url;
        this._headers = {};
        return window._realXHROpen.apply(this, arguments);
    };
    
    XMLHttpRequest.prototype.setRequestHeader = function(name, value) {
        if (!this._headers) this._headers = {};
        this._headers[name] = value;
        return window._realXHRSend.call(this);
    };
    
    XMLHttpRequest.prototype.send = function(data) {
        var self = this;
        this._body = data;
        
        // 拦截ticket/list请求
        if (this._url && this._url.includes('ticket/list')) {
            window._interceptedRequests.push({
                method: this._method,
                url: this._url,
                headers: this._headers,
                body: data,
                timestamp: Date.now()
            });
            console.log('[拦截] XMLHttpRequest请求:');
            console.log('  URL:', this._url);
            console.log('  Headers:', JSON.stringify(this._headers, null, 2));
            console.log('  Body:', data);
        }
        
        // 添加状态变化监听器
        this.onreadystatechange = function() {
            if (self.readyState === 4) {
                if (self._url && self._url.includes('ticket/list')) {
                    console.log('[拦截] 响应状态:', self.status);
                    console.log('[拦截] 响应内容:', self.responseText);
                }
            }
        };
        
        return window._realXHRSend.apply(this, arguments);
    };
    
    console.log('[拦截器已启动] 等待XMLHttpRequest请求...');
    """
    
    driver.execute_script(intercept_code)
    
    # 等待用户操作或自动等待
    print("\n等待中 (请点击购票按钮)... 30秒后自动分析")
    time.sleep(30)
    
    # 获取拦截的请求
    print("\n" + "="*80)
    print("获取拦截的请求...")
    print("="*80)
    
    intercepted = driver.execute_script("return JSON.stringify(window._interceptedRequests || []);")
    
    try:
        requests = json.loads(intercepted)
        if requests:
            print(f"\n捕获到 {len(requests)} 个API请求:")
            for i, req in enumerate(requests):
                print(f"\n--- 请求 {i+1} ---")
                print(f"URL: {req['url']}")
                print(f"方法: {req['method']}")
                print(f"请求头:")
                for k, v in req.get('headers', {}).items():
                    print(f"  {k}: {v}")
                print(f"请求体: {req.get('body', 'N/A')}")
                
                # 尝试解析请求体
                try:
                    body = json.loads(req.get('body', '{}'))
                    print(f"请求体(解析后):")
                    for k, v in body.items():
                        print(f"  {k}: {v}")
                except:
                    pass
        else:
            print("\n未捕获到任何API请求")
    except Exception as e:
        print(f"解析拦截数据失败: {e}")
    
    # 获取当前localStorage用于对比
    print("\n" + "="*80)
    print("当前localStorage内容:")
    print("="*80)
    
    storage = driver.execute_script("""
        var result = {};
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            try {
                result[key] = JSON.parse(localStorage.getItem(key));
            } catch(e) {
                result[key] = localStorage.getItem(key);
            }
        }
        return JSON.stringify(result, null, 2);
    """)
    
    print(storage)
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    intercept_real_request()