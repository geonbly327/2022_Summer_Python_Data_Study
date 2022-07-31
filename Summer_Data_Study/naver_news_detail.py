import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import time
import mysql_user_info # MySQL 정보

start_time = time.time()

# 뉴스의 기본 정보 수집
def basic_info(li):
    url = li.a['href']
    for t in li.select('#main_content > div > ul > li > dl > dt > a'):
        title = t.text.strip()
    date = li.select_one('#main_content > div > ul > li > dl > dd > span.date').text.strip()
    publisher = li.select_one('#main_content > div > ul > li > dl > dd > span.writing').text.strip()

    return title, date, publisher, url

# 뉴스 기사 내에서 세부정보 수집
def detail_info(url):
    res = requests.get(url, headers = headers)
    text = res.text
    ##print(text)

    soup = BeautifulSoup(text, 'html.parser')

    # contents
    try:
        contents = soup.select_one('#dic_area').text.strip()
    except:
        try:
            contents = soup.select_one('#newsEndContents').text.strip()
        except:
            contents = soup.select_one('#content > div.end_ct > div > div.end_body_wrp').text.strip()

    return contents

# MySQL db에 data 넣기
def insert_data(publisher, title, date):
    user = mysql_user_info.user_info
    db = pymysql.connect(db=user['db'], host=user['host'], user=user['user'], passwd=user['passwd'],
                         port=user['port'], charset=user['charset'])

    sql = 'INSERT INTO news (publisher, title, date) VALUES (%s, %s, %s)'

    with db:
        with db.cursor() as cursor:
            cursor.execute(sql, (publisher, title, date))
            db.commit()

##l = []

# headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

# 날짜 리스트 만들기
day_url = []
for day in range(30):
    day_url.append('https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=229&sid1=105&date='+ str(20220601 + day))

# 메인 반복문
for day in day_url:
    res = requests.get(day, headers=headers)
    text = res.text

    soup = BeautifulSoup(text, 'html.parser')

    # 탐색할 페이지 리스트 만들기
    page = [day]
    for li in soup.select('#main_content > div.paging > a'):
        page.append('https://news.naver.com/main/list.naver' + li['href'])

    # 페이지 탐색
    for li in reversed(page):
        res = requests.get(li, headers=headers)
        text = res.text

        soup = BeautifulSoup(text, 'html.parser')

        for li in reversed(soup.select('#main_content > div > ul > li')):
            title, date, publisher, url = basic_info(li)
            ##contents = detail_info(url)

            ##print(f'Title : \n{title}')
            print(f'Date : \n{date}')

            insert_data(publisher, title, date)

            ##print(f'Contents : \n{contents}')
            ##l.append([title, date, contents])

##df = pd.DataFrame(l, columns = ['title', 'url', 'contents'])
##df.to_excel('naver_news.xlsx', index = False)

# 실행 시간
print(f'Time : {time.time() - start_time}')