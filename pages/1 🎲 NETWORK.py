import sys
import time
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

current_page = "network"

@st.cache(allow_output_mutation=True)
def load_network(df):
    print('loading network!')
    return GameNetwork(df)

st.markdown("# Board Game Recommendation")
st.sidebar.markdown("Filtering Options")

# Sidebar
players = st.sidebar.slider("Number of Players:", value=[2,4], min_value=1, max_value=10)
min_playing_time, max_playing_time = st.sidebar.select_slider("Playing Time (Minutes):", options=[0, 30, 60, 120, 180, 'Max'], value=[0, 180])
min_age = st.sidebar.slider("Min. Age:", value=[5,10], min_value=5, max_value=25)
bayes_average = st.sidebar.slider("Rating:", value=[6,10], min_value=0, max_value=10) # 평점
min_rank, max_rank = st.sidebar.select_slider("Board Game Ranking:", options=[0, 10, 50, 100, 500, 1000, 5000, 10000, 'Max'], value=[0, 'Max']) # 랭킹
average_weight = st.sidebar.slider("Difficulty Level:", value=[2,4], min_value=0, max_value=5) # Difficulty

st.sidebar.markdown("Recommendation Options")
num_recommend = st.sidebar.number_input("Max. Number of Recommendation", value=10, step=1)
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")

# Post-processing
min_players = (players[0], None)
max_players = (None, players[1])

if max_playing_time == 'Max':
    playing_time = (min_playing_time, 60000)
else:
    playing_time = (min_playing_time, max_playing_time)

if max_rank == 'Max':
    board_game_rank = (min_rank, 99999)
else:
    board_game_rank = (min_rank, max_rank)

# filter 설정
filter = {'minplayers': min_players,
          'maxplayers': max_players,
          'playingtime': playing_time,
          'minage': min_age,
          'bayesaverage': bayes_average,
          'Board Game Rank': board_game_rank,
          'averageweight': average_weight}

# print(filter)

tab1, tab2 = st.tabs(["Network", "Details"])
data = np.random.randn(10, 1)

### Graph
# Read dataset (CSV)
df = pd.read_csv('data/tsne_game_info4.csv')
# df = pd.read_csv('data/tsne_game_info4_no_dup.csv')
# df = pd.read_csv('data/tsne_game_info2_mini.csv') # 빠른 실행을 위해

# GameNetwork 객체 생성(게임 정보 및 네트워크 핸들링)
game_network = load_network(df) # load_network 사용하면 옵션 바뀔 때마다 다시 실행되지 않음

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

    if run == True :
        if len(triggers) >= 1:  
            with st.spinner("Please wait..."):

                # 추천 게임 네트워크 도출(GameNetwork 내부 메서드 사용)
                recomm_G, recommended_df_dict = game_network.category_recomm_network(
                    triggers=triggers, 
                    filter=filter, 
                    recommend_num=num_recommend, 
                    concept=concept
                    )
                # print('recommended_df_dict')
                # print(recommended_df_dict.keys())
                # print('end')

                # 대표 node coloring 
                # AttributeError: 'GameNetwork' object has no attribute 'add_node' 발생
                # for node in recomm_G:
                #     if node in triggers:
                #         game_network.add_node(node, color='#FFFFFF', size=30)

                # node 출력
                print('recommended nodes:', recomm_G.nodes())
                # edge 출력
                # print('recommended edges:', recomm_G.edges())

                # Initiate PyVis network object
                game_net = Network(
                                height='400px',
                                width='100%',
                                bgcolor='#222222',
                                font_color='white'
                                )

                # add color and resize node
                for trigger in triggers:
                    game_net.add_node(trigger, label=trigger, color='#FFFFFF', size=40)

                for node in recomm_G.nodes():
                    game_net.add_node(node)
                for source, target in recomm_G.edges():
                    game_net.add_edge(source, target, color='#97c2fc')
                # Take Networkx graph and translate it to a PyVis graph format
                # game_net.from_nx(recomm_G)


                # Generate network with specific layout settings
                game_net.repulsion(
                                    node_distance=420,
                                    central_gravity=0.33,
                                    spring_length=110,
                                    spring_strength=0.10,
                                    damping=0.95
                                )

                # Save and read graph as HTML file (on Streamlit Sharing)
                try:
                    path = '/tmp'
                    game_net.save_graph(f'{path}/pyvis_graph.html')
                    HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

                # Save and read graph as HTML file (locally)
                except:
                    path = 'html_files'
                    game_net.save_graph(f'{path}/pyvis_graph.html')
                    HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

                # Load HTML file in HTML component for display on Streamlit page
                components.html(HtmlFile.read(), height=435)

                wait_sign = st.markdown("")

        elif len(triggers) == 0:
            st.write('Please select at least one game')

with tab2:
    if len(triggers) >= 1 and run == True :

        # st.write(recommended_df_dict.keys())

        for trigger in recommended_df_dict.keys():
            st.markdown(f'#### {trigger}')
            # st.write(recommended_df_dict[trigger])

            data = recommended_df_dict[trigger][["primary","minplayers","maxplayers","playingtime","averageweight","minage","Board Game Rank","bayesaverage"]].copy().round(2)

            players=[]
            for i in range(len(data)):
                player_str = "{} - {}".format(list(data["minplayers"])[i],list(data["maxplayers"])[i])
                players.append(player_str)
            data["players"]=players

            # print(data)

            priority = range(1, len(data)+1)
            data['priority'] = priority

            # recomm_no = ['Input'] * len(triggers)
            # i = 1
            # while len(recomm_no) < len(data):
            #     recomm_no.append(i)
            #     i += 1
            # data['recomm_no'] = recomm_no

            data_col_dict = {"priority": "Priority",
                            "primary":"Name",
                            "players":"Players",
                            "playingtime":"Playtime",
                            "averageweight":"Difficulty",
                            "minage":"Min. Age",
                            "Board Game Rank":"Ranking",
                            "bayesaverage": "Ratings"
                            }
            
            columns_list = st.columns([1,2,1,1,1,1,1,1])
            for i, column in enumerate(list(columns_list)):
                with column:
                    st.markdown("**{}**".format(list(data_col_dict.values())[i]))

            for data_idx in range(len(data)):
                columns_list = st.columns([1,2,1,1,1,1,1,1])
                for i, column in enumerate(list(columns_list)):
                    with column:
                        st.write(str(list(data[list(data_col_dict.keys())[i]])[data_idx]))

    else:
        st.write('Please run recommendation first')

