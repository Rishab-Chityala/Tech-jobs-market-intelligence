from src.models.job import Job

def transform_job(raw_job: dict) -> Job:
    """
    Converting Adzuna API job data to our internal job model.
    """
    area = raw_job.get("location", {}).get("area", [])

    country = area[0] if len(area) > 0 else None
    state = area[1] if len(area) > 1 else None  
    city = area[2] if len(area) > 2 else None

    return Job(

        job_id=str(raw_job.get("id")) if raw_job.get("id") is not None else None,
        title=raw_job.get("title"),
        company=raw_job.get("company", {}).get("display_name"),
        country=country,
        state=state,
        city=city,
        location=raw_job.get("location", {}).get("display_name"),
        category=raw_job.get("category", {}).get("label"),
        latitude=raw_job.get("latitude"),
        longitude=raw_job.get("longitude"),
        contract_type=raw_job.get("contract_time"),
        description=raw_job.get("description"),
        posted_date=raw_job.get("created"),
        job_url=raw_job.get("redirect_url"),
        salary_min=raw_job.get("salary_min"),
        salary_max=raw_job.get("salary_max"),
        salary_predicted=raw_job.get("salary_is_predicted") == "1",
    )

def transform_jobs(raw_jobs: list[dict]) -> list[Job]:
    return [transform_job(raw_job) for raw_job in raw_jobs]