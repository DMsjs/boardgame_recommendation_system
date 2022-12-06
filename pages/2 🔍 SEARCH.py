import streamlit as st
import sys
sys.path.append('./utils/')

from detailed_page import detailed_page
from get_from_api import id_name_df, id_name_dict, name_id_dict
from fuzzywuzzy import process

from PIL import Image
from io import BytesIO
import requests

def search_games(input_string, name_id_dict=name_id_dict()):
    name_list = list(name_id_dict.keys())
    results = process.extract(input_string, name_list, limit=5)
    results_dict = dict()
    for name,score in results:
        results_dict[name] = name_id_dict[name]

    return results_dict

def select_game(input_dict):
    col_list = st.columns(len(input_dict.keys()))
    # button_list = []
    for col_idx in range(len(input_dict.keys())):
        with col_list[col_idx]:
            st.button(label=list(input_dict.keys())[col_idx])
            game_id = input_dict[list(input_dict.keys())[col_idx]][0]
            img_url = requests.get('http://127.0.0.1:5000/api?data-source=basic-data-new&game-id='+str(game_id)+'&content=Thumbnail').text
            st.image(img_url)
            # button_list.append(st.button(list(input_dict.keys())[col_idx]))
            # img_response = requests.get('https://cf.geekdo-images.com/S3ybV1LAp-8SnHIXLLjVqA__micro/img/S4tXI3Yo7BtqmBoKINLLVUFsaJ0=/fit-in/64x64/filters:strip_icc()/pic1534148.jpg')
            # img = Image.open(BytesIO(img_response.content))
            # button_list.append(st.button(st.image(img)))

    # for i,button in enumerate(button_list):
    #     if button:
    #         st.session_state['button'] = i
    #         # st.image("")
    #     else:pass

    return st.session_state['button']



st.markdown("# Search Page")

input_string = st.text_input('Enter search words:',"")
name_id_dict = name_id_dict()

search_results = search_games(input_string=input_string, name_id_dict=name_id_dict)

#Seasrch Result Example
# input_dict = {"Halli Galli":"id1","Monopoly":"id2","Rumi Cube":"id3","Clue":"id4","Scrabble":"id5"}


session= select_game(search_results)

game_name = list(search_results.keys())[session]
game_id = search_results[game_name][0]


#game_name => game_id
detailed_page(game_name)
