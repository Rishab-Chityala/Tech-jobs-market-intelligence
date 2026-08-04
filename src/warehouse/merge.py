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
    
    WHEN MATCHED THEN
    UPDATE SET
    title = S.title,
    company = S.company,
    country = S.country,
    state = S.state,
    city = S.city,
    location = S.location,
    category = S.category,
    latitude = S.latitude,
    longitude = S.longitude,
    contract_type = S.contract_type,
    description = S.description,
    posted_date = S.posted_date,
    job_url = S.job_url,
    salary_min = S.salary_min,
    salary_max = S.salary_max,
    salary_predicted = S.salary_predicted,
    ingested_at = S.ingested_at

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

def clear_staging():
    query = f"""
    TRUNCATE TABLE `{client.project}.{DATASET_ID}.{STAGING_TABLE}`
    """

    client.query(query).result()

    print("Staging table cleared.")