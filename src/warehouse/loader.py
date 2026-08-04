from dataclasses import asdict
from datetime import datetime, timezone
from google.cloud import bigquery
from .client import get_bigquery_client
from src.config.warehouse import DATASET_ID, STAGING_TABLE
import pandas as pd 

client = get_bigquery_client()

def jobs_to_dataframe(jobs):
    rows = []
    
    for job in jobs:
        row = asdict(job)
        
        row["ingested_at"] = datetime.now(timezone.utc)
        
        rows.append(row)
    
        
    return pd.DataFrame(rows)
  
def load_to_staging(df):
  table_id = f"{client.project}.{DATASET_ID}.{STAGING_TABLE}"
  
  job = client.load_table_from_dataframe(df, table_id)
  
  job.result()  
  
  print(f"Loaded {len(df)} rows into staging.")


