from flask import Flask, render_template, send_from_directory
import requests
import pandas as pd
import data_wrangle
import matrix_factorization

app = Flask(__name__, static_url_path='', static_folder="../client/dist", template_folder="../client/dist")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/top10')
def top10():
  data = []
  games = data_wrangle.top10Games();
  for index, game in games.iterrows():
    currID = game['game_id']
    temp = data_wrangle.parseData(requests.get(f'https://api.geekdo.com/xmlapi2/thing?id={currID}'))
    temp['name'] = game['name']
    temp['bggRating'] = game['bggRating']
    data.append(temp)
  return {'data': data}

@app.route('/api/recommend/<user>')
def getRecc(user):
  data = []
  already_rated, predictions = matrix_factorization.recommender(user)
  for index, game in predictions.head(10).iterrows():
    currID = game['id']
    temp = data_wrangle.parseData(requests.get(f'https://api.geekdo.com/xmlapi2/thing?id={currID}'))
    temp['name'] = game['name']
    temp['bggRating'] = game['bggRating']
    data.append(temp)
  return {'data': data}

if __name__ == '__main__':
  app.run()