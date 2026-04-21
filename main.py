import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Market Dashboard", layout="wide")

st.title("📊 NIFTY 50 & SENSEX Dashboard")

TICKERS = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN"
}

st.sidebar.header("Settings")
period = st.sidebar.selectbox("Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"], index=2)
interval = st.sidebar.selectbox("Interval", ["5m", "15m", "1h", "1d"], index=3)

@st.cache_data
def load_data(ticker):
    return yf.download(ticker, period=period, interval=interval, progress=False)

col1, col2 = st.columns(2)

for i, (name, ticker) in enumerate(TICKERS.items()):
    data = load_data(ticker)

    # ✅ Proper empty check
    if data is not None and not data.empty:

        # ✅ Always use iloc
        latest_price = float(data['Close'].iloc[-1])
        prev_price = float(data['Close'].iloc[-2]) if len(data) > 1 else latest_price

        change = latest_price - prev_price
        pct_change = (change / prev_price) * 100 if prev_price != 0 else 0

        col = col1 if i == 0 else col2

        with col:
            st.subheader(name)

            st.metric(
                "Current Price",
                f"{latest_price:.2f}",
                f"{change:.2f} ({pct_change:.2f}%)"
            )

            # Plotly chart
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Close'
            ))

            fig.update_layout(template="plotly_dark", height=400)

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning(f"No data for {name}")
