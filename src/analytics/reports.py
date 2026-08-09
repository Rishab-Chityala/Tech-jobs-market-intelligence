from .queries import (
    top_hiring_companies,
    top_hiring_cities,
    top_hiring_states,
    most_common_job_titles,
    jobs_by_category,
    avg_salary_by_role,
    highest_paying_companies,
    highest_paying_cities,
    salary_distribution,
    roles_missing_salary,
    contract_type_breakdown,
    jobs_posted_today,
    jobs_posted_this_week,
    hiring_trend_over_time,
    top_skills,
    avg_skills_per_job,
    jobs_with_no_skills_detected,
    work_mode_breakdown
)

def company_report():
    df = top_hiring_companies()
    print("\nTop Hiring Companies:\n")
    print(df)


def city_report():
    df = top_hiring_cities()
    print("\nTop Hiring Cities:\n")
    print(df)


def state_report():
    df = top_hiring_states()
    print("\nTop Hiring States:\n")
    print(df)


def title_report():
    df = most_common_job_titles()
    print("\nMost Common Job Titles:\n")
    print(df)


def category_report():
    df = jobs_by_category()
    print("\nJobs by Category:\n")
    print(df)


def hiring_trends_report():
    company_report()
    city_report()
    state_report()
    title_report()
    category_report()
    
def salary_by_role_report():
    df = avg_salary_by_role()
    print("\nAverage Salary by Role:\n")
    print(df)


def highest_paying_companies_report():
    df = highest_paying_companies()
    print("\nHighest Paying Companies:\n")
    print(df)


def highest_paying_cities_report():
    df = highest_paying_cities()
    print("\nHighest Paying Cities:\n")
    print(df)


def salary_distribution_report():
    df = salary_distribution()
    print("\nSalary Distribution:\n")
    print(df)


def missing_salary_report():
    df = roles_missing_salary()
    print("\nRoles with Missing Salary Data:\n")
    print(df)


def salary_analytics_report():
    salary_by_role_report()
    highest_paying_companies_report()
    highest_paying_cities_report()
    salary_distribution_report()
    missing_salary_report()
    
def contract_type_report():
    df = contract_type_breakdown()
    print("\nEmployment Type Breakdown:\n")
    print(df)


def contract_analytics_report():
    contract_type_report()
    
    
def time_analytics_report():
    print("\nJobs Posted Today:\n")
    print(jobs_posted_today())

    print("\nJobs Posted This Week:\n")
    print(jobs_posted_this_week())

    print("\nHiring Trend (last 30 days):\n")
    print(hiring_trend_over_time())
    
def skill_analytics_report():
    print("\n[Note: based on Adzuna's ~500-char job excerpts, not full postings]\n")

    print("\nTop Skills in Demand:\n")
    print(top_skills())

    print("\nAverage Skills per Job:\n")
    print(avg_skills_per_job())

    print("\nJobs with No Skills Detected:\n")
    print(jobs_with_no_skills_detected())
    
def contract_analytics_report():
    contract_type_report()

    print("\nWork Mode Breakdown (Remote/Hybrid/Onsite):\n")
    print("[Note: based on Adzuna's ~500-char job excerpts \u2014 large Unspecified bucket expected]\n")
    print(work_mode_breakdown())