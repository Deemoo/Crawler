import requests
import os
import re
from bs4 import BeautifulSoup

def getImg(html):
    # print(html)
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'img')):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    # html = html.decode('utf-8')
    reg = r'"https://([^ >]+?[r]\.jpg)"'
    imgre = re.compile(reg)
    oldList = re.findall(imgre, html)
    imglist = []
    for letter in oldList:
        if letter not in imglist:
            imglist.append(letter)
    print(imglist)
    x = 0
    for imgurl in imglist:
        print('https://'+imgurl)
        try:
            img = requests.get('https://'+imgurl)
            img.raise_for_status()
            with open('img\\%s.jpg' % x, 'wb') as file:
                file.write(img.content)
                print('%s.jpg' % x)

        except BaseException:
            print("Error")
        finally:
            x += 1


agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}
r = requests.get("https://www.zhihu.com/question/27098131/answer/171523464", headers=headers)
getImg(r.text)

