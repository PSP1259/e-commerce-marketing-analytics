import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Siete Padel Dashboard – Debug", layout="wide")

st.title("Debug Dashboard – Raw GA4 Event Data")

@st.cache_data
def load_raw():
    # load ALL event CSV files and combine them
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "04_data-pipeline" / "data"

    # read all CSVs in folder
    csv_files = list(data_dir.glob("*.csv"))

    if not csv_files:
        return pd.DataFrame()

    df_list = []
    for f in csv_files:
        temp = pd.read_csv(f)
        temp["source_file"] = f.name
        df_list.append(temp)

    return pd.concat(df_list, ignore_index=True)

df = load_raw()

st.subheader("Raw Dataset Preview")
st.dataframe(df, use_container_width=True)

if "event_name" in df.columns:
    st.subheader("Event Counts")
    event_counts = df["event_name"].value_counts().reset_index()
    event_counts.columns = ["event_name", "count"]
    st.dataframe(event_counts)
else:
    st.info("Column 'event_name' not found in dataset.")
