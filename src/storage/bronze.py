import json
from pathlib import Path
from datetime import datetime

BRONZE_PATH = Path("data/bronze")

def save_raw_jobs(data: dict) -> Path:
    """
    Save the raw job data to a JSON file in the bronze layer.
    
    """

    BRONZE_PATH.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = BRONZE_PATH / f"jobs_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return filename