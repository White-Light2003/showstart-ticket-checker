#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
秀动余票查询工具 v3.4 (API模式修复版)
- 修正魔改MD5签名算法
- 修正API请求头字段（CUSIT, CDEVICENO等）
- 添加Token自动刷新机制
- 保留所有原有功能（歌词、推送、定时关闭等）
"""
import time
import subprocess
import ctypes
import traceback
import os
import requests
import json
import hashlib
import struct
import random
from datetime import datetime
from typing import List, Dict, Optional

# ===================== 常量配置 =====================
NAPCAT_HTTP_URL = "http://127.0.0.1:3000"
PUSHPLUS_TOKEN = "your code here"
DEEPSEEK_API_KEY = "your code here"

# ChiliChill乐团歌词库
CHILICHILL_LYRICS = [
    "你的世界才不是mono~你的表演才不是solo~——ChiliChill《不安灵魂收容所》(改编版)",
    "我时常对自己失望~没有一个超自信的理想~——ChiliChill《万一对了呢》",
    "毕竟天总会放晴雨会停~——ChiliChill《五块钱的伞》",
    "推开门🚪摆摆左手✋🏻转身右走🚶🏻‍♀️‍➡️——ChiliChill《辞职信》",
    "别转头🙂‍↔️撞进万万人潮之后👥——ChiliChill《辞职信》",
    "哦也许吧🧐人总有逃不掉的痛😣——ChiliChill《辞职信》",
    "哦也许吧🧐下个街口也没自由🤷🏻‍♀️——ChiliChill《辞职信》",
    "风不风🌬️昨日种种📒甩甩袖口👋——ChiliChill《辞职信》",
    "流不流🌊明天以后🔜不再逗留🏃🏻‍♀️‍➡️——ChiliChill《辞职信》",
    "哦也许吧🧐有种荒谬才是出口🚪——ChiliChill《辞职信》",
    "那天晚上🌃做了个我从前不敢做的梦😴💭——ChiliChill《辞职信》",
    "老板，来20串！——ChiliChill《饿魔少女》",
    "左牵黄，右擎苍，日行千里系沙袋~——ChiliChill《恋爱困难少女》",
    "请你管好你自己~我不需要你的废话大道理~——ChiliChill《管好你自己》",
    "等一个人来坐我的船~抚平我摇摇晃晃的不安~思绪不断~——ChiliChill《双人船》",
    "我们都会拥有美好的未来~——ChiliChill《飞鸟说》",
    "你走吧~此去山遥路远~——ChiliChill《山遥路远》",
    "不加糖，不加奶，放了几颗冰块的~Americano(啊美丽卡洛)——ChiliChill《啊！美丽卡洛》",
    "泡上一杯咖啡，今晚继续熬夜~——ChiliChill《社畜少女》",
    "我用世间最顺的笔尖~将我们的故事书写~——ChiliChill《芭蕉夜雨》",
    "一身素青纱，草柄当头花~——ChiliChill《下等马》",
    "夏末秋初，第一场雨，混了5%的酒精~——ChiliChill《入秋的第一场雨真让人矫情》",
    "Hakunama ta ta,my friend~——ChiliChill《提瓦特民谣》",
    "这里最美丽的咒语——谢谢你和我也爱你（呐喊）！——ChiliChill《混入人类计划》",
    "如今我却想往回走~——ChiliChill《衡山路宛平路》",
    "Itai Itai 明明忘了怎么突然清晰~——ChiliChill《难过233秒》",
    "场灯灭~拉幕帘~起配乐~——ChiliChill《演》",
    "你介绍给我的对象~现在还是八字没一撇~——ChiliChill《恋爱困难少男》",
    "或许你和我的缘分~并不值得三个铜板~——ChiliChill《橙子汽水》",
    "可以撩我的心~别撩我的头发——ChiliChill《别动我头发》",
    "今天到底是礼拜几~怎么就头晕脚无力~——ChiliChill《屑屑》",
    "我的破木箱~装满枯萎的花~——ChiliChill《我不曾忘记》",
    "高举一面夜色~星空替你记得~究竟为了什么活着~——ChiliChill《启航的歌》",
    "褪色的画面重叠~数着还没过完的日子入眠~—ChiliChill《时光盲盒》",
    "等天黑~再过一夜~—ChiliChill《搬家前，短暂夜》",
    "当你的天空突然下起了大雨，那是我在为你炸乌云~—ChiliChill《让风告诉你》",
    "Drop the beat~I feel~Like a rollercoaster going up and down~—ChiliChill《pinking》",
    "Overtake~Step on the GAS~Dash like a vroom vroom vroom~—ChiliChill《都市不丽人》",
    "摘一朵纯白色的花~塞西莉亚~塞西莉亚~—ChiliChill《别让我担心》",
    "告诉我~不想再继续~我的心就石沉大海~偏偏你~就是拖着不坦白~—ChiliChill《半梦》",
    "我的悲伤~是水做的~是水做的~—ChiliChill《我的悲伤是水做的》",
    "怎么不挽留~拦下~我的冲动~—ChiliChill《半醒》",
    "你没喝完的无糖可乐~冰箱里还剩几瓶~全部丢出去~全部丢出去~换成我爱的雪碧~—ChiliChill《心碎烧酒》",
    "心在波比~震天动地~是我是你~不太确定~—ChiliChill《有线耳机》",
    "高温缩减，长江中下游地带有大雨到暴雨~—ChiliChill《晚间天气预报》"
]

# 定时关闭任务配置
DAILY_SHUTDOWN_HOUR = 21
QQ_PUSH_END_DATE = datetime(2026, 6, 8, 0, 0, 0)
QQ_PUSH_NOTICE_DATES = [datetime(2026, 6, 4), datetime(2026, 6, 5), datetime(2026, 6, 6), datetime(2026, 6, 7)]
QQ_PUSH_NOTICE_TIME = (22, 0)
QQ_PUSH_END_NOTICE_SENT = False
DAILY_SHUTDOWN_DONE = False

NEW_SONG_PROMO_MSG = """【最新消息】

上海场无料现在开始征集，各位老师如有无料可以分享~
期待各位老师的无料！"""

# ===================== 秀动魔改MD5（完整正版） =====================
def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def uint32(x):
    return x & 0xFFFFFFFF

def custom_md5(message: bytes) -> str:
    """
    秀动魔改MD5实现
    根据逆向分析文档完整还原，与官方JS完全一致。
    """
    # 1. 填充（标准MD5方式）
    original_len = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('<Q', original_len)

    # 初始化哈希值
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476

    first = True

    # 2. 处理每个512位块
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        r = list(struct.unpack('<16I', block))

        if first:
            # ========== 首块特殊处理 ==========
            # Round 1 (步骤1-16)
            e = uint32(r[0] - 680876937)
            e = uint32(left_rotate(e, 7) - 271733879)

            t = uint32((uint32(-1732584194) ^ (2004318071 & e)) + r[1] - 117830708)
            t = uint32(left_rotate(t, 12) + e)

            a = uint32((uint32(-271733879) ^ (t & (uint32(-271733879) ^ e))) + r[2] - 1126478375)
            a = uint32(left_rotate(a, 17) + t)

            n = uint32((e ^ (a & (t ^ e))) + r[3] - 1316259209)
            n = uint32(left_rotate(n, 22) + a)

            # 步骤5
            e = uint32(e + (t ^ (n & (a ^ t))) + r[4] - 176418897)
            e = uint32(left_rotate(e, 7) + n)
            # 步骤6
            t = uint32(t + (a ^ (e & (n ^ a))) + r[5] + 1200080426)
            t = uint32(left_rotate(t, 12) + e)
            # 步骤7
            a = uint32(a + (n ^ (t & (e ^ n))) + r[6] - 1473231341)
            a = uint32(left_rotate(a, 17) + t)
            # 步骤8
            n = uint32(n + (e ^ (a & (t ^ e))) + r[7] - 45705983)
            n = uint32(left_rotate(n, 22) + a)
            # 步骤9
            e = uint32(e + (t ^ (n & (a ^ t))) + r[8] + 1770035416)
            e = uint32(left_rotate(e, 7) + n)
            # 步骤10
            t = uint32(t + (a ^ (e & (n ^ a))) + r[9] - 1958414417)
            t = uint32(left_rotate(t, 12) + e)
            # 步骤11
            a = uint32(a + (n ^ (t & (e ^ n))) + r[10] - 42063)
            a = uint32(left_rotate(a, 17) + t)
            # 步骤12
            n = uint32(n + (e ^ (a & (t ^ e))) + r[11] - 1990404162)
            n = uint32(left_rotate(n, 22) + a)
            # 步骤13
            e = uint32(e + (t ^ (n & (a ^ t))) + r[12] + 1804603682)
            e = uint32(left_rotate(e, 7) + n)
            # 步骤14
            t = uint32(t + (a ^ (e & (n ^ a))) + r[13] - 40341101)
            t = uint32(left_rotate(t, 12) + e)
            # 步骤15
            a = uint32(a + (n ^ (t & (e ^ n))) + r[14] - 1502002290)
            a = uint32(left_rotate(a, 17) + t)
            # 步骤16
            n = uint32(n + (e ^ (a & (t ^ e))) + r[15] + 1236535329)
            n = uint32(left_rotate(n, 22) + a)

            # Round 2 (步骤17-32) 使用函数 F = a ^ (t & (n ^ a))
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

            # Round 3 (步骤33-48) 使用函数 F = n ^ a ^ t
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

            # Round 4 (步骤49-64) 使用函数 F = a ^ (n | ~t)
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

            # 首块最终哈希值更新（特殊偏移）
            h0 = uint32(e + 1732584193)
            h1 = uint32(n - 271733879)
            h2 = uint32(a - 1732584194)
            h3 = uint32(t + 271733878)
            first = False
        else:
            # 后续块使用标准MD5算法（直接使用Python标准库加速，结果一致）
            md5_std = hashlib.md5(block).digest()
            std_words = struct.unpack('<4I', md5_std)
            h0 = uint32(h0 + std_words[0])
            h1 = uint32(h1 + std_words[1])
            h2 = uint32(h2 + std_words[2])
            h3 = uint32(h3 + std_words[3])

    # 3. 输出32位小写十六进制
    return struct.pack('<4I', h0, h1, h2, h3).hex()

# ===================== 签名相关函数 =====================
def generate_trace_id() -> str:
    """生成32位随机字符串 + 13位时间戳"""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    random_str = ''.join(random.choice(chars) for _ in range(32))
    timestamp = str(int(time.time() * 1000))
    return random_str + timestamp

def calculate_crpsign(access_token: str, sign: str, id_token: str, user_id: str,
                      token: str, body: str, url_path: str, terminal: str, trace_id: str) -> str:
    """计算CRPSIGN签名（使用标准MD5）"""
    raw = (access_token + sign + id_token + str(user_id) + "wap" +
           token + body + url_path + "997" + terminal + trace_id)
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

# ===================== API请求函数（修正版） =====================
def get_ticket_info_api(event_id: str, tokens: dict, driver=None) -> List[Dict]:
    """通过秀动API获取票务信息
    
    Args:
        event_id: 演出ID
        tokens: 登录凭证
        driver: 浏览器实例，如果提供则直接在浏览器中执行API请求
        
    Returns:
        票务信息列表
    """
    # 如果有浏览器实例，直接在浏览器中执行API请求
    if driver:
        return get_ticket_info_via_browser(driver, event_id)
    
    # 否则使用requests模拟请求
    try:
        url_path = '/wap/activity/V2/ticket/list'
        full_url = 'https://wap.showstart.com/v3' + url_path

        # 构建请求体（紧凑JSON，不转义中文）
        body_dict = {
            'activityId': str(event_id),
            'coupon': '',
            'st_flpv': tokens.get('st_flpv', ''),
            'sign': tokens.get('sign', ''),
            'trackPath': ''
        }
        body_str = json.dumps(body_dict, separators=(',', ':'), ensure_ascii=False)

        trace_id = generate_trace_id()

        # 计算签名
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

        # 请求头（严格按照文档4.2.1）
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
            'CUSID': str(tokens['userId']),
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
            'Pragma': 'no-cache',
            'x-requested-with': 'XMLHttpRequest'
        }

        # 使用Session添加Cookie
        session = requests.Session()
        session.trust_env = False
        
        saved_cookies = tokens.get('cookies', {})
        for name, value in saved_cookies.items():
            session.cookies.set(name, value)
        
        session.cookies.set('token', tokens.get('token', ''))
        session.cookies.set('accessToken', tokens.get('accessToken', ''))
        session.cookies.set('sign', tokens.get('sign', ''))
        session.cookies.set('idToken', tokens.get('idToken', ''))
        session.cookies.set('userId', str(tokens.get('userId', '')))
        
        response = session.post(full_url, data=body_str.encode('utf-8'), headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                ticket_list = result.get('data', {}).get('ticketList', [])
                tickets = []
                for t in ticket_list:
                    tickets.append({
                        'price': t.get('price', 0),
                        'name': t.get('ticketName', ''),
                        'status': '有票' if t.get('stock', 0) > 0 else '售罄'
                    })
                print("[API] SUCCESS: 成功获取 %d 个票档信息" % len(tickets))
                return tickets
            else:
                print("[API] ERROR: 接口返回错误: %s" % result.get('msg', '未知错误'))
                return []
        else:
            print("[API] ERROR: HTTP %d" % response.status_code)
            return []
    except Exception as e:
        print("[API] ERROR: 请求异常: %s" % e)
        return []

def get_ticket_info_via_browser(driver, event_id: str) -> List[Dict]:
    """通过浏览器直接执行API请求（保证认证状态）"""
    print("[API] INFO: 使用浏览器执行API请求...")
    try:
        # 先从localStorage获取参数
        params_js = """
            return JSON.stringify({
                accessToken: localStorage.getItem('accessToken') || '',
                sign: localStorage.getItem('sign') || '',
                idToken: localStorage.getItem('idToken') || '',
                token: localStorage.getItem('token') || '',
                userInfoStr: localStorage.getItem('userInfo') || '{}',
                st_flpv: localStorage.getItem('st_flpv') || ''
            });
        """
        params_json = driver.execute_script(params_js)
        params = json.loads(params_json)
        
        # 解析userId
        user_id = ''
        if params.get('userInfoStr'):
            try:
                user_info = json.loads(params['userInfoStr'])
                if user_info.get('data'):
                    user_id = str(user_info['data'].get('userId', ''))
            except:
                pass
        
        # 生成traceId
        import time
        import random
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        random_str = ''.join(random.choice(chars) for _ in range(32))
        trace_id = random_str + str(int(time.time() * 1000))
        
        # 构建body
        body_dict = {
            'activityId': str(event_id),
            'coupon': '',
            'st_flpv': params.get('st_flpv', ''),
            'sign': params.get('sign', ''),
            'trackPath': ''
        }
        body_str = json.dumps(body_dict, separators=(',', ':'), ensure_ascii=False)
        
        # 计算CRPSIGN（Python标准MD5）
        import hashlib
        url_path = '/wap/activity/V2/ticket/list'
        raw = (params['accessToken'] + params['sign'] + params['idToken'] + 
               user_id + 'wap' + params['token'] + body_str + 
               url_path + '997' + 'wap' + trace_id)
        crpsign = hashlib.md5(raw.encode('utf-8')).hexdigest()
        
        # 构建cdeviceinfo
        cdeviceinfo = '{"vendorName":"","deviceMode":"iPhone","deviceName":"","systemName":"ios","systemVersion":"17.0","cpuMode":" ","cpuCores":"","cpuArch":"","memerySize":"","diskSize":"","network":"4G","resolution":"390*844","pixelResolution":""}'
        
        # 在浏览器中执行请求，使用计算好的参数
        js_code = """
            var accessToken = arguments[0];
            var sign = arguments[1];
            var idToken = arguments[2];
            var userId = arguments[3];
            var token = arguments[4];
            var st_flpv = arguments[5];
            var body = arguments[6];
            var crpsign = arguments[7];
            var traceId = arguments[8];
            var cdeviceinfo = arguments[9];
            var eventId = arguments[10];
            
            var result = '';
            try {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', 'https://wap.showstart.com/v3/wap/activity/V2/ticket/list', false);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('Accept', '*/*');
                xhr.setRequestHeader('Accept-Language', 'zh-CN,zh;q=0.9');
                xhr.setRequestHeader('CDEVICEINFO', cdeviceinfo);
                xhr.setRequestHeader('CDEVICENO', token);
                xhr.setRequestHeader('CTERMINAL', 'wap');
                xhr.setRequestHeader('CSAPPID', 'wap');
                xhr.setRequestHeader('CVERSION', '997');
                xhr.setRequestHeader('CUSAT', accessToken);
                xhr.setRequestHeader('CUSUT', sign);
                xhr.setRequestHeader('CUSIT', idToken);
                xhr.setRequestHeader('CUSID', userId);
                xhr.setRequestHeader('CUSNAME', 'nil');
                xhr.setRequestHeader('CUUSERREF', token);
                xhr.setRequestHeader('CSOURCEPATH', '');
                xhr.setRequestHeader('CTRACKPATH', '');
                xhr.setRequestHeader('st_flpv', st_flpv);
                xhr.setRequestHeader('CRTRACEID', traceId);
                xhr.setRequestHeader('CRPSIGN', crpsign);
                xhr.setRequestHeader('Referer', 'https://wap.showstart.com/pages/activity/detail/detail?activityId=' + eventId);
                xhr.setRequestHeader('Origin', 'https://wap.showstart.com');
                xhr.setRequestHeader('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
                xhr.withCredentials = true;
                
                xhr.send(body);
                
                if (xhr.status === 200) {
                    result = xhr.responseText;
                } else {
                    result = JSON.stringify({'error': 'HTTP error', 'status': xhr.status, 'response': xhr.responseText || 'empty'});
                }
            } catch(e) {
                result = JSON.stringify({'error': 'Exception', 'message': e.message});
            }
            
            return result;
        """
        result_str = driver.execute_script(
            js_code,
            params['accessToken'],
            params['sign'],
            params['idToken'],
            user_id,
            params['token'],
            params.get('st_flpv', ''),
            body_str,
            crpsign,
            trace_id,
            cdeviceinfo,
            str(event_id)
        )
        
        print(f"[API] 浏览器响应: {result_str[:200]}...")
        
        result = json.loads(result_str)
        if result.get('code') == 0 or result.get('success'):
            ticket_list = result.get('data', {}).get('ticketList', result.get('data', []))
            tickets = []
            for t in ticket_list:
                tickets.append({
                    'price': t.get('price', 0),
                    'name': t.get('ticketName', t.get('name', '')),
                    'status': '有票' if t.get('stock', 0) > 0 else '售罄'
                })
            print("[API] SUCCESS: 通过浏览器API获取 %d 个票档信息" % len(tickets))
            return tickets
        else:
            print("[API] ERROR: 浏览器API返回错误: %s" % result.get('msg', '未知错误'))
            return []
            
    except Exception as e:
        print("[API] ERROR: 浏览器API请求失败: %s" % e)
        return []

# ===================== Token 刷新模块 =====================
def refresh_tokens_from_browser(keep_driver=False, driver=None) -> dict:
    """通过浏览器重新登录并刷新tokens.json（保存完整cookie）
    
    Args:
        keep_driver: 是否保留浏览器实例供后续使用
        driver: 已有的浏览器实例，如果提供则复用，否则新建
        
    Returns:
        tokens: 登录凭证字典
    """
    import time
    
    # 如果已有浏览器实例，先检查是否可用
    if driver:
        try:
            # 检查浏览器是否还连接着
            driver.title
            print("[Token] 🔄 使用已有的浏览器刷新凭证...")
        except Exception as e:
            print(f"[Token] 已有浏览器不可用: {e}")
            driver = None
    
    # 如果没有可用的浏览器，新建一个
    if not driver:
        print("[Token] 🔄 需要刷新登录凭证，正在启动浏览器...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # 模拟移动端设备（使用自定义参数，兼容旧版ChromeDriver）
        mobile_emulation = {
            "deviceMetrics": {
                "width": 390,
                "height": 844,
                "pixelRatio": 3.0
            },
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # 不设置 headless，让用户手动登录
        driver = webdriver.Chrome(options=options)
        driver.get("https://wap.showstart.com")
        input("请在浏览器中登录秀动账号（已切换为移动端），登录成功后按回车键继续...")
    else:
        # 复用已有浏览器，检查是否需要重新登录
        print("[Token] 检查浏览器登录状态...")
        # 尝试获取当前的token，看看是否还有效
        try:
            current_tokens = driver.execute_script("""
                return {
                    accessToken: localStorage.getItem('accessToken') || '',
                    sign: localStorage.getItem('sign') || '',
                    idToken: localStorage.getItem('idToken') || '',
                    token: localStorage.getItem('token') || ''
                };
            """)
            # 如果已有token，尝试刷新页面获取新凭证
            if current_tokens.get('accessToken'):
                print("[Token] 浏览器已有登录状态，尝试刷新凭证...")
                driver.get("https://wap.showstart.com")
                time.sleep(2)
            else:
                # 没有token，需要登录
                print("[Token] 浏览器需要重新登录...")
                input("请在浏览器中完成登录，登录成功后按回车键继续...")
        except:
            # 执行失败，可能需要重新加载页面
            print("[Token] 重新加载登录页面...")
            driver.get("https://wap.showstart.com")
            input("请在浏览器中完成登录，登录成功后按回车键继续...")
    
    # 登录成功后访问演出页面，触发完整的认证流程
    print("[Token] 正在访问演出页面以获取完整凭证...")
    driver.get("https://www.showstart.com/event/295821")
    time.sleep(3)
    
    # 获取localStorage中的token
    tokens = driver.execute_script("""
        var userInfoStr = localStorage.getItem('userInfo') || '{}';
        var userInfo = JSON.parse(userInfoStr);
        var userId = userInfo.data ? userInfo.data.userId : '';
        return {
            accessToken: localStorage.getItem('accessToken') || '',
            sign: localStorage.getItem('sign') || '',
            idToken: localStorage.getItem('idToken') || '',
            token: localStorage.getItem('token') || '',
            st_flpv: localStorage.getItem('st_flpv') || '',
            userId: userId || localStorage.getItem('userId') || ''
        };
    """)
    
    # 获取浏览器cookie（包含所有cookie，包括HttpOnly的）
    cookies = {}
    all_cookies = driver.get_cookies()
    print(f"[Token] 检测到 {len(all_cookies)} 个cookie")
    for cookie in all_cookies:
        cookies[cookie['name']] = cookie['value']
        print(f"[Token] Cookie: {cookie['name']} = {cookie['value'][:50]}...")
    tokens['cookies'] = cookies
    
    # 如果需要保留浏览器，返回driver供后续使用
    if keep_driver:
        tokens['_driver'] = driver
    else:
        driver.quit()
    
    # 保存到文件
    config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, 'tokens.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump({k: v for k, v in tokens.items() if k != '_driver'}, f, indent=2, ensure_ascii=False)
    print("[Token] ✅ 凭证已更新并保存")
    return tokens

# ===================== NapCat 心跳检测 =====================
NAPCAT_HEARTBEAT_INTERVAL = 60
last_heartbeat_time = 0
napcat_connected = True

def check_napcat_connection() -> bool:
    global napcat_connected
    try:
        url = f"{NAPCAT_HTTP_URL}/_ping"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            napcat_connected = True
            return True
        else:
            napcat_connected = False
            return False
    except:
        napcat_connected = False
        return False

def napcat_heartbeat():
    global last_heartbeat_time, napcat_connected
    current_time = time.time()
    if current_time - last_heartbeat_time >= NAPCAT_HEARTBEAT_INTERVAL:
        last_heartbeat_time = current_time
        is_connected = check_napcat_connection()
        if not is_connected and napcat_connected:
            print("\n[WARNING] ❌ NapCat 连接断开！")
            send_phone_notification("⚠️ NapCat连接断开", "NapCat服务已断开连接！请检查NapCat是否正常运行或QQ是否在线！")
            show_system_notification("⚠️ NapCat连接断开", "NapCat服务已断开连接！\n\n请检查：\n• NapCat是否正常运行\n• QQ是否在线\n• 网络连接是否正常")
        elif is_connected and not napcat_connected:
            print("\n[INFO] ✅ NapCat 重新连接成功！")
            send_phone_notification("✅ NapCat已重新连接", "NapCat服务已重新连接成功！")
            show_system_notification("✅ NapCat已重新连接", "NapCat服务已重新连接成功！")

# ===================== 推送相关函数 =====================
def generate_ticket_message(event_id: str, tickets: List[Dict]) -> str:
    """使用 DeepSeek AI 生成票务推送文案"""
    if not DEEPSEEK_API_KEY:
        return ""
    available_tickets = [t for t in tickets if t['status'] == '有票']
    if available_tickets:
        ticket_info = "\n".join([f"- {t['price']}元 ({t['name']})" for t in available_tickets])
        prompt = f"""
        请帮我写一段吸引眼球的QQ群回流票推送文案，要求：
        
        演出ID: {event_id}
        
        有票档位：
        {ticket_info}
        
        要求：
        1. 使用表情符号和换行，让消息更生动
        2. 语气要兴奋、紧迫，营造抢购氛围
        3. 突出"回流票"、"手速"、"快抢"等关键词
        4. 结尾加上催促大家去秀动APP抢购的号召
        5. 不要超过4行
        """
    else:
        prompt = f"""
        请帮我写一段QQ群票务状态通知文案，当前演出暂无余票，要求：
        
        演出ID: {event_id}
        
        当前票档状态：全部售罄
        
        要求：
        1. 使用表情符号和换行，让消息更易读
        2. 语气要亲切、鼓励，不要让大家失望
        3. 提醒大家继续关注，回流票随时可能出现
        4. 可以加点幽默或可爱的表情让氛围轻松一些
        5. 不要超过3行
        """
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个专业的票务通知文案撰写助手，擅长用简短、有趣、吸引人的方式编写群消息。"},
                {"role": "user", "content": prompt.strip()}
            ],
            "max_tokens": 200,
            "temperature": 0.8
        }
        response = requests.post(url, headers=headers, json=data, timeout=15)
        result = response.json()
        if result.get("choices"):
            message = result["choices"][0]["message"]["content"].strip()
            lyrics = random.choice(CHILICHILL_LYRICS)
            message = f"{message}\n\n{lyrics}"
            print(f"[AI生成] ✅ 成功生成推送文案")
            return message
        else:
            print(f"[AI生成] ❌ 生成失败: {result.get('error', {}).get('message', '未知错误')}")
            return ""
    except Exception as e:
        print(f"[AI生成] ❌ 请求异常: {e}")
        return ""

def clean_message(message: str) -> str:
    """清洗消息内容，移除可能导致 NapCat 解析错误的特殊字符"""
    cleaned = ''.join(char for char in message if ord(char) >= 32 or char in '\n\t')
    if len(cleaned) > 2000:
        cleaned = cleaned[:2000] + "..."
    cleaned = '\n'.join(line.strip() for line in cleaned.split('\n') if line.strip())
    return cleaned

def send_to_qq_group(group_id: int, message: str, max_retries: int = 2) -> bool:
    """通过 NapCat HTTP API 发送消息到 QQ 群"""
    retry_delay = 2
    message = clean_message(message)
    for attempt in range(max_retries + 1):
        try:
            url = f"{NAPCAT_HTTP_URL}/send_group_msg"
            params = {"group_id": group_id, "message": message}
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            if result.get("retcode") == 0:
                print(f"[QQ推送] ✅ 消息已发送到群 {group_id}")
                return True
            else:
                if attempt < max_retries:
                    print(f"[QQ推送] ⚠️ 发送失败(尝试 {attempt+1}/{max_retries+1}): {result}，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    continue
                print(f"[QQ推送] ❌ 发送失败: {result}")
                return False
        except requests.exceptions.ConnectionError:
            if attempt < max_retries:
                print(f"[QQ推送] ⚠️ 连接失败(尝试 {attempt+1}/{max_retries+1})，{retry_delay}秒后重试...")
                time.sleep(retry_delay)
                continue
            print(f"[QQ推送] ❌ 连接失败：无法连接到 NapCat 服务")
            return False
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                print(f"[QQ推送] ⚠️ 连接超时(尝试 {attempt+1}/{max_retries+1})，{retry_delay}秒后重试...")
                time.sleep(retry_delay)
                continue
            print(f"[QQ推送] ❌ 连接超时：NapCat 服务无响应")
            return False
        except Exception as e:
            if attempt < max_retries:
                print(f"[QQ推送] ⚠️ 发送异常(尝试 {attempt+1}/{max_retries+1}): {e}，{retry_delay}秒后重试...")
                time.sleep(retry_delay)
                continue
            print(f"[QQ推送] ❌ 发送异常: {e}")
            return False

def show_system_notification(title: str, message: str):
    """显示系统弹窗提醒"""
    try:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x1000 | 0x40)
    except Exception as e:
        print(f"[提醒] 无法显示系统通知: {e}")

def send_phone_notification(title: str, content: str) -> bool:
    """通过 PushPlus 发送手机消息推送"""
    if not PUSHPLUS_TOKEN:
        print(f"[手机推送] ⚠️ 未配置 PushPlus token，跳过手机推送")
        return False
    try:
        url = "http://www.pushplus.plus/send"
        data = {"token": PUSHPLUS_TOKEN, "title": title, "content": content, "template": "txt"}
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        if result.get("code") == 200:
            print(f"[手机推送] ✅ 消息已发送到手机")
            return True
        else:
            print(f"[手机推送] ❌ 发送失败: {result.get('msg', '未知错误')}")
            return False
    except Exception as e:
        print(f"[手机推送] ❌ 发送异常: {e}")
        return False

def get_available_groups() -> List[int]:
    """获取Bot所在的群列表"""
    try:
        url = f"{NAPCAT_HTTP_URL}/get_group_list"
        response = requests.get(url, timeout=5)
        result = response.json()
        if result.get("retcode") == 0:
            groups = result.get("data", [])
            return [g["group_id"] for g in groups]
        return []
    except:
        return []

def select_target_groups() -> Optional[List[int]]:
    """让用户选择目标群（支持多选）"""
    groups = get_available_groups()
    if not groups:
        print("[QQ推送] ❌ 无法获取群列表，请确保 NapCat HTTP 服务正常运行")
        print("[QQ推送] 💡 提示：请先确认 NapCat 已登录并且在群中")
        return None
    print("\n" + "="*50)
    print("📋 Bot 所在群列表：")
    print("="*50)
    for i, gid in enumerate(groups, 1):
        print(f"  {i}. {gid}")
    print("="*50)
    print("\n💡 输入示例：")
    print("  • 单选：输入 1")
    print("  • 多选：输入 1,3,5（用逗号分隔）")
    print("  • 全选：输入 all")
    while True:
        choice = input("\n请选择要推送的群号：").strip()
        if not choice:
            print("输入不能为空，请重新输入")
            continue
        if choice.lower() == 'all':
            return groups
        try:
            if ',' in choice:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
            else:
                indices = [int(choice) - 1]
            selected = [groups[i] for i in indices if 0 <= i < len(groups)]
            if selected:
                return selected
            print("无效选择，请重新输入")
        except ValueError:
            print("请输入有效数字，用逗号分隔多选")

def play_notification_sound():
    """播放通知声音"""
    try:
        import winsound
        winsound.Beep(1000, 500)
        time.sleep(0.1)
        winsound.Beep(1200, 500)
        time.sleep(0.1)
        winsound.Beep(1000, 500)
    except:
        pass

def print_ticket_info(tickets: List[Dict], event_name: str = ""):
    """显示票务信息"""
    if not tickets:
        print("未查询到票务信息")
        return
    print(f"\n{'='*40}")
    if event_name:
        print(f"🎵 {event_name}")
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('-' * 40)
    for ticket in tickets:
        status = "有票" if ticket['status'] == '有票' else "售罄"
        print(f"  ¥{ticket['price']} | {ticket['name']} | {status}")
    available = [t for t in tickets if t['status'] == '有票']
    print('-' * 40)
    print(f"当前 {len(available)}/{len(tickets)} 个档位有余票")
    print('='*40)

def should_disable_qq_push() -> bool:
    """检查是否应该关闭QQ推送"""
    now = datetime.now()
    return now >= QQ_PUSH_END_DATE

def check_and_send_shutdown_notice() -> bool:
    """检查并发送关闭通知"""
    global QQ_PUSH_END_NOTICE_SENT
    now = datetime.now()
    if now >= QQ_PUSH_END_DATE:
        return False
    for notice_date in QQ_PUSH_NOTICE_DATES:
        if (now.year == notice_date.year and 
            now.month == notice_date.month and 
            now.day == notice_date.day and
            now.hour == QQ_PUSH_NOTICE_TIME[0] and 
            now.minute == QQ_PUSH_NOTICE_TIME[1]):
            if not QQ_PUSH_END_NOTICE_SENT:
                QQ_PUSH_END_NOTICE_SENT = True
                return True
    return False

# ===================== 防睡眠函数 =====================
try:
    kernel32 = ctypes.windll.kernel32
    EXECUTION_STATE = 0x80000003
    def prevent_sleep():
        kernel32.SetThreadExecutionState(EXECUTION_STATE)
    def allow_sleep():
        kernel32.SetThreadExecutionState(0)
except:
    def prevent_sleep():
        pass
    def allow_sleep():
        pass

# ===================== Selenium 相关 =====================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ===================== 主类 =====================
class ShowstartTicketChecker:
    def __init__(self, headless: bool = False, use_api: bool = False):
        self.headless = headless
        self.use_api = use_api
        self.price_tiers = [880, 780, 580, 480, 380, 280]
        self.driver = None
        self.tokens_set = False
        self.tokens = self.load_tokens()

    def _init_driver(self):
        if self.driver:
            return
        options = Options()
        if self.headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1')
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-notifications')
        options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        custom_driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
        if os.path.exists(custom_driver_path):
            service = Service(custom_driver_path)
        else:
            driver_path = ChromeDriverManager().install()
            import shutil
            shutil.copy(driver_path, custom_driver_path)
            service = Service(custom_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en-US', 'en']});
            Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
        """)

    def _close_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

    def wait_for_login(self):
        # 初始化浏览器并访问登录页面
        self._init_driver()
        self.driver.get("https://wap.showstart.com")
        print("\n请在浏览器窗口中完成后续的登录操作")
        print("注意：请使用已经在秀动账号实名认证后的手机号登录，否则票务信息加载不完整。")
        print("   1. 输入手机号并获取验证码")
        print("   2. 输入验证码并勾选同意协议")
        print("   3. 点击'立即登录'")
        print("\n登录成功后，请回到命令行按回车键继续...")
        input()

    def save_tokens_after_login(self):
        """登录后保存token和cookie到配置文件"""
        import json
        import os
        print("\n[INFO] 正在捕获登录凭证...")
        try:
            # 获取localStorage中的token
            tokens = self.driver.execute_script("""
                var userInfoStr = localStorage.getItem('userInfo') || '{}';
                var userInfo = JSON.parse(userInfoStr);
                var userId = userInfo.data ? userInfo.data.userId : '';
                return JSON.stringify({
                    'accessToken': localStorage.getItem('accessToken') || '',
                    'sign': localStorage.getItem('sign') || '',
                    'idToken': localStorage.getItem('idToken') || '',
                    'token': localStorage.getItem('token') || '',
                    'st_flpv': localStorage.getItem('st_flpv') || '',
                    'userId': userId || localStorage.getItem('userId') || ''
                });
            """)
            
            # 获取浏览器cookie
            cookies = {}
            for cookie in self.driver.get_cookies():
                cookies[cookie['name']] = cookie['value']
            
            if tokens:
                config = json.loads(tokens)
                
                # 添加cookie到配置
                config['cookies'] = cookies
                
                if config.get('accessToken') and len(config['accessToken']) > 10:
                    config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
                    os.makedirs(config_dir, exist_ok=True)
                    config_path = os.path.join(config_dir, 'tokens.json')
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2)
                    print("[SUCCESS] 登录凭证已保存")
                    self.tokens = config
                    self.tokens_set = True
                    return True
                else:
                    print("[WARNING] 未获取到有效的登录凭证")
                    return False
            else:
                print("[WARNING] 获取登录凭证失败")
                return False
        except Exception as e:
            print(f"[ERROR] 保存登录凭证失败: {e}")
            return False

    def load_tokens(self):
        """加载保存的token"""
        config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
        config_path = os.path.join(config_dir, 'tokens.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None

    def set_tokens_to_browser(self):
        """将token设置到浏览器localStorage"""
        tokens = self.load_tokens()
        if not tokens:
            return False
        try:
            self._init_driver()
            self.driver.get("https://www.showstart.com")
            for key, value in tokens.items():
                if value:
                    self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
            print("[INFO] 已加载保存的登录凭证")
            return True
        except Exception as e:
            print(f"[ERROR] 设置登录凭证失败: {e}")
            return False

    def check_login_status(self):
        """检查登录状态"""
        tokens = self.load_tokens()
        return tokens and tokens.get('accessToken')

    def check_tickets(self, event_id: str) -> List[Dict]:
        """查询演出余票（支持API模式和浏览器模式）"""
        if not self.tokens:
            self.tokens = self.load_tokens()
        
        # API模式：直接调用API获取票务信息
        if self.use_api and self.tokens:
            print("[API] INFO: 使用API模式查询余票...")
            # 如果有浏览器实例，直接在浏览器中执行API请求
            existing_driver = getattr(self, 'driver', None)
            tickets = get_ticket_info_api(event_id, self.tokens, driver=existing_driver)
            if tickets:
                return tickets
            print("[API] WARN: API查询失败，尝试刷新token...")
            # 尝试刷新token（复用已有的浏览器实例，如果有的话）
            self.tokens = refresh_tokens_from_browser(keep_driver=True, driver=existing_driver)
            # 提取浏览器实例
            driver = self.tokens.pop('_driver', None)
            
            # 再次尝试API（使用刷新后的token和浏览器）
            tickets = get_ticket_info_api(event_id, self.tokens, driver=driver)
            if tickets:
                # 如果API成功了，关闭保留的浏览器
                if driver:
                    driver.quit()
                return tickets
            print("[API] WARN: 刷新后仍失败，回退到浏览器模式")
            # 如果API仍然失败，使用保留的浏览器实例
            if driver:
                self.driver = driver
                self.tokens_set = True  # 标记已设置token，避免重复设置
                try:
                    # 直接使用已登录的浏览器访问演出页面
                    url = f"https://www.showstart.com/event/{event_id}"
                    self.driver.get(url)
                    time.sleep(2)
                    # 尝试点击购票按钮并解析票务信息
                    buy_buttons_xpath = [
                        '//*[contains(text(), "立即购票")]',
                        '//*[contains(text(), "购票")]',
                        '//*[contains(text(), "预约")]',
                        '//button[contains(text(), "购票") or contains(text(), "立即购票")]',
                        '//div[contains(@class, "buy") or contains(@class, "ticket")]/button',
                        '//*[@id="buyBtn"]',
                        '//a[contains(text(), "购票") or contains(text(), "立即购票")]'
                    ]
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    from selenium.webdriver.common.by import By
                    clicked = False
                    for xpath in buy_buttons_xpath:
                        try:
                            buy_btn = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                            buy_btn.click()
                            time.sleep(1.5)
                            clicked = True
                            break
                        except:
                            continue
                    return self._parse_tickets()
                except Exception as e:
                    print(f"[API] ERROR: 使用保留浏览器失败: {e}")
                    # 浏览器连接失败，尝试关闭并重新初始化
                    try:
                        self.driver.quit()
                    except:
                        pass
                    print("[API] WARN: 重新初始化浏览器...")
        
        # 浏览器模式：使用Selenium
        self._init_driver()
        try:
            if self.tokens and not self.tokens_set:
                self.driver.get("https://www.showstart.com")
                time.sleep(0.5)
                for key, value in self.tokens.items():
                    if value:
                        self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
                self.tokens_set = True
            url = f"https://www.showstart.com/event/{event_id}"
            self.driver.get(url)
            time.sleep(1.5)
            buy_buttons_xpath = [
                '//*[contains(text(), "立即购票")]',
                '//*[contains(text(), "购票")]',
                '//*[contains(text(), "预约")]',
                '//button[contains(text(), "购票") or contains(text(), "立即购票")]',
                '//div[contains(@class, "buy") or contains(@class, "ticket")]/button',
                '//*[@id="buyBtn"]',
                '//a[contains(text(), "购票") or contains(text(), "立即购票")]'
            ]
            clicked = False
            for xpath in buy_buttons_xpath:
                try:
                    buy_btn = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    buy_btn.click()
                    time.sleep(1.5)
                    clicked = True
                    break
                except:
                    continue
            return self._parse_tickets()
        except Exception as e:
            print(f"[ERROR] 查询失败: {e}")
            return []

    def _parse_tickets(self) -> List[Dict]:
        """解析票务信息"""
        import re
        all_text = self.driver.execute_script("return document.body.innerText || document.documentElement.innerText;")
        found_tickets = {}
        patterns = [
            r'(\d{3,4})\s*元',
            r'¥\s*(\d{3,4})',
            r'(\d{3,4})\s*元\s*票',
            r'票\s*(\d{3,4})',
            r'(\d{3,4})元\D',
            r'(\d{3,4})\s*[元块]',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, all_text)
            for match in matches:
                price_str = match[0] if isinstance(match, tuple) else match
                if price_str.isdigit():
                    price_int = int(price_str)
                    if 100 <= price_int <= 2000 and price_int not in found_tickets:
                        found_tickets[price_int] = {
                            'price': price_int,
                            'name': f'{price_int}元票',
                            'status': '有票'
                        }
        lines = all_text.split('\n')
        for price in found_tickets:
            price_str = str(price)
            for i, line in enumerate(lines):
                if price_str in line:
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 3)
                    context = '\n'.join(lines[context_start:context_end])
                    if '票已售罄' in context or '已售罄' in context or '已售完' in context:
                        found_tickets[price]['status'] = '售罄'
                        break
                    # 检测"有乐迷未支付"状态
                    if '乐迷未支付' in context or '未支付' in context or '订单还未支付' in context:
                        found_tickets[price]['status'] = '回流票'
                        break
        return sorted(found_tickets.values(), key=lambda x: x['price'], reverse=True)

    def run_diagnostics(self) -> Dict[str, Dict]:
        """系统自检，诊断潜在问题"""
        results = {}
        print("\n" + "="*50)
        print("🔧 秀动余票查询工具 - 系统自检")
        print("="*50)
        results['chrome_driver'] = self._check_chrome_driver()
        results['network'] = self._check_network()
        results['website_access'] = self._check_website_access()
        results['selenium'] = self._check_selenium()
        print("\n" + "-"*50)
        print("📋 诊断结果汇总")
        print("-"*50)
        for check_name, result in results.items():
            status_icon = "✅" if result['status'] == 'pass' else ("⚠️" if result['status'] == 'warning' else "❌")
            print(f"{status_icon} {result['name']}: {result['message']}")
        print("\n" + "-"*50)
        print("💡 解决方案建议")
        print("-"*50)
        has_issues = False
        for check_name, result in results.items():
            if result['status'] != 'pass':
                has_issues = True
                print(f"\n📌 [{result['name']}]")
                for suggestion in result.get('suggestions', []):
                    print(f"   • {suggestion}")
        if not has_issues:
            print("🎉 所有检查项均通过！未发现问题。")
        print("\n" + "="*50)
        return results

    def _check_chrome_driver(self) -> Dict:
        result = {'name': 'ChromeDriver', 'status': 'pass', 'message': '正常', 'suggestions': []}
        custom_driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
        if os.path.exists(custom_driver_path):
            try:
                version_info = subprocess.run([custom_driver_path, '--version'], capture_output=True, text=True, timeout=5)
                if version_info.returncode == 0:
                    result['message'] = f"本地版本 - {version_info.stdout.strip()}"
                else:
                    result['status'] = 'warning'
                    result['message'] = '版本可能不匹配'
                    result['suggestions'] = ['当前chromedriver.exe可能与Chrome版本不匹配', '建议删除本地chromedriver.exe，让脚本自动下载匹配版本']
            except Exception as e:
                result['status'] = 'warning'
                result['message'] = f'本地驱动异常: {e}'
                result['suggestions'] = ['删除当前chromedriver.exe', '脚本将自动下载匹配版本']
        else:
            try:
                driver_path = ChromeDriverManager().install()
                if os.path.exists(driver_path):
                    result['message'] = '自动下载版本正常'
                else:
                    result['status'] = 'warning'
                    result['message'] = '驱动未找到'
                    result['suggestions'] = ['运行一次查询让脚本自动下载驱动']
            except Exception as e:
                result['status'] = 'error'
                result['message'] = f'驱动检查失败: {e}'
                result['suggestions'] = ['网络问题导致无法下载驱动', '请检查网络连接后重试']
        return result

    def _check_network(self) -> Dict:
        result = {'name': '网络连接', 'status': 'pass', 'message': '正常', 'suggestions': []}
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            result['message'] = '网络连接正常'
        except:
            result['status'] = 'error'
            result['message'] = '无法连接外网'
            result['suggestions'] = ['请检查网络连接', '确保电脑已连接到互联网', '尝试打开浏览器访问其他网站测试']
        return result

    def _check_website_access(self) -> Dict:
        result = {'name': '秀动网站访问', 'status': 'pass', 'message': '正常', 'suggestions': []}
        try:
            response = requests.get("https://www.showstart.com", timeout=10)
            if response.status_code == 200:
                result['message'] = '网站可正常访问'
            else:
                result['status'] = 'warning'
                result['message'] = f'网站返回状态码: {response.status_code}'
                result['suggestions'] = ['秀动网站可能正在维护', '稍后再试或联系秀动客服']
        except ImportError:
            result['status'] = 'warning'
            result['message'] = '无法验证（缺少requests库）'
            result['suggestions'] = ['网站应该可以访问', '如果实际访问有问题，请安装requests库: pip install requests']
        except Exception as e:
            result['status'] = 'error'
            result['message'] = f'网站无法访问: {e}'
            result['suggestions'] = ['秀动网站可能宕机或维护中', '稍后再试', '或检查网络代理设置']
        return result

    def _check_selenium(self) -> Dict:
        result = {'name': 'Selenium环境', 'status': 'pass', 'message': '正常', 'suggestions': []}
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            result['message'] = 'Selenium库正常'
        except ImportError as e:
            result['status'] = 'error'
            result['message'] = f'Selenium库缺失: {e}'
            result['suggestions'] = ['请安装Selenium: pip install selenium', '请安装webdriver-manager: pip install webdriver-manager']
        return result

# ===================== 主函数 =====================
def main():
    try:
        password = "Edgure2003"
        max_attempts = 3
        for attempt in range(max_attempts):
            input_pass = input("\n请输入管理员密码: ").strip()
            if input_pass == password:
                break
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"[ERROR] 密码错误，剩余尝试次数: {remaining}")
                else:
                    print("[ERROR] 密码错误次数过多，程序退出")
                    return
        
        use_api_mode = False
        api_choice = input("\n是否使用API模式（更快更稳定，需要已保存的登录凭证）？(y/n): ").strip().lower()
        if api_choice == 'y':
            use_api_mode = True
            print("[INFO] 🚀 已启用API模式")
        
        checker = ShowstartTicketChecker(use_api=use_api_mode)
        is_logged_in = checker.check_login_status()

        # 如果启用了API模式但没有登录凭证，先要求登录
        if use_api_mode and not checker.tokens:
            print("\n[INFO] API模式需要登录凭证，请先登录")
            checker.wait_for_login()
            checker.save_tokens_after_login()


        while True:
            print("\n" + "="*70)
            print("秀动余票查询工具 v3.4 (API模式修复版)")
            print("本版本更新：1. 修正魔改MD5签名算法")
            print("          2. 修复API请求头字段")
            print("          3. 增加Token自动刷新")
            print(f"当前模式: {'🚀 API模式' if use_api_mode else '🌐 浏览器模式'}")
            print("="*70)
            print("\n请选择操作：")
            print("  1. 查询一次余票")
            print("  2. 持续监控余票")
            print("  3. 持续监控余票 + QQ推送")
            print("  4. 故障诊断")
            print("  5. 退出\n")
            choice = input("请输入选项 (1/2/3/4/5): ").strip()
            
            if choice == '1':
                event_id = input("请输入演出ID: ").strip()
                if not event_id:
                    print("请输入有效的演出ID")
                    continue
                try:
                    print(f"\n[INFO] 正在查询该演出...")
                    tickets = checker.check_tickets(event_id)
                    print_ticket_info(tickets, f"演出 {event_id}")
                    if not tickets:
                        print("\n[INFO] 需要登录以查看更多票务信息")
                        checker.wait_for_login()
                        checker.save_tokens_after_login()
                        if not checker.use_api:
                            switch = input("\n是否切换到API模式以获得更快更稳定的查询体验？(y/n): ").strip().lower()
                            if switch == 'y':
                                checker.use_api = True
                                print("[INFO] 🚀 已切换到API模式")
                        print(f"\n[INFO] 登录成功，正在查询该演出的余票...")
                        tickets = checker.check_tickets(event_id)
                        print_ticket_info(tickets, f"演出 {event_id}")
                    checker._close_driver()
                    input("\n按回车键继续...")
                except Exception as e:
                    print(f"\n[ERROR] 查询过程出错: {e}")
                    checker._close_driver()
                    input("\n按回车键继续...")
            
            elif choice == '2':
                event_id = input("请输入演出ID: ").strip()
                if not event_id:
                    print("输错了呢，请检查后重新输入")
                    continue
                try:
                    print(f"\n[INFO] 正在查询该演出...")
                    tickets = checker.check_tickets(event_id)
                    print_ticket_info(tickets, f"演出 {event_id}")
                    if not tickets:
                        print("\n[INFO] 请登录查看更多票务信息")
                        checker.wait_for_login()
                        checker.save_tokens_after_login()
                        if not checker.use_api:
                            switch = input("\n是否切换到API模式以获得更快更稳定的查询体验？(y/n): ").strip().lower()
                            if switch == 'y':
                                checker.use_api = True
                                print("[INFO] 🚀 已切换到API模式")
                        print(f"\n[INFO] 登录成功，正在查询该演出的余票信息...")
                        tickets = checker.check_tickets(event_id)
                        print_ticket_info(tickets, f"演出 {event_id}")
                    try:
                        interval = int(input("\n请输入查票间隔(秒，默认30): ").strip() or 30)
                    except ValueError:
                        interval = 30
                    print(f"\n[INFO] 开始监控该演出的余票情况，每 {interval} 秒检查一次...")
                    print("[INFO] 已启用防睡眠模式，电脑不会自动熄屏")
                    print("[INFO] 按 Ctrl+C 停止监控\n")
                    last_available_count = -1
                    error_count = 0
                    max_errors = 3
                    while True:
                        try:
                            prevent_sleep()
                            tickets = checker.check_tickets(event_id)
                            # 重置错误计数
                            error_count = 0
                            available_count = sum(1 for t in tickets if t['status'] == '有票')
                            current_time = datetime.now().strftime('%H:%M:%S')
                            if available_count > 0 and available_count != last_available_count:
                                print(f"\n[{current_time}] 检测到余票变化！")
                                print_ticket_info(tickets, f"演出 {event_id}")
                                play_notification_sound()
                                last_available_count = available_count
                            elif available_count > 0:
                                print(f"[{current_time}] 仍有余票 ({available_count}个档位)")
                            else:
                                print(f"[{current_time}] 暂无余票")
                            time.sleep(interval)
                        except KeyboardInterrupt:
                            print("\n[INFO] 监控已停止")
                            break
                        except Exception as e:
                            error_count += 1
                            print(f"\n[ERROR] 监控过程出错: {e}")
                            
                            # 检查是否是浏览器连接问题
                            if "invalid session id" in str(e) or "disconnected" in str(e).lower():
                                print("[ERROR] 浏览器连接已断开")
                                if error_count <= max_errors:
                                    print(f"[INFO] 尝试重新初始化浏览器 ({error_count}/{max_errors})...")
                                    try:
                                        checker._close_driver()
                                    except:
                                        pass
                                    time.sleep(3)
                                    continue
                                else:
                                    print(f"[ERROR] 连续失败{max_errors}次，无法恢复，监控停止")
                                    break
                            
                            # 检查是否是登录过期问题
                            if "登录过期" in str(e) or "重新登录" in str(e):
                                print("[ERROR] 登录凭证已过期")
                                if error_count <= max_errors:
                                    print(f"[INFO] 尝试重新获取登录凭证 ({error_count}/{max_errors})...")
                                    try:
                                        checker._close_driver()
                                    except:
                                        pass
                                    checker.tokens = None
                                    time.sleep(3)
                                    continue
                                else:
                                    print(f"[ERROR] 连续失败{max_errors}次，无法恢复，监控停止")
                                    break
                            
                            print("[INFO] 等待5秒后继续监控...")
                            time.sleep(5)
                    allow_sleep()
                    checker._close_driver()
                    input("\n按回车键继续...")
                except Exception as e:
                    print(f"\n[ERROR] 监控初始化失败: {e}")
                    allow_sleep()
                    checker._close_driver()
                    input("\n按回车键继续...")
            
            elif choice == '3':
                event_id = input("请输入演出ID: ").strip()
                if not event_id:
                    print("输错了呢，请检查后重新输入")
                    continue
                try:
                    print(f"\n[INFO] 正在查询该演出...")
                    tickets = checker.check_tickets(event_id)
                    print_ticket_info(tickets, f"演出 {event_id}")
                    if not tickets:
                        print("\n[INFO] 请登录查看更多票务信息")
                        checker.wait_for_login()
                        checker.save_tokens_after_login()
                        print(f"\n[INFO] 登录成功，正在查询该演出的余票信息...")
                        tickets = checker.check_tickets(event_id)
                        print_ticket_info(tickets, f"演出 {event_id}")
                    try:
                        interval = int(input("\n请输入查票间隔(秒，默认30): ").strip() or 30)
                    except ValueError:
                        interval = 30
                    
                    target_groups = select_target_groups()
                    if not target_groups:
                        input("\n按回车键继续...")
                        continue
                    
                    monitor_start_time = datetime.now().strftime('%H:%M:%S')
                    print(f"\n[INFO] 开始监控该演出的余票情况，每 {interval} 秒检查一次...")
                    print(f"[INFO] QQ推送目标群: {', '.join(str(g) for g in target_groups)}")
                    print("[INFO] 已启用防睡眠模式，电脑不会自动熄屏")
                    print("[INFO] 按 Ctrl+C 停止监控\n")
                    try:
                        checker.driver.minimize_window()
                    except:
                        pass
                    
                    start_msg = f"📢 秀动回流票监控已启动！\n📍 监控演出ID: {event_id}\n⏰ 监控时段: {monitor_start_time} 开始\n🔔 有回流票会第一时间通知大家！\n\n请保持关注，祝各位群友刷到回流票！🎫"
                    for tg in target_groups:
                        send_to_qq_group(tg, start_msg)
                    send_phone_notification("🎉 监控已启动", f"秀动回流票监控已开始!\n\n演出ID: {event_id}\n推送群数: {len(target_groups)}个\n间隔: {interval}秒")
                    show_system_notification("🎉 监控已启动", f"秀动回流票监控已开始!\n\n演出ID: {event_id}\n推送群数: {len(target_groups)}个\n间隔: {interval}秒")
                    
                    last_available_count = -1
                    last_report_time = time.time()
                    report_interval = 300
                    has_shown_notification = False
                    maintenance_done_today = False
                    confirm_count = 0
                    CONFIRM_THRESHOLD = 2
                    global DAILY_SHUTDOWN_DONE, QQ_PUSH_END_NOTICE_SENT
                    
                    while True:
                        # 检查关闭通知
                        if check_and_send_shutdown_notice():
                            shutdown_notice = "📢 【重要通知】📢\n\n由于该演出2026/6/7 19:00以后不再接受退票，23:00为最后一波回流票高峰，故于2026/6/8零点起正式关闭QQ群推送。\n\n请各位群友提前做好准备，祝大家都能抢到票！🎫"
                            for tg in target_groups:
                                send_to_qq_group(tg, shutdown_notice)
                            QQ_PUSH_END_NOTICE_SENT = True
                        
                        now = datetime.now()
                        if now.weekday() == 2 and now.hour == 10 and now.minute >= 57 and not maintenance_done_today:
                            print("\n[INFO] ⏰ 检测到每周三维护时间，即将自动关闭脚本...")
                            maintenance_msg = f"📢 秀动回流票监控即将暂停维护！\n⏰ 维护时间: {now.strftime('%Y-%m-%d')} 11:00 - 11:10\n🔧 每周例行维护更新，预计10分钟后恢复\n\n感谢大家的理解与支持！🙏"
                            for tg in target_groups:
                                send_to_qq_group(tg, maintenance_msg)
                            send_phone_notification("⏰ 维护提醒", f"秀动回流票监控即将暂停维护！\n\n维护时间: {now.strftime('%Y-%m-%d')} 11:00-11:10")
                            show_system_notification("⏰ 维护提醒", "即将进行日常脚本维护，脚本将自动关闭！")
                            maintenance_done_today = True
                            break
                        
                        if now.hour == DAILY_SHUTDOWN_HOUR and now.minute == 0 and not DAILY_SHUTDOWN_DONE:
                            print(f"\n[INFO] ⏰ 检测到每日关闭时间（{DAILY_SHUTDOWN_HOUR}:00），即将自动关闭脚本...")
                            shutdown_msg = f"📢 秀动回流票监控已结束！\n⏰ 今日监控到此结束\n感谢大家的关注，明天同一时间再见！👋"
                            for tg in target_groups:
                                send_to_qq_group(tg, shutdown_msg)
                            send_phone_notification("⏹️ 监控已结束", f"秀动回流票监控已结束!\n\n演出ID: {event_id}\n今日监控到此结束，明天见！")
                            show_system_notification("⏹️ 监控已结束", f"秀动回流票监控已结束!\n\n演出ID: {event_id}\n今日监控到此结束，明天见！")
                            DAILY_SHUTDOWN_DONE = True
                            break
                        
                        napcat_heartbeat()
                        try:
                            prevent_sleep()
                            tickets = checker.check_tickets(event_id)
                            available_count = sum(1 for t in tickets if t['status'] == '有票')
                            # 检测回流票状态（乐迷未支付）
                            return_ticket_count = sum(1 for t in tickets if t['status'] == '回流票')
                            current_time_str = datetime.now().strftime('%H:%M:%S')
                            current_timestamp = time.time()
                            
                            # 检测回流票状态
                            if return_ticket_count > 0:
                                print(f"\n[{current_time_str}] ⚡ 检测到回流票机会！")
                                return_tickets = [t for t in tickets if t['status'] == '回流票']
                                ticket_info = "\n".join([f"• {t['price']}元 - {t['name']}" for t in return_tickets])
                                # 发送回流票消息
                                msg = f"⚡ 好快的手速，这个票很快就要没了，能够创建订单就是胜利，请某位欧气群友及时下单支付，谢谢~\n没创成功的也没事，下次总会有的~\n\n演出ID: {event_id}\n回流票档位：\n{ticket_info}"
                                if not should_disable_qq_push():
                                    for tg in target_groups:
                                        send_to_qq_group(tg, msg)
                                show_system_notification("⚡ 回流票机会！", f"演出ID: {event_id}\n\n回流票档位：\n{ticket_info}\n\n快去抢票！")
                            
                            if available_count > 0:
                                confirm_count += 1
                                is_new_detection = confirm_count == CONFIRM_THRESHOLD
                                if confirm_count < CONFIRM_THRESHOLD:
                                    print(f"\n[{current_time_str}] 🔍 检测到有票（确认中 {confirm_count}/{CONFIRM_THRESHOLD}）")
                                else:
                                    if is_new_detection:
                                        print(f"\n[{current_time_str}] 🎉 确认有回流票！")
                                        available_tickets = [t for t in tickets if t['status'] == '有票']
                                        ticket_info = "\n".join([f"• {t['price']}元 - {t['name']}" for t in available_tickets])
                                        msg = generate_ticket_message(event_id, tickets)
                                        if not should_disable_qq_push():
                                            for tg in target_groups:
                                                send_to_qq_group(tg, msg)
                                                send_to_qq_group(tg, NEW_SONG_PROMO_MSG)
                                        send_phone_notification("🎉 检测到回流票！", f"演出ID: {event_id}\n\n有票档位：\n{ticket_info}\n\n快去秀动抢票！")
                                        show_system_notification("🎉 检测到回流票！", f"演出ID: {event_id}\n\n有票档位：\n{ticket_info}\n\n快去秀动抢票！")
                                        has_shown_notification = False
                                    else:
                                        print(f"\n[{current_time_str}]  仍有余票 ({available_count}个档位)")
                                        if current_timestamp - last_report_time >= report_interval:
                                            msg = generate_ticket_message(event_id, tickets)
                                            if not should_disable_qq_push():
                                                for tg in target_groups:
                                                    send_to_qq_group(tg, msg)
                                                    send_to_qq_group(tg, NEW_SONG_PROMO_MSG)
                                            last_report_time = current_timestamp
                                last_available_count = available_count
                                if is_new_detection:
                                    last_report_time = current_timestamp
                            else:
                                confirm_count = 0
                                print(f"[{current_time_str}]  暂无余票")
                                if current_timestamp - last_report_time >= report_interval:
                                    msg = generate_ticket_message(event_id, tickets)
                                    if not should_disable_qq_push():
                                        for tg in target_groups:
                                            send_to_qq_group(tg, msg)
                                            send_to_qq_group(tg, NEW_SONG_PROMO_MSG)
                                    last_report_time = current_timestamp
                            time.sleep(interval)
                        except KeyboardInterrupt:
                            print("\n[INFO] 监控已停止")
                            break
                        except Exception as e:
                            print(f"\n[ERROR] 监控过程出错: {e}")
                            print("[INFO] 等待5秒后继续监控...")
                            time.sleep(5)
                except Exception as e:
                    print(f"\n[ERROR] 监控初始化失败: {e}")
                finally:
                    allow_sleep()
                    checker._close_driver()
                    input("\n按回车键继续...")
            
            elif choice == '4':
                print("\n[INFO] 正在启动系统诊断...")
                checker.run_diagnostics()
                input("\n按回车键继续...")
            
            elif choice == '5':
                print("感谢您的使用，祝您抢票成功，再见！")
                break
            else:
                print("无效选项，请重新输入")
    except Exception as e:
        print(f"\n[FATAL ERROR] 程序发生致命错误: {e}")
    finally:
        allow_sleep()
        if 'checker' in locals():
            checker._close_driver()
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()