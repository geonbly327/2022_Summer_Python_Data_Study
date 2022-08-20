from konlpy.tag import Okt
from collections import Counter
import pymysql
import mysql_user_info
import time

start_time = time.time()

# news 테이블에서 data 가져오기
def fetch():
    with pymysql.connect(db=user['db'], host=user['host'], user=user['user'], passwd=user['passwd'], port=user['port'], charset=user['charset']) as db:
        with db.cursor(pymysql.cursors.DictCursor) as cur:
            sql = 'SELECT * FROM news'
            cur.execute(sql)
            db.commit()

            data = cur.fetchall()

    return data

# morpheme 테이블에 data 넣기
def insert_data(id, type, word, sort):
    try:
        with pymysql.connect(db=user['db'], host=user['host'], user=user['user'], passwd=user['passwd'], port=user['port'], charset=user['charset']) as db:
            with db.cursor() as cursor:
                sql = 'INSERT INTO ' + sort + '_morpheme (id, type, word) VALUES (%s, %s, %s)'
                cursor.execute(sql, (id, type, word))
                db.commit()
    except:
        pass

# data fetch
user = mysql_user_info.user_info
data = fetch()

# Okt 객체 선언
okt = Okt()

# main
for i in data:
    # id 생성
    id = i['publisher'] + '-' + i['date']
    print(id)

    # 형태소 분석
    title_pos = okt.pos(i['title'])
    title_noun = okt.phrases((i['title']))
    body_pos = okt.pos(i['body'])
    body_noun = okt.phrases((i['body']))

    # 제목 형태소 분석을 db에 넣기
    for k in title_noun:
        insert_data(id, 'noun', k, 'title')

    # 본문 형태소 분석을 db에 넣기
    for k in body_noun:
        insert_data(id, 'noun', k, 'body')
    for k in body_pos:
        if k[1] == 'adjective':
            insert_data(id, 'adjective', k[0], 'body')
        else:
            continue

# 실행 시간
print(f'Time : {time.time() - start_time}')