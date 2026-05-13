#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""精确修改文件"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

# 读取所有行
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到需要修改的位置并修改
new_lines = []
i = 0
while i < len(lines):
    new_lines.append(lines[i])
    
    # 在 is_logged_in 这行之后插入代码
    if 'is_logged_in = checker.check_login_status()' in lines[i]:
        # 添加空行
        new_lines.append('\n')
        # 添加检查代码
        new_lines.append('        # 如果启用了API模式但没有登录凭证，先要求登录\n')
        new_lines.append('        if use_api_mode and not checker.tokens:\n')
        new_lines.append('            print("\\n[INFO] API模式需要登录凭证，请先登录")\n')
        new_lines.append('            checker.wait_for_login()\n')
        new_lines.append('            checker.save_tokens_after_login()\n')
        new_lines.append('\n')
    
    i += 1

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ 修复完成！")
print("\n现在的流程：")
print("1. 选择 API 模式")
print("2. 如果没有保存的 token，立即提示登录")
print("3. 登录成功后保存 token 到内存和文件")
print("4. 进入主菜单，所有查询都会显示 [API] INFO: 使用API模式查询余票...")
