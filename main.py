import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Indian Market Dashboard", layout="wide")

st.title("📊 NIFTY 50 & SENSEX Dashboard (Plotly)")

# Tickers
TICKERS = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN"
}

# Sidebar
st.sidebar.header("Settings")
period = st.sidebar.selectbox("Select Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"], index=2)
interval = st.sidebar.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d"], index=4)

# Load data
@st.cache_data
def load_data(ticker, period, interval):
    return yf.download(ticker, period=period, interval=interval, progress=False)

col1, col2 = st.columns(2)

for i, (name, ticker) in enumerate(TICKERS.items()):
    data = load_data(ticker, period, interval)

    if not data.empty:
        latest_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2] if len(data) > 1 else latest_price
        change = latest_price - prev_price
        pct_change = (change / prev_price) * 100 if prev_price != 0 else 0

        col = col1 if i == 0 else col2

        with col:
            st.subheader(name)

            # Metric
            st.metric(
                label="Current Price",
                value=f"{latest_price:.2f}",
                delta=f"{change:.2f} ({pct_change:.2f}%)"
            )

            # 📈 Plotly Line Chart
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Close Price'
            ))

            fig.update_layout(
                title=f"{name} Price Chart",
                xaxis_title="Date",
                yaxis_title="Price",
                template="plotly_dark",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

            # Optional: Candlestick toggle
            if st.checkbox(f"Show Candlestick for {name}", key=name):
                fig_candle = go.Figure(data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close']
                )])

                fig_candle.update_layout(
                    title=f"{name} Candlestick Chart",
                    template="plotly_dark",
                    height=500
                )

                st.plotly_chart(fig_candle, use_container_width=True)

            # Data
            with st.expander("Show Data"):
                st.dataframe(data.tail(50))

    else:
        st.warning(f"No data available for {name}")
