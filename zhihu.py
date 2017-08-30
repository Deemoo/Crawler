import requests
import os
import re
import time

def empty():
    if not os.path.exists(os.path.join(os.getcwd(), 'img')):
        os.mkdir(os.path.join(os.getcwd(), 'img'))
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'img')):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def getImg(html,num,name):
    # print(html)
    reg = r'"https://([^ >]+?[b]\.jpg)"'
    imgre = re.compile(reg)
    oldList = re.findall(imgre, html)
    imglist = []
    for letter in oldList:
        if letter not in imglist:
            imglist.append(letter)
    print(imglist)
    for imgurl in imglist:
        print('https://'+imgurl)
        try:
            img = requests.get('https://'+imgurl,timeout=1)
            img.raise_for_status()
            with open(os.path.join('img','%s.jpg' % (str(num)+"_"+name)), 'wb') as file:
                file.write(img.content)
                print(str(num) + " " + time.strftime('%Y-%m-%d %H:%M:%S - ',time.localtime(time.time()))+'%s.jpg' % name)
        except BaseException as e:
            print(str(num) + " Error: "+str(e))
        finally:
            num += 1
    return num

def getAllImg(url, headers):
    empty()
    count = 1
    num = 0
    while count != 0:
        answers = requests.get(url, headers=headers)
        j = answers.json()
        # print(j)
        url = j["paging"]["next"].replace("http", "https")
        data = j["data"]
        count = len(data)
        for d in data:
            answerUrl = "https://www.zhihu.com/question/27098131/answer/"
            id = d["id"]
            name = d["author"]["name"]
            if id == 171523464:
                continue
            answer = requests.get(answerUrl + str(id), headers=headers)
            num = getImg(answer.text, num, name)

cookie = 'q_c1=ac034d58525c4acea95ec75eb68ef1c0|1499851327000|1491816798000; d_c0="AJCCam6aDQyPTqnFo4in0Ij79xLt4dJGEUI=|1499851328"; _zap=4e16b7cd-a49a-465d-9d9f-363562d3e56b; capsion_ticket="2|1:0|10:1502268642|14:capsion_ticket|44:MWIxZmFmYjcyYzgwNDViZTk4MjAzMGUxZDc3N2VkZWM=|ac881bf9e1a6b080d45268218a2447af61f194a9de7b16f15cd2a6641d43ddb7"; aliyungf_tc=AQAAAEArUikL/QYAe5ducaML+K2QikuB; q_c1=ac034d58525c4acea95ec75eb68ef1c0|1502849450000|1491816798000; _xsrf=d2d500e0-b817-4c40-bcac-01735e2bb9b0; r_cap_id="YWVhYjIzMzA2NzYxNGU5YmI0OTM4YWZiODAyZDFkNjU=|1502849488|47c297080e03aa8fe231cfff151e32d11b4111f1"; cap_id="OTFhMTlkY2E5MWFlNDE3OTljOTBjNDYyMTdmNmZlZDc=|1502849488|2fde97ec9f5d4a736afa40070145bf1f90d4edf0"; z_c0=Mi4xQ1N1NUFBQUFBQUFBa0lKcWJwb05EQmNBQUFCaEFsVk42VGE3V1FBZG5sZ2Q2QnVmTG9LVXQxRnZrT3lMeldqbEJn|1502849513|48ebd479b456ab533695e89b49e107b5ae970b0f'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Connection": "keep-alive",
    "Cookie": cookie
}
url = "https://www.zhihu.com/api/v4/questions/27098131/answers?limit=20&offset=0"

getAllImg(url, headers)
