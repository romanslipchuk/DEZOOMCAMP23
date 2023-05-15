from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from prefect_gcp import GcpCredentials
from datetime import timedelta

@task(log_prints=True, 
      retries=3,
      cache_key_fn=task_input_hash,
      cache_expiration=timedelta(days=1))
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("de-zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path)
    return Path(f"{gcs_path}")


@task(log_prints=True, retries=3)
def transform(path: Path) -> pd.DataFrame:
    """data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df.passenger_count.isna().sum()}")
    df.passenger_count.fillna(0,inplace=True)
    print(f"post: missing passenger count: {df.passenger_count.isna().sum()}")
    return df

@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
    """Write df to BigQuerry"""
    gcp_credentials_block = GcpCredentials.load("gcp-key")

    df.to_gbq(
        destination_table="de_zoom_camp.yellow_rides",
        project_id="dtc-de-course-384415",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow()
def etl_dgc_to_bq():
    """ETL flow to load data to BigQuerry"""
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)




if __name__ == "__main__":
    etl_dgc_to_bq()

