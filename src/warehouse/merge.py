from .client import get_bigquery_client
from src.config.warehouse import DATASET_ID, JOBS_TABLE, STAGING_TABLE

client = get_bigquery_client()


def merge_jobs():

    query = f"""
    MERGE `{client.project}.{DATASET_ID}.{JOBS_TABLE}` T
    
    USING (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY job_id
                   ORDER BY ingested_at DESC
               ) AS rn
        FROM `{client.project}.{DATASET_ID}.{STAGING_TABLE}`
    )
    WHERE rn = 1
) S

    ON T.job_id = S.job_id

    WHEN NOT MATCHED THEN
    INSERT (
        job_id,
        title,
        company,
        country,
        state,
        city,
        location,
        category,
        latitude,
        longitude,
        contract_type,
        description,
        posted_date,
        job_url,
        salary_min,
        salary_max,
        salary_predicted,
        ingested_at
    )

    VALUES (
        S.job_id,
        S.title,
        S.company,
        S.country,
        S.state,
        S.city,
        S.location,
        S.category,
        S.latitude,
        S.longitude,
        S.contract_type,
        S.description,
        S.posted_date,
        S.job_url,
        S.salary_min,
        S.salary_max,
        S.salary_predicted,
        S.ingested_at
    )
    """

    job = client.query(query)

    job.result()

    print("Merge completed.")