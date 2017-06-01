from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from json import load
import socket,socks,requests
import random,sys,csv,time
import os

#セッションを生成する
SESSION = requests.Session()
RESPONSE = ""
AUTH_TOKEN = ""
PATH = "r00tapple.png"

USERNAME = ""
PASSWORD = ""

class changeimage:
    global SESSION, RESPONSE,AUTH_TOKEN

    login = {
        "session[username_or_email]": USERNAME,
        "session[password]": PASSWORD,
        "remember_me": "1",
        "return_to_ssl": "true",
        "scribe_log": "",
        "redirect_after_login": "/",
        "authenticity_token": ""
    }


    image = {
        "authenticity_token": "",
        "height": "512",
        "mediaId": "",
        "offsetLeft": "0",
        "offsetTop": "0",
        "page_context": "me",
        "scribeElement": "upload",
        "section_context": "profile",
        "uploadType": "avatar",
        "width": "512"
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, sdch, br",
        "accept-language": "ja,en-US;q=0.8,en;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0",
        "origin": "https://twitter.com",
        "referer": "https://twitter.com/",
        "x-requested-width": "XMLHttpRequest"
    }

    imageheaders = {
        "User-Agent": "Mozilla/5.0",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "origin": "https://twitter.com",
        "authority": "upload.twitter.com",
        "referer": "https://twitter.com/r00tapple",
        "content-length": "55096"
    }

    try:
        # GETリクエストでHTML取得
        RESPONSE = SESSION.get('https://twitter.com/', headers=headers, allow_redirects=False)
        # lxmlを指定する
        soup = BeautifulSoup(RESPONSE.text, "lxml")
        # HTMLからauthenticity_tokenを取得
        AUTH_TOKEN = soup.find(attrs={'name': 'authenticity_token'}).get('value')
        login['authenticity_token'] = AUTH_TOKEN
        image['authenticity_token'] = AUTH_TOKEN
        RESPONSE = SESSION.post('https://twitter.com/sessions', headers=headers, data=login, allow_redirects=False)
    except Exception as e:
        print("[+] ログインに失敗しました")
        sys.exit()

    imageids = SESSION.post('https:upload.twitter.com/1/media/upload.json?command=INIT&total_bytes=' + str(os.path.getsize(PATH)) +
                            "&media_type=image%2Fjpeg&media_category=tweet_image",
                            headers=headers,
                            coookies=RESPONSE.cookies
                            )

    imageids = imageids.json()
    imageId = imageids['media_id']
    image['mediaId'] = imageId
    files = {'media': open('r00tapple.png', 'rb')}

    RESPONSE = SESSION.post('https:upload.twitter.com/1/media/upload.json?command=APPEND&media_id=' + str(imageId) +
                            "&segment_index=0",
                            files=files,
                            headers=imageheaders,
                            coookies=RESPONSE.cookies
                            )

    RESPONSE = SESSION.post('https:upload.twitter.com/1/media/upload.json?command=FINALIZE&media_id=' + str(imageId),
                            files=files,
                            headers=imageheaders,
                            coookies=RESPONSE.cookies
                            )

    RESPONSE = SESSION.post('https:upload.twitter.com/1/profiles/update_profile_image',
                            data=image,
                            allow_redirects=False,
                            headers=headers,
                            coookies=RESPONSE.cookies
                            )
    print("[+] プロフィール画像更新完了 HTTP status: " + str(RESPONSE.status_code) + RESPONSE.text)

if __name__ == "__main__":
    changeimage()
