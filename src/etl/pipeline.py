import pandas as pd

from src.api.clients import fetch_jobs
from src.etl.transform import transform_jobs
from src.etl.validate import validate_jobs
from src.storage.bronze import save_raw_jobs
from src.warehouse.loader import jobs_to_dataframe, load_to_staging
from src.warehouse.merge import merge_jobs, clear_staging
from config.roles import ROLES


def run_pipeline(pages: int = 3):
    print("========== TechPulse ETL ==========")

    all_roles = []
    for role in ROLES:
        print(f"\nFetching jobs for role: {role}")
        jobs = fetch_jobs(role, pages=pages)
        all_roles.extend(jobs)

    file_path = save_raw_jobs(all_roles)
    print(f"\nSaved raw jobs to: {file_path}")

    jobs = transform_jobs(all_roles)
    valid_jobs = validate_jobs(jobs)

    df = jobs_to_dataframe(valid_jobs)
    df["job_id"] = df["job_id"].astype(str)
    df["posted_date"] = pd.to_datetime(df["posted_date"], utc=True, errors="coerce")

    load_to_staging(df)

    print(f"Fetched: {len(jobs)}")
    print(f"Valid: {len(valid_jobs)}")

    merge_jobs()
    clear_staging()

    print("\nPipeline completed successfully.")