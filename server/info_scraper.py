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

# set up dataframe and init variables
df_info = pd.DataFrame(columns = ['id', 'name', 'rank', 'image', 'link', 'bggRating', 'avgRating', 'numRatings']) # df
pageNum = 1 # bgg page number
minRatings = 1000 # minimum number of ratings
greater = True # check if >minRatings

while greater:
    url = f'https://boardgamegeek.com/browse/boardgame/page/{pageNum}?sort=numvoters&sortdir=desc' # url with pageNum variable, sorted by descending number of voters
    r = request(url) # request

    # BS4 parsing
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find_all('tr') # find all table rows

    # parse each row of the table to scrape data (look at html to see each category) and skip first row of labels
    for i in range(1, len(table)):
        image = table[i].find('td', class_ = 'collection_thumbnail').find('img')['src']
        link = table[i].find('td', class_ = 'collection_thumbnail').find('a')['href']
        print(image, link)

        # print(i) # debug to see if it was collecting 100 per page
        ratings = table[i].find_all('td', class_ = 'collection_bggrating')
        bggRating = ratings[0].text.split()[0]
        avgRating = ratings[1].text.split()[0]
        numRatings = ratings[2].text.split()[0]

        # check minimum ratings
        if int(numRatings) < minRatings:
            greater = False
            break

        rankHeader = table[i].find('td', class_ = 'collection_rank').find('a') # parse if it has a rank or not (expansions are unranked)
        if not rankHeader:
            continue
        else:
            rank = rankHeader['name']
        idNum = table[i].find('td', class_ = 'collection_objectname').find('a')['href'].split('/')[2]
        name = table[i].find('td', class_ = 'collection_objectname').find('a').text

        df_info = df_info.append(pd.Series([idNum, name, rank, image, link, bggRating, avgRating, numRatings], index=['id', 'name', 'rank', 'image', 'link', 'bggRating', 'avgRating', 'numRatings']), ignore_index=True) # append data

    pageNum += 1 #increment page number
    greater = False
#df_info.to_csv('bg_info.csv', encoding='utf-8', index=False)