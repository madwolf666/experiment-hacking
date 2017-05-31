from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from json import load
import socket,socks,requests
import random,sys,csv,time

class TwitterCreateAccount:
    def __init__(self):
        #プロキシの設定
        proxy_ip = '127.0.0.1'
        proxy_port = 9050
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_ip, proxy_port)
        socket.socket = socks.socksocket
        self.screename = ""

    def getScreenName(self):
        return self.screename

    def mail(self):
        source_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
        username = "r00t" + "".join([random.choice(source_str) for x in range(8)])
        domain = "r00t" + "".join([random.choice(source_str) for x in range(8)])
        mail = username + "@" + domain + ".com"
        self.screename = username
        return mail

    def main(self):
        payload = {
            "authenticity_token": "",
            "signup_metrics": "",
            "m_metrics": "",
            "d_metrics": "",
            "user[name]": "",
            "user[email]": "",
            "user[user_password]": "Passw0rd",
            "asked_cookie_personalization_setting": "1",
            "ad_ref": "",
            "user[discoverable_by_email]": "1",
            "asked_discoverable_by_email": "1",
            "user[discoverable_by_mobile_phone]": "1",
            "asked_discoverable_by_mobile_phone": "1",
        }

        #ツイートPOST送信のリクエスト
        tweet = {
            "authenticity_token": "",
            "is_permalink_page": "false",
            "place_id": "",
            "status": "#r00tapple New foooooo!!!!!!",
            "tagged_users": "",
        }

        follow = {
            "authenticity_token": "",
            "challenges_passed": "false",
            "handles_challenges": "1",
            "user_id": "459072132",
        }

        fav = {
            "authenticity_token": "",
            "id": "682695260602929153",
            "tweet_stat_count": "0",
        }

        retweet = {
            "authenticity_token": "",
            "id": "682695260602929153",
            "tweet_stat_count": "0",
        }

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

        # 新規アカウント生成
        try:
            # authenticity_tokenをpayloadに設定
            payload['authenticity_token'] = auth_token
            payload['user[email]'] = self.mail()
            payload['user[name]'] = self.getScreenName()

            response = session.post('https://twitter.com/account/create', headers=headers, data=payload, allow_redirects=False)
            print("[+] 新規アカウント生成完了　HTTP status: " + str(response.status_code))
        except:
            print("[+] 新規アカウント生成失敗　HTTP status: " + str(response.status_code))

        #ツイートを投稿
        try:
            print("========================================")
            twitter_username = payload['user[name]']
            url = "https://twitter.com/" + payload['user[name]']
            print("[+] authenticityトークン......" + payload['authenticity_token'])
            print("[+] タイムラインURL......" + url)
            print("[+] アカウントメールアドレス......" + payload['user[email]'])
            print("[+] アカウントパスワード......" + payload['user[user_password]'])
            print("========================================")
        except:
            print("[+] 新規アカウント生成失敗")
            sys.exit()

        if response.status_code == 302:
            try:
                try:
                    response = session.get(url, headers=headers, allow_redirects=False)
                    print("[+] " + url + "に接続OK　HTTP status: " + str(response.status_code))
                except:
                    print("[+] " + url + "に接続できず　HTTP status: " + str(response.status_code))

                if response.status_code != 200:
                    print("[+] このアカウントを使用するには携帯電話認証が必要")
                    sys.exit()
                elif response.status_code == 200:
                    print("[+] 正常にアカウントが作成されました")
                    try:
                        follow['authenticity_token'] = auth_token
                        tweet['authenticity_token'] = auth_token
                        fav['authenticity_token'] = auth_token
                        retweet['authenticity_token'] = auth_token
                        response = session.post('https://twitter.com/i/tweet/create', headers=headers, data=tweet, allow_redirects=False, cookies=response.cookies)
                        print("[+] ツイート完了　HTTP status: " + str(response.status_code))
                        response = session.post('https://twitter.com/i/tweet/retweet', headers=headers, data=retweet, allow_redirects=False, cookies=response.cookies)
                        print("[+] リツイート完了　HTTP status: " + str(response.status_code))
                    except:
                        print("[+] フォロー失敗")
                    finally:
                        sys.exit()
            except ConnectionError:
                print("[+] " + url + "接続エラー")
                sys.exit()
            finally:
                return

        else:
            print("[+] ツイート失敗　HTTP status: " + str(response.status_code))

if __name__ == "__main__":
    TwiACC = TwitterCreateAccount()
    start = time.time()
    TwiACC.mail()
    elapsed_time = time.time() - start
    print("[+] 一連の処理時間は： {0}".format(elapsed_time) + "秒")
