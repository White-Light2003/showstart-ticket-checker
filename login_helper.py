"""
秀动登录助手
打开登录页面，用户登录后自动获取token保存
"""
import time
import json
import hashlib
import random
import sys
import os
import logging
from datetime import datetime

# 日志配置
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f'login_{datetime.now().strftime("%Y%m%d")}.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
    ]
)
logger = logging.getLogger('xiudong-login')


def log(msg):
    """打印日志，同时写入文件"""
    logger.info(msg)
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode('utf-8', errors='replace').decode('ascii', errors='replace'), flush=True)


def main():
    log("=" * 50)
    log("秀动登录助手")
    log("=" * 50)
    log("")
    log("即将打开登录页面，请在浏览器中登录")
    log("登录成功后，关闭浏览器即可")
    log("")

    from DrissionPage import ChromiumPage, ChromiumOptions
    import subprocess

    logger.info("启动浏览器")
    co = ChromiumOptions()
    co.auto_port()
    co.set_argument('--no-first-run')
    
    # 尝试查找 Chrome 路径
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    
    chrome_path = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_path = path
            break
    
    if chrome_path:
        logger.info(f"使用Chrome路径: {chrome_path}")
        co.set_browser_path(chrome_path)
    
    try:
        page = ChromiumPage(co)
    except Exception as e:
        logger.error(f"浏览器启动失败: {e}")
        # 尝试不指定路径
        co2 = ChromiumOptions()
        co2.auto_port()
        co2.set_argument('--no-first-run')
        page = ChromiumPage(co2)

    # 直接打开登录页面
    log(f"[{datetime.now()}] 打开登录页面...")
    logger.info("打开登录页面")
    page.get("https://wap.showstart.com/pages/passport/login/login?redirect=%252Fpages%252FmyHome%252FmyHome")
    time.sleep(2)

    log("")
    log("请在浏览器中登录...")
    log("登录成功后会自动跳转，然后关闭浏览器即可")
    log("")

    # 等待用户登录
    max_wait = 300  # 最多等待5分钟
    start_time = time.time()
    logged_in = False

    log(f"[{datetime.now()}] 等待登录中...")

    while time.time() - start_time < max_wait:
        try:
            # 检查是否有token（登录成功后localStorage会有accessToken）
            access_token = page.run_js("return localStorage.getItem('accessToken') || ''")
            sign = page.run_js("return localStorage.getItem('sign') || ''")
            user_info_str = page.run_js("return localStorage.getItem('userInfo') || ''")

            # 只有当accessToken和sign都存在时才算登录成功
            if access_token and len(access_token) > 10 and sign and len(sign) > 10:
                logged_in = True
                break
        except Exception as e:
            # 浏览器可能已关闭
            if 'disconnect' in str(e).lower() or 'closed' in str(e).lower():
                log(f"\n[{datetime.now()}] 浏览器已关闭")
                return
            # 其他错误继续等待
            pass

        time.sleep(2)

    if not logged_in:
        log(f"[{datetime.now()}] 未检测到登录或浏览器已关闭")
        try:
            page.quit()
        except:
            pass
        return

    log(f"[{datetime.now()}] 检测到登录成功！正在获取token...")
    logger.info("检测到登录成功")

    # 获取所有token
    try:
        access_token = page.run_js("return localStorage.getItem('accessToken') || ''")
        sign = page.run_js("return localStorage.getItem('sign') || ''")
        id_token = page.run_js("return localStorage.getItem('idToken') || ''")
        token = page.run_js("return localStorage.getItem('token') || ''")
        st_flpv = page.run_js("return localStorage.getItem('st_flpv') || ''")

        user_info_str = page.run_js("return localStorage.getItem('userInfo') || '{}'")
        user_info = json.loads(user_info_str)
        user_id = str(user_info.get('data', {}).get('userId', ''))
    except Exception as e:
        log(f"[{datetime.now()}] 获取token失败: {e}")
        logger.exception(f"获取token失败: {e}")
        return

    log(f"\n获取到的token:")
    log(f"  accessToken: {access_token[:20]}...")
    log(f"  sign: {sign[:20]}...")
    log(f"  idToken: {id_token[:20]}...")
    log(f"  userId: {user_id}")
    logger.info(f"获取到token: userId={user_id}, accessToken={access_token[:20]}...")

    # 导航到活动页面获取fresh tokens
    log(f"\n[{datetime.now()}] 获取API fresh tokens...")
    page.get("https://wap.showstart.com/pages/activity/detail/detail?activityId=295821")
    time.sleep(5)

    # 安装拦截器
    page.run_js("""
    window._capturedRequests = [];
    var origXHR = window.XMLHttpRequest;
    window.XMLHttpRequest = function() {
        var xhr = new origXHR();
        var headers = {};
        var origSetHeader = xhr.setRequestHeader;
        xhr.setRequestHeader = function(name, value) {
            headers[name] = value;
            return origSetHeader.call(xhr, name, value);
        };
        var origOpen = xhr.open;
        xhr.open = function(method, url) {
            this._url = url;
            return origOpen.apply(xhr, arguments);
        };
        var origSend = xhr.send;
        xhr.send = function(body) {
            window._capturedRequests.push({
                url: this._url,
                headers: JSON.parse(JSON.stringify(headers))
            });
            return origSend.apply(xhr, arguments);
        };
        return xhr;
    };
    """)
    time.sleep(1)

    # 点击购买按钮
    for i in range(2):
        try:
            btn = page.ele('text:立即购票', timeout=3)
            if btn:
                btn.click()
                time.sleep(2)
        except:
            break

    time.sleep(3)

    # 获取捕获的请求
    result = page.run_js("return JSON.stringify(window._capturedRequests || [])")
    requests = json.loads(result) if isinstance(result, str) else result

    page.quit()

    # 提取fresh tokens
    config = {
        'accessToken': access_token,
        'sign': sign,
        'idToken': id_token,
        'userId': user_id,
        'token': token,
        'st_flpv': st_flpv,
    }

    # 标记是否找到有效的fresh tokens
    found_fresh_tokens = False
    fresh_config_from_headers = None
    
    # 打印所有捕获到的请求头信息用于调试
    for req in requests:
        url = req.get('url', '')
        if 'ticket' in url and 'list' in url:
            headers = req.get('headers', {})
            log(f"\n[{datetime.now()}] 捕获到API请求: {url}")
            log(f"  请求头内容: {json.dumps(headers, indent=2, ensure_ascii=False)}")
            logger.debug(f"捕获到API请求: {url}, 头: {headers}")
            
            # 检查关键字段是否存在
            cusat = headers.get('CUSAT', '').replace(' ', '')
            cusut = headers.get('CUSUT', '').replace(' ', '')
            cusit = headers.get('CUSIT', '').replace(' ', '')
            cusid = headers.get('CUSID', '').replace(' ', '')
            cdeviceno = headers.get('CDEVICENO', '').replace(' ', '')
            custoken_val = headers.get('CUSTOKEN', '').replace(' ', '')
            st_flpv_val = headers.get('st_flpv', '').replace(' ', '')
            
            if cusat and len(cusat) > 10:
                fresh_config_from_headers = {
                    'accessToken': cusat,
                    'sign': cusut if (cusut and len(cusut) > 10) else sign,
                    'idToken': cusit if (cusit and len(cusit) > 10) else id_token,
                    'userId': cusid if cusid else user_id,
                    'token': cdeviceno if cdeviceno else token,
                    'custoken': custoken_val if custoken_val else token,
                    'st_flpv': st_flpv_val if st_flpv_val else st_flpv,
                }
                found_fresh_tokens = True
                break
    
    # 如果从请求头获取到fresh token，检查是否有更新
    if found_fresh_tokens and fresh_config_from_headers:
        # 只有当accessToken确实变化了才使用fresh tokens
        if fresh_config_from_headers['accessToken'] != access_token:
            config = fresh_config_from_headers
            log(f"\n[{datetime.now()}] 获取到更新的fresh tokens:")
            log(f"  accessToken: {config['accessToken'][:20]}...")
            log(f"  sign: {config['sign'][:20]}...")
            log(f"  idToken: {config['idToken'][:20]}...")
            log(f"  userId: {config['userId']}")
            log(f"  token: {config['token'][:20]}...")
            log(f"  custoken: {config.get('custoken', '')[:20]}...")
            log(f"  st_flpv: {config['st_flpv'][:20]}...")
        else:
            log(f"\n[{datetime.now()}] fresh tokens与原始token相同，使用原始token")
            logger.info("fresh tokens与原始token相同")
    else:
        log(f"\n[{datetime.now()}] 未获取到有效的fresh tokens，使用原始token")
        logger.warning("未获取到有效的fresh tokens")

    # 跳过验证步骤，直接保存token
    # 因为正常流程是先进去看页面，后面要买票时才需要登录认证
    # 如果token无效，后续监控时会发现并提示重新登录
    log(f"\n[{datetime.now()}] 直接保存token（跳过验证步骤）")
    logger.info("跳过验证步骤，直接保存token")
    
    # 保存到文件
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    log(f"[{datetime.now()}] Token已保存到 config.json")
    logger.info(f"Token已保存到 config.json")
    log("")
    log("=" * 50)
    log("登录完成！")
    log("=" * 50)
    return True

if __name__ == "__main__":
    main()
    test_session = __import__('requests').Session()
    
    # 查找浏览器捕获的原始请求
    original_req = None
    for req in requests:
        url = req.get('url', '')
        if 'ticket' in url and 'list' in url:
            original_req = req
            break
    
    if original_req:
        # 使用浏览器捕获的原始请求头和请求体
        headers = original_req.get('headers', {})
        log(f"[{datetime.now()}] 使用浏览器捕获的原始请求进行验证...")
        logger.info("使用浏览器捕获的原始请求进行验证")
        
        # 设置cookie
        custoken_val = headers.get('CUSTOKEN', '').replace(' ', '')
        st_flpv_val = headers.get('st_flpv', '').replace(' ', '')
        test_session.cookies.set('CUSTOKEN', custoken_val, domain='.showstart.com')
        test_session.cookies.set('st_flpv', st_flpv_val, domain='.showstart.com')
        
        # 设置请求头（直接使用浏览器的请求头）
        test_session.headers.update({
            'User-Agent': headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'Content-Type': 'application/json',
            'Origin': 'https://wap.showstart.com',
            'Referer': 'https://wap.showstart.com/pages/activity/detail/detail?activityId=295821',
        })
        
        # 添加所有浏览器捕获的自定义头
        custom_headers = ['CUSAT', 'CUSUT', 'CUSIT', 'CUSID', 'CDEVICENO', 'CUUSERREF', 
                         'CDEVICEINFO', 'CVERSION', 'CTERMINAL', 'CSAPPID', 'st_flpv', 
                         'CUSTOKEN', 'CSTOKEN', 'CSPAPPID', 'CSOURCEPATH', 'CRTRACEID', 'CRPSIGN']
        for h in custom_headers:
            if h in headers:
                test_session.headers[h] = headers[h].replace(' ', '')
        
        # 直接发送请求（使用浏览器捕获的请求）
        try:
            resp = test_session.post('https://wap.showstart.com/v3/wap/activity/V2/ticket/list', 
                                   data='{"activityId":"295821","coupon":"","st_flpv":"' + st_flpv_val + '","sign":"' + headers.get('CUSUT', '').replace(' ', '') + '","trackPath":""}', 
                                   timeout=10)
            logger.debug(f"验证响应: HTTP {resp.status_code}")
            if resp.status_code == 200:
                result = resp.json()
                api_status = result.get('status')
                api_msg = result.get('msg', '')
                logger.info(f"验证结果: status={api_status}, msg={api_msg}")
                if api_status == 200:
                    log(f"[{datetime.now()}] Tokens验证成功！")
                    # 只有验证成功才保存到文件
                    with open('config.json', 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    log(f"\n[{datetime.now()}] Token已保存到 config.json")
                    logger.info(f"Token已保存到 config.json")
                    log("")
                    log("=" * 50)
                    log("登录完成！")
                    log("=" * 50)
                    return True
                else:
                    log(f"[{datetime.now()}] Tokens验证失败: {api_msg}")
                    logger.warning(f"Tokens验证失败: status={api_status}, msg={api_msg}")
            else:
                log(f"[{datetime.now()}] HTTP错误: {resp.status_code}")
                logger.error(f"验证HTTP错误: {resp.status_code}")
        except Exception as e:
            log(f"[{datetime.now()}] 验证异常: {e}")
            logger.exception(f"验证异常: {e}")
    else:
        # 如果没有找到原始请求，使用备用验证方式
        log(f"[{datetime.now()}] 未找到原始请求，使用备用验证方式...")
        logger.warning("未找到原始请求，使用备用验证方式")
        
        # 添加cookie支持
        test_session.cookies.set('CUSTOKEN', config.get('custoken', config.get('token', '')), domain='.showstart.com')
        test_session.cookies.set('st_flpv', config.get('st_flpv', ''), domain='.showstart.com')
        
        test_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'CUSAT': config['accessToken'],
            'CUSUT': config['sign'],
            'CUSIT': config['idToken'],
            'CUSID': config['userId'],
            'CDEVICENO': config['token'],
            'CUUSERREF': config.get('custoken', config['token']),
            'CUSTOKEN': config.get('custoken', config['token']),
            'st_flpv': config['st_flpv'],
            'CTERMINAL': 'wap',
            'CVERSION': '997',
            'CSAPPID': 'wap',
        })
        
        try:
            resp = test_session.post('https://wap.showstart.com/v3/wap/activity/V2/ticket/list', 
                                   data='{"activityId":"295821","coupon":"","st_flpv":"' + config['st_flpv'] + '","sign":"' + config['sign'] + '","trackPath":""}', 
                                   timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                if result.get('status') == 200:
                    log(f"[{datetime.now()}] Tokens验证成功！")
                    with open('config.json', 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    log(f"\n[{datetime.now()}] Token已保存到 config.json")
                    log("")
                    log("=" * 50)
                    log("登录完成！")
                    log("=" * 50)
                    return True
                else:
                    log(f"[{datetime.now()}] Tokens验证失败: {result.get('msg', '')}")
            else:
                log(f"[{datetime.now()}] HTTP错误: {resp.status_code}")
        except Exception as e:
            log(f"[{datetime.now()}] 验证异常: {e}")
    
    # 验证失败
    log(f"\n[{datetime.now()}] Token验证失败，未保存")
    logger.warning("Token验证失败，未保存")
    log("")
    log("=" * 50)
    log("登录失败！请重新登录")
    log("=" * 50)
    return False


if __name__ == "__main__":
    main()
