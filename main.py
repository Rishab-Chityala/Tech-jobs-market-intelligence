from src.etl.pipeline import run_pipeline
from src.warehouse.schema import create_job_skills_table, create_job_work_mode_table
from src.skills.extract import run_skill_extraction
from src.work_mode.classify import run_work_mode_classification

from src.analytics.reports import (
    hiring_trends_report,
    salary_analytics_report,
    contract_analytics_report,
    time_analytics_report,
    skill_analytics_report,
)


def run_full_pipeline():
    print("\n########## STAGE 1: ETL ##########")
    run_pipeline()

    print("\n########## STAGE 2: Enrichment ##########")
    create_job_skills_table()
    run_skill_extraction()

    create_job_work_mode_table()
    run_work_mode_classification()

    print("\n########## STAGE 3: Analytics ##########")
    hiring_trends_report()
    salary_analytics_report()
    contract_analytics_report()
    time_analytics_report()
    skill_analytics_report()

    print("\n########## Pipeline run complete ##########")


if __name__ == "__main__":
    run_full_pipeline()
    