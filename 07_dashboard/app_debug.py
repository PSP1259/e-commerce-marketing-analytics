import streamlit as st
import pandas as pd

st.set_page_config(page_title="Siete Padel Dashboard – Debug", layout="wide")

st.title("Debug Dashboard – Raw GA4 Event Data")

@st.cache_data
def load_raw():
    return pd.read_csv("04_data-pipeline" / "data")

df = load_raw()

st.subheader("Raw Dataset Preview")
st.dataframe(df, use_container_width=True)

st.subheader("Event Counts")
event_counts = df["event_name"].value_counts().reset_index()
event_counts.columns = ["event_name", "count"]
st.dataframe(event_counts)
