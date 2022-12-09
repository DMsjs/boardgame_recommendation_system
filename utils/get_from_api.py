import requests
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def id_name_df():
    """
    게임 id, name에 대한 dataframe 반환
    """
    # id_list = requests.get('http://127.0.0.1:5000/game_list?mode=all').json()
    # name_list = []
    # for id in id_list:
    #     name_list.append(requests.get('http://127.0.0.1:5000/api?data-source=basic-data-new&game-id='+str(id)+'&content=Name').text)
    name_id_dict = requests.get('http://127.0.0.1:5000/name_id_dict?mode=name-id').json()
    result_df = pd.DataFrame({'id':list(name_id_dict.values()), 'name':list(name_id_dict.keys())})
    
    return result_df

def id_name_dict():
    """
    {'id':'name'} 형태의 dictinary 반환
    """
    result_dict = requests.get('http://127.0.0.1:5000/name_id_dict?mode=id-name').json()
    return result_dict

def name_id_dict():
    """
    {'name':'id'} 형태의 dictinary 반환
    """
    result_dict = requests.get('http://127.0.0.1:5000/name_id_dict?mode=name-id').json()
    return result_dict

def input_df_for_network():
    """
    network 구성에 필요한 input dataframe 반환
    """
    id_list = requests.get('http://127.0.0.1:5000/game_list?mode=all').json()
    row_list = []
    for id in id_list:
        detailed_game_data = requests.get('http://127.0.0.1:5000/api?data-source=detailed-data&game-id='+str(id)).json()
        row_list.append(detailed_game_data)
    input_df = pd.DataFrame(row_list)
    input_df = input_df[['primary','minplayers','maxplayers','playingtime','minage','boardgamecategory',
                         'boardgamemechanic','boardgamefamily','bayesaverage','Board Game Rank','averageweight']]
    return input_df

def review_data_dict(id=None):
    """
    id가 입력되지 않는 경우, key: game_id, value: list of reviews 형태의 dictionary 반환 
    id가 입력되면, 해당 game에 대한 review(commet)들의 list 반환
    """
    if id == None:
        id_list = requests.get('http://127.0.0.1:5000/game_list?mode=all').json()
        result_dict = dict()
        for id in id_list:
            review_data = requests.get('http://127.0.0.1:5000/api?data-source=review-data-new&game-id='+str(id)+'&content=comment').json()
            result_dict[id] = review_data
        return result_dict
    else:
        review_data = requests.get('http://127.0.0.1:5000/api?data-source=review-data-new&game-id='+str(id)+'&content=comment').json()
        return review_data


if __name__ == '__main__':
    print(review_data_dict(30549))
