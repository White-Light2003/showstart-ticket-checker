#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试不同的header组合"""

import json
import struct
import hashlib
import requests
import time
import random

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

def generate_trace_id() -> str:
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    random_str = ''.join(random.choice(chars) for _ in range(32))
    timestamp = str(int(time.time() * 1000))
    return random_str + timestamp

def test_with_headers(event_id: str, tokens: dict, use_extra_headers: bool):
    url_path = '/wap/activity/V2/ticket/list'
    full_url = 'https://wap.showstart.com/v3' + url_path

    body_dict = {
        'activityId': str(event_id),
        'coupon': '',
        'st_flpv': tokens.get('st_flpv', ''),
        'sign': tokens.get('sign', ''),
        'trackPath': ''
    }
    body_str = json.dumps(body_dict, separators=(',', ':'), ensure_ascii=False)

    trace_id = generate_trace_id()
    crpsign = custom_md5((tokens['accessToken'] + tokens['sign'] + tokens['idToken'] + str(tokens['userId']) + "wap" +
           tokens['token'] + body_str + url_path + "997" + "wap" + trace_id).encode('utf-8'))

    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'CTERMINAL': 'wap',
        'CSAPPID': 'wap',
        'CVERSION': '997',
        'CUSAT': tokens['accessToken'],
        'CUSUT': tokens['sign'],
        'CUSIT': tokens['idToken'],
        'CUSID': str(tokens['userId']),
        'CUSNAME': 'nil',
        'CDEVICENO': tokens['token'],
        'CUUSERREF': tokens['token'],
        'st_flpv': tokens.get('st_flpv', ''),
        'CRPSIGN': crpsign,
        'CRTRACEID': trace_id,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
        'Host': 'wap.showstart.com',
        'Origin': 'https://wap.showstart.com',
        'Referer': f'https://wap.showstart.com/pages/activity/detail/detail?activityId={event_id}'
    }

    if use_extra_headers:
        headers.update({
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'CDEVICEINFO': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
            'CSPAPPID': 'ssapp',
            'CSOURCEPATH': '/pages/activity/detail/detail',
            'CUSTOKEN': tokens.get('token', ''),
            'CSTOKEN': tokens.get('token', ''),
            'Connection': 'keep-alive'
        })

    session = requests.Session()
    if tokens.get('st_flpv'):
        session.cookies.set('st_flpv', tokens['st_flpv'], domain='.showstart.com')
    if tokens.get('token'):
        session.cookies.set('CUSTOKEN', tokens['token'], domain='.showstart.com')

    response = session.post(full_url, data=body_str.encode('utf-8'), headers=headers, timeout=10)
    result = response.json()
    print(f"  Response: {result.get('msg', 'Unknown')}")
    return result

if __name__ == "__main__":
    print("=" * 60)
    print("Header Combination Test")
    print("=" * 60)

    with open('config.json', 'r', encoding='utf-8') as f:
        tokens = json.load(f)

    event_id = input("Enter event ID (default 295821): ").strip() or "295821"

    print("\nTest 1: Basic Headers Only")
    print("-" * 40)
    test_with_headers(event_id, tokens, use_extra_headers=False)

    print("\nTest 2: With Extra Headers")
    print("-" * 40)
    test_with_headers(event_id, tokens, use_extra_headers=True)
