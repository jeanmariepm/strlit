import streamlit as st
from db import stock_sql as sql


def run():
    st.subheader("Stock Screener")
    sql.start()
