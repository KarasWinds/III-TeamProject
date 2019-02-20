from urllib.request import urlopen
from bs4 import BeautifulSoup

def news(html, type="列表"):
    # type預設值"列表"為抓取當頁全部新聞，type="熱門新聞"為抓取熱門新聞
    newsurldata = []
    for news in html.find("ul",  {"data-desc": type}).find_all("li"):
        newsurl = news.find("a")["href"]
        title = news.find("div", class_="list_title").text
        newsurldata.append({"url": newsurl, "title": title})
    return newsurldata

def newstext(html):
    pic = html.find("div", class_="news_p").find("span", class_="ph_i").find("img")
    time = html.find("div", class_="c_time").text
    picurl = str(pic.get('src'))
    pictext = html.find("div", class_="news_p").find("p", class_="").text
    text = []
    for n in html.find("div", class_="news_p").find_all("p", class_=""):
        if '<p>' in str(n) and '><' not in str(n):
            text.append(n.text)
    return {"time": time, "picurl": picurl, "pictext": pictext, "text": text}

def getnewstext(url, newsurldata):
    for n in newsurldata:
        newsurl = url + n["url"]
        response = urlopen(newsurl)
        html = BeautifulSoup(response, features="html5lib")
        newsdata = newstext(html)
        n["time"] = newsdata["time"]
        n["picurl"] = newsdata["picurl"]
        n["pictext"] = newsdata["pictext"]
        n["text"] = newsdata["text"]
    return newsurldata

if __name__ == '__main__':
    url = "http://sports.ltn.com.tw/"
    response = urlopen(url)
    html = BeautifulSoup(response, features="html5lib")
    newsurldata = news(html, type="熱門新聞")
    newsdata = getnewstext(url, newsurldata)

    print(newsdata)








