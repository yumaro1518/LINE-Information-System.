import requests
from bs4 import BeautifulSoup
import time

# LINE Notifyのトークン
LINE_NOTIFY_TOKEN = '2Xmk5BTy4dlsxQBjRlVRUUXCQPZqDlN6BYE9iV3PSNo'

# 監視対象のウェブサイトのURLリスト
WEBSITES = [
    'https://kamigame.jp/bluearchive/index.html',
    'https://gamewith.jp/nikke/',
    'https://akiba-souken.com/article/anime/',
    'https://bluearchive.jp/news/newsJump',
    'https://1kuji.com/',
    'https://pjsekai.sega.jp/',
    'https://it-chiba.com/nyushi/enrollment/',
    'https://www.cit-s.com/textbook/',
]

# 前回のページの内容を保存するための辞書
last_page_content = {url: '' for url in WEBSITES}

def send_line_notify(message):
    """
    LINE Notify APIを使用して通知を送信する関数
    """
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN}
    payload = {'message': message}
    requests.post(url, headers=headers, data=payload)

def check_web_page_for_updates(url):
    global last_page_content
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
        if page_content != last_page_content[url]:
            # ページの内容が変更された場合に通知を送る
            notification_message = f'{url} が更新されました！\n詳しくはこちらからご確認ください：{url}'
            send_line_notify(notification_message)
            last_page_content[url] = page_content
    else:
        print("Error:", response.status_code)

def main():
    while True:
        for website_url in WEBSITES:
            check_web_page_for_updates(website_url)
        # 任意の間隔でウェブサイトをチェックするための待機時間
        time.sleep(600)

if __name__ == "__main__":
    main()
