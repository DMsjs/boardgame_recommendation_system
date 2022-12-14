from flask import Flask, request
from flask import render_template
from pyarrow import csv

app = Flask(__name__)

basic_data_new = csv.read_csv('./data/2022-01-08.csv').to_pandas()
detailed_data = csv.read_csv('./data/detailed_with_tsne.csv').to_pandas()
review_data_new = csv.read_csv('./data/review_lang_included.csv').to_pandas()
games = csv.read_csv('./data/games.csv').to_pandas()
network_input = csv.read_csv('./data/tsne_game_info4.csv').to_pandas()


@app.route("/")
def init():
    return "DataVisualization Project (Team 2) - API"

@app.route('/api')
def get_data():
    args = request.args
    source = args.get('data-source')
    
    # if source == 'basic-data-old':
    #     game_id = args.get('game-id')
    #     content = args.get('content')
    #     data = basic_data_old[basic_data_old['ID']==int(game_id)]
    #     if content == None:
    #         return data.to_dict(orient='records')[0]
    #     else:
    #         return data.to_dict(orient='records')[0][content]

    if source == 'basic-data-new':
        game_id = args.get('game-id')
        content = args.get('content')
        data = basic_data_new[basic_data_new['ID']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')[0]
        else:
            return str(data.to_dict(orient='records')[0][content])

    elif source == 'detailed-data':
        game_id = args.get('game-id')
        content = args.get('content')
        data = detailed_data[detailed_data['id']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')[0]
        else:
            return str(data.to_dict(orient='records')[0][content])
    
    elif source == 'games':
        game_id = args.get('game-id')
        content = args.get('content')
        data = games[games['BGGId']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')[0]
        else:
            return str(data.to_dict(orient='records')[0][content])

    elif source == 'network-input':
        game_id = args.get('game-id')
        content = args.get('content')
        data = network_input[network_input['id']==int(game_id)]
        if content == None:
            return data.to_dict(orient='records')[0]
        else:
            return str(data.to_dict(orient='records')[0][content])
    
    # elif source == 'review-data-old':
    #     game_id = args.get('game-id')
    #     content = args.get('content')
    #     data = review_data_old[review_data_old['ID']==int(game_id)]
    #     if content == None:
    #         return data.to_dict(orient='records')
    #     else:
    #         result = []
    #         for item in data.to_dict(orient='records'):
    #             result.append(item[content])
    #         return result

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
        raise Exception('Error: invalid data source')

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
    elif mode == 'top5':
        return list(detailed_data['id'][detailed_data['Board Game Rank'].apply(rank_to_int)<=5])
    elif mode == 'network-input':
        return list(network_input['id'])
    else:
        raise Exception('Error: invalid mode')

@app.route('/name_id_dict')
def get_name_id_dict():
    args = request.args
    mode = args.get('mode')
    df = basic_data_new[['ID','Name']]
    if mode == 'name-id':
        return df.set_index('Name').T.to_dict('list')
    elif mode == 'id-name':
        return df.set_index('ID').T.to_dict('list')
    else:
        raise Exception('Error: invalid mode')

if __name__=="__main__":
    app.run(host="127.0.0.1", port="5000", debug=False)