import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.title("📊 Stock Price Dashboard")

# ✅ Load your CSV
df = pd.read_csv("Stock_T.csv", parse_dates=["Date"])

# Show available stocks
st.subheader("Select a Stock")
stock_list = df["Stock"].unique()
selected_stock = st.selectbox("Choose a stock", stock_list)

# Filter
r = df[df["Stock"] == selected_stock]

# Plot
st.subheader(f"Closing Price Trend for {selected_stock}")
fig, ax = plt.subplots(figsize=(10,5))
sb.lineplot(x=r["Date"], y=r["Close"], ax=ax)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Download CSV
st.subheader("Download Filtered Data")
csv = r.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f"{selected_stock}_data.csv",
    mime="text/csv"
)
