import requests
import time

from .config import APP_ID, APP_KEY, COUNTRY
from .endpoints import BASE_URL

def fetch_jobs(role : str , page : int = 1 , retries : int = 3):
    """
    Fetch jobs from the Adzuna Api
    
    args: 
        role : str : The job role to search for
        page : int : The page number to fetch (default is 1)
        retries : int : The number of times to retry the request (default is 3)

    returns:
        dict : Json response from the Adzuna API containing job listings
    """

    URL = f"{BASE_URL}/{COUNTRY}/search/{page}"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 10,
        "what": role,
    }

    
    headers = {"User-Agent": "TechPulseIndia/1.0"}

    for attempt in range(retries):
        try:
            response = requests.get(URL, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            raise
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise