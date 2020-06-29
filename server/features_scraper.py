from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
#import sqlite3 # for future database storage
import os

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

df_info = pd.read_csv('bg_info.csv')
print(df_info['id'])

feature_list = []
for idNum in df_info['id']:
    url = f'https://www.boardgamegeek.com/xmlapi2/thing?id={idNum}'
    r = request(url)
    soup = BeautifulSoup(r.text, 'xml')
    tags = soup.find_all('link')
    tag_list = []
    for tag in tags:
        if tag['type'] == 'boardgamecategory':
            tag_list.append(tag['value'])
        if tag['type'] == 'boardgamemechanic':
            tag_list.append(tag['value'])
    feature_list.append(','.join(tag_list))

df_features = pd.DataFrame({'id': df_info['id'], 'features': feature_list})
df_features.to_csv('bg_features.csv', encoding = 'utf-8', index=False)