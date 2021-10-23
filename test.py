
import re
findTitle = re.compile('htm">(.*?)</a>')   
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}
request = urllib.request.Request("http://paper.people.com.cn/rmrb/html/2021-10/23/nbs.D110000renmrb_01.htm", headers=header) 
response = urllib.request.urlopen(request)  
html = response.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser") 
contens = soup.find_all("ul",class_="news-list") 
content = str(contens)
news = re.findall(findTitle,content)
print(news)


