import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from plotly import graph_objs as go


@st.cache
def load_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data


def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="stock_open"))
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="stock_close"))
    fig.layout.update(
        title_text="Time Series data with Rangeslider", xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig)
