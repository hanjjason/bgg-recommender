from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import time
import numpy as np

def request(url): 
    status_code = 500
    while status_code != 200: 
        sleep(5) # TOS
        try: 
            r = requests.get(url)
            status_code = r.status_code
            print(status_code)
        except: 
            print('failed')
            sleep(3)
    return r

df_ratings_list = []
df_info = pd.read_csv('bg_info.csv')

count = 1 # debug purposes
for group in np.array_split(df_info, 20): 
    pageNum = 1
    while 1: 
        idNums = ','.join(map(str,group['id'].tolist()))
        url = f'https://www.boardgamegeek.com/xmlapi2/thing?id={idNums}&ratingcomments=1&page={pageNum}'
        r = request(url)

        soup = BeautifulSoup(r.text, 'xml')
        items = soup.find_all('item')
        check = items[0].find_all('comment')
        print(items[0]['id'])
        if not check: 
            break

        id_list = []
        username_list = []
        rating_list = []
        for i in range(len(items)): 
            comments = items[i].find_all('comment')
            for com in comments: 
                id_list.append(items[i]['id'])
                username_list.append(com['username'])
                rating_list.append(com['rating'])
                
        df_ratings_list.append(pd.DataFrame(list(zip(id_list, username_list, rating_list)), columns = ['game_id', 'username', 'rating']))

        print(pageNum)
        pageNum += 1
    print(f'count: {count}')
    count += 1

df_ratings = pd.concat(df_ratings_list)
df_ratings.to_csv('bg_ratings.csv', encoding = 'utf-8', index=False)