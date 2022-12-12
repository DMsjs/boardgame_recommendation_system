import streamlit as st
from streamlit_modal import Modal
import streamlit_wordcloud as wordcloud
import streamlit.components.v1 as components

import pandas as pd
import re

import plotly.express as px

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


from collections import Counter

import webbrowser

import sys
sys.path.append('./utils/')
from get_from_api import review_data
import requests


def get_rating_bar_chart(Game_Name,Game_ID):
    # 확인 필요!!
    # Input df : 특정 Game ID에 대한 리뷰 데이터
    # Create distplot with custom bin_size
    data = review_data(id=Game_ID, content='rating')
    fig = px.histogram(data, labels={"value": "rating"}, nbins=15)

    # Plot
    st.plotly_chart(fig, use_container_width=True)



def get_wordcloud_chart(Game_ID, df,current_page):
    # 확인 필요!!
    # Input df : 특정 Game ID에 대한 리뷰 데이터

    all_str = " ".join(list(df[df["lang"]=="en"]["comment"])).lower()
    preprocessed_words = re.sub("[^a-z]"," ",all_str).split()

    #Remove STOPWORDS 
    stops = set(stopwords.words('english'))
    stops.add("game")
    stops.add("play")
    stops.add("player")
    stops.add("played")
    stops.add("playing")


    no_stops = [word for word in preprocessed_words if not word in stops]

    #LEMMATIZING
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in no_stops]
    lemmatized_words = [word for word in lemmatized_words if not word in stops]

    #Remove Short words
    final_words = [word for word in lemmatized_words if len(word)>2]

    counted_words = Counter(final_words)

    if len(counted_words)>50:
        max_words = 50
    else:
        max_words=len(counted_words)
    
    if current_page == "search" :
        if max_words != 0:
            top_k = st.slider("Display Records:",0,max_words,round(max_words/2))
        else:
            top_k = 0
            st.write('No reviews')
    else:
        top_k=round(max_words/2)
    most_common_words = dict(counted_words.most_common(top_k))

    words_for_wc = []
    for keyword in most_common_words.keys():
        words_for_wc.append(dict(text=keyword, value=most_common_words[keyword]))
        
    wordcloud.visualize(words_for_wc, tooltip_data_fields={'text':'Word', 'value':'Word Count'}, per_word_coloring=False)




def detailed_page(Game_Name,Game_ID,current_page):
    # Input 데이터 확인 필요!!
    df_game = pd.read_csv("./data/games.csv")
    dict_game = requests.get('http://147.46.94.205:8000/api?data-source=games&game-id='+str(Game_ID)).json()


    # df_review = pd.read_csv("./data/games_example_data.csv")
    # df_review = df_review[df_review["ID"]==Game_ID]
    df_review = review_data(id=Game_ID)

    st.markdown("## {}".format(Game_Name))
    col1,col2 = st.columns([1,2])

    game_row = df_game[df_game["BGGId"]==Game_ID]

    with col1:
        st.image(dict_game["ImagePath"])

    with col2:
        data_dict = {"o":["Details"],
                "Players":["{} - {}".format(dict_game["MinPlayers"],dict_game["MaxPlayers"])],
                "Play Time":["{} minute".format(dict_game["MfgPlaytime"])],
                "Difficulty":[round(dict_game["GameWeight"],3)],
                "Minimum Age":[dict_game["MfgAgeRec"]],
                "Average Rating":[round(dict_game["AvgRating"],1)]}

        data= pd.DataFrame(data_dict).set_index("o").T
        st.table(data)
        
        saved_df = pd.read_csv("./pages/saved_results/saved_game.csv")

        if Game_ID in list(saved_df["BGGId"]):
            save_button=st.button("Unsave this game")
            if save_button:
                saved_df=saved_df.drop(saved_df[saved_df["BGGId"]==Game_ID].index)
                saved_df.reset_index(drop=True,inplace=True)
                saved_df.to_csv("./pages/saved_results/saved_game.csv")
                st.experimental_rerun()

        
        else:
            save_button=st.button("Save this game")
            if save_button:
                saved_df=pd.concat([saved_df,df_game[df_game["BGGId"]==Game_ID]])
                saved_df.reset_index(drop=True,inplace=True)
                saved_df.to_csv("./pages/saved_results/saved_game.csv")
                st.experimental_rerun()



    but_col1, but_col2, but_col3 = st.columns(3)
    with but_col1:
        pass
    with but_col2:
        buy_button=st.button("Buy This Game")
        if buy_button:
            webbrowser.open("https://search.shopping.naver.com/search/all?query={}".format(Game_Name))
    with but_col3:
        play_button=st.button("Watch on Youtube")
        if play_button:
            webbrowser.open("https://www.youtube.com/results?search_query=How to Play {}".format(Game_Name))
    

    

    if current_page =="network": 
        pass
    else:
        st.markdown("### Rating Distribution")
        get_rating_bar_chart(Game_Name,Game_ID)

    
    st.markdown("### Review Wordcloud")
    df_review.dropna(subset=["comment"],inplace=True)
    if len(df_review)>20:
        get_wordcloud_chart(Game_ID, df_review,current_page)
    else:
        st.markdown("Not enough Reviews")





def make_popup(Game_Name,Game_ID,current_page):
    open_modal = st.button("Open")
    modal = Modal("Game Details","mode")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            detailed_page(Game_Name,Game_ID,current_page)

