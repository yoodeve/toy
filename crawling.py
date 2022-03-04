# DB
from pymongo import MongoClient

from config import MONGODB_SETTIING

client = MongoClient(MONGODB_SETTIING.values())
db = client.dbsparta
# 크롤링
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#검색어 list
temp =['화이자백신후유증','모더나백신후유증','아스트라제네카백신후유증','얀센백신후유증']
search = []

#검색어 list 를 인코딩하여 다시 Search 리스트에 append 시킴.
for a in temp:
    b = urllib.parse.quote_plus(a)
    search.append(b)

pageNum = 1

while pageNum < 11:
    for a in search:
        url = f'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query={a}' \
              f'&sm=tab_pge&srchby=all&st=sim&where=post&start={pageNum}'
        print(url)
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        nSearch = soup.select_one('meta[property="og:title"]')['content'].split(":")[0]
        print(nSearch)
        title = soup.find_all(class_='api_txt_lines total_tit')

        print(f'-----{pageNum}페이지 결과입니다.-----')
        for a in title[0:8]:
            total = list(db.naver_view.find())
            print(len(total))
            b = len(total)

            print(a.text)
            print(a.attrs['href'])

            doc = {
                'title': a.text,
                'url': a.attrs['href'],
                'search': nSearch
            }
            db.naver_view.insert_one(doc)
    pageNum += 1