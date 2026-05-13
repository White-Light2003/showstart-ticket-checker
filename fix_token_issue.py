#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 save_tokens_after_login 函数"""

# 读取文件内容
with open(r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复 save_tokens_after_login 函数
old_str = '''                config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
                    os.makedirs(config_dir, exist_ok=True)
                    config_path = os.path.join(config_dir, 'tokens.json')
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2)
                    print("[SUCCESS] 登录凭证已保存")
                    self.tokens_set = True
                    return True'''

new_str = '''                config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
                    os.makedirs(config_dir, exist_ok=True)
                    config_path = os.path.join(config_dir, 'tokens.json')
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2)
                    print("[SUCCESS] 登录凭证已保存")
                    self.tokens = config  # 设置到内存中
                    self.tokens_set = True
                    return True'''

content = content.replace(old_str, new_str)

# 同时修复 __init__ 函数，初始化时加载token
old_init = '''    def __init__(self, headless: bool = False, use_api: bool = False):
        self.headless = headless
        self.use_api = use_api
        self.price_tiers = [880, 780, 580, 480, 380, 280]
        self.driver = None
        self.tokens_set = False
        self.tokens = None'''

new_init = '''    def __init__(self, headless: bool = False, use_api: bool = False):
        self.headless = headless
        self.use_api = use_api
        self.price_tiers = [880, 780, 580, 480, 380, 280]
        self.driver = None
        self.tokens_set = False
        self.tokens = self.load_tokens()  # 初始化时加载token'''

content = content.replace(old_init, new_init)

# 保存修复后的文件
with open(r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] 已修复 save_tokens_after_login 和 __init__ 函数")
print("现在登录后会立即设置 token 到内存，监控时就会使用 API 模式了")
