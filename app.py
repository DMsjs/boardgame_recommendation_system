from flask import Flask, request
from flask import render_template
# import csv
from csv import DictReader
from pyarrow import csv

app = Flask(__name__)

basic_data_old = csv.read_csv('./data/2020-08-19.csv').to_pandas()
basic_data_new = csv.read_csv('./data/2022-01-08.csv').to_pandas()
detailed_data = csv.read_csv('./data/games_detailed_info.csv').to_pandas()
review_data_old = csv.read_csv('./data/bgg-15m-reviews.csv').to_pandas()
review_data_new = csv.read_csv('./data/bgg-19m-reviews.csv').to_pandas()

@app.route("/")
def init():
    return "DataVisualization Project (Team 2) - API"

@app.route('/api')
def get_data():
    args = request.args
    source = args.get('data-source')
    
    if source == 'basic-data-old':
        game_id = args.get('game-id')
        content = args.get('content')
        data = basic_data_old[basic_data_old['ID']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')[0]
        else:
            return data.to_dict(orient='records')[0][content]

    if source == 'basic-data-new':
        game_id = args.get('game-id')
        content = args.get('content')
        data = basic_data_new[basic_data_new['ID']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')[0]
        else:
            return data.to_dict(orient='records')[0][content]

    elif source == 'detailed-data':
        game_id = args.get('game-id')
        content = args.get('content')
        data = detailed_data[detailed_data['id']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')[0]
        else:
            return data.to_dict(orient='records')[0][content]
    
    elif source == 'review-data-old':
        game_id = args.get('game-id')
        content = args.get('content')
        data = review_data_old[review_data_old['ID']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')
        else:
            result = []
            for item in data.to_dict(orient='records'):
                result.append(item[content])
            return result

    elif source == 'review-data-new':
        game_id = args.get('game-id')
        content = args.get('content')
        data = review_data_new[review_data_new['ID']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')
        else:
            result = []
            for item in data.to_dict(orient='records'):
                result.append(item[content])
            return result

    else:
        raise Exception('Error: wrong data source')

def rank_to_int(x):
    if x.isdigit():
        return int(x)
    else:
        return 1000000

@app.route('/game_list')
def get_game_list():
    args = request.args
    mode = args.get('mode')

    if mode == 'all':
        return list(detailed_data['id'])
    elif mode == 'top100':
        return list(detailed_data['id'][detailed_data['Board Game Rank'].apply(rank_to_int)<=100])
    