CREATE OR REPLACE VIEW `techpulse-india.tech_jobs.v_salary_distribution` AS
WITH estimates AS (
  SELECT
    CASE
      WHEN salary_min IS NOT NULL AND salary_min >= 100000 THEN (salary_min + salary_max) / 2
      ELSE salary_max
    END AS salary_estimate
  FROM `techpulse-india.tech_jobs.jobs`
  WHERE salary_max IS NOT NULL
)
SELECT
  COUNT(*) AS jobs_with_salary,
  ROUND(MIN(salary_estimate), 2) AS min_salary,
  ROUND(APPROX_QUANTILES(salary_estimate, 4)[OFFSET(1)], 2) AS p25,
  ROUND(APPROX_QUANTILES(salary_estimate, 4)[OFFSET(2)], 2) AS median,
  ROUND(APPROX_QUANTILES(salary_estimate, 4)[OFFSET(3)], 2) AS p75,
  ROUND(MAX(salary_estimate), 2) AS max_salary,
  ROUND(AVG(salary_estimate), 2) AS avg_salary
FROM estimates
WHERE salary_estimate >= 100000;
