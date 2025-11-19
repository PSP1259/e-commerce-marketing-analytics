import os
import pandas as pd

# Pfad zum Data-Ordner
DATA_DIR = os.path.join("..", "04_data-pipeline", "data")

# CSV-Dateien einlesen
files = {
    "view_item": "view_item.csv",
    "add_to_cart": "add_to_cart.csv",
    "begin_checkout": "begin_checkout.csv",
    "purchase": "purchase.csv",
}

events = {}
for key, filename in files.items():
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Falls Datei leer ist → event_count = 0
        if len(df) > 0:
            events[key] = int(df["event_count"].sum())
        else:
            events[key] = 0
    else:
        events[key] = 0

# Event Counts
views = events["view_item"]
add_to_cart = events["add_to_cart"]
checkout = events["begin_checkout"]
purchase = events["purchase"]

# Funnel-Kennzahlen (Schutz bei 0-Division)
def rate(num, den):
    return round((num / den) * 100, 2) if den > 0 else 0

funnel = pd.DataFrame([
    {"Stage": "Product View", "Events": views, "Rate vs Prev": "100%"},
    {"Stage": "Add to Cart", "Events": add_to_cart, "Rate vs Prev": f"{rate(add_to_cart, views)}%"},
    {"Stage": "Checkout", "Events": checkout, "Rate vs Prev": f"{rate(checkout, add_to_cart)}%"},
    {"Stage": "Purchase", "Events": purchase, "Rate vs Prev": f"{rate(purchase, checkout)}%"},
])

print("\nAktueller Siete Funnel (GA4 Exporte)")
print(funnel)
