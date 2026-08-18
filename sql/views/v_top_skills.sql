CREATE OR REPLACE VIEW `techpulse-india.tech_jobs.v_top_skills` AS
SELECT
  skill,
  COUNT(DISTINCT job_id) AS job_count,
  ROUND(
    COUNT(DISTINCT job_id) * 100.0 /
    (SELECT COUNT(*) FROM `techpulse-india.tech_jobs.jobs`),
    2
  ) AS pct_of_all_jobs
FROM `techpulse-india.tech_jobs.job_skills`
GROUP BY skill
ORDER BY job_count DESC;
