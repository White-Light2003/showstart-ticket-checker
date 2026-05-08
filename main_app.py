"""
秀动回流票监控 - 主程序
引导用户一步步完成登录、配置、监控
"""
import sys
import os
import json
import time
import logging
from datetime import datetime


def get_base_path():
    """获取基础路径（支持打包后的exe）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


# 日志文件路径
BASE_PATH = get_base_path()
LOG_DIR = os.path.join(BASE_PATH, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f'main_{datetime.now().strftime("%Y%m%d")}.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
    ]
)
logger = logging.getLogger('xiudong-main')


def log(msg):
    """打印日志，同时写入文件"""
    logger.info(msg)
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode('utf-8', errors='replace').decode('ascii', errors='replace'), flush=True)


def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """打印横幅"""
    log("=" * 50)
    log("        秀动回流票监控 v2.0")
    log("=" * 50)
    log("  轻量级API监控 | 自动Token刷新")
    log("=" * 50)
    log("")


def print_menu(title, options):
    """打印菜单"""
    log(f"  {title}")
    log("-" * 40)
    for key, desc in options:
        log(f"  {key}. {desc}")
    log("-" * 40)
    log("")


def get_config_path():
    """获取配置文件路径"""
    return os.path.join(get_base_path(), 'config.json')


def load_config():
    """加载配置"""
    config_path = get_config_path()
    logger.info(f"加载配置: {config_path}")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            if config.get('accessToken') and config.get('sign'):
                logger.info(f"配置加载成功: userId={config.get('userId')}, accessToken={config['accessToken'][:20]}...")
                return config
            else:
                logger.warning("配置缺少必要字段: accessToken或sign为空")
        except Exception as e:
            logger.exception(f"配置加载失败: {e}")
    else:
        logger.info("配置文件不存在")
    return None


def save_config(config):
    """保存配置"""
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def step_login():
    """步骤：登录获取Token"""
    log("")
    log("=" * 50)
    log("  步骤 1：登录获取Token")
    log("=" * 50)
    log("")
    log("  接下来会自动打开浏览器，请在浏览器中登录秀动账号。")
    log("  登录成功后页面会自动跳转，然后关闭浏览器即可。")
    log("")
    input("  按 Enter 键开始登录...")
    log("")

    logger.info("开始登录流程")
    try:
        from login_helper import main as login_main
        login_success = login_main()
        if not login_success:
            log(f"  登录失败: 请重新登录")
            logger.error("登录失败")
    except Exception as e:
        log(f"  登录失败: {e}")
        logger.exception("登录异常")
        log("  请确保已安装 Chrome 浏览器")
        logger.exception(f"登录异常: {e}")
        return False

    # 检查是否成功
    config = load_config()
    if config:
        log("")
        log("  登录成功！Token 已保存。")
        logger.info(f"登录成功: userId={config.get('userId')}")
        return True
    else:
        log("")
        log("  登录未完成，请重试。")
        logger.warning("登录后未找到有效配置")
        return False


def step_check_config():
    """步骤：检查配置"""
    config = load_config()
    if not config:
        return None

    log("")
    log("  已检测到登录信息:")
    user_id = config.get('userId', '未知')
    log(f"  用户ID: {user_id}")
    log(f"  Token: {config['accessToken'][:20]}...")
    log("")
    return config


def step_input_activity():
    """步骤：输入演出ID"""
    log("")
    log("=" * 50)
    log("  步骤 2：设置监控目标")
    log("=" * 50)
    log("")
    log("  请输入要监控的演出ID。")
    log("  演出ID可以从秀动APP或网页的演出链接中获取。")
    log("  例如链接: https://wap.showstart.com/pages/activity/detail/detail?activityId=295821")
    log("  其中的 295821 就是演出ID。")
    log("")

    while True:
        activity_id = input("  请输入演出ID (直接回车使用默认 295821): ").strip()
        if not activity_id:
            activity_id = '295821'
        if activity_id.isdigit():
            return activity_id
        log("  请输入有效的数字ID！")
        log("")


def step_input_interval():
    """步骤：输入检查间隔"""
    log("")
    log("  设置检查间隔（秒）。")
    log("  建议 5-30 秒，间隔太短可能被限流。")
    log("")

    while True:
        interval = input("  请输入检查间隔 (直接回车默认30秒): ").strip()
        if not interval:
            return 30
        if interval.isdigit() and int(interval) >= 3:
            return int(interval)
        log("  请输入 >= 3 的数字！")
        log("")


def step_start_monitor(config, activity_id, interval):
    """步骤：开始监控"""
    log("")
    log("=" * 50)
    log("  开始监控")
    log("=" * 50)
    log(f"  演出ID: {activity_id}")
    log(f"  检查间隔: {interval}秒")
    log(f"  Token: {config['accessToken'][:20]}...")
    log("=" * 50)
    log("")
    log("  按 Ctrl+C 停止监控")
    log("")

    logger.info(f"启动监控: activityId={activity_id}, interval={interval}")
    logger.info(f"accessToken={config['accessToken'][:20]}..., userId={config.get('userId')}")

    from direct_api_monitor import DirectAPIMonitor

    monitor = DirectAPIMonitor(config)

    def on_change(msg):
        """检测到变化时的回调"""
        log("")
        log("!" * 50)
        log(f"  [!] {msg}")
        log("!" * 50)
        log("")
        logger.info(f"检测到变化: {msg}")

    try:
        monitor.monitor_loop(activity_id, interval, callback=on_change)
    except KeyboardInterrupt:
        log("")
        log("  监控已停止")
        logger.info("用户停止监控")
    except Exception as e:
        log(f"  监控异常: {e}")
        logger.exception(f"监控异常: {e}")


def flow_monitor(config):
    """监控流程"""
    activity_id = step_input_activity()
    interval = step_input_interval()
    step_start_monitor(config, activity_id, interval)


def flow_login_and_monitor():
    """先登录再监控"""
    if step_login():
        config = load_config()
        if config:
            flow_monitor(config)
    else:
        log("  登录失败，无法开始监控。")


def main():
    """主流程"""
    base_path = get_base_path()
    os.chdir(base_path)

    while True:
        clear_screen()
        print_banner()

        # 检查配置
        config = step_check_config()

        if config:
            # 已登录状态
            print_menu("请选择操作", [
                ("1", "开始监控回流票"),
                ("2", "重新登录（刷新Token）"),
                ("3", "退出程序"),
            ])

            choice = input("  请输入选项 (1/2/3): ").strip()

            if choice == '1':
                flow_monitor(config)
                input("\n  按 Enter 键返回主菜单...")
            elif choice == '2':
                step_login()
                input("\n  按 Enter 键返回主菜单...")
            elif choice == '3':
                log("\n  感谢使用，再见！")
                break
            else:
                log("\n  无效选项，请重新输入")
                time.sleep(1)
        else:
            # 未登录状态
            print_menu("欢迎使用", [
                ("1", "登录秀动账号（首次使用）"),
                ("2", "退出程序"),
            ])

            choice = input("  请输入选项 (1/2): ").strip()

            if choice == '1':
                flow_login_and_monitor()
                input("\n  按 Enter 键返回主菜单...")
            elif choice == '2':
                log("\n  感谢使用，再见！")
                break
            else:
                log("\n  无效选项，请重新输入")
                time.sleep(1)


if __name__ == '__main__':
    main()
