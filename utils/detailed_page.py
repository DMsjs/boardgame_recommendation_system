import streamlit as st
from streamlit_modal import Modal
import streamlit_wordcloud as wordcloud
import streamlit.components.v1 as components

import pandas as pd
import re

import plotly.express as px

import nltk
from nltk.corpus import stopwords

from collections import Counter

import webbrowser



def get_rating_bar_chart(Game_Name,Game_ID,df):
    # 확인 필요!!
    # Input df : 특정 Game ID에 대한 리뷰 데이터
    # Create distplot with custom bin_size
    fig = px.histogram(data, x="rating",nbins=15)

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
        top_k = st.slider("Display Records:",0,max_words,round(max_words/2))
    else:
        top_k=round(max_words/2)
    most_common_words = dict(counted_words.most_common(top_k))

    words_for_wc = []
    for keyword in most_common_words.keys():
        words_for_wc.append(dict(text=keyword, value=most_common_words[keyword]))

    
    wordcloud.visualize(words_for_wc, tooltip_data_fields={'text':'Word', 'value':'Word Count'}, per_word_coloring=False)




def detailed_page(Game_Name,Game_ID,current_page):
    # Input 데이터 확인 필요!!
    df_game = pd.read_csv("games.csv")
    df_review = pd.read_csv("games_example_data.csv")
    df_review = df_review[df_review["ID"]==Game_ID]

    st.markdown("## {}".format(Game_Name))
    col1,col2 = st.columns([1,2])

    game_row = df_game[df_game["BGGId"]==Game_ID]

    with col1:
        st.image(list(game_row["ImagePath"])[0])

    with col2:
        data_dict = {"o":["Details"],
                "Players":["{} - {}".format(list(game_row["MinPlayers"])[0],list(game_row["MaxPlayers"])[0])],
                "Play Time":["{} minute".format(list(game_row["MfgPlaytime"])[0])],
                "Difficulty":[round(list(game_row["GameWeight"])[0],3)],
                "Minimum Age":[list(game_row["MfgAgeRec"])[0]],
                "Average Rating":[round(list(game_row["AvgRating"])[0],1)]}

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
        get_rating_bar_chart(Game_Name,Game_ID,df_review)
    
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
            