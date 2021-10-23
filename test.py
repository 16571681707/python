
# from BeautifulSoup4 import BeautifulSoup
# import time
# import re
# import json
# import urllib.request
# import urllib.error
# import requests
# import ssl
ssl._create_default_https_context = ssl._create_unverified_context  

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

findTitle = re.compile(r'htm">(.*?)</a>')

findUrl = re.compile(r'href="(.*?)"')

findMode = re.compile("nbs.D110000renmrb")
baseLast = {}

def main():
    makeUrl(None)
    testUrl()
    getLasturl()
    askUrl()


def makeUrl(last):
    global base,baseUrl
    today = time.strftime("%Y-%m", time.localtime())  
    day = int(time.strftime("%d", time.localtime()))
    hours = int(time.strftime("%H", time.localtime())) 
    if last is not None:
        lasts = last
    else:
        lasts = "/nbs.D110000renmrb_01.htm"
        print("检测板块数目。。。")
        time.sleep(2)
    if hours > 9:
        baseUrl = "http://paper.people.com.cn/rmrb/html/" + str(today) + "/" + str(day) + lasts
        base = "http://paper.people.com.cn/rmrb/html/" + str(today) + "/" + str(day)
    else:
        baseUrl = "http://paper.people.com.cn/rmrb/html/" + str(today) + "/" + str(day - 1) + lasts
        base = "http://paper.people.com.cn/rmrb/html/" + str(today) + "/" + str(day - 1)

def testUrl():
    
    try:
        global num,baseUrl
        request = urllib.request.Request(baseUrl, headers=header) 
        response = urllib.request.urlopen(request)  
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")  
        modes = soup.find_all("a",id="pageLink") 
        num = len(modes)
        print("共有：%d个板块"%num)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e, "code")
        if hasattr(e, "reason"):
            print(e, "reason")

def getLasturl():
    for i in range(0,num):
        if num < 10:
            baseLast[i] = '/nbs.D110000renmrb_0' + str(i + 1) + '.htm'
        else:
            baseLast[i] = '/nbs.D110000renmrb_' + str(i + 1) + '.htm'

def askUrl():
    global newsContent,newsnum
    newsContent = "当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
    newsnum = 0
    for i in range(0,num):
        makeUrl(baseLast[i])
        scanUrl(baseUrl)
        print("开始第%d个板块内容爬取。。"%(i+1))
        time.sleep(9)
    meassage("人民日报每日新闻",newsContent)
def scanUrl(url):
   
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    try:
        global newsContent,newsnum
        request = urllib.request.Request(url, headers=header) 
        response = urllib.request.urlopen(request)  
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser") 
        contens = soup.find_all("ul",class_="news-list") 
        content = str(contens)
        news = re.findall(findTitle,content)
        newsUrl = re.findall(findUrl,content)
        for i in range(0,len(news)):
            newsnum = newsnum + 1
            newsContent = newsContent + "第%d条、"%(newsnum) + news[i] + "\n" + "链接:" + '<a href="' + base + "/" + newsUrl[i] +'">' + base + "/" + newsUrl[i] + '</a>' +"\n"
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e, "code")
        if hasattr(e, "reason"):
            print(e, "reason")

def meassage(title,content):
    messageUrl = r'http://www.pushplus.plus/send'
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    data = {
        "token": "d50b5607baa44295b5783caded166730",
        "title": title,
        "content": content,
        "topic": "0513",
        "template": "json"
    }
    response = requests.post(messageUrl, data=json.dumps(data), headers=header).text
    print(response)

if __name__ == '__main__':
    main()
