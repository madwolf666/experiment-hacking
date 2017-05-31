import socks
import socket
#import urllib
import requests

class Tor:
    def __init__(self):
        #プロキシの設定
        proxy_ip = '127.0.0.1'
        proxy_port = 9050
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_ip, proxy_port)
        socket.socket = socks.socksocket
        #urllib.socket.socket = socks.socksocket

    def get_ip(self):
        session = requests.Session()
        return session.get('https://api.ipify.org/').text

if __name__ == "__main__":
    Tor = Tor()
    ip = Tor.get_ip()
    print(ip)
