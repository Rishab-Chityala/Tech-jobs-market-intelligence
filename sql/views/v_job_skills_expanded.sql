CREATE OR REPLACE VIEW `techpulse-india.tech_jobs.v_job_skills_expanded` AS
SELECT
  s.job_id,
  s.skill,
  INITCAP(TRIM(j.title)) AS title,
  j.company,
  j.state,
  j.city,
  DATE(j.posted_date, "Asia/Kolkata") AS posted_date_ist,
  

  CASE s.skill
    WHEN 'Python' THEN 'Languages' WHEN 'SQL' THEN 'Languages'
    WHEN 'Java' THEN 'Languages' WHEN 'JavaScript' THEN 'Languages'
    WHEN 'TypeScript' THEN 'Languages' WHEN 'C++' THEN 'Languages'
    WHEN 'C#' THEN 'Languages' WHEN 'Golang' THEN 'Languages'
    WHEN 'AWS' THEN 'Cloud' WHEN 'Azure' THEN 'Cloud' WHEN 'GCP' THEN 'Cloud'
    WHEN 'Docker' THEN 'DevOps & Infra' WHEN 'Kubernetes' THEN 'DevOps & Infra'
    WHEN 'Terraform' THEN 'DevOps & Infra' WHEN 'Jenkins' THEN 'DevOps & Infra'
    WHEN 'CI/CD' THEN 'DevOps & Infra' WHEN 'Git' THEN 'DevOps & Infra'
    WHEN 'Linux' THEN 'DevOps & Infra'
    WHEN 'Spark' THEN 'Data & Big Data' WHEN 'Kafka' THEN 'Data & Big Data'
    WHEN 'Hadoop' THEN 'Data & Big Data' WHEN 'Airflow' THEN 'Data & Big Data'
    WHEN 'TensorFlow' THEN 'ML & AI' WHEN 'PyTorch' THEN 'ML & AI'
    WHEN 'GenAI' THEN 'ML & AI' WHEN 'LangChain' THEN 'ML & AI'
    WHEN 'Scikit-learn' THEN 'ML & AI' WHEN 'NLP' THEN 'ML & AI'
    WHEN 'Machine Learning' THEN 'ML & AI' WHEN 'Deep Learning' THEN 'ML & AI'
    WHEN 'MongoDB' THEN 'Databases' WHEN 'PostgreSQL' THEN 'Databases'
    WHEN 'MySQL' THEN 'Databases' WHEN 'Snowflake' THEN 'Databases'
    WHEN 'Redis' THEN 'Databases' WHEN 'Oracle' THEN 'Databases'
    WHEN 'Power BI' THEN 'BI & Visualization' WHEN 'Tableau' THEN 'BI & Visualization'
    WHEN 'Excel' THEN 'BI & Visualization'
    WHEN 'React' THEN 'Frameworks' WHEN 'Angular' THEN 'Frameworks'
    WHEN 'Vue' THEN 'Frameworks' WHEN 'Node.js' THEN 'Frameworks'
    WHEN 'Django' THEN 'Frameworks' WHEN 'Flask' THEN 'Frameworks'
    WHEN 'Spring Boot' THEN 'Frameworks' WHEN '.NET' THEN 'Frameworks'
    ELSE 'Other'
  END AS skill_category

FROM `techpulse-india.tech_jobs.job_skills` s
INNER JOIN `techpulse-india.tech_jobs.jobs` j 
  ON s.job_id = j.job_id;
