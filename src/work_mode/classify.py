import re
import pandas as pd
from google.cloud import bigquery
from src.warehouse.client import get_bigquery_client
from src.config.warehouse import DATASET_ID, JOBS_TABLE, JOB_WORK_MODE_TABLE
from .dictionary import WORK_MODE_PATTERNS

client = get_bigquery_client()

def fetch_job_text():
    query = f"""
        SELECT 
        j.job_id,
        COALESCE(j.description, '') as description,
        COALESCE(j.location, '') as location

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}` j
        LEFT JOIN (
            SELECT DISTINCT job_id FROM `{client.project}.{DATASET_ID}.{JOB_WORK_MODE_TABLE}`
        ) w
        ON j.job_id = w.job_id
        WHERE w.job_id IS NULL
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def classify_work_mode(text):
    matched = set()
    for label, patterns in WORK_MODE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matched.add(label)
                break
    if len(matched) == 0:
        return "Unspecified"
    if len(matched) == 1:
        return matched.pop()
    return "Mixed/Unclear"

def run_work_mode_classification():
    df = fetch_job_text()

    if len(df) == 0:
        print("No new jobs to classify work mode for.")
        return pd.DataFrame(columns=["job_id", "work_mode"])

    print(f"Classifying work mode for {len(df)} new jobs...")

    rows = []
    for _, row in df.iterrows():
        combined_text = f"{row['description']} {row['location']}"
        label = classify_work_mode(combined_text)
        rows.append({"job_id": row["job_id"], "work_mode": label})

    result_df = pd.DataFrame(rows, columns=["job_id", "work_mode"])
    print(result_df["work_mode"].value_counts())

    table_id = f"{client.project}.{DATASET_ID}.{JOB_WORK_MODE_TABLE}"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        schema=[
            bigquery.SchemaField("job_id", "STRING"),
            bigquery.SchemaField("work_mode", "STRING"),
        ],
    )
    load_job = client.load_table_from_dataframe(result_df, table_id, job_config=job_config)
    load_job.result()
    print(f"Appended {len(result_df)} rows to {JOB_WORK_MODE_TABLE}.")

    return result_df