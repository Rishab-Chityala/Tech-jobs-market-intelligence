from dataclasses import dataclass
from typing import Optional

@dataclass
class Job:
    job_id: str
    title: str
    company: str

    country: str
    state: str
    city: str
    location: str

    category: str

    latitude: Optional[float]
    longitude: Optional[float]

    contract_type: Optional[str]

    description: str

    posted_date: str

    job_url: str

    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_predicted: bool = False