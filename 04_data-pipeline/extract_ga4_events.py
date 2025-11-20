# GA4 Events Extraction Script
# This script reads cofiguration form config.yaml (config_example.yaml as fallback), authenticates against the GA4 Data API using a service account and exports specified events within a date range to CSV files.

import os # operating system functions
import yaml # YAML file parsing
import pandas as pd # row and column data manipulation csv export

from google.analytics.data_v1beta import BetaAnalyticsDataClient # GA4 Data API client library
from google.analytics.data_v1beta.types import ( # request-object types to the GA4 Data API
    RunReportRequest,
    DateRange,
    Metric,
    Dimension,
    Filter,
    FilterExpression, 
)
from google.oauth2 import service_account  # service account authentication

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # base directory of the script, advantage: works independent of the current working directory


def load_config(): # load configuration from config.yaml or config_example.yaml
    if os.path.exists(os.path.join(BASE_DIR, "config.yaml")):
        config_path = os.path.join(BASE_DIR, "config.yaml")
    else:
        config_path = os.path.join(BASE_DIR, "config_example.yaml") # fallback for repositories git-ignored config.yaml

    with open(config_path, "r", encoding="utf-8") as f: # open and read the config file
        return yaml.safe_load(f)


def get_client(key_file): # authenticate against GA4 Data API using service account key file
    credentials = service_account.Credentials.from_service_account_file(key_file) # load service account credentials from JSON key file
    return BetaAnalyticsDataClient(credentials=credentials) # create GA4 Data API client with the loaded credentials


def fetch_event_report(
    client: BetaAnalyticsDataClient,
    property_id: str,
    event_name: str,
    start_date: str,
    end_date: str,
):
    """
    Request an event level GA4 report for a single event name.

    The report returns:
    - one row per date and eventName
    - metric: eventCount

    Important:
    We deliberately do not request itemName here, because itemName is item scoped
    and eventCount is event scoped. This combination is incompatible in GA4.
    """
    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[
            # How often the event was triggered
            Metric(name="eventCount"),
        ],
        dimensions=[
            # Aggregation per calendar date
            Dimension(name="date"),
            # Keep the eventName in case we reuse this function with multiple events later
            Dimension(name="eventName"),
        ],
        date_ranges=[
            DateRange(start_date=start_date, end_date=end_date),
        ],
        # Only keep rows for the specific event we are interested in
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter=Filter.StringFilter(value=event_name),
            )
        ),
    )
    return client.run_report(request) # execute the report request and return the response


def save_report_to_csv(report, event_name: str, output_folder: str) -> None:
    """
    Convert a GA4 API response into a pandas DataFrame and write it to CSV.

    Output schema:
    - date
    - event_name
    - event_count

    One file is written per event, for example:
    data/view_item.csv
    data/add_to_cart.csv
    """
    rows = []

    # Each row in report.rows contains dimension_values and metric_values arrays
    for row in report.rows:
        rows.append(
            {
                # date is the first dimension in the RunReportRequest
                "date": row.dimension_values[0].value,
                # eventName is the second dimension
                "event_name": row.dimension_values[1].value,
                # eventCount is the first metric
                "event_count": int(row.metric_values[0].value),
            }
        )

    os.makedirs(output_folder, exist_ok=True) # # Ensure output folder exists
    output_path = os.path.join(output_folder, f"{event_name}.csv") # Create file path (e.g. data/view_item.csv)
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Exported: {output_path}")


def main(): 
    """"
    Main pipeline execution: 
    1. Load config
    2. Create GA4 API client 
    3. Loop thorugh all configured events
    4. Request event data from GA4 API 
    5. Export each event to CSV file
    """
    cfg = load_config()                                                    
    client = get_client(cfg["ga4"]["key_file"])
    property_id = cfg["ga4"]["property_id"] 
    start_date = cfg["export"]["start_date"]
    end_date = cfg["export"]["end_date"] 
    output_folder = os.path.join(BASE_DIR, cfg["export"]["output_folder"])

    events = cfg["export"]["events"]

    for event_name in events: # loop through all configured events, fetch data and export to CSV
        print(f"Fetching: {event_name}")
        report = fetch_event_report(client, property_id, event_name, start_date, end_date)
        save_report_to_csv(report, event_name, output_folder)


if __name__ == "__main__": # Execute pipeline when script is run directly
    main()