"""
Token刷新器 - 通过浏览器获取fresh tokens
"""
import time
import json
import sys
import os
import logging
from datetime import datetime

# 日志配置（复用主程序的日志目录）
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f'refresh_{datetime.now().strftime("%Y%m%d")}.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
    ]
)
logger = logging.getLogger('xiudong-refresh')


def log(msg):
    """打印日志，同时写入文件"""
    logger.info(msg)
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode('utf-8', errors='replace').decode('ascii', errors='replace'), flush=True)


def refresh_tokens(config, activity_id='295821'):
    """
    通过浏览器刷新token
    返回更新后的config，如果失败返回None
    """
    logger.info(f"开始刷新token, activityId={activity_id}")
    logger.info(f"当前accessToken: {config.get('accessToken', '')[:20]}...")
    try:
        from DrissionPage import ChromiumOptions, ChromiumPage
        
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
        
        page = ChromiumPage(co)
        logger.info("浏览器启动成功")

        # 设置token到localStorage
        page.get('https://wap.showstart.com')
        time.sleep(2)

        for key, val in config.items():
            if key != 'userId':
                page.run_js(f"localStorage.setItem('{key}', '{val}')")

        user_info = json.dumps({
            'type': 'object',
            'data': {
                'st_flpv': config.get('st_flpv', ''),
                'userId': int(config['userId']),
                'userType': 1,
                'userName': 'monitor',
                'sign': config.get('sign', ''),
                'idtoken': config.get('idToken', ''),
            }
        }, ensure_ascii=False)
        page.run_js(f"localStorage.setItem('userInfo', '{user_info}')")
        time.sleep(1)

        # 导航到活动页面
        log(f"[{datetime.now()}] 导航到活动页面...")
        page.get(f'https://wap.showstart.com/pages/activity/detail/detail?activityId={activity_id}')
        time.sleep(5)

        # 安装拦截器捕获请求头（获取fresh tokens的关键）
        page.run_js("""
        window._capturedRequests = [];
        
        // 拦截XMLHttpRequest请求头
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
        
        // 拦截fetch请求头
        var origFetch = window.fetch;
        window.fetch = function(input, init) {
            var url = typeof input === 'string' ? input : input.url || '';
            var headers = {};
            if (init && init.headers) {
                for (var pair of init.headers.entries()) {
                    headers[pair[0]] = pair[1];
                }
            }
            window._capturedRequests.push({url: url, headers: headers});
            return origFetch.apply(this, arguments);
        };
        """)
        time.sleep(0.5)

        # 点击按钮触发API
        log(f"[{datetime.now()}] 点击购买按钮...")
        for i in range(2):
            try:
                btn = page.ele('text:立即购票', timeout=3)
                if btn:
                    btn.click()
                    time.sleep(1.5)
            except:
                break

        time.sleep(3)

        # 获取捕获的请求（提取fresh tokens）
        result = page.run_js("return JSON.stringify(window._capturedRequests || [])")
        requests = json.loads(result) if isinstance(result, str) else result

        log(f"[{datetime.now()}] 捕获到 {len(requests)} 个API请求")
        logger.info(f"捕获到 {len(requests)} 个API请求")

        # 从请求头中提取fresh tokens
        fresh_config = None
        for req in requests:
            url = req.get('url', '')
            if 'ticket' in url and 'list' in url:
                headers = req.get('headers', {})
                # 从请求头中提取fresh tokens（服务器会在响应中更新这些值）
                fresh_config = {
                    'accessToken': headers.get('CUSAT', '').replace(' ', ''),
                    'sign': headers.get('CUSUT', '').replace(' ', ''),
                    'idToken': headers.get('CUSIT', '').replace(' ', ''),
                    'userId': headers.get('CUSID', config.get('userId', '')).replace(' ', ''),
                    'token': headers.get('CDEVICENO', config.get('token', '')).replace(' ', ''),
                    'st_flpv': headers.get('st_flpv', config.get('st_flpv', '')).replace(' ', ''),
                }
                logger.info(f"从请求头提取fresh tokens: accessToken={fresh_config['accessToken'][:20]}...")
                break

        if not fresh_config or not fresh_config['accessToken']:
            log(f"[{datetime.now()}] 未提取到有效的fresh tokens")
            logger.warning("未提取到有效的fresh tokens")
            page.quit()
            return None

        # 检查token是否有变化
        if fresh_config['accessToken'] == config.get('accessToken'):
            logger.warning("token未变化，可能刷新失败")

        # 验证tokens是否有效
        log(f"[{datetime.now()}] 验证新tokens...")
        test_result = test_tokens(fresh_config, activity_id)
        
        if not test_result:
            # 从请求头提取的可能是旧token，尝试从localStorage重新读取
            log(f"[{datetime.now()}] 请求头token验证失败，尝试从localStorage读取...")
            logger.info("请求头token验证失败，尝试从localStorage读取")
            
            # 等待页面更新localStorage
            time.sleep(2)
            
            # 从localStorage读取最新的token
            ls_tokens = page.run_js("""
                return JSON.stringify({
                    accessToken: localStorage.getItem('accessToken') || '',
                    sign: localStorage.getItem('sign') || '',
                    idToken: localStorage.getItem('idToken') || '',
                    token: localStorage.getItem('token') || '',
                    st_flpv: localStorage.getItem('st_flpv') || ''
                });
            """)
            ls_fresh = json.loads(ls_tokens) if isinstance(ls_tokens, str) else ls_tokens
            
            # 更新fresh_config
            if ls_fresh.get('accessToken'):
                fresh_config['accessToken'] = ls_fresh['accessToken']
                fresh_config['sign'] = ls_fresh['sign']
                fresh_config['idToken'] = ls_fresh['idToken']
                if ls_fresh.get('token'):
                    fresh_config['token'] = ls_fresh['token']
                if ls_fresh.get('st_flpv'):
                    fresh_config['st_flpv'] = ls_fresh['st_flpv']
                
                logger.info(f"从localStorage读取新token: accessToken={fresh_config['accessToken'][:20]}...")
                
                # 再次验证
                log(f"[{datetime.now()}] 再次验证localStorage中的token...")
                test_result = test_tokens(fresh_config, activity_id)
        
        if test_result:
            log(f"[{datetime.now()}] Token验证成功")
            logger.info("Token验证成功")
        else:
            log(f"[{datetime.now()}] Token验证失败，可能需要重新登录")
            logger.warning("Token验证失败")
            page.quit()
            return None

        page.quit()

        log(f"[{datetime.now()}] Token刷新成功")
        logger.info("Token刷新成功")
        return fresh_config

    except Exception as e:
        log(f"[{datetime.now()}] Token刷新失败: {e}")
        logger.exception(f"Token刷新异常: {e}")
        return None


def test_tokens(config, activity_id):
    """测试tokens是否有效"""
    import requests
    import hashlib
    import random

    url_path = '/wap/activity/V2/ticket/list'
    full_url = 'https://wap.showstart.com/v3' + url_path

    data = {
        "activityId": str(activity_id),
        "coupon": "",
        "st_flpv": config['st_flpv'],
        "sign": config['sign'],
        "trackPath": ""
    }
    body_str = json.dumps(data, separators=(',', ':'))

    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    crtraceid = ''.join(random.choice(chars) for _ in range(32)) + str(int(time.time() * 1000))
    R = (config['accessToken'] + config['sign'] + config['idToken'] +
         config['userId'] + 'wap' + config['token'] + body_str + url_path + '997' + 'wap' + crtraceid)
    crpsign = hashlib.md5(R.encode('utf-8')).hexdigest()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/json',
        'CTERMINAL': 'wap',
        'CSAPPID': 'wap',
        'CVERSION': '997',
        'CUSAT': config['accessToken'],
        'CUSUT': config['sign'],
        'CUSIT': config['idToken'],
        'CUSID': config['userId'],
        'CDEVICENO': config['token'],
        'st_flpv': config['st_flpv'],
        'CRPSIGN': crpsign,
        'CRTRACEID': crtraceid,
    }

    try:
        resp = requests.post(full_url, data=body_str, headers=headers, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            return result.get('status') == 200
    except Exception as e:
        logger.error(f"Token验证异常: {e}")
    
    return False


if __name__ == '__main__':
    import os

    # 读取配置
    config = None
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

    if not config:
        print("未找到config.json，请先运行登录")
        exit(1)

    log(f"[{datetime.now()}] 刷新token...")
    log(f"  原accessToken: {config['accessToken'][:30]}...")

    updated = refresh_tokens(config)

    if updated:
        log(f"[{datetime.now()}] 刷新成功!")
        log(f"  新accessToken: {updated['accessToken'][:30]}...")

        # 保存到config.json
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(updated, f, indent=2, ensure_ascii=False)

        print("已保存到config.json")
    else:
        log(f"[{datetime.now()}] 刷新失败")
