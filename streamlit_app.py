import streamlit as st

pg = st.navigation([
    st.Page('pages/main.py', title="Анализ акций Nasdaq"),
    st.Page('pages/first_page.py', title="Анализ чаевых"),
])

pg.run()