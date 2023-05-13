from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from prefect_gcp import GcpCredentials

def extract_from_gcs(colol: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"

@flow()
def etl_dgc_to_bq():
    """ETL floe to load data to BigQuerry"""
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
