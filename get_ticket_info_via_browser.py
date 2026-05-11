def get_ticket_info_via_browser(driver, event_id: str) -> List[Dict]:
    """通过浏览器直接执行API请求（保证认证状态）"""
    print("[API] INFO: 使用浏览器执行API请求...")
    try:
        # 先获取浏览器中的所有localStorage值并打印
        js_get_storage = """
            var result = {};
            for (var i = 0; i < localStorage.length; i++) {
                var key = localStorage.key(i);
                result[key] = localStorage.getItem(key);
            }
            return JSON.stringify(result);
        """
        storage_str = driver.execute_script(js_get_storage)
        import json
        storage = json.loads(storage_str)
        print("[API] DEBUG: localStorage内容:")
        for key, value in storage.items():
            if isinstance(value, str) and len(value) > 30:
                print(f"  {key}: {value[:30]}...")
            else:
                print(f"  {key}: {value}")
        
        # 在浏览器中执行JavaScript发送API请求
        js_code = f"""
            // 获取所有必要的token
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
            
            // 构造请求体
            var body = JSON.stringify({{
                activityId: '{event_id}',
                coupon: '',
                st_flpv: st_flpv,
                sign: sign,
                trackPath: '',
                deviceType: 'H5'
            }});
            
            // 发送请求（使用fetch）
            var result = '';
            try {{
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
                }}).then(function(response) {{
                    return response.text();
                }}).then(function(data) {{
                    result = data;
                }}).catch(function(error) {{
                    result = 'ERROR: ' + error;
                }});
                
                // 等待请求完成
                var start = Date.now();
                while (result === '' && Date.now() - start < 5000) {{
                    // 等待
                }}
            }} catch(e) {{
                result = 'EXCEPTION: ' + e.message;
            }}
            
            return result;
        """
        
        result_str = driver.execute_script(js_code)
        print(f"[API] 浏览器响应: {result_str[:300]}...")
        
        result = json.loads(result_str)
        if result.get('code') == 0 or result.get('success'):
            ticket_list = result.get('data', {}).get('ticketList', result.get('data', []))
            tickets = []
            for t in ticket_list:
                tickets.append({
                    'price': t.get('price', 0),
                    'name': t.get('ticketName', t.get('name', '')),
                    'status': '有票' if t.get('stock', 0) > 0 else '售罄'
                })
            print("[API] SUCCESS: 通过浏览器API获取 %d 个票档信息" % len(tickets))
            return tickets
        else:
            print("[API] ERROR: 浏览器API返回错误: %s" % result.get('msg', '未知错误'))
            return []
            
    except Exception as e:
        print("[API] ERROR: 浏览器API请求失败: %s" % e)
        return []