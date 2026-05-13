#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试浏览器中的CRPSIGN计算"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Chrome用户配置文件路径 - 用户需要根据自己的系统配置修改
# Windows默认路径: C:\Users\<用户名>\AppData\Local\Google\Chrome\User Data
# macOS默认路径: ~/Library/Application Support/Google/Chrome
# Linux默认路径: ~/.config/google-chrome
CHROME_USER_DATA_DIR = None  # 设置为None时使用临时配置文件

def debug_crpsign_in_browser():
    # 配置浏览器选项
    options = Options()
    
    # 如果设置了用户配置文件路径，使用指定路径；否则使用临时配置
    if CHROME_USER_DATA_DIR:
        options.add_argument(f'--user-data-dir={CHROME_USER_DATA_DIR}')
        options.add_argument('--profile-directory=Default')
        print(f"[INFO] 使用指定的Chrome配置文件: {CHROME_USER_DATA_DIR}")
    else:
        print("[INFO] 使用临时Chrome配置文件（首次运行需要重新登录）")
    
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # 打开秀动页面
        driver.get('https://wap.showstart.com/pages/activity/detail/detail?activityId=295821')
        time.sleep(3)
        
        # 执行调试JavaScript
        js_code = """
            // 生成traceId
            function generateTraceId() {
                var chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
                var randomStr = '';
                for (var i = 0; i < 32; i++) {
                    randomStr += chars[Math.floor(Math.random() * chars.length)];
                }
                return randomStr + Date.now();
            }
            
            // 标准MD5实现
            function md5(input) {
                function md5cycle(x, k) {
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
                    c = hh(c, d, a, b, k[7], 16, -155497632);
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
                    b = ii(b, c, d, a, k[9], 21, -343485551);
                    x[0] = add32(a, x[0]);
                    x[1] = add32(b, x[1]);
                    x[2] = add32(c, x[2]);
                    x[3] = add32(d, x[3]);
                }
                function cmn(q, a, b, x, s, t) {
                    a = add32(add32(a, q), add32(x, t));
                    return add32((a << s) | (a >>> (32 - s)), b);
                }
                function ff(a, b, c, d, x, s, t) {
                    return cmn((b & c) | ((~b) & d), a, b, x, s, t);
                }
                function gg(a, b, c, d, x, s, t) {
                    return cmn((b & d) | (c & (~d)), a, b, x, s, t);
                }
                function hh(a, b, c, d, x, s, t) {
                    return cmn(b ^ c ^ d, a, b, x, s, t);
                }
                function ii(a, b, c, d, x, s, t) {
                    return cmn(c ^ (b | (~d)), a, b, x, s, t);
                }
                function add32(a, b) {
                    return (a + b) & 0xFFFFFFFF;
                }
                function rhex(num) {
                    var str = "", i;
                    for (i = 0; i < 4; i++) {
                        str += ((num >> (8 * (3 - i))) & 0xFF).toString(16).padStart(2, "0");
                    }
                    return str;
                }
                function str2binl(str) {
                    var bin = [], mask = 0xFF, i;
                    for (i = 0; i < str.length * 8; i += 8) {
                        bin[i >> 5] |= (str.charCodeAt(i / 8) & mask) << (24 - (i % 32));
                    }
                    return bin;
                }
                var nblk = ((input.length + 8) >> 6) + 1;
                var blks = new Array(nblk * 16);
                for (var i = 0; i < blks.length; i++) blks[i] = 0;
                for (i = 0; i < input.length; i++) {
                    blks[i >> 2] |= input.charCodeAt(i) << (24 - (i % 4) * 8);
                }
                blks[i >> 2] |= 0x80 << (24 - (i % 4) * 8);
                blks[nblk * 16 - 2] = input.length * 8;
                var x = [1732584193, 4023233417, 2562383102, 271733878];
                for (i = 0; i < nblk; i++) {
                    var w = new Array(16);
                    for (var j = 0; j < 16; j++) {
                        w[j] = blks[i * 16 + j];
                    }
                    md5cycle(x, w);
                }
                return rhex(x[0]) + rhex(x[1]) + rhex(x[2]) + rhex(x[3]);
            }
            
            // 获取localStorage中的值
            var accessToken = localStorage.getItem('accessToken') || '';
            var sign = localStorage.getItem('sign') || '';
            var idToken = localStorage.getItem('idToken') || '';
            var token = localStorage.getItem('token') || '';
            var userInfoStr = localStorage.getItem('userInfo') || '{}';
            var userInfo = JSON.parse(userInfoStr);
            var userId = userInfo.data ? userInfo.data.userId : (localStorage.getItem('userId') || '');
            var st_flpv = userInfo.data && userInfo.data.st_flpv ? userInfo.data.st_flpv : (localStorage.getItem('st_flpv') || '');
            
            var urlPath = '/wap/activity/V2/ticket/list';
            var terminal = 'wap';
            var version = '997';
            var traceId = generateTraceId();
            
            var body = JSON.stringify({
                activityId: '295821',
                coupon: '',
                st_flpv: st_flpv,
                sign: sign,
                trackPath: ''
            });
            
            // 计算CRPSIGN签名
            var raw = accessToken + sign + idToken + (userId ? userId.toString() : '') + terminal + token + body + urlPath + version + terminal + traceId;
            var crpsign = md5(raw);
            
            // 返回调试信息
            return JSON.stringify({
                accessToken: accessToken,
                sign: sign,
                idToken: idToken,
                token: token,
                userId: userId,
                st_flpv: st_flpv,
                terminal: terminal,
                version: version,
                traceId: traceId,
                body: body,
                urlPath: urlPath,
                raw: raw,
                crpsign: crpsign,
                rawLength: raw.length,
                hasEmpty: !accessToken || !sign || !idToken || !token || !userId
            });
        """
        
        result = driver.execute_script(js_code)
        print("浏览器调试结果：")
        print(result)
        
    finally:
        driver.quit()

if __name__ == '__main__':
    debug_crpsign_in_browser()
