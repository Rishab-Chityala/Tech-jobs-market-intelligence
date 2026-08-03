import json

from src.models.job import Job
import json

from src.models.job import Job
from src.api.clients import fetch_jobs
from src.etl.transform import transform_jobs
from src.validation.validator import validate_jobs
from src.storage.bronze import save_raw_jobs
from src.warehouse.loader import jobs_to_rows, load_jobs

def main():
    response = fetch_jobs("Software Engineer")

    file_path = save_raw_jobs(response)

    print(f"Saved raw jobs to: {file_path}")

    jobs = transform_jobs(response["results"])

    valid_jobs = validate_jobs(jobs)
    
    rows = jobs_to_rows(valid_jobs)
    
    load_jobs(rows)

    print(f"Fetched: {len(jobs)}")
    print(f"Valid: {len(valid_jobs)}")

    print(valid_jobs[0])



if __name__ == "__main__":
    main()