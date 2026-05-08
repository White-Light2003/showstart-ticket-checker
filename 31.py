import requests
import time

BOT_TOKEN = ""
CHAT_ID = ""

URL = "https://xcx001.antank.cn/thvendor/member/show/listBydate.xhtml"

HEADERS = {
    "ksmpid": "",
    "content-type": "application/x-www-form-urlencoded",
    "ksclient": "",
    "mpsessid": "",
    "ksversion": "",
    "version": "1.0.12",
    "cmpappkey": "qtxd",
    "User-Agent": "Mozilla/5.0"
}

DATA = {
    "programId": "9113",
    "action": "commit",
    "date": "2026-06-21",
    "gradeBuy": "memberCard"
}

CHECK_INTERVAL = 10  # 秒

last_has_ticket = False


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })


def check_ticket():
    try:
        r = requests.post(URL, headers=HEADERS, data=DATA, timeout=10)
        j = r.json()

        ticket_types = j["data"][0]["ticketTypes"]

        available = []
        for t in ticket_types:
            if t["availableNum"] > 0:
                available.append(f'{t["cnName"]} 剩余 {t["availableNum"]}')

        return available

    except Exception as e:
        print("error:", e)
        return None


while True:
    result = check_ticket()

    if result is not None:
        has_ticket = len(result) > 0

        if has_ticket and not last_has_ticket:
            msg = "🎫 有票了！\n" + "\n".join(result)
            send_telegram(msg)
            print(msg, flush=True)
        else:
            print("无票了，继续监控...", flush=True)

        last_has_ticket = has_ticket

    time.sleep(CHECK_INTERVAL)
