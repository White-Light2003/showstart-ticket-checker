#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 wait_for_login 函数，确保打开浏览器"""

file_path = r'c:\Users\35184\Documents\trae_projects\showstart\showstart_ticket_checker（DS）.py'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修改 wait_for_login 函数
old_str = '''    def wait_for_login(self):
        print("\\n请在浏览器窗口中完成后续的登录操作")
        print("注意：请使用已经在秀动账号实名认证后的手机号登录，否则票务信息加载不完整。")
        print("   1. 输入手机号并获取验证码")
        print("   2. 输入验证码并勾选同意协议")
        print("   3. 点击'立即登录'")
        print("\\n登录成功后，请回到命令行按回车键继续...")
        input()'''

new_str = '''    def wait_for_login(self):
        # 初始化浏览器并访问登录页面
        self._init_driver()
        self.driver.get("https://wap.showstart.com")
        print("\\n请在浏览器窗口中完成后续的登录操作")
        print("注意：请使用已经在秀动账号实名认证后的手机号登录，否则票务信息加载不完整。")
        print("   1. 输入手机号并获取验证码")
        print("   2. 输入验证码并勾选同意协议")
        print("   3. 点击'立即登录'")
        print("\\n登录成功后，请回到命令行按回车键继续...")
        input()'''

content = content.replace(old_str, new_str)

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] wait_for_login 函数已修复！")
print("\n现在选择 API 模式后会：")
print("1. 自动打开浏览器")
print("2. 访问 wap.showstart.com")
print("3. 提示完成登录")
