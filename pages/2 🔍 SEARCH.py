import streamlit as st
import sys
sys.path.append('./utils/')

from detailed_page import detailed_page
from get_from_api import id_name_df, id_name_dict, name_id_dict
from fuzzywuzzy import process

from PIL import Image
from io import BytesIO
import requests

st.set_page_config(page_title='Search', page_icon="🔍")

def search_games(input_string, name_id_dict=name_id_dict()):
    if input_string == '':
        top5_id_list = requests.get('http://127.0.0.1:5000/game_list?mode=top5').json()
        results_dict = dict()
        for id in top5_id_list:
            game_name = requests.get('http://127.0.0.1:5000/api?data-source=basic-data-new&game-id='+str(id)+'&content=Name').text
            results_dict[game_name] = [id]
        st.subheader('Top 5 Games')
        
    else:
        name_list = list(name_id_dict.keys())
        results = process.extract(input_string, name_list, limit=5)
        results_dict = dict()
        for name,score in results:
            results_dict[name] = name_id_dict[name]
        st.subheader('Results')

    return results_dict

def select_game(input_dict):
    col_list = st.columns(len(input_dict.keys()))
    button_list = []
    image_list = []
    for col_idx in range(len(input_dict.keys())):
        with col_list[col_idx]:
            try: # image url이 반환되지 않는 경우 예외 처리
                if len(list(input_dict.keys())[col_idx]) > 22:
                    button_text = list(input_dict.keys())[col_idx][:20] + '...'
                else: button_text = list(input_dict.keys())[col_idx]
                button_list.append(st.button(label=button_text, key=list(input_dict.keys())[col_idx]))
                game_id = input_dict[list(input_dict.keys())[col_idx]][0]
                img_url = requests.get('http://127.0.0.1:5000/api?data-source=detailed-data&game-id='+str(game_id)+'&content=image').text
                img_response = requests.get(img_url)
                img = Image.open(BytesIO(img_response.content))
                resized_img = img.resize((300,400))
                st.image(image=resized_img, use_column_width='always')
            except:
                pass
    for i,button in enumerate(button_list):
        if button:
            st.session_state['button'] = i
        else:pass
    
    return st.session_state['button']

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

local_css('css/style.css')
# remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')


st.markdown("# Search Page")

input_string = st.text_input('Enter search words:',"")
name_id_dict = name_id_dict()

search_results = search_games(input_string=input_string, name_id_dict=name_id_dict)

if 'button' not in st.session_state:
    st.session_state['button'] = 0

session = select_game(search_results)

game_name = list(search_results.keys())[session]
game_id = search_results[game_name][0]

detailed_page(game_name)
