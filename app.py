import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime

# App title
st.markdown(
    """
# Stock Price App
Shown are the stock price data for query companies!

**About**
- App source code at https://github.com/jeanmariepm/strlit.git
- Built in `Python` using `streamlit`,`yfinance`, `cufflinks`, `pandas` and `datetime`
"""
)
st.write("---")

# Sidebar
st.sidebar.subheader("Query parameters")
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date.today())

# Retrieving tickers data
tl = pd.read_csv(
    "https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt"
)
defaultTickerIndex = tl.index[tl["ABT"] == "AAPL"][0]
tickerSymbol = st.sidebar.selectbox("Stock ticker", tl, index=int(defaultTickerIndex))
tickerData = yf.Ticker(tickerSymbol)  # Get ticker data
tickerDf = tickerData.history(
    period="1d", start=start_date, end=end_date
)  # get the historical prices for this ticker

# Ticker information
col1, col2 = st.columns(2)
with col1:
    string_logo = "<img src=%s>" % tickerData.info["logo_url"]
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
st.header("**Ticker data**")
st.line_chart(tickerDf[["Close"]])

# Bollinger bands
# st.header("**Bollinger Bands**")
# qf = cf.QuantFig(tickerDf, title="First Quant Figure", legend="top", name="GS")
# qf.add_bollinger_bands()
# fig = qf.iplot(asFigure=True)
# st.plotly_chart(fig)

####
# st.write('---')
# st.write(tickerData.info)

earlyiestExpDate = datetime.date.today() + datetime.timedelta(weeks=3)
optionsX = pd.DataFrame()
exps = (e for e in tickerData.options if e > str(earlyiestExpDate))
try:
    for e in exps:
        opt = tickerData.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt["expirationDate"] = e
        optionsX = optionsX.append(opt, ignore_index=True)
except:
    pass


# Options data
opt_cols = [
    "contractSymbol",
    "expirationDate",
    "strike",
    "lastPrice",
    "openInterest",
    "impliedVolatility",
]
filter = (optionsX["impliedVolatility"] < 1) & (optionsX["lastPrice"] > 0.01)
optionsY = optionsX[filter]
optionsY = optionsY[opt_cols]
st.header("**Options data**")
st.write(optionsY)
