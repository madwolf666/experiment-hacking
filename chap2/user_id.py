from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import sys


class TwitterUserID:
    def __init__(self):
        self.user_id = ""

    def userid(self):
        # セッションを生成する
        session = requests.Session()

        # Twitterに送信するヘッダ情報
        headers = {
            "User-Agent": "Mozilla/5.0",
            "accept": "text/html,application/xhtml+xml,application/xml",
            "accept-language": "ja,en-US;q=0.8,en;q=0.6",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://twitter.com",
            "referer": "https://twitter.com/",
            "upgrade-insecure-requests": "1"
        }

        # user_idの取得
        try:
            # GETリクエストでHTML取得
            url = 'https://twitter.com/' + input('user_id値を調べたいユーザ：')
            response = session.get(url, headers=headers, allow_redirects=False)
            # lxmlを指定する
            soup = BeautifulSoup(response.text, "lxml")
            self.user_id = soup.find('div', attrs={'class': 'ProfileNav'}).get('data-user-id')
        except:
            print("[+] Twitter中に通信エラー HTTP status: " + str(response.status_code))
        return self.user_id

if __name__ == "__main__":
    TwiUserID = TwitterUserID()
    print("[+]user_id: " + TwiUserID.userid())
