import json

from src.models.job import Job
from src.api.clients import fetch_jobs
from src.etl.transform import transform_jobs
from src.validation.validator import validate_jobs

def main():
    response = fetch_jobs("Software Engineer")

    jobs = transform_jobs(response["results"])

    valid_jobs = validate_jobs(jobs)

    print(f"Fetched: {len(jobs)}")
    print(f"Valid: {len(valid_jobs)}")

    print(valid_jobs[0])



if __name__ == "__main__":
    main()