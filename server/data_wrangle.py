import pandas as pd
import os
from bs4 import BeautifulSoup
import requests

def top10Games():
  df_bg_info = pd.read_csv(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'bg_info.csv'),
  )
  return df_bg_info.sort_values('rank').iloc[:10]

def parseData(r):
  soup = BeautifulSoup(r.text, 'lxml')
  res = {}
  res['image'] = soup.find_all('image')[0].getText()
  res['name'] = soup.find_all('name')[0]['value']
  res['description'] = soup.find_all('description')[0].getText()
  res['year'] = soup.find_all('yearpublished')[0]['value']
  res['minplaytime'] = soup.find_all('minplaytime')[0]['value']
  res['maxplaytime'] = soup.find_all('maxplaytime')[0]['value']
  return res