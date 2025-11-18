# 04_data-pipeline – GA4 Event Export

This folder contains the complete data extraction layer for the Siete Padel analytics project.  
It pulls **e-commerce funnel events** from Google Analytics 4 via the **GA4 Data API** using a service account.

All exported data is written to local CSV files and ignored by Git version control.

## Folder Contents

| File / Folder | Description | Version Control |
|---------------|-------------|----------------|
| `extract_ga4_events.py` | Main ETL script. Authenticates via service account, queries GA4, exports event data.
| `config_example.yaml` | Template configuration with placeholder values for onboarding.
| `config.yaml` | Local configuration containing real GA4 property ID + credential path.
| `data/` | Output folder containing generated CSV files (one per event).
| `requirements.txt` | Python dependencies required for local execution.
| `README.md` | Documentation for this pipeline. 

No credentials, tokens, raw export data, or virtual environments are committed to the repository.

## Export Scope

The script exports the following GA4 ecommerce events:

- `view_item`
- `add_to_cart`
- `begin_checkout`
- `purchase`

Each file includes the following dimensions and metrics:

| Column | Meaning |
|--------|---------|
| date | Event date (YYYYMMDD format from GA4) |
| item_name | Name of the product associated with the event |
| event_name | The exact GA4 event type |
| event_count | Number of occurrences |

Expected output files:

04_data-pipeline/data/
├─ view_item.csv
├─ add_to_cart.csv
├─ begin_checkout.csv
└─ purchase.csv

## How It Works (Process Flow)

1. Load config (`config.yaml` preferred, fallback: `config_example.yaml`)
2. Build GA4 API client from service account JSON key
3. Loop through the event list defined in configuration
4. Execute **RunReportRequest** with:
   - Metrics: `eventCount`
   - Dimensions: `date`, `itemName`, `eventName`
   - Filter by event name
5. Save results to a dedicated CSV file per event

Console output example:

Fetching: view_item
Exported: ...\data\view_item.csv
Fetching: add_to_cart
Exported: ...\data\add_to_cart.csv

## Local Execution

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r 04_data-pipeline/requirements.txt
python 04_data-pipeline/extract_ga4_events.py

google-analytics-data
google-auth
PyYAML
pandas


