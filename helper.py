from requests.api import options
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from plotly import graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from py_vollib_vectorized import price_dataframe, get_all_greeks
import util
import logging
logging.getLogger('fbprophet').setLevel(logging.WARNING)


@st.cache
def load_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data


@st.cache
def getOptions(tickerSymbol, expDate, putCall, currentPeice):
    options = pd.DataFrame()
    opt = yf.Ticker(tickerSymbol).option_chain(expDate)
    if putCall == "Put":
        opt = pd.DataFrame().append(opt.puts)
    else:
        opt = pd.DataFrame().append(opt.calls)
    options = options.append(opt, ignore_index=True)
    year_fraction = (
        datetime.datetime.strptime(
            expDate, "%Y-%m-%d") - datetime.datetime.now()
    ).days / 365
    options['Flag'] = putCall[0].lower()
    options['S'] = currentPeice
    options['K'] = options['strike']
    options['T'] = year_fraction
    options['R'] = 0.04
    options['IV'] = options['impliedVolatility']
    result = price_dataframe(options, flag_col='Flag', underlying_price_col='S', strike_col='K', annualized_tte_col='T',
                             riskfree_rate_col='R', sigma_col='IV', model='black_scholes', inplace=False)
    options['delta'] = abs(result['delta'])*100
    return options


@ st.cache
def load_tickers():
    table = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    mycols = table[0][["Symbol"]]
    etfs = ["QQQ", "SPY"]
    etf_dict = [{"Symbol": etf} for etf in etfs]
    return mycols.append(etf_dict, ignore_index=True)


def plot_data(data):
    # Predict forecast with Prophet.
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    prophet = Prophet()
    with util.suppress_stdout_stderr():
        prophet.fit(df_train)
        future = prophet.make_future_dataframe(periods=90)
        forecast = prophet.predict(future)
        fig1 = plot_plotly(prophet, forecast)
        st.plotly_chart(fig1)


def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"],
                  y=data["Open"], name="stock_open"))
    fig.add_trace(go.Scatter(x=data["Date"],
                  y=data["Close"], name="stock_close"))
    fig.layout.update(
        title_text="Time Series data with Rangeslider", xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig)


class StopExecution(Exception):
    pass
