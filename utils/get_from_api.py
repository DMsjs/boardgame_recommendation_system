import requests
import pandas as pd
import numpy as np


def top100_games_info():
    """
    100위권 내 게임들의 basic-data 반환
    """
    top100_id_list = requests.get('http://127.0.0.1:5000/game_list?mode=top100')
    top100_id_list = top100_id_list.json()

    top100_basic_data = []
    for id in top100_id_list:
        game_info = requests.get('http://127.0.0.1:5000/api?data-source=basic-data-new&game-id='+id)
        top100_basic_data.append(game_info.json())

    return top100_basic_data

def top100_games_review():
    """
    100위권 내 게임들의 review 반환
    """
    top100_id_list = requests.get('http://127.0.0.1:5000/game_list?mode=top100')
    top100_id_list = top100_id_list.json()

    top100_review_data = []
    for id in top100_id_list:
        review = requests.get('http://127.0.0.1:5000/api?data-source=review-data-old&game-id='+id)
        top100_games_review.append(review.json())
    
    return top100_review_data

def id_name_df():
    """
    게임 id, name에 대한 dataframe 반환
    """
    id_list = requests.get('http://127.0.0.1:5000/game_list?mode=all').json()
    name_list = []
    for id in id_list:
        name_list.append(requests.get('http://127.0.0.1:5000/api?data-source=basic-data-new&game-id='+str(id)+'&content=Name').text)
    result_df = pd.DataFrame({'id':id_list, 'name':name_list})
    
    return result_df

def id_name_dict():
    """
    {'id':'name'} 형태의 dictinary 반환
    """
    pass

def name_id_dict():
    """
    {'name':'id'} 형태의 dictinary 반환
    """
    pass

    

if __name__ == '__main__':
    print(id_name_df())
