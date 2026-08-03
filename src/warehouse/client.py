import os

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

def get_bigquery_client():
    """
    create and return a BigQuery client.
    
    """

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    return bigquery.Client()
