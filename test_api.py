#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试API功能"""

import json
import os
import struct
import random
import hashlib

# ===================== 魔改MD5 =====================
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

        if first:
            w = [0] * 64
            for j in range(16):
                w[j] = struct.unpack('<I', block[j*4:(j+1)*4])[0]
            
            a = h0
            b = h1
            c = h2
            d = h3
            
            for j in range(64):
                if j < 16:
                    f = (b & c) | ((~b) & d)
                    g = j
                elif j < 32:
                    f = (d & b) | ((~d) & c)
                    g = (5*j + 1) % 16
                elif j < 48:
                    f = b ^ c ^ d
                    g = (3*j + 5) % 16
                else:
                    f = c ^ (b | (~d))
                    g = (7*j) % 16
                
                temp = d
                d = c
                c = b
                b = uint32(b + left_rotate(uint32(a + f + [
                    0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE,
                    0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
                    0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE,
                    0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821,
                    0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA,
                    0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
                    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED,
                    0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A,
                    0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C,
                    0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
                    0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05,
                    0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
                    0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039,
                    0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
                    0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1,
                    0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391
                ][j] + w[g]), [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                              5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                              4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                              6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21][j]))
                a = temp
            
            h0 = uint32(h0 + a)
            h1 = uint32(h1 + b)
            h2 = uint32(h2 + c)
            h3 = uint32(h3 + d)
            
            first = False
        else:
            import hashlib
            md5 = hashlib.md5()
            md5.update(block)
            block_hash = md5.digest()
            
            a = h0
            b = h1
            c = h2
            d = h3
            
            w = list(struct.unpack('<16I', block_hash + b'\x00' * 48))[:16]
            
            for j in range(64):
                if j < 16:
                    f = (b & c) | ((~b) & d)
                    g = j
                elif j < 32:
                    f = (d & b) | ((~d) & c)
                    g = (5*j + 1) % 16
                elif j < 48:
                    f = b ^ c ^ d
                    g = (3*j + 5) % 16
                else:
                    f = c ^ (b | (~d))
                    g = (7*j) % 16
                
                temp = d
                d = c
                c = b
                b = uint32(b + left_rotate(uint32(a + f + [
                    0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE,
                    0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
                    0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE,
                    0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821,
                    0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA,
                    0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
                    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED,
                    0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A,
                    0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C,
                    0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
                    0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05,
                    0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
                    0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039,
                    0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
                    0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1,
                    0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391
                ][j] + w[g]), [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                              5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                              4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                              6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21][j]))
                a = temp
            
            h0 = uint32(h0 + a)
            h1 = uint32(h1 + b)
            h2 = uint32(h2 + c)
            h3 = uint32(h3 + d)

    digest = struct.pack('<4I', h0, h1, h2, h3)
    return ''.join(f'{b:02x}' for b in digest)

def generate_trace_id() -> str:
    """生成随机traceId"""
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(32))

def calculate_crpsign(access_token: str, sign: str, id_token: str, user_id: str,
                      token: str, body: str, url_path: str, terminal: str, trace_id: str) -> str:
    raw = (access_token + sign + id_token + str(user_id) + "wap" +
           token + body + url_path + "997" + terminal + trace_id)
    print(f"[DEBUG] 签名原料长度: {len(raw)}")
    print(f"[DEBUG] 签名原料前50字符: {raw[:50]}")
    result = custom_md5(raw.encode('utf-8'))
    print(f"[DEBUG] 生成的签名: {result}")
    return result

def get_ticket_info_api(event_id: str, tokens: dict):
    import requests
    
    try:
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

        print(f"[DEBUG] 请求URL: {full_url}")
        print(f"[DEBUG] 请求体: {body_str}")
        print(f"[DEBUG] tokens字段: {list(tokens.keys())}")
        
        crpsign = calculate_crpsign(
            access_token=tokens['accessToken'],
            sign=tokens['sign'],
            id_token=tokens['idToken'],
            user_id=str(tokens['userId']),
            token=tokens['token'],
            body=body_str,
            url_path=url_path,
            terminal='wap',
            trace_id=trace_id
        )

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
            'Referer': 'https://wap.showstart.com/'
        }
        
        print(f"[DEBUG] 请求头数量: {len(headers)}")
        print(f"[DEBUG] 请求头中的关键字段:")
        print(f"  CUSAT: {headers['CUSAT'][:20]}...")
        print(f"  CUSUT: {headers['CUSUT'][:20]}...")
        print(f"  CUSIT: {headers['CUSIT'][:20]}...")
        print(f"  CRPSIGN: {headers['CRPSIGN']}")
        print(f"  CRTRACEID: {headers['CRTRACEID']}")

        response = requests.post(full_url, data=body_str.encode('utf-8'), headers=headers, timeout=10)
        print(f"[DEBUG] HTTP状态码: {response.status_code}")
        print(f"[DEBUG] 响应内容: {response.text[:500]}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"[DEBUG] 响应JSON: {result}")
            
            if result.get('code') == 0:
                ticket_list = result.get('data', {}).get('ticketList', [])
                print(f"[SUCCESS] 成功获取 {len(ticket_list)} 个票档!")
                for t in ticket_list:
                    print(f"  - {t.get('ticketName', '')}: {t.get('price', 0)}元, 库存: {t.get('stock', 0)}")
                return ticket_list
            else:
                print(f"[ERROR] 接口返回错误: {result.get('msg', '未知错误')}")
                return None
        else:
            print(f"[ERROR] HTTP错误: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[ERROR] 异常: {e}")
        import traceback
        print(traceback.format_exc())
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("API测试脚本")
    print("=" * 60)
    
    # 尝试从config.json加载tokens
    tokens = None
    
    if os.path.exists('config.json'):
        print("从config.json加载tokens...")
        with open('config.json', 'r', encoding='utf-8') as f:
            tokens = json.load(f)
        print(f"加载到的tokens字段: {list(tokens.keys())}")
    
    # 如果没有，尝试从tokens.json加载
    if not tokens:
        config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
        config_path = os.path.join(config_dir, 'tokens.json')
        if os.path.exists(config_path):
            print(f"从{config_path}加载tokens...")
            with open(config_path, 'r', encoding='utf-8') as f:
                tokens = json.load(f)
            print(f"加载到的tokens字段: {list(tokens.keys())}")
    
    if not tokens:
        print("ERROR: 无法找到tokens配置文件!")
        exit(1)
    
    print()
    event_id = input("请输入演出ID (默认: 295821): ").strip()
    if not event_id:
        event_id = "295821"
    
    print()
    print(f"正在测试演出 {event_id} 的API...")
    print("-" * 60)
    result = get_ticket_info_api(event_id, tokens)
    print("-" * 60)
    
    if result:
        print("\n✅ API测试成功!")
    else:
        print("\n❌ API测试失败!")

