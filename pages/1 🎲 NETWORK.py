import pandas as pd
import numpy as np

import streamlit as st

from streamlit_modal import Modal
import streamlit.components.v1 as components

from utils.detailed_page import make_popup



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

#Pop-up Module, to be modified to use Game_ID as an input
make_popup("Halli Galli")

