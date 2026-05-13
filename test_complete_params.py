#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试完整参数的API请求"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_params():
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
    
    event_id = "295821"
    
    # 使用修复后的完整参数
    js_test = f"""
        // MD5实现
        function md5(input) {{
            function md5cycle(x, k) {{
                var a = x[0], b = x[1], c = x[2], d = x[3];
                a = ff(a, b, c, d, k[0], 7, -680876936);
                d = ff(d, a, b, c, k[1], 12, -389564586);
                c = ff(c, d, a, b, k[2], 17, 606105819);
                b = ff(b, c, d, a, k[3], 22, -1044525330);
                a = ff(a, b, c, d, k[4], 7, -176418897);
                d = ff(d, a, b, c, k[5], 12, 1200080426);
                c = ff(c, d, a, b, k[6], 17, -1473231341);
                b = ff(b, c, d, a, k[7], 22, -45705983);
                a = ff(a, b, c, d, k[8], 7, 1770035416);
                d = ff(d, a, b, c, k[9], 12, -1958414417);
                c = ff(c, d, a, b, k[10], 17, -42063);
                b = ff(b, c, d, a, k[11], 22, -1990404162);
                a = ff(a, b, c, d, k[12], 7, 1804603682);
                d = ff(d, a, b, c, k[13], 12, -40341101);
                c = ff(c, d, a, b, k[14], 17, -1502002290);
                b = ff(b, c, d, a, k[15], 22, 1236535329);
                a = gg(a, b, c, d, k[1], 5, -165796510);
                d = gg(d, a, b, c, k[6], 9, -1069501632);
                c = gg(c, d, a, b, k[11], 14, 643717713);
                b = gg(b, c, d, a, k[0], 20, -373897302);
                a = gg(a, b, c, d, k[5], 5, -701558691);
                d = gg(d, a, b, c, k[10], 9, 38016083);
                c = gg(c, d, a, b, k[15], 14, -660478335);
                b = gg(b, c, d, a, k[4], 20, -405537848);
                a = gg(a, b, c, d, k[9], 5, 568446438);
                d = gg(d, a, b, c, k[14], 9, -1019803690);
                c = gg(c, d, a, b, k[3], 14, -187363961);
                b = gg(b, c, d, a, k[8], 20, 1163531501);
                a = gg(a, b, c, d, k[13], 5, -1444681467);
                d = gg(d, a, b, c, k[2], 9, -51403784);
                c = gg(c, d, a, b, k[7], 14, 1735328473);
                b = gg(b, c, d, a, k[12], 20, -1926607734);
                a = hh(a, b, c, d, k[5], 4, -378558);
                d = hh(d, a, b, c, k[8], 11, -2022574463);
                c = hh(c, d, a, b, k[11], 16, 1839030562);
                b = hh(b, c, d, a, k[14], 23, -35309556);
                a = hh(a, b, c, d, k[1], 4, -1530992060);
                d = hh(d, a, b, c, k[4], 11, 1272893353);
                c = gg(c, d, a, b, k[7], 16, -155497632);
                b = hh(b, c, d, a, k[10], 23, -1094730640);
                a = hh(a, b, c, d, k[13], 4, 681279174);
                d = hh(d, a, b, c, k[0], 11, -358537222);
                c = hh(c, d, a, b, k[3], 16, -722521979);
                b = hh(b, c, d, a, k[6], 23, 76029189);
                a = hh(a, b, c, d, k[9], 4, -640364487);
                d = hh(d, a, b, c, k[12], 11, -421815835);
                c = hh(c, d, a, b, k[15], 16, 530742520);
                b = hh(b, c, d, a, k[2], 23, -995338651);
                a = ii(a, b, c, d, k[0], 6, -198630844);
                d = ii(d, a, b, c, k[7], 10, 1126891415);
                c = ii(c, d, a, b, k[14], 15, -1416354905);
                b = ii(b, c, d, a, k[5], 21, -57434055);
                a = ii(a, b, c, d, k[12], 6, 1700485571);
                d = ii(d, a, b, c, k[3], 10, -1894986606);
                c = ii(c, d, a, b, k[10], 15, -1051523);
                b = ii(b, c, d, a, k[1], 21, -2054922799);
                a = ii(a, b, c, d, k[8], 6, 1873313359);
                d = ii(d, a, b, c, k[15], 10, -30611744);
                c = ii(c, d, a, b, k[6], 15, -1560198380);
                b = ii(b, c, d, a, k[13], 21, 1309151649);
                a = ii(a, b, c, d, k[4], 6, -145523070);
                d = ii(d, a, b, c, k[11], 10, -1120210379);
                c = ii(c, d, a, b, k[2], 15, 718787259);
                b = ii(b, c, d, a, k[9], 21, -289933462);
                a = ii(a, b, c, d, k[6], 6, -206413683);
                d = ii(d, a, b, c, k[13], 10, -1604182996);
                c = ii(c, d, a, b, k[0], 15, -1134597877);
                b = ii(b, c, d, a, k[7], 21, 1855165014);
                a = ii(a, b, c, d, k[14], 6, 1310974796);
                d = ii(d, a, b, c, k[5], 10, 1157377689);
                c = ii(c, d, a, b, k[12], 15, -1112649068);
                b = ii(b, c, d, a, k[3], 21, -1703811985);
                a = ii(a, b, c, d, k[10], 6, -1516987130);
                d = ii(d, a, b, c, k[1], 10, -1321499986);
                c = ii(c, d, a, b, k[8], 15, -1902582663);
                b = ii(b, c, d, a, k[15], 21, 855351967);
                return [a, b, c, d];
            }}
            
            function cmn(q, a, b, x, s, t) {{
                a = add(a, add(add(q, x), t));
                return add((a << s) | (a >>> (32 - s)), b);
            }}
            
            function ff(a, b, c, d, x, s, t) {{ return cmn((b & c) | ((~b) & d), a, b, x, s, t); }}
            function gg(a, b, c, d, x, s, t) {{ return cmn((b & d) | (c & (~d)), a, b, x, s, t); }}
            function hh(a, b, c, d, x, s, t) {{ return cmn(b ^ c ^ d, a, b, x, s, t); }}
            function ii(a, b, c, d, x, s, t) {{ return cmn(c ^ (b | (~d)), a, b, x, s, t); }}
            
            function md5blk(s) {{
                var md5blks = [], i;
                for (i = 0; i < 64; i += 4) {{
                    md5blks[i >> 2] = s.charCodeAt(i) + (s.charCodeAt(i + 1) << 8) + (s.charCodeAt(i + 2) << 16) + (s.charCodeAt(i + 3) << 24);
                }}
                return md5blks;
            }}
            
            var hex_chr = '0123456789abcdef'.split('');
            function rhex(n) {{
                var s = '', j = 0;
                for (; j < 4; j++)
                    s += hex_chr[(n >> (j * 8 + 4)) & 0x0F] + hex_chr[(n >> (j * 8)) & 0x0F];
                return s;
            }}
            
            function add(a, b) {{ return (a + b) & 0xFFFFFFFF; }}
            
            var s = input, n = s.length * 8, x = md5blk(s);
            x[n >> 5] |= 0x80 << ((n) % 32);
            x[(((n + 64) >>> 9) << 4) + 14] = n;
            
            var a = 1732584193, b = -271733879, c = -1732584194, d = 271733878;
            
            for (var i = 0; i < x.length; i += 16) {{
                var olda = a, oldb = b, oldc = c, oldd = d;
                var cycle = md5cycle([a, b, c, d], x.slice(i, i + 16));
                a = cycle[0]; b = cycle[1]; c = cycle[2]; d = cycle[3];
            }}
            
            return rhex(a) + rhex(b) + rhex(c) + rhex(d);
        }}
        
        // 获取参数
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        var st_flpv = userInfo.data && userInfo.data.st_flpv ? userInfo.data.st_flpv : (localStorage.getItem('st_flpv') || '');
        var uniqueCode = userInfo.data ? userInfo.data.uniqueCode : '';
        
        // 生成traceId
        var chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        var randomStr = '';
        for (var i = 0; i < 32; i++) {{
            randomStr += chars[Math.floor(Math.random() * chars.length)];
        }}
        var traceId = randomStr + Date.now();
        
        var urlPath = '/wap/activity/V2/ticket/list';
        var terminal = 'wap';
        var version = '997';
        
        // 请求体
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
            idToken: idToken,
            uniqueCode: uniqueCode,
            timestamp: Date.now()
        }});
        
        // 计算CRPSIGN
        var raw = accessToken + sign + idToken + (userId ? userId.toString() : '') + terminal + token + body + urlPath + version + terminal + traceId;
        var crpsign = md5(raw);
        
        console.log('=== 请求信息 ===');
        console.log('accessToken:', accessToken);
        console.log('sign:', sign);
        console.log('idToken:', idToken);
        console.log('userId:', userId);
        console.log('st_flpv:', st_flpv);
        console.log('token:', token);
        console.log('uniqueCode:', uniqueCode);
        console.log('CRPSIGN:', crpsign);
        console.log('Request body:', body);
        
        // 发送请求
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('CTERMINAL', 'wap');
        xhr.setRequestHeader('CSAPPID', 'wap');
        xhr.setRequestHeader('CVERSION', '997');
        xhr.setRequestHeader('CUSAT', accessToken);
        xhr.setRequestHeader('CUSUT', sign);
        xhr.setRequestHeader('CUSIT', idToken);
        xhr.setRequestHeader('CUSID', userId ? userId.toString() : '');
        xhr.setRequestHeader('CDEVICENO', token);
        xhr.setRequestHeader('st_flpv', st_flpv);
        xhr.setRequestHeader('CRTRACEID', traceId);
        xhr.setRequestHeader('CRPSIGN', crpsign);
        xhr.setRequestHeader('Referer', 'https://wap.showstart.com/pages/activity/detail/detail?activityId={event_id}');
        xhr.setRequestHeader('Origin', 'https://wap.showstart.com');
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.withCredentials = true;
        
        xhr.send(body);
        
        console.log('=== 响应 ===');
        console.log('Status:', xhr.status);
        console.log('Response:', xhr.responseText);
        
        return xhr.responseText;
    """
    
    print("\n" + "="*80)
    print("测试完整参数的API请求")
    print("="*80)
    
    result = driver.execute_script(js_test)
    print(f"\n响应: {result}")
    
    # 解析响应
    try:
        result_json = json.loads(result)
        print(f"\n解析结果:")
        print(f"  code: {result_json.get('code')}")
        print(f"  success: {result_json.get('success')}")
        print(f"  msg: {result_json.get('msg')}")
        print(f"  state: {result_json.get('state')}")
        if 'data' in result_json:
            data = result_json['data']
            print(f"  data类型: {type(data)}")
            if isinstance(data, dict) and 'ticketList' in data:
                print(f"  票档数量: {len(data['ticketList'])}")
                for t in data['ticketList']:
                    print(f"    - {t.get('ticketName', t.get('name', ''))}: ¥{t.get('price', 0)}")
    except Exception as e:
        print(f"\n解析JSON失败: {e}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    test_complete_params()