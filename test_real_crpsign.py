#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用真实cURL值测试CRPSIGN签名"""
import hashlib
import requests

# 用户cURL中的真实值
real_accessToken = 'db1cd22118e20c436a03533bIhfCMxeF'
real_sign = '47ef9cd5c7855295527f881a2a860257'
real_idToken = '7ad44157656c33fa6a035355SYP53LCQ'
real_userId = '18726052'
real_token = 'q6ac0i82mk6dzs877ln0g1yt8uyk07bj'
real_st_flpv = 'OZ920fB62TS4h1j14QR0'
real_traceId = '7s0a97IS5X84V53hC37pAru01sZ0V88o1778600758843'
real_crpsign = '9c431cf1ca07710c66c0e027d70feee3'
event_id = '295821'

url = 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list'
urlPath = '/wap/activity/V2/ticket/list'
terminal = 'wap'
version = '997'

# 构造body
body = f'{{"activityId":"{event_id}","coupon":"","st_flpv":"{real_st_flpv}","sign":"{real_sign}","trackPath":""}}'

# 计算CRPSIGN签名
raw = real_accessToken + real_sign + real_idToken + real_userId + terminal + real_token + body + urlPath + version + terminal + real_traceId
calculated_crpsign = hashlib.md5(raw.encode('utf-8')).hexdigest()

print("="*80)
print("CRPSIGN签名验证")
print("="*80)
print(f"\n[参数值]")
print(f"accessToken: {real_accessToken}")
print(f"sign: {real_sign}")
print(f"idToken: {real_idToken}")
print(f"userId: {real_userId}")
print(f"token: {real_token}")
print(f"terminal: {terminal}")
print(f"version: {version}")
print(f"urlPath: {urlPath}")
print(f"traceId: {real_traceId}")
print(f"\n[body]")
print(body)
print(f"\n[签名原料]")
print(raw)
print(f"\n[计算结果]")
print(f"计算的CRPSIGN: {calculated_crpsign}")
print(f"真实的CRPSIGN: {real_crpsign}")
print(f"匹配: {calculated_crpsign == real_crpsign}")

# 如果匹配，发送真实请求测试
if calculated_crpsign == real_crpsign:
    print("\n" + "="*80)
    print("发送真实API请求测试")
    print("="*80)
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'CDEVICEINFO': '{"vendorName":"","deviceMode":"iPhone","deviceName":"","systemName":"ios","systemVersion":"17.0","cpuMode":" ","cpuCores":"","cpuArch":"","memerySize":"","diskSize":"","network":"4G","resolution":"390*844","pixelResolution":""}',
        'CDEVICENO': real_token,
        'CTERMINAL': terminal,
        'CSAPPID': terminal,
        'CVERSION': version,
        'CUSAT': real_accessToken,
        'CUSUT': real_sign,
        'CUSIT': real_idToken,
        'CUSID': real_userId,
        'CUSNAME': 'nil',
        'CUUSERREF': real_token,
        'CSOURCEPATH': '',
        'CTRACKPATH': '',
        'st_flpv': real_st_flpv,
        'CRTRACEID': real_traceId,
        'CRPSIGN': calculated_crpsign,
        'Referer': f'https://wap.showstart.com/pages/activity/detail/detail?activityId={event_id}',
        'Origin': 'https://wap.showstart.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }
    
    cookies = {
        'Hm_lvt_da038bae565bb601b53cc9cb25cdca74': '1778600711',
        'Hm_lpvt_da038bae565bb601b53cc9cb25cdca74': '1778600711',
        'HMACCOUNT': '9A0C02E9852D74A0'
    }
    
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=body)
        print(f"\nHTTP状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
