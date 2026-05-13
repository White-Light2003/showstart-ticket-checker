#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐个测试每个参数的正确性"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_each_param():
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
    driver.get("https://wap.showstart.com")
    
    input("请登录后按回车继续...")
    
    event_id = "295821"
    
    # 首先检查localStorage
    print("\n" + "="*80)
    print("检查localStorage内容:")
    print("="*80)
    
    storage_check = driver.execute_script("""
        var accessToken = localStorage.getItem('accessToken');
        var sign = localStorage.getItem('sign');
        var idToken = localStorage.getItem('idToken');
        var token = localStorage.getItem('token');
        var st_flpv = localStorage.getItem('st_flpv');
        var userInfoStr = localStorage.getItem('userInfo');
        
        console.log('accessToken:', accessToken);
        console.log('sign:', sign);
        console.log('idToken:', idToken);
        console.log('token:', token);
        console.log('st_flpv:', st_flpv);
        console.log('userInfo:', userInfoStr);
        
        var userInfo = JSON.parse(userInfoStr || '{}');
        var userId = userInfo.data ? userInfo.data.userId : null;
        
        return JSON.stringify({
            accessToken: accessToken,
            sign: sign,
            idToken: idToken,
            token: token,
            st_flpv: st_flpv,
            userId: userId,
            userIdType: typeof userId,
            userInfo: userInfo
        }, null, 2);
    """)
    
    print(storage_check)
    
    # 测试1: 检查是否有CRPSIGN签名头缺失
    print("\n" + "="*80)
    print("测试1: 添加CRPSIGN签名头...")
    print("="*80)
    
    js_test1 = f"""
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var st_flpv = localStorage.getItem('st_flpv') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: st_flpv,
            sign: sign,
            trackPath: ''
        }});
        
        // 生成traceId
        var chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        var randomStr = '';
        for (var i = 0; i < 32; i++) {{
            randomStr += chars[Math.floor(Math.random() * chars.length)];
        }}
        var traceId = randomStr + Date.now();
        
        // MD5签名计算
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
                b = ii(b, c, d, a, k[5], 21, -289933462);
                a = ii(a, b, c, d, k[12], 6, -206413683);
                d = ii(d, a, b, c, k[3], 10, -1604182996);
                c = ii(c, d, a, b, k[10], 15, -1134597877);
                b = ii(b, c, d, a, k[1], 21, 1855165014);
                a = ii(a, b, c, d, k[8], 6, 1310974796);
                d = ii(d, a, b, c, k[15], 10, 1157377689);
                c = ii(c, d, a, b, k[6], 15, -1112649068);
                b = ii(b, c, d, a, k[13], 21, -1703811985);
                a = ii(a, b, c, d, k[4], 6, -1516987130);
                d = ii(d, a, b, c, k[11], 10, -1321499986);
                c = ii(c, d, a, b, k[2], 15, -1902582663);
                b = ii(b, c, d, a, k[9], 21, 855351967);
                a = ii(a, b, c, d, k[0], 6, 1191212859);
                d = ii(d, a, b, c, k[7], 10, 1083174350);
                c = ii(c, d, a, b, k[14], 15, -2137633280);
                b = ii(b, c, d, a, k[5], 21, -1364441957);
                a = ii(a, b, c, d, k[12], 6, 1837980176);
                d = ii(d, a, b, c, k[3], 10, -996138196);
                c = ii(c, d, a, b, k[10], 15, 401469339);
                b = ii(b, c, d, a, k[1], 21, 818396325);
                a = ii(a, b, c, d, k[8], 6, -2064611695);
                d = ii(d, a, b, c, k[15], 10, -1917505487);
                c = ii(c, d, a, b, k[6], 15, 1547411193);
                b = ii(b, c, d, a, k[13], 21, -1508917512);
                a = ii(a, b, c, d, k[4], 6, -1835160172);
                d = ii(d, a, b, c, k[11], 10, -1350670110);
                c = ii(c, d, a, b, k[2], 15, -1426017123);
                b = ii(b, c, d, a, k[9], 21, 2064611695);
                return [a, b, c, d];
            }}
            
            function cmn(q, a, b, x, s, t) {{
                a = add(a, add(add(q, x), t));
                return add((a << s) | (a >>> (32 - s)), b);
            }}
            
            function ff(a, b, c, d, x, s, t) {{
                return cmn((b & c) | ((~b) & d), a, b, x, s, t);
            }}
            
            function gg(a, b, c, d, x, s, t) {{
                return cmn((b & d) | (c & (~d)), a, b, x, s, t);
            }}
            
            function hh(a, b, c, d, x, s, t) {{
                return cmn(b ^ c ^ d, a, b, x, s, t);
            }}
            
            function ii(a, b, c, d, x, s, t) {{
                return cmn(c ^ (b | (~d)), a, b, x, s, t);
            }}
            
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
            
            function hex(x) {{
                for (var i = 0; i < x.length; i++)
                    x[i] = rhex(x[i]);
                return x.join('');
            }}
            
            function add(a, b) {{
                return (a + b) & 0xFFFFFFFF;
            }}
            
            var i, j, s = input, md5blklist = md5blks(s);
            var n = md5blklist.length;
            s = '';
            for (i = 0; i < n; i++) {{
                j = i * 4;
                s += String.fromCharCode(md5blklist[j]) + String.fromCharCode(md5blklist[j + 1]) + String.fromCharCode(md5blklist[j + 2]) + String.fromCharCode(md5blklist[j + 3]);
            }}
            s = md5blklist.map(function(x) {{ return String.fromCharCode(x & 0xff, (x >>> 8) & 0xff, (x >>> 16) & 0xff, (x >>> 24) & 0xff); }}).join('');
            
            n = 8 * s.length;
            var x = md5blklist;
            x[n >> 5] |= 0x80 << ((n) % 32);
            x[(((n + 64) >>> 9) << 4) + 14] = n;
            
            var a = 1732584193, b = -271733879, c = -1732584194, d = 271733878;
            
            for (i = 0; i < x.length; i += 16) {{
                var olda = a, oldb = b, oldc = c, oldd = d;
                a = md5cycle([a, b, c, d], x.slice(i, i + 16));
                d = md5cycle(d, [a, b, c, d], x.slice(i, i + 16));
                c = md5cycle(c, [d, a, b, d], x.slice(i, i + 16));
                b = md5cycle(b, [c, d, a, d], x.slice(i, i + 16));
                a = md5cycle(a, [b, c, d, d], x.slice(i, i + 16));
                d = md5cycle(d, [a, b, c, d], x.slice(i, i + 16));
                c = md5cycle(c, [d, a, b, d], x.slice(i, i + 16));
                b = md5cycle(b, [c, d, a, d], x.slice(i, i + 16));
                d = md5cycle(d, [a, b, c, d], x.slice(i, i + 16));
                c = md5cycle(c, [d, a, b, d], x.slice(i, i + 16));
                b = md5cycle(b, [c, d, a, d], x.slice(i, i + 16));
                a = md5cycle(a, [b, c, d, d], x.slice(i, i + 16));
                a = add(a, olda);
                b = add(b, oldb);
                c = add(c, oldc);
                d = add(d, oldd);
            }}
            return hex([a, b, c, d]);
        }}
        
        // 计算CRPSIGN
        var urlPath = '/wap/activity/V2/ticket/list';
        var terminal = 'wap';
        var version = '997';
        var raw = accessToken + sign + idToken + (userId ? userId.toString() : '') + terminal + token + body + urlPath + version + terminal + traceId;
        console.log('CRPSIGN计算原料:', raw);
        var crpsign = md5(raw);
        console.log('CRPSIGN:', crpsign);
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://wap.showstart.com/v3' + urlPath, false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('CTERMINAL', terminal);
        xhr.setRequestHeader('CSAPPID', terminal);
        xhr.setRequestHeader('CVERSION', version);
        xhr.setRequestHeader('CUSAT', accessToken);
        xhr.setRequestHeader('CUSUT', sign);
        xhr.setRequestHeader('CUSIT', idToken);
        xhr.setRequestHeader('CUSID', userId ? userId.toString() : '');
        xhr.setRequestHeader('CDEVICENO', token);
        xhr.setRequestHeader('st_flpv', st_flpv);
        xhr.setRequestHeader('CRPSIGN', crpsign);
        xhr.setRequestHeader('CRTRACEID', traceId);
        xhr.withCredentials = true;
        
        xhr.send(body);
        
        console.log('Response:', xhr.responseText);
        return JSON.stringify({{
            status: xhr.status,
            response: xhr.responseText,
            crpsign: crpsign,
            raw: raw
        }});
    """
    
    result1 = driver.execute_script(js_test1)
    print(f"\n测试1结果: {result1}")
    
    # 测试2: 检查Referer和Origin头
    print("\n" + "="*80)
    print("测试2: 添加Referer和Origin头...")
    print("="*80)
    
    js_test2 = f"""
        var accessToken = localStorage.getItem('accessToken') || '';
        var sign = localStorage.getItem('sign') || '';
        var idToken = localStorage.getItem('idToken') || '';
        var token = localStorage.getItem('token') || '';
        var st_flpv = localStorage.getItem('st_flpv') || '';
        var userInfoStr = localStorage.getItem('userInfo') || '{{}}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: st_flpv,
            sign: sign,
            trackPath: ''
        }});
        
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
        xhr.setRequestHeader('Referer', 'https://wap.showstart.com/');
        xhr.setRequestHeader('Origin', 'https://wap.showstart.com');
        xhr.withCredentials = true;
        
        xhr.send(body);
        
        return JSON.stringify({{
            status: xhr.status,
            response: xhr.responseText
        }});
    """
    
    result2 = driver.execute_script(js_test2)
    print(f"\n测试2结果: {result2}")
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    test_each_param()