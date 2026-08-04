import json

from src.models.job import Job
import json

from src.models.job import Job
from src.api.clients import fetch_jobs
from src.etl.transform import transform_jobs
from src.validation.validator import validate_jobs
from src.storage.bronze import save_raw_jobs
from src.warehouse.loader import jobs_to_dataframe, load_to_staging
import pandas as pd

def main():
    raw_jobs = fetch_jobs("Software Engineer", pages = 5)

    file_path = save_raw_jobs(raw_jobs)

    print(f"Saved raw jobs to: {file_path}")

    jobs = transform_jobs(raw_jobs)

    valid_jobs = validate_jobs(jobs)
    
    df = jobs_to_dataframe(valid_jobs)
  
    df["job_id"] = df["job_id"].astype(str)
    
    df["posted_date"] = pd.to_datetime(df["posted_date"], utc=True, errors="coerce")
    
    load_to_staging(df)

    print(f"Fetched: {len(jobs)}")
    print(f"Valid: {len(valid_jobs)}")

    
    



if __name__ == "__main__":
    main()