import streamlit as st

from utils.detailed_page import detailed_page


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

st.text_input('Enter search words:',"halli galli")

#Seasrch Result Example
input_dict = {"Halli Galli":"id1","Monopoly":"id2","Rumi Cube":"id3","Clue":"id4","Scrabble":"id5"}

session= select_game(input_dict)

game_name = list(input_dict.keys())[session]
game_id = input_dict[game_name]

#game_name => game_id
detailed_page(game_name)


