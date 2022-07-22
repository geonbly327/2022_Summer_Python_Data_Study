import requests
from bs4 import BeautifulSoup
import pandas as pd

#headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def detail_info(url):
    res = requests.get(url, headers = headers)
    text = res.text
    ##print(text)

    soup = BeautifulSoup(text, 'html.parser')

    #title
    try :
        title = soup.select_one('#ct > div > div > h2').text.strip()
    except:
        title = soup.select_one('#content > div > div > div > div > h4').text.strip()
    #date
    try:
        date = soup.select_one('#ct > div > div > div > div > span').text.strip()
    except:
        date = soup.select_one('#content > div > div> div > div> div > span').text.strip()
    #contents
    try:
        contents = soup.select_one('#dic_area').text.strip()
    except:
        contents = soup.select_one('#newsEndContents').text.strip()

    return title, date, contents

res = requests.get('https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=229&sid1=105&date=20220701', headers=headers)
text = res.text

soup = BeautifulSoup(text, 'html.parser')

l = []
for li in soup.select('#main_content > div > ul > li'):
    url = li.a['href']

    title, date, contents = detail_info(url)
    print(f'Title : \n{title}')
    print(f'Date : \n{date}')
    print(f'Contents : \n{contents}')
    l.append([title, date, contents])

df = pd.DataFrame(l, columns = ['title', 'url', 'contents'])
df.to_excel('naver_news.xlsx', index = False)