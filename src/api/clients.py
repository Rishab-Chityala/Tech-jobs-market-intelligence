import requests

from .config import APP_ID, APP_KEY, COUNTRY
from .endpoints import BASE_URL

def fetch_jobs(role : str , page : int = 1):
    """
    Fetch jobs from the Adzuna Api
    
    args: 
        role : str : The job role to search for
        page : int : The page number to fetch (default is 1)
        
    returns:
        dict : Json response from the Adzuna API containing job listings
    """

    URL = f"{BASE_URL}/{COUNTRY}/search/{page}"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 10,
        "what": role,
        "content-type": "application/json"
    }

    response = requests.get(URL , params = params , timeout = 30)

    response.raise_for_status()

    return response.json()