#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复重复代码"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

# 读取所有行
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 删除第1542-1548行（从0开始计数的话是1541-1547）
# 实际看起来是从第1542行开始重复了
del lines[1542:1549]  # 删除重复的代码

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("[OK] 重复代码已删除！")
