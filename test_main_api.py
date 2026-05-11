#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试修改后的API函数"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from showstart_ticket_checker import get_ticket_info_api

def test_api():
    config_path = os.path.join(os.path.expanduser('~'), '.showstart_checker', 'tokens.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        tokens = json.load(f)
    
    print("测试修改后的API函数...")
    print("Token信息:")
    print("  userId:", tokens.get('userId'))
    print("  accessToken:", tokens.get('accessToken', '')[:10], "...")
    print("  sign:", tokens.get('sign', '')[:10], "...")
    print("  idToken:", tokens.get('idToken', '')[:10], "...")
    print("  token:", tokens.get('token', '')[:10], "...")
    print("  st_flpv:", tokens.get('st_flpv', '')[:10], "...")
    
    result = get_ticket_info_api("295821", tokens)
    print("\nAPI返回结果:")
    print(result)

if __name__ == "__main__":
    test_api()