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

**Credits**
- App built by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor))
- Built in `Python` using `streamlit`,`yfinance`, `cufflinks`, `pandas` and `datetime`
"""
)
st.write("---")

# Sidebar
st.sidebar.subheader("Query parameters")
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date.today())

# Retrieving tickers data
ticker_list = pd.read_csv(
    "https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt"
)
tickerSymbol = st.sidebar.selectbox("Stock ticker", ticker_list)  # Select ticker symbol
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
        st.metric(f"{attribute}", f"{tickerData.info[attribute]:,}")

# miscInfo = tickerData.info.keys()
# st.info(f"Misc Info: {miscInfo}")

# Ticker data
st.header("**Ticker data**")
st.write(tickerDf[["Open", "High", "Low", "Close", "Volume"]])

# Bollinger bands
st.header("**Bollinger Bands**")
qf = cf.QuantFig(tickerDf, title="First Quant Figure", legend="top", name="GS")
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

####
# st.write('---')
# st.write(tickerData.info)
