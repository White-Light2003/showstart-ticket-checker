import webbrowser
import time
import json
import os

def main():
    print("[音乐] 秀动余票查询工具 - 简化版")
    print("="*40)
    
    print("\n1. 打开登录页面")
    print("2. 退出")
    
    choice = input("\n请输入选项: ").strip()
    
    if choice == '1':
        print("\n[INFO] 正在打开秀动登录页面...")
        webbrowser.open("https://www.showstart.com")
        
        print("\n请在浏览器中完成登录后:")
        print("1. 按 F12 打开开发者工具")
        print("2. 切换到 Application 面板")
        print("3. 在左侧 Storage -> Local Storage 中找到 showstart.com")
        print("4. 复制以下值:")
        print("   - accessToken")
        print("   - sign")
        print("   - userId")
        
        input("\n复制完成后按回车键继续...")
        
        print("\n请依次输入复制的值:")
        config = {
            'accessToken': input("accessToken: ").strip(),
            'sign': input("sign: ").strip(),
            'userId': input("userId: ").strip(),
            'idToken': '',
            'token': '',
            'st_flpv': ''
        }
        
        config_dir = os.path.join(os.path.expanduser('~'), '.showstart_checker')
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, 'tokens.json')
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n[SUCCESS] 登录凭证已保存到: {config_path}")
        
    elif choice == '2':
        print("退出...")
        
    else:
        print("无效选项")

if __name__ == "__main__":
    main()