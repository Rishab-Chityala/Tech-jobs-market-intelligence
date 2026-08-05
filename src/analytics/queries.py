from src.warehouse.client import get_bigquery_client
from src.config.warehouse import DATASET_ID,JOBS_TABLE

client = get_bigquery_client()

def top_hiring_companies(limit=10):
    query = f"""
        SELECT 
        company,
        COUNT(*) as job_count
        
        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        GROUP BY company
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe()