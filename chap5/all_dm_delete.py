from bs4 import BeautifulSoup
import json
import requests
import sys

#セッションを生成する
SESSION = requests.Session()
RESPONSE = ""
AUTH_TOKEN = ""
USERNAME = ""
PASSWORD = ""
DM_LINK = "https://twitter.com/messages/with/conversation?id=459072132-459072132&last_note_ts=3"

def dm_delete(self):
    global SESSION,RESPONSE,AUTH_TOKEN,JOB_LIST,BOTS_ALIVE,COMMANDS

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, sdch, br",
        "accept-language": "ja,en-US;q=0.8,en;q=0.6",
        "User-Agent": "Mozilla/5.0",
        "referer": "https://twitter.com/",
        "x-requested-with": "XMLHttpRequest"
    }

    delete = {
        "authenticity_token": AUTH_TOKEN,
        "conversation_id": "459072132-4590272132",
        "cursor": "GRwmhICpjZzZjYsVFoiAq7nY75OLFSUkAAA",
        "id": ""
    }

    try:
        delete['authenticity_token'] = AUTH_TOKEN
        #r00tappleのダイレクトメッセージ
        dm = SESSION.get(DM_LINK, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
    except:
        print("[+]ダイレクトメッセージの取得失敗")
        #再ログイン
        login()
        #処理を中断して終了
        sys.exit()

    #DMのJSONを取得
    dm = dm.json()
    #itemsを取得
    items = dm['items']
    #各種変数を更新
    del_count = 0
    for line in dm['items']:
        try:
            soup = BeautifulSoup(items[line], "lxml")
            #ダイレクトメッセージのIDを取得
            delete['id'] = soup.find('div', attrs={'class':'DirectMessage'}).get('data-item-id')
            RESPONSE = SESSION.post("https://twitter.com/i/direct_messages/destroy", data=delete, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
            del_count += 1
        except:
            pass

    if (del_count == 0):
        print("[+]" + str(del_count) + "件の命令を削除しました")
        sys.exit()
    else:
        print("[+]" + str(del_count) + "件の命令を削除しました")

def login(self):
    global SESSION,RESPONSE,AUTH_TOKEN

    headers = {
        "User-Agent": "Mozilla/5.0",
        "referer": "https://twitter.com/"
    }

    payload = {
        "session[username_or_email]": USERNAME,
        "session[password]": PASSWORD,
        "remember_me": "1",
        "return_to_ssl": "true",
        "scribe_log": "",
        "redirect_after_login": "/",
        "authenticity_token": ""
    }

    try:
        RESPONSE = SESSION.post("https://twitter.com/", allow_redirects=False, headers=headers)
        soup = BeautifulSoup(RESPONSE.text, "lxml")
        AUTH_TOKEN = soup.find(attrs={'name': 'authenticity_token'}).get('value')
        payload['authenticity_token'] = AUTH_TOKEN
        #ログイン
        RESPONSE = SESSION.post("https://twitter.com/sessions", data=payload, allow_redirects=False, headers=headers)

    except Exception as e:
        print("[+]ログインに失敗しました")

if __name__ == "__main__":
    #ログイン
    login()
    while(1):
        #起動時に送受信を行う事でデータを取得更新する
        dm_delete()
