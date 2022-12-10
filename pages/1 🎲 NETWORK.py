import sys
import pandas as pd
import numpy as np

import networkx as nx
from pyvis.network import Network

import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components

from utils.detailed_page import make_popup

sys.path.append('../')
from network_function.network_generater import GameNetwork

st.markdown("# Network Page")
st.sidebar.markdown("Filtering Options")

# Sidebar
min_players = st.sidebar.slider("Min. Players:", value=[2,4], min_value=0, max_value=10)
max_players = st.sidebar.slider("Max. Players:", value=[5,8], min_value=2, max_value=999)
playing_time = st.sidebar.slider("Playing Time:", value=[10,60], min_value=10, max_value=60000, step=10)
min_age = st.sidebar.slider("Min. Age:", value=[5,10], min_value=5, max_value=25)
bayes_average = st.sidebar.slider("Rating:", value=[7,10], min_value=0, max_value=10) # 평점
board_game_rank = st.sidebar.slider("Board Game Rank:", value=[1,100], min_value=1, max_value=99999) # 랭킹
average_weight = st.sidebar.slider("Weight:", value=[2,4], min_value=0, max_value=5) # Weight

# filter 설정
filter = {'minplayers': min_players,
          'maxplayers': max_players,
          'playingtime': playing_time,
          'minage': min_age,
          'bayesaverage': bayes_average,
          'Board Game Rank': board_game_rank,
          'averageweight': average_weight}

tab1, tab2 = st.tabs(["Network", "Details"])
data = np.random.randn(10, 1)

### Graph
# Read dataset (CSV)
df = pd.read_csv('data/tsne_game_info2.csv')

# GameNetwork 객체 생성(게임 정보 및 네트워크 핸들링)
game_network = GameNetwork(df)

# Define list of selection options and sort alphabetically
game_list = list(df['primary'])
game_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
# trigger 설정(1, 2, 3개 설정)(사실 4개 이상도 되긴 함)
with tab1:
    concept = st.radio("Get recommendation based on", ('Category', 'Mechanism'))

    triggers = st.multiselect('Choose 1~3 games to start', game_list)

    # 사용자가 지정한 node 정보 (대표 node 3개)
    for i in triggers:
        print(i)
    print()

    run = st.button('Run')

    # Category 기반 추천
    if 1 <= len(triggers) <= 3 and concept == 'Category' and run == True:  
        # 추천 게임 네트워크 도출(GameNetwork 내부 메서드 사용)
        recomm_G = game_network.category_recomm_network(triggers=triggers, filter=filter, recommend_num=10)

        # 대표 node coloring 
        # AttributeError: 'GameNetwork' object has no attribute 'add_node' 발생
        # for node in recomm_G:
        #     if node in triggers:
        #         game_network.add_node(node, color='#FFFFFF', size=30)

        # node 출력
        print(recomm_G.nodes())
        # edge 출력
        print(recomm_G.edges())

        # 그래프 보여주는 부분 추가 필요

    # Mechanism 기반 추천
    elif 1 <= len(triggers) <= 3 and concept == 'Mechanism' and run == True:
        pass


tab2.subheader("A tab with the data")
tab2.write(data)

#Pop-up Module, to be modified to use Game_ID as an input
# make_popup("Halli Galli")
