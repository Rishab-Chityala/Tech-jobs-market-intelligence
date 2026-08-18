from src.warehouse.client import get_bigquery_client

client = get_bigquery_client()

print("connected to bigquery")

print(client.project)