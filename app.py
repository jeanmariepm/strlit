import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from plotly import graph_objs as go
import helper


# st.subheader("Query parameters")
end_date = datetime.date.today() - datetime.timedelta(days=1)
start_date = st.slider(
    "Start Data?",
    min_value=datetime.date(2010, 1, 1),
    max_value=end_date,
    value=end_date - datetime.timedelta(days=365),
    format="MM/DD/YYYY",
)

# Retrieving tickers data
tl = helper.load_tickers()
defaultTickerIndex = tl.index[tl["ABT"] == "AAPL"][0]
tickerSymbol = st.selectbox("Stock ticker", tl, index=int(defaultTickerIndex))
tickerData = yf.Ticker(tickerSymbol)  # Get ticker data

# Ticker information
col1, col2 = st.columns(2)
with col1:
    string_logo = "<img src=%s width='50' height='50'>" % tickerData.info["logo_url"]
    st.markdown(string_logo, unsafe_allow_html=True)

with col2:
    string_name = tickerData.info["longName"]
    st.header("**%s**" % string_name)

cols = st.columns(3)
attributes = [
    "targetMedianPrice",
    "currentPrice",
    "marketCap",
    "totalRevenue",
    "grossProfits",
    "trailingPE",
]
for ndx, attribute in enumerate(attributes):
    with cols[ndx % 3]:
        st.metric(f"{attribute}", f"{tickerData.info[attribute]:,.3f}")

# miscInfo = tickerData.info.keys()
# st.info(f"Misc Info: {miscInfo}")

# Ticker data
data = helper.load_data(tickerSymbol, start_date, end_date)
st.header("**Ticker data**")
helper.plot_raw_data(data)

# Options data
exps = tickerData.options
expDate = st.selectbox("Expiry Date", exps, index=3)
optionsX = pd.DataFrame()
opt = tickerData.option_chain(expDate)
opt = pd.DataFrame().append(opt.calls).append(opt.puts)
optionsX = optionsX.append(opt, ignore_index=True)


# Options data
opt_cols = [
    "contractSymbol",
    "strike",
    "lastPrice",
    "openInterest",
    "impliedVolatility",
]
filter = (optionsX["impliedVolatility"] < 1) & (optionsX["lastPrice"] > 0.1)
optionsY = optionsX[filter]
optionsY = optionsY[opt_cols]
st.header("**Options data**")
st.write(optionsY)


# App title
st.markdown(
    """
**About**
- App source code at https://github.com/jeanmariepm/strlit.git
- Built in `Python` using `streamlit`,`yfinance`, `cufflinks`, `pandas` and `datetime`
"""
)
st.write("---")
