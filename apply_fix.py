#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 showstart_ticket_checker（DS）.py 中的 token 问题"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复 1: save_tokens_after_login 函数中设置 self.tokens
old_part1 = '''                    print("[SUCCESS] 登录凭证已保存")
                    self.tokens_set = True
                    return True'''

new_part1 = '''                    print("[SUCCESS] 登录凭证已保存")
                    self.tokens = config
                    self.tokens_set = True
                    return True'''

content = content.replace(old_part1, new_part1)

# 修复 2: __init__ 函数中初始化时加载 token
old_part2 = '''    def __init__(self, headless: bool = False, use_api: bool = False):
        self.headless = headless
        self.use_api = use_api
        self.price_tiers = [880, 780, 580, 480, 380, 280]
        self.driver = None
        self.tokens_set = False
        self.tokens = None'''

new_part2 = '''    def __init__(self, headless: bool = False, use_api: bool = False):
        self.headless = headless
        self.use_api = use_api
        self.price_tiers = [880, 780, 580, 480, 380, 280]
        self.driver = None
        self.tokens_set = False
        self.tokens = self.load_tokens()'''

content = content.replace(old_part2, new_part2)

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("="*70)
print("修复完成！")
print("="*70)
print("\n修复内容：")
print("1. 登录后立即将 token 保存到 self.tokens")
print("2. 初始化时自动加载已保存的 token")
print("\n现在监控模式会使用 API 模式了！")
