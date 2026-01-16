import streamlit as st
import pandas as pd

st.set_page_config(page_title="Insider Threat Dashboard", layout="wide")

st.title("🔐 Insider Threat Detection Dashboard")

# Load CSV data
@st.cache_data
def load_data():
    df = pd.read_csv("alerts.csv")
    return df

df = load_data()

# Summary
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Alerts", len(df))

with col2:
    st.metric("High Severity", (df["severity"] == "HIGH").sum())

with col3:
    st.metric("Medium Severity", (df["severity"] == "MEDIUM").sum())

st.subheader("📝 Alerts Table")

# Colour logic
def color_severity(val):
    if val == "HIGH":
        color = "rgba(255, 80, 80, 0.6)"  # red
    elif val == "MEDIUM":
        color = "rgba(255, 165, 0, 0.5)"  # orange
    else:
        color = "rgba(144, 238, 144, 0.5)"  # green
    return f"background-color: {color}"

st.dataframe(
    df.style.applymap(color_severity, subset=["severity"]),
    use_container_width=True
)