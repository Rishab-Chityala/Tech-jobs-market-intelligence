import requests
import time

from .config import APP_ID, APP_KEY, COUNTRY
from .endpoints import BASE_URL

def fetch_jobs(role: str, pages: int = 1, retries: int = 3):
    """
    Fetch jobs from the Adzuna API.

    Args:
        role (str): The job role to search for.
        pages (int): The number of pages to fetch (default is 1).
        retries (int): The number of times to retry the request (default is 3)."""
        
    all_jobs = []
    
    headers = {"User-Agent": "TechPulseIndia/1.0"}
    
    for page in range(1, pages + 1):
        
        url = f"{BASE_URL}/{COUNTRY}/search/{page}"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": role,
            "results_per_page": 50,
        }

        success = False

        for attempt in range(3):
            try:
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=30,
                )

                response.raise_for_status()

                data = response.json()
                all_jobs.extend(data.get("results", []))

                print(f"Fetched page {page}: {len(data.get('results', []))} jobs.")
                success = True
                break

            except requests.exceptions.RequestException as e:
                print(f"Page {page}, Attempt {attempt + 1} failed: {e}")
                time.sleep(2)

        if not success:
            print(f"Skipping page {page}")
    
    return all_jobs




