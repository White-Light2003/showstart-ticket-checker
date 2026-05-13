#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试CRPSIGN签名计算"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_crsign():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://wap.showstart.com")
    
    input("请登录后按回车继续...")
    
    event_id = "295821"
    
    # 使用真实cURL中的值来测试
    js_test = f"""
        // 真实cURL中的值
        var real_accessToken = 'db1cd22118e20c436a03533bIhfCMxeF';
        var real_sign = '47ef9cd5c7855295527f881a2a860257';
        var real_idToken = '7ad44157656c33fa6a035355SYP53LCQ';
        var real_userId = '18726052';
        var real_token = 'q6ac0i82mk6dzs877ln0g1yt8uyk07bj';
        var real_st_flpv = 'OZ920fB62TS4h1j14QR0';
        var real_traceId = '7s0a97IS5X84V53hC37pAru01sZ0V88o1778600758843';
        var real_crpsign = '9c431cf1ca07710c66c0e027d70feee3';
        
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
            
            function md51(s) {{
                var n = s.length, state = [1732584193, -271733879, -1732584194, 271733878], i;
                for (i = 64; i <= n; i += 64) {{
                    state = md5cycle(state, md5blk(s.substring(i - 64, i)));
                }}
                s = s.substring(i - 64);
                var p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                for (i = 0; i < s.length; i++) p[i >> 2] |= s.charCodeAt(i) << ((i % 4) << 3);
                p[i >> 2] |= 0x80 << ((i % 4) << 3);
                if (i > 55) {{ state = md5cycle(state, p); p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; }}
                p[14] = n * 8;
                state = md5cycle(state, p);
                return state;
            }}
            
            function md5blk(s) {{
                var md5blks = [], i;
                for (i = 0; i < 64; i += 4) {{
                    md5blks[i >> 2] = s.charCodeAt(i) + (s.charCodeAt(i + 1) << 8) + (s.charCodeAt(i + 2) << 16) + (s.charCodeAt(i + 3) << 24);
                }}
                return md5blks;
            }}
            
            function rhex(n) {{
                var s = '', j = 0;
                for (; j < 4; j++) s += ((n >>> j * 8) & 0xff).toString(16).padStart(2, '0');
                return s;
            }}
            
            function hex(x) {{ return x.map(rhex).join(''); }}
            
            function add(a, b) {{ return (a + b) & 0xffffffff; }}
            
            return hex(md51(input));
        }}
        
        // 构造请求体
        var body = JSON.stringify({{
            activityId: '{event_id}',
            coupon: '',
            st_flpv: real_st_flpv,
            sign: real_sign,
            trackPath: ''
        }});
        
        // URL和参数
        var urlPath = '/wap/activity/V2/ticket/list';
        var terminal = 'wap';
        var version = '997';
        
        // 计算CRPSIGN
        var raw = real_accessToken + real_sign + real_idToken + real_userId + terminal + real_token + body + urlPath + version + terminal + real_traceId;
        console.log('CRPSIGN计算原料:', raw);
        console.log('长度:', raw.length);
        var crpsign = md5(raw);
        console.log('计算的CRPSIGN:', crpsign);
        console.log('真实的CRPSIGN:', real_crpsign);
        console.log('是否相同:', crpsign === real_crpsign);
        
        return JSON.stringify({{
            crpsign_calc: crpsign,
            crpsign_real: real_crpsign,
            match: crpsign === real_crpsign,
            raw: raw
        }});
    """
    
    print("\n" + "="*80)
    print("调试CRPSIGN签名计算")
    print("="*80)
    
    result = driver.execute_script(js_test)
    result_json = json.loads(result)
    
    print(f"\n计算的CRPSIGN: {result_json['crpsign_calc']}")
    print(f"真实的CRPSIGN: {result_json['crpsign_real']}")
    print(f"是否匹配: {result_json['match']}")
    print(f"\nCRPSIGN计算原料:")
    print(result_json['raw'])
    
    input("\n按回车退出...")
    driver.quit()

if __name__ == "__main__":
    debug_crsign()