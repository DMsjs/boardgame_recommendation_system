import streamlit as st
from streamlit_modal import Modal
import streamlit_wordcloud as wordcloud

import pandas as pd
import re

import plotly.express as px

import nltk
from nltk.corpus import stopwords

from collections import Counter



def get_rating_bar_chart(Game_Name,Game_ID,df):
    data = df[df["ID"]==Game_ID]["rating"]
    st.markdown("Rating Average : {}".format(round(sum(data)/len(data),3)) )

    # Create distplot with custom bin_size
    fig = px.histogram(data, x="rating",nbins=15)

    # Plot
    st.plotly_chart(fig, use_container_width=True)



def get_wordcloud_chart(Game_ID, df):

    all_str = " ".join(list(df[df["lang"]=="en"]["comment"]))
    preprocessed_words = re.sub("[^a-z]"," ",all_str.lower()).split()

    #Remove STOPWORDS 
    stops = set(stopwords.words('english'))
    stops.add("game")
    stops.add("play")

    no_stops = [word for word in preprocessed_words if not word in stops]

    #LEMMATIZING
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in no_stops]

    #Remove Short words
    final_words = [word for word in lemmatized_words if len(word)>2]

    counted_words = Counter(final_words)


    if len(counted_words)>50:
        max_words = 50
    else:
        max_words=len(counted_words)

    top_k = st.slider("Display Records:",0,max_words,round(max_words/2))
    most_common_words = dict(counted_words.most_common(top_k))

    words_for_wc = []
    for keyword in most_common_words.keys():
        words_for_wc.append(dict(text=keyword, value=most_common_words[keyword]))

    
    wordcloud.visualize(words_for_wc, tooltip_data_fields={'text':'Word', 'value':'Word Count'}, per_word_coloring=False)



def detailed_page(Game_Name,Game_ID, df_game,df_review):

    st.markdown("## {}".format(Game_Name))
    col1,col2 = st.columns([1,2])

    game_row = df_game[df_game["BGGId"]==Game_ID]

    with col1:
        st.image(list(game_row["ImagePath"])[0])

    with col2:
        st.write("- Players : {}-{} players".format(list(game_row["MinPlayers"])[0],list(game_row["MaxPlayers"])[0]))
        st.write(list(game_row["Description"])[0])


    col1_g,col2_g = st.columns([1,1])

    with col1_g:
        st.markdown("### Rating Distribution")
        get_rating_bar_chart(Game_Name,Game_ID,df_review)

    with col2_g:
        st.markdown("### Review Wordcloud")
        df_review.dropna(subset=["comment"],inplace=True)
        if len(df_review)>20:
            get_wordcloud_chart(Game_ID, df_review)
        else:
            st.markdown("Not enough Reviews")



    save_button=st.button("Save this game")
    modal = Modal("Saved","mode")
    if save_button:
        modal.open()
    if modal.is_open():
        with modal.container():
            st.markdown( "**{}** saved".format(Game_Name))


def make_popup(Game_ID,df):
    open_modal = st.button("Open")
    modal = Modal(Game_id,"mode")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            detailed_page(Game_ID,df)
            