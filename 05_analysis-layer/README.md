# 05_analysis-layer – Funnel KPI Computation

This folder contains the analytical layer of the project.  
It processes the event exports generated in `04_data-pipeline` and computes the core funnel KPIs used later in dashboards or notebooks.

This module focuses on **metric computation**, not visualization.

## Folder Contents

| File | Description |
|------|-------------|
| `funnel_analysis.py` | CLI-based funnel analysis script. Loads GA4 event CSVs, computes KPIs, and renders an ASCII funnel. |
| `README.md` | Documentation for the analysis layer and its purpose within the architecture. |

Input data must be present in: 04_data-pipeline/data/ `view_item.csv` `add_to_cart.csv` `begin_checkout.csv` `purchase.csv`


These files are produced by `extract_ga4_events.py` in the data pipeline.

## ASCII funnel rendering

### ===== Siete Padel – Funnel Analysis =====


### Raw funnel counts:

view_item:      12

add_to_cart:    11

begin_checkout: 7

purchase:       5


### Funnel KPIs (in %):

view → cart:        91.67%

cart → checkout:    63.64%

view → purchase:    41.67%


Product views (view_item)   | ######################################## (12)

Add to cart (add_to_cart)   | ################################ (11)

Checkout (begin_checkout)   | ##################### (7)

Purchases (purchase)        | ############ (5)

## Running the Analysis

```bash
.venv\Scripts\activate
python 05_analysis-layer/funnel_analysis.py



