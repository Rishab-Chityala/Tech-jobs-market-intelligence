from src.warehouse.client import get_bigquery_client
from src.config.warehouse import DATASET_ID, JOBS_TABLE

client = get_bigquery_client()

def top_hiring_companies(limit=10):
    query = f"""
        SELECT 
        company,
        COUNT(*) as job_count
        
        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        GROUP BY company
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def top_hiring_cities(limit=10):
    query = f"""
        SELECT 
        city,
        COUNT(*) as job_count

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        WHERE city IS NOT NULL
        GROUP BY city
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def top_hiring_states(limit=10):
    query = f"""
        SELECT 
        state,
        COUNT(*) as job_count

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        WHERE state IS NOT NULL
        GROUP BY state
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def jobs_by_category(limit=20):
    query = f"""
        SELECT 
        category,
        COUNT(*) as job_count

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def most_common_job_titles(limit=10):
    query = f"""
        SELECT 
        INITCAP(TRIM(title)) as title,
        COUNT(*) as job_count

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        WHERE title IS NOT NULL
        GROUP BY 1
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def avg_salary_by_role(limit=10, min_count=3):
    query = f"""
        WITH normalized_jobs AS (
            SELECT
                INITCAP(TRIM(REGEXP_REPLACE(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(title, r'(?i)^\\s*(Sr|Senior)[\\.\\-\\s]+', 'Senior '),
                        r'(?i)^\\s*(Jr|Junior)[\\.\\-\\s]+', 'Junior '
                    ),
                    r'\\s+', ' '
                ))) AS title,
                CASE
                    WHEN salary_min IS NOT NULL AND salary_min >= 100000 THEN (salary_min + salary_max) / 2
                    ELSE salary_max
                END AS salary_estimate
            FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
            WHERE salary_max IS NOT NULL
        )
        SELECT
        title,
        COUNT(*) as job_count,
        ROUND(AVG(salary_estimate), 2) as avg_salary

        FROM normalized_jobs
        WHERE salary_estimate >= 100000
        GROUP BY title
        HAVING job_count >= {min_count}
        ORDER BY avg_salary DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def highest_paying_companies(limit=10, min_count=3):
    query = f"""
        WITH estimates AS (
            SELECT
                company,
                CASE
                    WHEN salary_min IS NOT NULL AND salary_min >= 100000 THEN (salary_min + salary_max) / 2
                    ELSE salary_max
                END AS salary_estimate
            FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
            WHERE salary_max IS NOT NULL
        )
        SELECT
        company,
        COUNT(*) as job_count,
        ROUND(AVG(salary_estimate), 2) as avg_salary

        FROM estimates
        WHERE salary_estimate >= 100000
        GROUP BY company
        HAVING job_count >= {min_count}
        ORDER BY avg_salary DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def highest_paying_cities(limit=10, min_count=3):
    query = f"""
        WITH estimates AS (
            SELECT
                city,
                CASE
                    WHEN salary_min IS NOT NULL AND salary_min >= 100000 THEN (salary_min + salary_max) / 2
                    ELSE salary_max
                END AS salary_estimate
            FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
            WHERE salary_max IS NOT NULL AND city IS NOT NULL
        )
        SELECT
        city,
        COUNT(*) as job_count,
        ROUND(AVG(salary_estimate), 2) as avg_salary

        FROM estimates
        WHERE salary_estimate >= 100000
        GROUP BY city
        HAVING job_count >= {min_count}
        ORDER BY avg_salary DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def salary_distribution():
    query = f"""
        WITH estimates AS (
            SELECT
                CASE
                    WHEN salary_min IS NOT NULL AND salary_min >= 100000 THEN (salary_min + salary_max) / 2
                    ELSE salary_max
                END AS salary_estimate
            FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
            WHERE salary_max IS NOT NULL
        )
        SELECT
        COUNT(*) as total_jobs_with_salary,
        ROUND(MIN(salary_estimate), 2) as min_salary,
        ROUND(MAX(salary_estimate), 2) as max_salary,
        ROUND(AVG(salary_estimate), 2) as avg_salary,
        ROUND(APPROX_QUANTILES(salary_estimate, 4)[OFFSET(1)], 2) as p25,
        ROUND(APPROX_QUANTILES(salary_estimate, 4)[OFFSET(2)], 2) as median,
        ROUND(APPROX_QUANTILES(salary_estimate, 4)[OFFSET(3)], 2) as p75

        FROM estimates
        WHERE salary_estimate >= 100000
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def roles_missing_salary(limit=10):
    query = f"""
        WITH normalized_jobs AS (
            SELECT
                INITCAP(TRIM(REGEXP_REPLACE(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(title, r'(?i)^\\s*(Sr|Senior)[\\.\\-\\s]+', 'Senior '),
                        r'(?i)^\\s*(Jr|Junior)[\\.\\-\\s]+', 'Junior '
                    ),
                    r'\\s+', ' '
                ))) AS title,
                CASE
                    WHEN salary_min IS NOT NULL AND salary_min >= 100000 THEN (salary_min + salary_max) / 2
                    ELSE salary_max
                END AS salary_estimate
            FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
            WHERE title IS NOT NULL
        )
        SELECT
        title,
        COUNT(*) as job_count

        FROM normalized_jobs
        WHERE salary_estimate IS NULL OR salary_estimate < 100000
        GROUP BY title
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def contract_type_breakdown():
    query = f"""
        SELECT 
        COALESCE(contract_type, 'unspecified') as contract_type,
        COUNT(*) as job_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct_of_total

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        GROUP BY contract_type
        ORDER BY job_count DESC
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def jobs_posted_today():
    query = f"""
        SELECT 
        COUNT(*) as jobs_posted_today

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        WHERE DATE(posted_date, "Asia/Kolkata") = CURRENT_DATE("Asia/Kolkata")
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def jobs_posted_this_week():
    query = f"""
        SELECT 
        COUNT(*) as jobs_posted_this_week

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        WHERE DATE(posted_date, "Asia/Kolkata") >= DATE_SUB(CURRENT_DATE("Asia/Kolkata"), INTERVAL 7 DAY)
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def hiring_trend_over_time(days=30):
    query = f"""
        SELECT 
        DATE(posted_date, "Asia/Kolkata") as post_date,
        COUNT(*) as job_count

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`
        WHERE posted_date IS NOT NULL
        AND DATE(posted_date, "Asia/Kolkata") >= DATE_SUB(CURRENT_DATE("Asia/Kolkata"), INTERVAL {days} DAY)
        GROUP BY post_date
        ORDER BY post_date
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def top_skills(limit=15):
    query = f"""
        SELECT 
        skill,
        COUNT(DISTINCT job_id) as job_count,
        ROUND(COUNT(DISTINCT job_id) * 100.0 / (SELECT COUNT(*) FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}`), 2) as pct_of_all_jobs

        FROM `{client.project}.{DATASET_ID}.job_skills`
        GROUP BY skill
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def top_skills_for_role(title_keyword, limit=10):
    query = f"""
        SELECT 
        s.skill,
        COUNT(DISTINCT s.job_id) as job_count

        FROM `{client.project}.{DATASET_ID}.job_skills` s
        JOIN `{client.project}.{DATASET_ID}.{JOBS_TABLE}` j
        ON s.job_id = j.job_id
        WHERE LOWER(j.title) LIKE LOWER('%{title_keyword}%')
        GROUP BY s.skill
        ORDER BY job_count DESC
        LIMIT {limit}
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def avg_skills_per_job():
    query = f"""
        SELECT 
        ROUND(AVG(skill_count), 2) as avg_skills_per_job,
        MAX(skill_count) as max_skills_in_one_job

        FROM (
            SELECT job_id, COUNT(*) as skill_count
            FROM `{client.project}.{DATASET_ID}.job_skills`
            GROUP BY job_id
        )
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def jobs_with_no_skills_detected():
    query = f"""
        SELECT 
        COUNT(*) as jobs_with_no_skills

        FROM `{client.project}.{DATASET_ID}.{JOBS_TABLE}` j
        LEFT JOIN `{client.project}.{DATASET_ID}.job_skills` s
        ON j.job_id = s.job_id
        WHERE s.job_id IS NULL
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)

def work_mode_breakdown():
    query = f"""
        SELECT 
        work_mode,
        COUNT(*) as job_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct_of_total

        FROM `{client.project}.{DATASET_ID}.job_work_mode`
        GROUP BY work_mode
        ORDER BY job_count DESC
    """
    return client.query(query).to_dataframe(create_bqstorage_client=False)
