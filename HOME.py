import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image

st.title(" :telescope: Discover your board game!")


st.markdown("* * *")
st.write("**Hello! Are you looking for a new board game? However, you don't know what to choose because there are so many unknown unknowns? Well, this interactive application containing data of 20K+ games and 1M+ reviews allows you to discover a new board game that suits your need.**")
st.markdown("* * *")

st.write("๐ฅ Team 2 : ๊นํ์ข, ๋ฐ์ํ, ์ฌ์ฌ์น, ์ ํ๋ฏผ, ์กฐ์ฑ๋ฐฐ")
st.write("You can find the source code in the [SNUDV_Team2 GitHub Repository](https://github.com/DMsjs/boardgame_recommendation_system)")

landing_image=Image.open('landing image.png')
st.image(landing_image)

if 'a' not in st.session_state:
    st.session_state['a'] = []