from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import sys


class TwitterLogin:
    def __init__(self):
        # ログインするユーザのアカウント名
        self.username = "chappyharry"
        # ログインするユーザのパスワード
        self.password = "harry666"

    def tweet(self):
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

        # Twitterのログイン時に必要な引数
        payload = {
            "session[username_or_email]": "",
            "session[password]": "",
            "remember_me": "1",
            "return_to_ssl": "true",
            "scribe_log": "",
            "redirect_after_login": "/"
        }

        #ツイートPOST送信のリクエスト
        tweet = {
            "authenticity_token": "",
            "is_permalink_page": "false",
            "place_id": "",
            "status": "pythonからのツイート試験２",
            "tagged_users": ""
        }

        #ツイートPOST送信のリクエスト
        destroy = {
            "_method": "DELETE",
            "authenticity_token": "",
            "id": ""
        }

        # authenticity_token値の取得
        try:
            # GETリクエストでHTML取得
            response = session.get('https://twitter.com/', headers=headers, allow_redirects=False)
            # lxmlを指定する
            soup = BeautifulSoup(response.text, "lxml")
            # HTMLからauthenticity_tokenを取得
            auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
        except ConnectionError:
            print("[*] Twitterへ接続できません")
            sys.exit()

        # authenticity_tokenをpayloadに設定
        payload['authenticity_token'] = auth_token
        # twitterのユーザIDをpayloadに設定
        payload['session[username_or_email]'] = self.username
        # twitterのパスワードをpayloadに設定
        payload['session[password]'] = self.password

        # twitterへログイン
        try:
            login = session.post('https://twitter.com/sessions', headers=headers, data=payload, allow_redirects=False)
            if login.status_code == 302:
                print("[+] ログイン完了　HTTP status: " + str(login.status_code))
            else:
                print("[+] ログイン失敗　HTTP status: " + str(login.status_code))
        except:
            print("[+] ログイン中に通信エラー")

        #ツイートを投稿
        try:
            tweet = session.post('https://twitter.com/i/tweet/create', headers=headers, cookies=login.cookies, data=tweet, allow_redirects=False)
            if tweet.status_code == 200:
                print("[+] ツイート完了　HTTP status: " + str(login.status_code))
            elif tweet.status_code == 403:
                response = session.get('https://twitter.com/r00tapple', headers=headers, allow_redirects=False)
                soup = BeautifulSoup(response.text, "lxml")
                destroy['id'] = soup.find('div', attrs={'class': 'stream-container'}).get('data-max-position')
                destroy = session.post('https://twitter.com/i/tweet/destroy', headers=headers, cookies=login.cookies, data=destroy, allow_redirects=False)
                if destroy.status_code == 200:
                    print("[+] 重複ツイート削除成功　HTTP status: " + str(login.status_code))
                else:
                    print("[+] 重複ツイート削除失敗　HTTP status: " + str(login.status_code))
            else:
                print("[+] ツイート失敗　HTTP status: " + str(login.status_code))
        except:
            print("[+] ツイート中に通信エラー")

if __name__ == "__main__":
    TwiLogin = TwitterLogin()
    TwiLogin.tweet()
