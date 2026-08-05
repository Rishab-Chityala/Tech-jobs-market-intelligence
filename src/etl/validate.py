from src.models.job import Job


def validate_job(job: Job) -> tuple[bool, str | None]:

    if not job.job_id:
        return False, "Job ID is required."
    if not job.title:
        return False, "Job title is required."
    if not job.company:
        return False, "Company name is required."
    if not job.country:
        return False, "Country is required."
    if not job.description:
        return False, "Job description is required."
    if not job.posted_date:
        return False, "Posted date is required."
    if not job.job_url:
        return False, "Job URL is required."

    return True, None

def validate_jobs(jobs: list[Job]) -> list[Job]:
    """
    Filter out invalid jobs from a list of jobs."""

    valid_jobs = []
    
    for job in jobs:
        valid, _ = validate_job(job)
        if valid:
            valid_jobs.append(job)
    return valid_jobs
