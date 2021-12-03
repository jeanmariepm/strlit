import streamlit as st
from db import stock_sql as sql


def run(user):
    st.subheader(f"Stock Screener for {user.username}")
    sql.start()
