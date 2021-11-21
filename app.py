import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

import helper

st.title("Stocks with VIP")
col1, col2 = st.columns(2)
with col2:
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = st.slider(
        "Start Data?",
        min_value=datetime.date(2010, 1, 1),
        max_value=end_date,
        value=end_date - datetime.timedelta(days=3*365),
        format="MM/DD/YYYY",
    )

with col1:
    # Retrieving tickers data
    # tl = helper.load_tickers()
    # defaultTickerIndex = tl.index[tl["Symbol"] == "AAPL"][0]
    # ickerSymbol = st.selectbox("Stock ticker", tl, index=int(defaultTickerIndex))
    tickerSymbol = st.text_input("Stock ticker", value="AAPL", max_chars=None)
    tickerData = yf.Ticker(tickerSymbol)  # Get ticker data
    if "shortName" not in tickerData.info:
        st.write("Invalid ticker symbol... try another")
        raise helper.StopExecution


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
        attribute[:15]
        f"{metric:,.3f}" if metric else f"{metric}"

# miscInfo = tickerData.info.keys()
# st.info(f"Misc Info: {miscInfo}")

# Ticker data
st.subheader('Closing price trend')
data = helper.load_data(tickerSymbol, start_date, end_date)
helper.plot_data(data)

# Options data
st.header("**Options chain**")
exps = tickerData.options
col1, col2, col3 = st.columns(3)
with col1:
    expDate = st.selectbox("Expiry Date", exps, index=3)
with col2:
    putCall = st.selectbox("Put/Call", ["Put", "Call"])
with col3:
    roi = st.slider("ROI", min_value=1, max_value=35, value=15, step=1)
options = helper.getOptions(tickerSymbol, expDate, putCall, currentPrice)


# Options data
opt_cols = [
    "strike",
    "lastPrice",
    "ROI",
    "impliedVolatility",
    "openInterest",
]
roiFilter = options["ROI"] >= roi
putFilter = options["strike"] < 1.1 * currentPrice
callFilter = options["strike"] > 0.9 * currentPrice

optionsY = options[roiFilter]
if putCall == "Put":
    optionsY = optionsY[putFilter]
else:
    optionsY = optionsY[callFilter]
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
