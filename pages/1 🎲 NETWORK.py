import pandas as pd
import numpy as np

import streamlit as st

from streamlit_modal import Modal
import streamlit.components.v1 as components



st.markdown("# Main page")
st.sidebar.markdown("Welcome to")
st.sidebar.slider("Display Records:",0,100,50)


#row = st.sidebar.slider("Display Records:",0,100,50)

#if st.checkbox("Show original dataset"):
#    st.write(data.iloc[0:row])


tab1, tab2 = st.tabs(["Network", "Details"])
data = np.random.randn(10, 1)

tab1.subheader("A tab with a chart")
tab1.line_chart(data)

tab2.subheader("A tab with the data")
tab2.write(data)


modal = Modal("Halli Galli","mode")
open_modal = st.button("Open")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        col1,col2 = st.columns([1,2])

        with col1:
            st.image("https://cf.geekdo-images.com/kxYYgRlwM1NbHJHp62FLqg__opengraph/img/mbR9g_6T0kOKF1Me6ig6rWDJvX8=/fit-in/1200x630/filters:strip_icc()/pic458934.jpg")

        with col2:
            st.write("- Players : 2-6 players")

        st.write("Some fancy text")
        value = st.checkbox("Check me")
