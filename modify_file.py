#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接修改文件"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到要修改的部分
i = 0
while i < len(lines):
    if 'checker = ShowstartTicketChecker(use_api=use_api_mode)' in lines[i]:
        # 在这之后插入代码
        insert_lines = [
            '        is_logged_in = checker.check_login_status()\n',
            '\n',
            '        # 如果启用了API模式但没有登录凭证，先要求登录\n',
            '        if use_api_mode and not checker.tokens:\n',
            '            print("\\n[INFO] API模式需要登录凭证，请先登录")\n',
            '            checker.wait_for_login()\n',
            '            checker.save_tokens_after_login()\n',
            '\n',
            '        while True:\n'
        ]
        # 删除后面的几行
        del lines[i+1:i+5]  # 删除 is_logged_in 到 while True 之前的行
        # 插入新代码
        lines[i+1:i+1] = insert_lines
        break
    i += 1

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("修复完成！现在启用API模式时会先要求登录")
