import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Stock Dashboard", layout="wide")

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>📈 Stock Price Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interactive view of stock closing prices</p>", unsafe_allow_html=True)
st.divider()

# --- LOAD DATA ---
df = pd.read_csv("Stock_T.csv", parse_dates=["Date"])

# --- SIDEBAR ---
st.sidebar.header("🔍 Filters")
stock_list = sorted(df["Stock"].unique())
selected_stock = st.sidebar.selectbox("Select Stock", stock_list)

min_date = df["Date"].min()
max_date = df["Date"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# --- FILTER DATA ---
r = df[
    (df["Stock"] == selected_stock) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# --- MAIN CONTENT ---
col1, col2 = st.columns([3,1])

with col1:
    st.subheader(f"📊 Closing Price Trend — {selected_stock}")
    fig, ax = plt.subplots(figsize=(10,5))
    sb.lineplot(x=r["Date"], y=r["Close"], ax=ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("📌 Summary")
    st.metric("Records", len(r))
    if not r.empty:
        st.metric("Latest Close", f"{r['Close'].iloc[-1]:.2f}")
        st.metric("Highest Close", f"{r['Close'].max():.2f}")
        st.metric("Lowest Close", f"{r['Close'].min():.2f}")

# --- DOWNLOAD ---
st.divider()
st.subheader("⬇ Download Data")
csv = r.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, f"{selected_stock}_filtered.csv", "text/csv")
