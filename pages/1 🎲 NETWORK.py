import pandas as pd
import numpy as np

import networkx as nx
from pyvis.network import Network

import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components

from utils.detailed_page import make_popup


st.markdown("# Main page")
st.sidebar.markdown("Welcome to")
# st.sidebar.slider("Display Records:",0,100,50)


#row = st.sidebar.slider("Display Records:",0,100,50)

#if st.checkbox("Show original dataset"):
#    st.write(data.iloc[0:row])


tab1, tab2 = st.tabs(["Network", "Details"])
data = np.random.randn(10, 1)

# tab1.subheader("A tab with a chart")
# tab1.line_chart(data)

### Graph
# Read dataset (CSV)
df_interact = pd.read_csv('example/data_drug/processed_drug_interactions.csv')


# Define list of selection options and sort alphabetically
drug_list = ['Metformin', 'Glipizide', 'Lisinopril', 'Simvastatin',
            'Warfarin', 'Aspirin', 'Losartan', 'Ibuprofen']
drug_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
selected_drugs = st.multiselect('Select drug(s) to visualize', drug_list)

# Set info message on initial site load
if len(selected_drugs) == 0:
    st.text('Choose at least 1 drug to start')

# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['drug_1_name'].isin(selected_drugs) | \
                                df_interact['drug_2_name'].isin(selected_drugs)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'drug_1_name', 'drug_2_name', 'weight')

    # Initiate PyVis network object
    drug_net = Network(
                       height='400px',
                       width='100%',
                       bgcolor='#222222',
                       font_color='white'
                      )

    # 대표 node coloring
    for node in G:
        if node in selected_drugs:
            drug_net.add_node(node, color='#FFFFFF', size=30)

    # 사용자가 지정한 node 정보 (대표 node 3개)
    for i in selected_drugs:
        print(i)
    print()

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

    # Generate network with specific layout settings
    drug_net.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)


tab2.subheader("A tab with the data")
tab2.write(data)

#Pop-up Module, to be modified to use Game_ID as an input
make_popup("Halli Galli")

