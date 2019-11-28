# 定向爬虫：安排去中国大学排名  http://www.zuihaodaxue.com/zuihaodaxuepaiming2019.html

import requests
import bs4
from bs4 import BeautifulSoup

def getHTML(url):
    try:
        r = requests.get(url, timeout=50)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error occured with status_code="+r.status_code)

def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:      # 对表格tbody中的每一行
        if isinstance(tr, bs4.element.Tag):     # 过滤去非tr标签元素
            tds = tr('td')                      # 取出对应的各列的值    
            ulist.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string])
    
def printUnivList(ulist, num):
    tplt = '{:^6}\t{:^10}\t{:^10}\t{:^6}'
    print(tplt.format('排名','学校名称', '省市', '分数'))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], u[3]))
        
    print('Success!')         

def main():
    unifo = []
    url = "http://www.zuihaodaxue.com/zuihaodaxuepaiming2019.html"
    html = getHTML(url)
    fillUnivList(unifo, html)
    printUnivList(unifo, 40)

main()

