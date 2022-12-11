import streamlit as st
from streamlit_modal import Modal
import streamlit_wordcloud as wordcloud


def detailed_page(Game_id):

    st.markdown("## {}".format(Game_id))
    col1,col2 = st.columns([1,2])

    with col1:
        st.image("https://cf.geekdo-images.com/kxYYgRlwM1NbHJHp62FLqg__opengraph/img/mbR9g_6T0kOKF1Me6ig6rWDJvX8=/fit-in/120git0x630/filters:strip_icc()/pic458934.jpg")

    with col2:
        st.write("- Players : 2-6 players")

    words = [
        dict(text="Robinhood", value=16000, color="#b5de2b", country="US", industry="Cryptocurrency"),
        dict(text="Personio", value=8500, color="#b5de2b", country="DE", industry="Human Resources"),
        dict(text="Boohoo", value=6700, color="#b5de2b", country="UK", industry="Beauty"),
        dict(text="Deliveroo", value=13400, color="#b5de2b", country="UK", industry="Delivery"),
        dict(text="SumUp", value=8300, color="#b5de2b", country="UK", industry="Credit Cards"),
        dict(text="CureVac", value=12400, color="#b5de2b", country="DE", industry="BioPharma"),
        dict(text="Deezer", value=10300, color="#b5de2b", country="FR", industry="Music Streaming"),
        dict(text="Eurazeo", value=31, color="#b5de2b", country="FR", industry="Asset Management"),
        dict(text="Drift", value=6000, color="#b5de2b", country="US", industry="Marketing Automation"),
        dict(text="Twitch", value=4500, color="#b5de2b", country="US", industry="Social Media"),
        dict(text="Plaid", value=5600, color="#b5de2b", country="US", industry="FinTech"),
    ]

    wordcloud.visualize(words, tooltip_data_fields={
        'text':'Company', 'value':'Mentions', 'country':'Country of Origin', 'industry':'Industry'
    }, per_word_coloring=False)

    save_button=st.button("Save this game")
    modal = Modal("Saved","mode")
    if save_button:
        modal.open()
    if modal.is_open():
        with modal.container():
            st.markdown( "**{}** saved".format(Game_id))


def make_popup(Game_id):
    open_modal = st.button("Open")
    modal = Modal(Game_id,"mode")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            detailed_page(Game_id)
            









