"""
Funnel analysis module for GA4 event data exported by 04_data-pipeline.

Reads CSV exports (view_item, add_to_cart, begin_checkout, purchase)
and computes simple funnel KPIs. Outputs a textual summary and an
ASCII-style funnel to the terminal.
"""

import os
import pandas as pd

# Base directory of this analysis module
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directory of the exported CSVs from extract_ga4_events.py
DATA_DIR = os.path.join(BASE_DIR, "..", "04_data-pipeline", "data")


def load_event_csv(event_name):
    """Load a CSV file for a single GA4 event."""
    file_path = os.path.join(DATA_DIR, f"{event_name}.csv")

    if not os.path.exists(file_path):
        print(f"Warning: No file found for event: {event_name}")
        return pd.DataFrame()

    return pd.read_csv(file_path)


def funnel_counts():
    """Aggregate basic funnel event counts from exported CSVs."""

    events = ["view_item", "add_to_cart", "begin_checkout", "purchase"]
    funnel = {}

    for event in events:
        df = load_event_csv(event)

        if df.empty:
            funnel[event] = 0
        elif "event_count" in df.columns:
            funnel[event] = int(df["event_count"].sum())
        else:
            funnel[event] = len(df)

    return funnel


def funnel_metrics():
    """Convert raw counts into funnel KPIs."""

    counts = funnel_counts()

    def safe_rate(num, den):
        return round((num / den) * 100, 2) if den > 0 else 0.0

    metrics = {
        **counts,
        "ctr_view_to_cart_pct": safe_rate(
            counts["add_to_cart"], counts["view_item"]
        ),
        "ctr_cart_to_checkout_pct": safe_rate(
            counts["begin_checkout"], counts["add_to_cart"]
        ),
        "final_conversion_rate_pct": safe_rate(
            counts["purchase"], counts["view_item"]
        ),
    }

    return metrics


def print_ascii_funnel(counts):
    """Render a simple ASCII funnel chart to the terminal."""

    stages = [
        ("Product views (view_item)", counts.get("view_item", 0)),
        ("Add to cart (add_to_cart)", counts.get("add_to_cart", 0)),
        ("Checkout (begin_checkout)", counts.get("begin_checkout", 0)),
        ("Purchases (purchase)", counts.get("purchase", 0)),
    ]

    max_count = max((c for _, c in stages), default=0)
    max_width = 40

    print("\nASCII funnel (relative size by event count):\n")

    if max_count == 0:
        print("No events available for funnel rendering.\n")
        return

    for label, count in stages:
        bar_len = int(count / max_count * max_width) if max_count > 0 else 0
        bar = "#" * bar_len
        print(f"{label:30} | {bar} ({count})")

    print()


def main():
    """Print a readable summary of funnel performance."""

    print("\n===== Siete Padel – Funnel Analysis =====\n")

    metrics = funnel_metrics()

    print("Raw funnel counts:")
    print(f"view_item:      {metrics['view_item']}")
    print(f"add_to_cart:    {metrics['add_to_cart']}")
    print(f"begin_checkout: {metrics['begin_checkout']}")
    print(f"purchase:       {metrics['purchase']}\n")

    print("Funnel KPIs (percent):")
    print(
        f"view → cart:        {metrics['ctr_view_to_cart_pct']}%"
    )
    print(
        f"cart → checkout:    {metrics['ctr_cart_to_checkout_pct']}%"
    )
    print(
        f"view → purchase:    {metrics['final_conversion_rate_pct']}%"
    )

    print_ascii_funnel(metrics)

    print("Funnel analysis complete.\n")


if __name__ == "__main__":
    main()

