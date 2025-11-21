from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Siete Padel Funnel Dashboard", layout="wide")
st.title("Siete Padel – Funnel Dashboard")
st.caption("Powered by GA4 daily exports and the 04_data-pipeline")

EVENTS = ["view_item", "add_to_cart", "begin_checkout", "purchase"]

@st.cache_data
def load_event_csv(event_name: str) -> pd.DataFrame:
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "04_data-pipeline" / "data"
    file_path = data_dir / f"{event_name}.csv"

    if not file_path.exists():
        return pd.DataFrame()

    df = pd.read_csv(file_path)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d", errors="coerce")
    if "event_count" not in df.columns:
        df["event_count"] = 1

    return df

@st.cache_data
def load_all_events():
    return {e: load_event_csv(e) for e in EVENTS}

data = load_all_events()

def total_count(df: pd.DataFrame) -> int:
    return int(df["event_count"].sum()) if not df.empty else 0

st.subheader("Funnel KPIs")

kpis = {
    "Product Views": total_count(data["view_item"]),
    "Add to Cart": total_count(data["add_to_cart"]),
    "Checkout Starts": total_count(data["begin_checkout"]),
    "Purchases": total_count(data["purchase"]),
}

col1, col2, col3, col4 = st.columns(4)
for col, (name, value) in zip([col1, col2, col3, col4], kpis.items()):
    col.metric(label=name, value=value)

st.divider()
st.subheader("Daily Funnel Trend")

trend_frames = []
for e, df in data.items():
    if not df.empty and "date" in df.columns:
        g = df.groupby("date", as_index=False)["event_count"].sum()
        g["event"] = e
        g.rename(columns={"event_count": "count"}, inplace=True)
        trend_frames.append(g)

if trend_frames:
    df_trend = pd.concat(trend_frames, ignore_index=True).sort_values("date")
    fig = px.line(df_trend, x="date", y="count", color="event", markers=True, title="Daily Funnel Trend")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No date data found in exports.")

st.divider()
st.subheader("Raw data preview")

event_choice = st.selectbox("Select event", EVENTS)
df_preview = data.get(event_choice, pd.DataFrame())

if not df_preview.empty:
    st.dataframe(df_preview.head(100), use_container_width=True)
else:
    st.info(f"No data available for {event_choice}.")
