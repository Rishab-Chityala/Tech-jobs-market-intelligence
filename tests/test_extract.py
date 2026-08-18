from src.warehouse.schema import create_job_skills_table
from src.skills.extract import run_skill_extraction

create_job_skills_table()
run_skill_extraction()