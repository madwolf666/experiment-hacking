from bs4 import BeautifulSoup
import requests

#セッションを生成する
session = requests.Session()

#Twitterに送信するヘッダ情報
headers = {
    "User-Agent": "Mozilla/5.0",
    "accept": "text/html,application/xhtml+xml,application/xml",
    "accept-language": "ja,en-US;q=0.8,en;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://twitter.com",
    "referer": "https://twitter.com/",
    "upgrade-insecure-requests": "1"
}

#GETリクエストでHTML取得
response = session.get('https://twitter.com/', headers=headers, allow_redirects=True)
#lxmlを指定する
soup = BeautifulSoup(response.text, "lxml")
#HTMLからauthenticity_tokenを取得
auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')

#表示
print("authenticity_token: " + auth_token)
