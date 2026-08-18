from src.api.clients import fetch_jobs
from src.etl.transform import transform_jobs
from src.validation.validator import validate_jobs
import pandas as pd

from src.warehouse.loader import jobs_to_dataframe, load_to_staging


response = fetch_jobs("Software Engineer")

jobs = transform_jobs(response["results"])

valid_jobs = validate_jobs(jobs)

df = jobs_to_dataframe(valid_jobs)


print(df.head())

df["posted_date"] = pd.to_datetime(df["posted_date"], utc=True)
df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
load_to_staging(df)