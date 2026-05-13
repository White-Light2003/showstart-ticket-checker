#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试API模式 - 验证token是否有效"""
import json
import os
import sys

def test_api_mode():
    # 读取token
    config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
    config_path = os.path.join(config_dir, 'tokens.json')

    if not os.path.exists(config_path):
        print("[-] tokens.json 文件不存在")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        tokens = json.load(f)

    print("="*80)
    print("测试秀动API模式")
    print("="*80)
    print(f"\n[当前Token信息]")
    print(f"accessToken: {tokens.get('accessToken', '')[:30]}...")
    print(f"sign: {tokens.get('sign', '')[:30]}...")
    print(f"idToken: {tokens.get('idToken', '')[:30]}...")
    print(f"userId: {tokens.get('userId', '')}")
    print(f"token: {tokens.get('token', '')[:30]}...")
    print(f"st_flpv: {tokens.get('st_flpv', '')}")

    # 测试API调用
    print("\n" + "="*80)
    print("测试API调用")
    print("="*80)

    import hashlib
    import requests

    event_id = '295821'
    url = 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list'
    urlPath = '/wap/activity/V2/ticket/list'
    terminal = 'wap'
    version = '997'

    accessToken = tokens.get('accessToken', '')
    sign = tokens.get('sign', '')
    idToken = tokens.get('idToken', '')
    token = tokens.get('token', '')
    userId = str(tokens.get('userId', ''))
    st_flpv = tokens.get('st_flpv', '')

    # 生成traceId
    import time
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    randomStr = ''.join([chars[int(time.time() * 1000 + i) % len(chars)] for i in range(32)])
    traceId = randomStr + str(int(time.time() * 1000))

    # 构造body
    body = f'{{"activityId":"{event_id}","coupon":"","st_flpv":"{st_flpv}","sign":"{sign}","trackPath":""}}'

    # 计算CRPSIGN
    raw = accessToken + sign + idToken + userId + terminal + token + body + urlPath + version + terminal + traceId
    crpsign = hashlib.md5(raw.encode('utf-8')).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'CDEVICEINFO': '{"vendorName":"","deviceMode":"iPhone","deviceName":"","systemName":"ios","systemVersion":"17.0","cpuMode":" ","cpuCores":"","cpuArch":"","memerySize":"","diskSize":"","network":"4G","resolution":"390*844","pixelResolution":""}',
        'CDEVICENO': token,
        'CTERMINAL': terminal,
        'CSAPPID': terminal,
        'CVERSION': version,
        'CUSAT': accessToken,
        'CUSUT': sign,
        'CUSIT': idToken,
        'CUSID': userId,
        'CUSNAME': 'nil',
        'CUUSERREF': token,
        'CSOURCEPATH': '',
        'CTRACKPATH': '',
        'st_flpv': st_flpv,
        'CRTRACEID': traceId,
        'CRPSIGN': crpsign,
        'Referer': f'https://wap.showstart.com/pages/activity/detail/detail?activityId={event_id}',
        'Origin': 'https://wap.showstart.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }

    cookies = tokens.get('cookies', {})

    print(f"\n[发送请求]")
    print(f"URL: {url}")
    print(f"traceId: {traceId}")
    print(f"CRPSIGN: {crpsign}")

    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=body, timeout=10)
        print(f"\n[响应状态]")
        print(f"HTTP状态码: {response.status_code}")

        try:
            result = response.json()
            print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

            if result.get('success'):
                print("\n[OK] API调用成功!")
            elif result.get('msg'):
                print(f"\n[ERROR] API返回错误: {result.get('msg')}")
                if '登录过期' in result.get('msg', ''):
                    print("\n[SOLUTION] 需要重新登录")
                    print("   请运行主脚本,选择y启用API模式,然后按提示登录")
        except:
            print(f"响应内容: {response.text}")

    except Exception as e:
        print(f"\n[ERROR] 请求失败: {e}")

if __name__ == '__main__':
    test_api_mode()
