#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复API模式初始化逻辑"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复：启用API模式但没有token时，先要求登录
old_part = '''        checker = ShowstartTicketChecker(use_api=use_api_mode)
        is_logged_in = checker.check_login_status()
        
        while True:'''

new_part = '''        checker = ShowstartTicketChecker(use_api=use_api_mode)
        is_logged_in = checker.check_login_status()
        
        # 如果启用了API模式但没有登录凭证，先要求登录
        if use_api_mode and not checker.tokens:
            print("\n[INFO] API模式需要登录凭证，请先登录")
            checker.wait_for_login()
            checker.save_tokens_after_login()
        
        while True:'''

content = content.replace(old_part, new_part)

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("="*70)
print("修复完成！")
print("="*70)
print("\n修复内容：")
print("启用API模式但没有token时，会先要求登录")
print("\n现在的流程：")
print("1. 选择API模式")
print("2. 如果没有token，立即提示登录")
print("3. 登录成功后保存token")
print("4. 后续查询都会使用API模式")
