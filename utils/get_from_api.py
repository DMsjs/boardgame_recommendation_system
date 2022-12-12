import requests
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from langdetect import detect

def id_name_df():
    """
    게임 id, name에 대한 dataframe 반환
    """
    # id_list = requests.get('http://147.46.94.205:8000/game_list?mode=all').json()
    # name_list = []
    # for id in id_list:
    #     name_list.append(requests.get('http://147.46.94.205:8000/api?data-source=basic-data-new&game-id='+str(id)+'&content=Name').text)
    name_id_dict = requests.get('http://147.46.94.205:8000/name_id_dict?mode=name-id').json()
    result_df = pd.DataFrame({'id':list(name_id_dict.values()), 'name':list(name_id_dict.keys())})
    
    return result_df

def id_name_dict():
    """
    {'id':'name'} 형태의 dictinary 반환
    """
    result_dict = requests.get('http://147.46.94.205:8000/name_id_dict?mode=id-name').json()
    return result_dict

def name_id_dict():
    """
    {'name':'id'} 형태의 dictinary 반환
    """
    result_dict = requests.get('http://147.46.94.205:8000/name_id_dict?mode=name-id').json()
    return result_dict

def input_df_for_network():
    """
    network 구성에 필요한 input dataframe 반환 (detailed_data에서 필터링해서 뽑는 방식)
    """
    id_list = requests.get('http://147.46.94.205:8000/game_list?mode=all').json()
    row_list = []
    for id in id_list:
        detailed_game_data = requests.get('http://147.46.94.205:8000/api?data-source=detailed-data&game-id='+str(id)).json()
        row_list.append(detailed_game_data)
    input_df = pd.DataFrame(row_list)
    input_df = input_df[['primary','minplayers','maxplayers','playingtime','minage','boardgamecategory',
                         'boardgamemechanic','boardgamefamily','bayesaverage','Board Game Rank','averageweight',
                         'category_tsne_0', 'category_tsne_1', 'mechanic_tsne_0', 'mechanic_tsne_1', 'drop']]
    return input_df[input_df['drop']==False]

def direct_network_input():
    """
    network 구성에 필요한 input dataframe 반환 (input 형태 그대로 api에 올린 데이터를 그대로 가져오는 방식)
    """
    id_list = requests.get('http://147.46.94.205:8000/game_list?mode=network-input').json()
    row_list = []
    for id in id_list:
        detailed_game_data = requests.get('http://147.46.94.205:8000/api?data-source=network-input&game-id='+str(id)).json()
        row_list.append(detailed_game_data)
    input_df = pd.DataFrame(row_list)
    return input_df


def get_lang(comment):
    try:
        return detect(comment)
    except:
        return None
    # if comment == None:
    #     return None
    # else:
    #     return detect(comment)
    # for comment in review_data_new["comment"]:
    #     try:
    #         languages.append(detect(comment))
    #     except:
    #         languages.append(None)

def review_data(id=None, content=None):
    """
    id가 입력되지 않는 경우, key: game_id, value: list of content(comment, rating, lang 등) 형태의 dictionary 반환 
    id만 입력되면, 해당 game에 대해 comment 및 language를 column으로 하는 dataframe 반환
    id 및 content가 모두 입력되면, 해당 game에 대한 list of content(comment, rating, lang 등) 반환
    """
    if id == None:
        id_list = requests.get('http://147.46.94.205:8000/game_list?mode=all').json()
        result_dict = dict()
        for id in id_list:
            review_data = requests.get('http://147.46.94.205:8000/api?data-source=review-data-new&game-id='+str(id)+'&content='+content).json()
            result_dict[id] = review_data
        return result_dict

    elif (id is not None) and (content is None):
        comment_list = requests.get('http://147.46.94.205:8000/api?data-source=review-data-new&game-id='+str(id)+'&content=comment').json()
        lang_list = requests.get('http://147.46.94.205:8000/api?data-source=review-data-new&game-id='+str(id)+'&content=lang').json()
        result_df = pd.DataFrame({'comment':comment_list, 'lang':lang_list})
        return result_df
    
    elif (id is not None) and (content is not None):
        review_data = requests.get('http://147.46.94.205:8000/api?data-source=review-data-new&game-id='+str(id)+'&content='+content).json()
        return review_data

    # elif (id is not None) and (mode =='Language'):
    #     review_data = requests.get('http://147.46.94.205:8000/api?data-source=review-data-new&game-id='+str(id)+'&content=comment').json()
    #     lang_list = []
    #     for comment in review_data:
    #         try:
    #             lang_list.append(detect(comment))
    #         except:
    #             lang_list.append(None)
        
    #     result_df = pd.DataFrame({'comment':review_data, 'lang':lang_list})
        
        return result_df
    
    else:
        raise Exception('Error: undefined input pair')

if __name__ == '__main__':
    # print(review_data(id=30549, content='rating'))
    print(direct_network_input())
