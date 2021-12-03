import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

import helper
import tradier


def run(user):
    st.subheader("Stock Analyzer")
    tickerSymbol = st.text_input(
        "Stock ticker", value="AAPL", max_chars=None)
    tickerData = yf.Ticker(tickerSymbol)  # Get ticker data
    if "shortName" not in tickerData.info:
        tickerSymbol = helper.findTicker(tickerSymbol)
        if tickerSymbol:
            st.write(tickerSymbol)
            tickerData = yf.Ticker(tickerSymbol)  # Get ticker data
        else:
            st.error("Invalid ticker symbol or company name... try another")
            return

    # Ticker information
    col1, col2 = st.columns(2)
    with col1:
        logo_name = tickerData.info["logo_url"]
        if not logo_name:
            logo_name = "No image"
        string_logo = f"<img src={logo_name} width='50' height='50' >"
        st.markdown(string_logo, unsafe_allow_html=True)

    with col2:
        string_name = tickerData.info["longName"]
        st.header("**%s**" % string_name)

    cols = st.columns(6)
    attributes = [
        "targetMedianPrice",
        "currentPrice",
        "marketCap",
        "totalRevenue",
        "grossProfits",
        "trailingPE",
    ]
    if "currentPrice" not in tickerData.info:
        tickerData.info["currentPrice"] = tickerData.info["ask"]
    currentPrice = float(tickerData.info["currentPrice"])

    for ndx, attribute in enumerate(attributes):
        if attribute not in tickerData.info:
            tickerData.info[attribute] = None
        with cols[ndx % len(cols)]:
            metric = tickerData.info[attribute]
            metric = metric / 1000000 if metric and metric > 1000000 else metric
            st.write(attribute[:15])
            st.write(f"{metric:,.3f}" if metric else f"{metric}")

    # miscInfo = tickerData.info.keys()
    # st.info(f"Misc Info: {miscInfo}")

    # pick an action and run
    actions = [
        {'title': 'Options Chain', 'function': chain},
        {'title': 'Stock Trend', 'function': trend},
    ]
    action = st.selectbox("Action",
                          actions,
                          format_func=lambda action: action['title']
                          )
    # run the action
    action['function'](tickerSymbol, currentPrice)


def trend(tickerSymbol, currentPrice):
    # Ticker data
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = st.slider(
        "Start Data?",
        min_value=datetime.date(2010, 1, 1),
        max_value=end_date,
        value=end_date - datetime.timedelta(days=3*365),
        format="MM/DD/YYYY",
    )
    st.subheader('Closing price trend')
    data = helper.load_data(tickerSymbol, start_date, end_date)
    helper.plot_data(data)


def chain(tickerSymbol, currentPrice):
    # Options data
    st.header("**Options chain**")
    exps = yf.Ticker(tickerSymbol).options
    col1, col2, col3 = st.columns(3)
    with col1:
        expDate = st.selectbox("Expiry Date", exps, index=3)
    with col2:
        putCall = st.selectbox("Put/Call", ["put", "call"])
    with col3:
        defaultDelta = 75  # 35 if putCall == 'call' else 25
        delta = st.slider("delta", min_value=0, max_value=100,
                          value=defaultDelta, step=5)
    options = tradier.getOptions(tickerSymbol, expDate, putCall)
    options['currentPrice'] = currentPrice
    # Options data
    opt_cols = [
        "currentPrice",
        "strike",
        "lastPrice",
        'delta',
        "openInterest",
    ]

    deltaFilter = (options["delta"] < delta) & (options["delta"] > 100 - delta)
    options = options[deltaFilter]
    priceFilter = (options["strike"] > 0.5 *
                   currentPrice) & (options["strike"] < 1.5 * currentPrice)
    options = options[priceFilter]
    options = options[opt_cols]
    st.write(options)
