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
defaultTickerIndex = tl.index[tl["Symbol"] == "AAPL"][0]
tickerSymbol = st.selectbox("Stock ticker", tl, index=int(defaultTickerIndex))
tickerData = yf.Ticker(tickerSymbol)  # Get ticker data

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

cols = st.columns(3)
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

for ndx, attribute in enumerate(attributes):
    if attribute not in tickerData.info:
        tickerData.info[attribute] = None
    with cols[ndx % 3]:
        metric = tickerData.info[attribute]
        if metric:
            st.metric(f"{attribute}", f"{metric:,.3f}")
        else:
            st.metric(f"{attribute}", f"{metric}")

# miscInfo = tickerData.info.keys()
# st.info(f"Misc Info: {miscInfo}")

# Ticker data
data = helper.load_data(tickerSymbol, start_date, end_date)
helper.plot_raw_data(data)

# Options data
st.header("**Options chain**")
exps = tickerData.options
col1, col2 = st.columns(2)
with col1:
    expDate = st.selectbox("Expiry Date", exps, index=3)
with col2:
    putCall = st.selectbox("Put/Call", ["Put", "Call"])
options = helper.getOptions(tickerSymbol, expDate, putCall)


# Options data
opt_cols = [
    "strike",
    "lastPrice",
    "openInterest",
    "impliedVolatility",
]
filter = (options["impliedVolatility"] < 1) & (options["lastPrice"] > 0.1)
optionsY = options[filter]
optionsY = optionsY[opt_cols]
st.write(optionsY)


# App title
st.markdown(
    """
**About**
- App source code <a href='https://github.com/jeanmariepm/strlit.git'>here </a>
- Built in `Python` using `streamlit`,`yfinance`, `plotly`, `pandas` and more
""",
    unsafe_allow_html=True,
)
st.write("---")
