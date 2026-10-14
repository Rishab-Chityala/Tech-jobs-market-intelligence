JOB_SCHEMA = [
    bigquery.SchemaField("job_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("company", "STRING"),
    bigquery.SchemaField("country", "STRING"),
    bigquery.SchemaField("state", "STRING"),
    bigquery.SchemaField("city", "STRING"),
    bigquery.SchemaField("location", "STRING"),
    bigquery.SchemaField("category", "STRING"),
    bigquery.SchemaField("latitude", "FLOAT"),
    bigquery.SchemaField("longitude", "FLOAT"),
    bigquery.SchemaField("contract_type", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("posted_date", "TIMESTAMP"),
    bigquery.SchemaField("job_url", "STRING"),
    bigquery.SchemaField("salary_min", "FLOAT"),
    bigquery.SchemaField("salary_max", "FLOAT"),
    bigquery.SchemaField("salary_predicted", "BOOLEAN"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP"),
]

JOB_SKILLS_SCHEMA = [
    bigquery.SchemaField("job_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("skill", "STRING", mode="REQUIRED"),
]

JOB_WORK_MODE_SCHEMA = [
    bigquery.SchemaField("job_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("work_mode", "STRING", mode="REQUIRED"),
]

def create_table(table_name: str, schema=JOB_SCHEMA):
    table_id = f"{client.project}.{DATASET_ID}.{table_name}"
    table = bigquery.Table(table_id, schema=schema)

    try:
        client.get_table(table_id)
        print(f"{table_name} already exists.")
    except Exception:
        client.create_table(table)
        print(f"{table_name} created.")

def create_jobs_table():
    create_table(JOBS_TABLE)

def create_staging_table():
    create_table(STAGING_TABLE)

def create_job_skills_table():
    create_table(JOB_SKILLS_TABLE, schema=JOB_SKILLS_SCHEMA)

def create_job_work_mode_table():
    create_table(JOB_WORK_MODE_TABLE, schema=JOB_WORK_MODE_SCHEMA)
