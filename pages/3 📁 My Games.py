import streamlit as st
import pandas as pd
import time

from utils.detailed_page import detailed_page

current_page = "my_games"
tab1, tab2 = st.tabs(["Games", "Recommendation Results"])


tab1.subheader("Saved Games")
tab2.subheader("A tab with results obtained from Network Recommendation")


with tab1:
    saved_df = pd.read_csv("pages/saved_results/saved_game.csv")

    data = saved_df[["BGGId","Name","MinPlayers","MaxPlayers","MfgPlaytime","GameWeight","MfgAgeRec","AvgRating"]].copy()

    players=[]
    for i in range(len(data)):
        player_str = "{} - {}".format(data["MinPlayers"][i],data["MaxPlayers"][i])
        players.append(player_str)
    data["Players"]=players

    data_col_dict = {"Name":"Name","Players":"Players","MfgPlaytime":"Playtime",
                    "GameWeight":"Difficulty","MfgAgeRec":"Age","AvgRating": "Ratings","Button":"Button"}
    
    columns_list = st.columns([2,1,1,1,1,1,2])
    for i, column in enumerate(list(columns_list)):
        with column:
            st.markdown("**{}**".format(list(data_col_dict.values())[i]))


    button_list = []

    for data_idx in range(len(data)):
        columns_list = st.columns([2,1,1,1,1,1,2])
        for i, column in enumerate(list(columns_list[:-1])):
            with column:
                st.write(data[list(data_col_dict.keys())[i]][data_idx])
    
        with columns_list[-1]:
            button_list.append(st.button("Delete {}".format(data_idx)))
    

    for i,button in enumerate(button_list):
        if button:
            time.sleep(1)
            saved_df = saved_df.drop([i])
            saved_df.reset_index(drop=True,inplace=True)
            saved_df.to_csv("./pages/saved_results/saved_game.csv")
            st.experimental_rerun()
        else:pass


    option = st.selectbox('See Detailed Game Page',[""]+list(data["Name"]),format_func=lambda x: 'Select an option' if x == '' else x)

    if option in list(data["Name"]):
        game_id = int(data[data["Name"]==option]["BGGId"])

        detailed_page(option,game_id,current_page)