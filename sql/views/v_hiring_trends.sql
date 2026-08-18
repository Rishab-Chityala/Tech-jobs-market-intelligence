CREATE OR REPLACE VIEW `techpulse-india.tech_jobs.v_hiring_trends` AS
SELECT
  j.job_id,
  
  
  CASE 
    WHEN REGEXP_CONTAINS(LOWER(j.title), r'^(sr|senior)\b.*machine learning engineer') 
      THEN 'Senior Machine Learning Engineer'
    WHEN REGEXP_CONTAINS(LOWER(j.title), r'^(jr|junior)\b.*machine learning engineer') 
      THEN 'Junior Machine Learning Engineer'
    ELSE INITCAP(TRIM(REGEXP_REPLACE(
      REGEXP_REPLACE(
        REGEXP_REPLACE(j.title, r'(?i)\bsr\.?\b', 'Senior'),
        r'(?i)\bjr\.?\b', 'Junior'
      ),
      r'\s+', ' '
    )))
  END AS title,

  j.company,
  j.country,
  j.state,
  j.city,
  j.category,
  j.contract_type,
  j.salary_min,
  j.salary_max,
  
  CASE
    WHEN j.salary_max IS NULL THEN NULL
    WHEN j.salary_min IS NOT NULL AND j.salary_min >= 100000
      THEN ROUND((j.salary_min + j.salary_max) / 2, 2)
    WHEN j.salary_max >= 100000 THEN ROUND(j.salary_max, 2)
    ELSE NULL
  END AS avg_salary,

  CASE WHEN j.salary_min IS NULL AND j.salary_max IS NULL THEN 1 ELSE 0 END AS is_salary_missing,
  j.salary_predicted,
  j.posted_date,
  DATE(j.posted_date, "Asia/Kolkata") AS posted_date_ist,
  COALESCE(w.work_mode, "Unspecified") AS work_mode
  
FROM `techpulse-india.tech_jobs.jobs` j
LEFT JOIN `techpulse-india.tech_jobs.job_work_mode` w
  ON j.job_id = w.job_id;
