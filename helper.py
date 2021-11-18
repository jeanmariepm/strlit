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


@st.cache
def load_tickers():
    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    mycols = table[0][["Symbol"]]
    etfs = ["QQQ", "SPY"]
    etf_dict = [{"Symbol": etf} for etf in etfs]
    return mycols.append(etf_dict, ignore_index=True)


def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="stock_open"))
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="stock_close"))
    fig.layout.update(
        title_text="Time Series data with Rangeslider", xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig)
