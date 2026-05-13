#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""删除重复的代码"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

# 读取所有行
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到需要删除的重复部分
# 我们要保留第一个插入的代码，删除后面重复的
new_lines = []
i = 0
while i < len(lines):
    # 如果找到重复的开始
    if i > 1535 and '如果启用了API模式但没有登录凭证，先要求登录' in lines[i]:
        # 跳过重复的 8 行
        i += 8
    else:
        new_lines.append(lines[i])
        i += 1

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("[OK] 删除重复代码完成！")
