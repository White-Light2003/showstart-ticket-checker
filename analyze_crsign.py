#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析CRPSIGN的组成"""
import hashlib

# 真实cURL中的值
real_accessToken = 'db1cd22118e20c436a03533bIhfCMxeF'
real_sign = '47ef9cd5c7855295527f881a2a860257'
real_idToken = '7ad44157656c33fa6a035355SYP53LCQ'
real_userId = '18726052'
real_token = 'q6ac0i82mk6dzs877ln0g1yt8uyk07bj'
real_st_flpv = 'OZ920fB62TS4h1j14QR0'
real_traceId = '7s0a97IS5X84V53hC37pAru01sZ0V88o1778600758843'
real_crpsign = '9c431cf1ca07710c66c0e027d70feee3'

event_id = '295821'
body = f'{{"activityId":"{event_id}","coupon":"","st_flpv":"{real_st_flpv}","sign":"{real_sign}","trackPath":""}}'
urlPath = '/wap/activity/V2/ticket/list'
terminal = 'wap'
version = '997'

# 不同的CRPSIGN计算公式
formulas = [
    {
        'name': '公式1: accessToken+sign+idToken+userId+terminal+token+body+urlPath+version+terminal+traceId',
        'raw': real_accessToken + real_sign + real_idToken + real_userId + terminal + real_token + body + urlPath + version + terminal + real_traceId
    },
    {
        'name': '公式2: accessToken+sign+idToken+userId+token+body+urlPath+version+traceId',
        'raw': real_accessToken + real_sign + real_idToken + real_userId + real_token + body + urlPath + version + real_traceId
    },
    {
        'name': '公式3: 无userId',
        'raw': real_accessToken + real_sign + real_idToken + terminal + real_token + body + urlPath + version + terminal + real_traceId
    },
    {
        'name': '公式4: 交换顺序 accessToken+idToken+sign+userId+terminal+token+body+urlPath+version+terminal+traceId',
        'raw': real_accessToken + real_idToken + real_sign + real_userId + terminal + real_token + body + urlPath + version + terminal + real_traceId
    },
    {
        'name': '公式5: body在后',
        'raw': real_accessToken + real_sign + real_idToken + real_userId + terminal + real_token + urlPath + version + terminal + real_traceId + body
    },
    {
        'name': '公式6: 使用MD5而非MD5Cycle',
        'raw': real_accessToken + real_sign + real_idToken + real_userId + terminal + real_token + body + urlPath + version + terminal + real_traceId
    }
]

print("="*80)
print("CRPSIGN签名分析")
print("="*80)

print(f"\n[真实值]")
print(f"accessToken: {real_accessToken}")
print(f"sign: {real_sign}")
print(f"idToken: {real_idToken}")
print(f"userId: {real_userId}")
print(f"token: {real_token}")
print(f"st_flpv: {real_st_flpv}")
print(f"traceId: {real_traceId}")
print(f"\n[body]")
print(body)
print(f"\n[真实CRPSIGN]")
print(real_crpsign)

print("\n" + "="*80)
print("测试不同的CRPSIGN计算公式")
print("="*80)

import hashlib

for formula in formulas:
    # 使用标准MD5
    m = hashlib.md5()
    m.update(formula['raw'].encode('utf-8'))
    md5_result = m.hexdigest()
    
    print(f"\n【{formula['name']}】")
    print(f"MD5: {md5_result}")
    print(f"匹配: {md5_result == real_crpsign}")
    print(f"原料: {formula['raw']}")

# 测试变体：加盐
print("\n" + "="*80)
print("测试加盐变体")
print("="*80)

salt_test = [
    ('加_showstart', 'showstart' + real_accessToken + real_sign + real_idToken + real_userId + terminal + real_token + body + urlPath + version + terminal + real_traceId),
    ('加_Key', real_accessToken + real_sign + real_idToken + real_userId + terminal + real_token + body + urlPath + version + terminal + real_traceId + 'Key'),
]

for name, raw in salt_test:
    m = hashlib.md5()
    m.update(raw.encode('utf-8'))
    md5_result = m.hexdigest()
    print(f"\n【{name}】")
    print(f"MD5: {md5_result}")
    print(f"匹配: {md5_result == real_crpsign}")