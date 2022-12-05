import streamlit as st
import sys
sys.path.append('./utils/')

from detailed_page import detailed_page
from get_from_api import id_name_df, id_name_dict, name_id_dict
from fuzzywuzzy import process


def search_games(input_string, name_id_dict=name_id_dict()):
    name_list = list(name_id_dict.keys())
    results = process.extract(input_string, name_list, limit=5)
    results_dict = dict()
    for name, score in results:
        results_dict[name] = name_id_dict[name]
    
    return results_dict

def select_game(input_dict):
    col_list = st.columns(len(input_dict.keys()))
    button_list = []
    for col_idx in range(len(input_dict.keys())):
        with col_list[col_idx]:
            button_list.append(st.button(list(input_dict.keys())[col_idx]))

    for i,button in enumerate(button_list):
        if button:
            st.session_state['button'] = i
        else:pass

    return st.session_state['button']



st.markdown("# Search Page")

input_string = st.text_input('Enter search words:',"")
name_id_dict_ex = {"Halli Galli":"id1","Monopoly":"id2","Rumi Cube":"id3","Clue":"id4","Scrabble":"id5",
                    "game6":"id6","game7":"id7","game8":"id8"}
search_results = search_games(input_string=input_string, name_id_dict=name_id_dict_ex)

#Seasrch Result Example
# input_dict = {"Halli Galli":"id1","Monopoly":"id2","Rumi Cube":"id3","Clue":"id4","Scrabble":"id5"}

# if 'button' not in st.session_state:
#     st.session_state['button'] = 0

session= select_game(search_results)

game_name = list(search_results.keys())[session]
game_id = search_results[game_name]

#game_name => game_id
detailed_page(game_name)
