import re
import pandas as pd
from google.cloud import bigquery
from src.warehouse.client import get_bigquery_client
from src.config.warehouse import DATASET_ID, JOBS_TABLE, JOB_SKILLS_TABLE
from .dictionary import SKILL_PATTERNS

client = get_bigquery_client()

def fetch_job_descriptions():
    query = f"""
        SELECT j.job_id, j.description
        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}` j
        LEFT JOIN (
            SELECT DISTINCT job_id FROM `{client.project}.{DATASET_ID}.{JOB_SKILLS_TABLE}`
        ) s
        ON j.job_id = s.job_id
        WHERE j.description IS NOT NULL
        AND s.job_id IS NULL
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def extract_skills_from_text(text):
    matched = []
    for skill, pattern in SKILL_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            matched.append(skill)
    return matched

def run_skill_extraction():
    df = fetch_job_descriptions()

    if len(df) == 0:
        print("No new jobs to extract skills for.")
        return pd.DataFrame(columns=["job_id", "skill"])

    print(f"Scanning {len(df)} new job descriptions for skills...")

    rows = []
    for _, row in df.iterrows():
        for skill in extract_skills_from_text(row["description"]):
            rows.append({"job_id": row["job_id"], "skill": skill})

    result_df = pd.DataFrame(rows, columns=["job_id", "skill"])
    print(f"Found {len(result_df)} skill mentions across {result_df['job_id'].nunique()} new jobs.")

    table_id = f"{client.project}.{DATASET_ID}.{JOB_SKILLS_TABLE}"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        schema=[
            bigquery.SchemaField("job_id", "STRING"),
            bigquery.SchemaField("skill", "STRING"),
        ],
    )
    load_job = client.load_table_from_dataframe(result_df, table_id, job_config=job_config)
    load_job.result()
    print(f"Appended {len(result_df)} rows to {JOB_SKILLS_TABLE}.")

    return result_df