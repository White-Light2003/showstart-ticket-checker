#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""详细调试签名计算"""
import os
import sys
import json
import time
import random
import struct
import hashlib
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def uint32(x):
    return x & 0xFFFFFFFF

def custom_md5(message: bytes) -> str:
    original_len = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('<Q', original_len)

    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476

    first = True

    for i in range(0, len(message), 64):
        block = message[i:i+64]
        r = list(struct.unpack('<16I', block))

        if first:
            e = uint32(r[0] - 680876937)
            e = uint32(left_rotate(e, 7) - 271733879)
            t = uint32((uint32(-1732584194) ^ (2004318071 & e)) + r[1] - 117830708)
            t = uint32(left_rotate(t, 12) + e)
            a = uint32((uint32(-271733879) ^ (t & (uint32(-271733879) ^ e))) + r[2] - 1126478375)
            a = uint32(left_rotate(a, 17) + t)
            n = uint32((e ^ (a & (t ^ e))) + r[3] - 1316259209)
            n = uint32(left_rotate(n, 22) + a)
            e = uint32(e + (t ^ (n & (a ^ t))) + r[4] - 176418897)
            e = uint32(left_rotate(e, 7) + n)
            t = uint32(t + (a ^ (e & (n ^ a))) + r[5] + 1200080426)
            t = uint32(left_rotate(t, 12) + e)
            a = uint32(a + (n ^ (t & (e ^ n))) + r[6] - 1473231341)
            a = uint32(left_rotate(a, 17) + t)
            n = uint32(n + (e ^ (a & (t ^ e))) + r[7] - 45705983)
            n = uint32(left_rotate(n, 22) + a)
            e = uint32(e + (t ^ (n & (a ^ t))) + r[8] + 1770035416)
            e = uint32(left_rotate(e, 7) + n)
            t = uint32(t + (a ^ (e & (n ^ a))) + r[9] - 1958414417)
            t = uint32(left_rotate(t, 12) + e)
            a = uint32(a + (n ^ (t & (e ^ n))) + r[10] - 42063)
            a = uint32(left_rotate(a, 17) + t)
            n = uint32(n + (e ^ (a & (t ^ e))) + r[11] - 1990404162)
            n = uint32(left_rotate(n, 22) + a)
            e = uint32(e + (t ^ (n & (a ^ t))) + r[12] + 1804603682)
            e = uint32(left_rotate(e, 7) + n)
            t = uint32(t + (a ^ (e & (n ^ a))) + r[13] - 40341101)
            t = uint32(left_rotate(t, 12) + e)
            a = uint32(a + (n ^ (t & (e ^ n))) + r[14] - 1502002290)
            a = uint32(left_rotate(a, 17) + t)
            n = uint32(n + (e ^ (a & (t ^ e))) + r[15] + 1236535329)
            n = uint32(left_rotate(n, 22) + a)

            e = uint32(e + (a ^ (t & (n ^ a))) + r[1] - 165796510)
            e = uint32(left_rotate(e, 5) + n)
            t = uint32(t + (n ^ (a & (e ^ n))) + r[6] - 1069501632)
            t = uint32(left_rotate(t, 9) + e)
            a = uint32(a + (e ^ (n & (t ^ e))) + r[11] + 643717713)
            a = uint32(left_rotate(a, 14) + t)
            n = uint32(n + (t ^ (e & (a ^ t))) + r[0] - 373897302)
            n = uint32(left_rotate(n, 20) + a)
            e = uint32(e + (a ^ (t & (n ^ a))) + r[5] - 701558691)
            e = uint32(left_rotate(e, 5) + n)
            t = uint32(t + (n ^ (a & (e ^ n))) + r[10] + 38016083)
            t = uint32(left_rotate(t, 9) + e)
            a = uint32(a + (e ^ (n & (t ^ e))) + r[15] - 660478335)
            a = uint32(left_rotate(a, 14) + t)
            n = uint32(n + (t ^ (e & (a ^ t))) + r[4] - 405537848)
            n = uint32(left_rotate(n, 20) + a)
            e = uint32(e + (a ^ (t & (n ^ a))) + r[9] + 568446438)
            e = uint32(left_rotate(e, 5) + n)
            t = uint32(t + (n ^ (a & (e ^ n))) + r[14] - 1019803690)
            t = uint32(left_rotate(t, 9) + e)
            a = uint32(a + (e ^ (n & (t ^ e))) + r[3] - 187363961)
            a = uint32(left_rotate(a, 14) + t)
            n = uint32(n + (t ^ (e & (a ^ t))) + r[8] + 1163531501)
            n = uint32(left_rotate(n, 20) + a)
            e = uint32(e + (a ^ (t & (n ^ a))) + r[13] - 1444681467)
            e = uint32(left_rotate(e, 5) + n)
            t = uint32(t + (n ^ (a & (e ^ n))) + r[2] - 51403784)
            t = uint32(left_rotate(t, 9) + e)
            a = uint32(a + (e ^ (n & (t ^ e))) + r[7] + 1735328473)
            a = uint32(left_rotate(a, 14) + t)
            n = uint32(n + (t ^ (e & (a ^ t))) + r[12] - 1926607734)
            n = uint32(left_rotate(n, 20) + a)

            i_val = n ^ a
            e = uint32(e + (i_val ^ t) + r[5] - 378558)
            e = uint32(left_rotate(e, 4) + n)
            t = uint32(t + (i_val ^ e) + r[8] - 2022574463)
            t = uint32(left_rotate(t, 11) + e)
            o = t ^ e
            a = uint32(a + (o ^ n) + r[11] + 1839030562)
            a = uint32(left_rotate(a, 16) + t)
            n = uint32(n + (o ^ a) + r[14] - 35309556)
            n = uint32(left_rotate(n, 23) + a)
            i_val = n ^ a
            e = uint32(e + (i_val ^ t) + r[1] - 1530992060)
            e = uint32(left_rotate(e, 4) + n)
            t = uint32(t + (i_val ^ e) + r[4] + 1272893353)
            t = uint32(left_rotate(t, 11) + e)
            o = t ^ e
            a = uint32(a + (o ^ n) + r[7] - 155497632)
            a = uint32(left_rotate(a, 16) + t)
            n = uint32(n + (o ^ a) + r[10] - 1094730640)
            n = uint32(left_rotate(n, 23) + a)
            i_val = n ^ a
            e = uint32(e + (i_val ^ t) + r[13] + 681279174)
            e = uint32(left_rotate(e, 4) + n)
            t = uint32(t + (i_val ^ e) + r[0] - 358537222)
            t = uint32(left_rotate(t, 11) + e)
            o = t ^ e
            a = uint32(a + (o ^ n) + r[3] - 722521979)
            a = uint32(left_rotate(a, 16) + t)
            n = uint32(n + (o ^ a) + r[6] + 76029189)
            n = uint32(left_rotate(n, 23) + a)
            i_val = n ^ a
            e = uint32(e + (i_val ^ t) + r[9] - 640364487)
            e = uint32(left_rotate(e, 4) + n)
            t = uint32(t + (i_val ^ e) + r[12] - 421815835)
            t = uint32(left_rotate(t, 11) + e)
            o = t ^ e
            a = uint32(a + (o ^ n) + r[15] + 530742520)
            a = uint32(left_rotate(a, 16) + t)
            n = uint32(n + (o ^ a) + r[2] - 995338651)
            n = uint32(left_rotate(n, 23) + a)

            e = uint32(e + (a ^ (n | ~t)) + r[0] - 198630844)
            e = uint32(left_rotate(e, 6) + n)
            t = uint32(t + (n ^ (e | ~a)) + r[7] + 1126891415)
            t = uint32(left_rotate(t, 10) + e)
            a = uint32(a + (e ^ (t | ~n)) + r[14] - 1416354905)
            a = uint32(left_rotate(a, 15) + t)
            n = uint32(n + (t ^ (a | ~e)) + r[5] - 57434055)
            n = uint32(left_rotate(n, 21) + a)
            e = uint32(e + (a ^ (n | ~t)) + r[12] + 1700485571)
            e = uint32(left_rotate(e, 6) + n)
            t = uint32(t + (n ^ (e | ~a)) + r[3] - 1894986606)
            t = uint32(left_rotate(t, 10) + e)
            a = uint32(a + (e ^ (t | ~n)) + r[10] - 1051523)
            a = uint32(left_rotate(a, 15) + t)
            n = uint32(n + (t ^ (a | ~e)) + r[1] - 2054922799)
            n = uint32(left_rotate(n, 21) + a)
            e = uint32(e + (a ^ (n | ~t)) + r[8] + 1873313359)
            e = uint32(left_rotate(e, 6) + n)
            t = uint32(t + (n ^ (e | ~a)) + r[15] - 30611744)
            t = uint32(left_rotate(t, 10) + e)
            a = uint32(a + (e ^ (t | ~n)) + r[6] - 1560198380)
            a = uint32(left_rotate(a, 15) + t)
            n = uint32(n + (t ^ (a | ~e)) + r[13] + 1309151649)
            n = uint32(left_rotate(n, 21) + a)
            e = uint32(e + (a ^ (n | ~t)) + r[4] - 145523070)
            e = uint32(left_rotate(e, 6) + n)
            t = uint32(t + (n ^ (e | ~a)) + r[11] - 1120210379)
            t = uint32(left_rotate(t, 10) + e)
            a = uint32(a + (e ^ (t | ~n)) + r[2] + 718787259)
            a = uint32(left_rotate(a, 15) + t)
            n = uint32(n + (t ^ (a | ~e)) + r[9] - 343485551)
            n = uint32(left_rotate(n, 21) + a)

            h0 = uint32(e + 1732584193)
            h1 = uint32(n - 271733879)
            h2 = uint32(a - 1732584194)
            h3 = uint32(t + 271733878)
            first = False
        else:
            md5_std = hashlib.md5(block).digest()
            std_words = struct.unpack('<4I', md5_std)
            h0 = uint32(h0 + std_words[0])
            h1 = uint32(h1 + std_words[1])
            h2 = uint32(h2 + std_words[2])
            h3 = uint32(h3 + std_words[3])

    return struct.pack('<4I', h0, h1, h2, h3).hex()

def generate_trace_id():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    random_str = ''.join(random.choice(chars) for _ in range(32))
    timestamp = str(int(time.time() * 1000))
    return random_str + timestamp

def debug_signature():
    config_path = os.path.join(os.path.expanduser('~'), '.showstart_checker', 'tokens.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        tokens = json.load(f)

    event_id = "295821"
    url_path = '/wap/activity/V2/ticket/list'

    body_dict = {
        'activityId': str(event_id),
        'coupon': '',
        'st_flpv': tokens.get('st_flpv', ''),
        'sign': tokens.get('sign', ''),
        'trackPath': ''
    }
    body_str = json.dumps(body_dict, separators=(',', ':'), ensure_ascii=False)
    trace_id = generate_trace_id()
    user_id = str(tokens.get('userId', ''))
    terminal = 'wap'

    print("=" * 70)
    print("签名计算详细调试")
    print("=" * 70)
    
    print("\n1. 原始参数:")
    print("   accessToken: %s" % tokens['accessToken'])
    print("   sign: %s" % tokens['sign'])
    print("   idToken: %s" % tokens['idToken'])
    print("   userId: %s" % user_id)
    print("   terminal(wap): %s" % "wap")
    print("   token: %s" % tokens['token'])
    print("   body: %s" % body_str)
    print("   url_path: %s" % url_path)
    print("   CVERSION(997): %s" % "997")
    print("   terminal: %s" % terminal)
    print("   trace_id: %s" % trace_id)
    
    print("\n2. 拼接顺序:")
    print("   accessToken + sign + idToken + userId + \"wap\" + token + body + url_path + \"997\" + terminal + trace_id")
    
    raw = (tokens['accessToken'] + tokens['sign'] + tokens['idToken'] + 
           user_id + "wap" + tokens['token'] + body_str + url_path + 
           "997" + terminal + trace_id)
    
    print("\n3. 拼接后的原始字符串长度: %d" % len(raw))
    print("   原始字符串前200字符: %s" % raw[:200])
    print("   原始字符串后100字符: %s" % raw[-100:])
    
    print("\n4. 计算签名:")
    crpsign = custom_md5(raw.encode('utf-8'))
    print("   CRPSIGN: %s" % crpsign)
    
    print("\n5. 发送请求测试...")
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'CTERMINAL': 'wap',
        'CSAPPID': 'wap',
        'CVERSION': '997',
        'CUSAT': tokens['accessToken'],
        'CUSUT': tokens['sign'],
        'CUSIT': tokens['idToken'],
        'CUSID': user_id,
        'CUSNAME': 'nil',
        'CDEVICENO': tokens['token'],
        'CUUSERREF': tokens['token'],
        'st_flpv': tokens.get('st_flpv', ''),
        'CRPSIGN': crpsign,
        'CRTRACEID': trace_id,
        'CSOURCEPATH': '',
        'CTRACKPATH': '',
        'CDEVICEINFO': '%7B%22vendorName%22:%22%22,%22deviceMode%22:%22PC%22,%22deviceName%22:%22%22,%22systemName%22:%22windows%22,%22systemVersion%22:%2210%20x64%22%7D',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Host': 'wap.showstart.com',
        'Origin': 'https://wap.showstart.com',
        'Referer': 'https://wap.showstart.com/',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

    session = requests.Session()
    session.trust_env = False  # 禁用代理
    session.cookies.set('token', tokens.get('token', ''), domain='.showstart.com')
    session.cookies.set('accessToken', tokens.get('accessToken', ''), domain='.showstart.com')
    session.cookies.set('sign', tokens.get('sign', ''), domain='.showstart.com')
    session.cookies.set('idToken', tokens.get('idToken', ''), domain='.showstart.com')
    session.cookies.set('userId', user_id, domain='.showstart.com')

    try:
        resp = session.post('https://wap.showstart.com/v3' + url_path, 
                          data=body_str.encode('utf-8'), headers=headers, timeout=10)
        print("\n6. 响应结果:")
        print("   HTTP状态: %d" % resp.status_code)
        print("   响应内容: %s" % resp.text)
        
        try:
            result = resp.json()
            print("\n7. 响应解析:")
            print("   success: %s" % result.get('success'))
            print("   msg: %s" % result.get('msg'))
            print("   state: %s" % result.get('state'))
            print("   code: %s" % result.get('code'))
        except:
            print("   响应不是JSON格式")
    except Exception as e:
        print("\n6. 请求失败: %s" % e)

if __name__ == "__main__":
    debug_signature()