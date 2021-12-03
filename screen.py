import streamlit as st
import pandas as pd
from db.stock_sql import StockSql

SS = StockSql()


def run(user):
    st.subheader(f"TBD Stock Screener for {user.username}")
