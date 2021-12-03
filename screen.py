import streamlit as st
import pandas as pd
from db.stock_sql import StockSql

SS = StockSql()


def run(user):
    st.subheader(f"Stock Screener for {user.username}")
    members = SS.listMembers()
    st.write(members)
