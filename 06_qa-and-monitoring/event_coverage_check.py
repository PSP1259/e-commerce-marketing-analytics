"""
Basic QA script to validate that the GA4 export files exist
and contain non-empty data.

This ensures the data pipeline (04_data-pipeline) has produced
valid output before running any analysis or dashboards.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "04_data-pipeline", "data")

REQUIRED_EVENTS = [
    "view_item",
    "add_to_cart",
    "begin_checkout",
    "purchase",
]


def check_event_file(event_name):
    file_path = os.path.join(DATA_DIR, f"{event_name}.csv")

    if not os.path.exists(file_path):
        return f"❌ Missing file: {event_name}.csv"

    df = pd.read_csv(file_path)

    if df.empty:
        return f"⚠️ Empty file: {event_name}.csv (0 rows)"

    if "event_count" in df.columns and df['event_count'].sum() == 0:
        return f"⚠️ No event_count values: {event_name}.csv (all zero)"

    return f"✔ OK: {event_name}.csv ({len(df)} rows)"


def main():
    print("\n===== Siete Padel – QA: Event Coverage Check =====\n")

    for event in REQUIRED_EVENTS:
        result = check_event_file(event)
        print(result)

    print("\nEvent coverage check complete.\n")


if __name__ == "__main__":
    main()
