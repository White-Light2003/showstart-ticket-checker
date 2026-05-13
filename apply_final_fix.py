#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在启用API模式后、进入主循环前检查并要求登录"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到位置
old_str = '''        checker = ShowstartTicketChecker(use_api=use_api_mode)
        is_logged_in = checker.check_login_status()
        
        while True:'''

new_str = '''        checker = ShowstartTicketChecker(use_api=use_api_mode)
        is_logged_in = checker.check_login_status()
        
        # 如果启用了API模式但没有登录凭证，先要求登录
        if use_api_mode and not checker.tokens:
            print("\\n[INFO] API模式需要登录凭证，请先登录")
            checker.wait_for_login()
            checker.save_tokens_after_login()
        
        while True:'''

# 替换
content = content.replace(old_str, new_str)

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修复完成！")
print("\n现在的流程：")
print("1. 选择 API 模式")
print("2. 如果没有保存的 token，立即提示登录")
print("3. 登录成功后保存 token 到内存和文件")
print("4. 进入主菜单，所有查询都会使用 API 模式")
