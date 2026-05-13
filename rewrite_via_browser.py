#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重写 get_ticket_info_via_browser 函数，先在Python中计算好签名"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 get_ticket_info_via_browser 函数的位置并完全替换
old_function_start = '''def get_ticket_info_via_browser(driver, event_id: str) -> List[Dict]:
    """通过浏览器直接执行API请求（保证认证状态）"""
    print("[API] INFO: 使用浏览器执行API请求...")
    try:
        # 在浏览器中执行JavaScript发送API请求，包含完整的签名计算
        js_code = f"""'""

# 先读取完整的函数内容，让我找个安全的方式替换
# 让我读取整个文件然后找到这个函数的范围
lines = content.split('\n')
function_start_idx = None
function_end_idx = None

# 找到函数开始
for i, line in enumerate(lines):
    if line.strip().startswith('def get_ticket_info_via_browser'):
        function_start_idx = i
        break

# 找到函数结束（下一个函数或空行）
if function_start_idx is not None:
    brace_count = 0
    in_string = False
    for i in range(function_start_idx, len(lines)):
        line = lines[i]
        # 简单的括号计数
        for c in line:
            if c == '"' or c == "'":
                in_string = not in_string
            if not in_string and c == '{':
                brace_count += 1
            if not in_string and c == '}':
                brace_count -= 1
        if brace_count == 0 and i > function_start_idx and (
            lines[i].strip().startswith('def ') or
            lines[i].strip().startswith('# ====') or
            (i+1 < len(lines) and not lines[i+1].strip())
        ):
            function_end_idx = i + 1
            break
    # 如果没找到，用后面的函数开始作为结束
    if function_end_idx is None:
        for i in range(function_start_idx, len(lines)):
            if i > function_start_idx and lines[i].strip().startswith('def '):
                function_end_idx = i
                break

if function_start_idx is not None and function_end_idx is not None:
    # 构建新函数
    new_function = '''def get_ticket_info_via_browser(driver, event_id: str) -> List[Dict]:
    """通过浏览器直接执行API请求（保证认证状态）"""
    print("[API] INFO: 使用浏览器执行API请求...")
    try:
        # 先从localStorage获取参数
        params_js = """
            return JSON.stringify({
                accessToken: localStorage.getItem('accessToken') || '',
                sign: localStorage.getItem('sign') || '',
                idToken: localStorage.getItem('idToken') || '',
                token: localStorage.getItem('token') || '',
                userInfoStr: localStorage.getItem('userInfo') || '{}',
                st_flpv: localStorage.getItem('st_flpv') || ''
            });
        """
        params_json = driver.execute_script(params_js)
        params = json.loads(params_json)
        
        # 解析userId
        user_id = ''
        if params.get('userInfoStr'):
            try:
                user_info = json.loads(params['userInfoStr'])
                if user_info.get('data'):
                    user_id = str(user_info['data'].get('userId', ''))
            except:
                pass
        if not user_id:
            user_id = str(localStorage.getItem('userId', ''))
        
        # 生成traceId
        import time
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        random_str = ''.join([chars[int(time.time() * 1000 + i) % len(chars)] for i in range(32)])
        trace_id = random_str + str(int(time.time() * 1000))
        
        # 构建body
        body_dict = {
            'activityId': str(event_id),
            'coupon': '',
            'st_flpv': params.get('st_flpv', ''),
            'sign': params.get('sign', ''),
            'trackPath': ''
        }
        body_str = json.dumps(body_dict, separators=(',', ':'), ensure_ascii=False)
        
        # 计算CRPSIGN（Python标准MD5）
        import hashlib
        url_path = '/wap/activity/V2/ticket/list'
        raw = (params['accessToken'] + params['sign'] + params['idToken'] + 
               user_id + 'wap' + params['token'] + body_str + 
               url_path + '997' + 'wap' + trace_id)
        crpsign = hashlib.md5(raw.encode('utf-8')).hexdigest()
        
        # 构建cdeviceinfo
        cdeviceinfo = '{"vendorName":"","deviceMode":"iPhone","deviceName":"","systemName":"ios","systemVersion":"17.0","cpuMode":" ","cpuCores":"","cpuArch":"","memerySize":"","diskSize":"","network":"4G","resolution":"390*844","pixelResolution":""}'
        
        # 在浏览器中执行请求，使用计算好的参数
        js_code = """
            var accessToken = arguments[0];
            var sign = arguments[1];
            var idToken = arguments[2];
            var userId = arguments[3];
            var token = arguments[4];
            var st_flpv = arguments[5];
            var body = arguments[6];
            var crpsign = arguments[7];
            var traceId = arguments[8];
            var cdeviceinfo = arguments[9];
            var eventId = arguments[10];
            
            var result = '';
            try {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('Accept', '*/*');
                xhr.setRequestHeader('Accept-Language', 'zh-CN,zh;q=0.9');
                xhr.setRequestHeader('CDEVICEINFO', cdeviceinfo);
                xhr.setRequestHeader('CDEVICENO', token);
                xhr.setRequestHeader('CTERMINAL', 'wap');
                xhr.setRequestHeader('CSAPPID', 'wap');
                xhr.setRequestHeader('CVERSION', '997');
                xhr.setRequestHeader('CUSAT', accessToken);
                xhr.setRequestHeader('CUSUT', sign);
                xhr.setRequestHeader('CUSIT', idToken);
                xhr.setRequestHeader('CUSID', userId);
                xhr.setRequestHeader('CUSNAME', 'nil');
                xhr.setRequestHeader('CUUSERREF', token);
                xhr.setRequestHeader('CSOURCEPATH', '');
                xhr.setRequestHeader('CTRACKPATH', '');
                xhr.setRequestHeader('st_flpv', st_flpv);
                xhr.setRequestHeader('CRTRACEID', traceId);
                xhr.setRequestHeader('CRPSIGN', crpsign);
                xhr.setRequestHeader('Referer', 'https://wap.showstart.com/pages/activity/detail/detail?activityId=' + eventId);
                xhr.setRequestHeader('Origin', 'https://wap.showstart.com');
                xhr.setRequestHeader('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
                xhr.withCredentials = true;
                
                xhr.send(body);
                
                if (xhr.status === 200) {
                    result = xhr.responseText;
                } else {
                    result = JSON.stringify({'error': 'HTTP error', 'status': xhr.status, 'response': xhr.responseText || 'empty'});
                }
            } catch(e) {
                result = JSON.stringify({'error': 'Exception', 'message': e.message});
            }
            
            return result;
        """
        result_str = driver.execute_script(
            js_code,
            params['accessToken'],
            params['sign'],
            params['idToken'],
            user_id,
            params['token'],
            params.get('st_flpv', ''),
            body_str,
            crpsign,
            trace_id,
            cdeviceinfo,
            str(event_id)
        )
        
        print(f"[API] 浏览器响应: {result_str[:200]}...")
        
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
'''
    # 替换函数
    new_content = '\n'.join(lines[:function_start_idx]) + '\n' + new_function + '\n' + '\n'.join(lines[function_end_idx:])
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("[OK] get_ticket_info_via_browser 函数已重写！")
else:
    print("[ERROR] 找不到函数位置")
