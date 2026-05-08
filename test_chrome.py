import subprocess
import time

print("测试1: 检查Chrome路径是否存在...")
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
import os
if os.path.exists(chrome_path):
    print(f"✅ Chrome路径存在: {chrome_path}")
else:
    print(f"❌ Chrome路径不存在: {chrome_path}")

print("\n测试2: 尝试直接启动Chrome...")
try:
    process = subprocess.Popen([chrome_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(timeout=10)
    print(f"✅ Chrome版本: {stdout.decode().strip()}")
except subprocess.TimeoutExpired:
    print("❌ Chrome启动超时")
except Exception as e:
    print(f"❌ Chrome启动失败: {e}")

print("\n测试3: 尝试下载ChromeDriver...")
try:
    from webdriver_manager.chrome import ChromeDriverManager
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("正在尝试下载ChromeDriver...")
    driver_path = ChromeDriverManager().install()
    print(f"✅ ChromeDriver下载成功: {driver_path}")
except Exception as e:
    print(f"❌ ChromeDriver下载失败: {type(e).__name__}: {e}")

print("\n测试完成!")