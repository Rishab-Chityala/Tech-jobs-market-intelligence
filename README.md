# TechPulse India — Tech Job Market Intelligence Platform

An automated, end-to-end data platform that tracks, enriches, and analyzes the Indian tech job market. Jobs are pulled daily from the Adzuna API, loaded into BigQuery, enriched with skill and work-mode detection, and surfaced through both a CLI reporting layer and a 5-page Looker Studio dashboard — all running on a fully automated daily pipeline via GitHub Actions.

**Live dashboard:** [Looker Studio link here]

---

## What it does

- **Ingests** tech job postings daily from the Adzuna API across 13 role searches (Software Engineer, Data Engineer, Data Scientist, ML Engineer, AI Engineer, Python Developer, Backend/Frontend/Full Stack Developer, DevOps Engineer, Cloud Engineer, Business Analyst, Data Analyst)
- **Warehouses** the data in BigQuery, deduplicating against previously-seen postings on every run
- **Enriches** each job with:
  - Detected tech skills, via dictionary/regex matching against job descriptions (~45 tracked skills across languages, cloud, DevOps, ML/AI, databases, BI tools, and frameworks)
  - Work mode classification (Remote / Hybrid / Onsite / Mixed-Unclear / Unspecified), via keyword matching on description + location
- **Analyzes** across 5 domains — Hiring Trends, Salary Insights, Contract & Work Mode, Time Trends, and Skills & Tech Stack — both as CLI reports and as an interactive Looker Studio dashboard
- **Automates** the entire pipeline to run once daily, with zero manual intervention, via GitHub Actions

---

## Architecture

```
Adzuna API
    │
    ▼
ETL  (src/etl/)
  fetch → transform → validate → bronze snapshot (local JSON, gitignored)
    │
    ▼
BigQuery staging table  →  merge  →  jobs table
    │
    ▼
Enrichment  (incremental — only processes newly ingested jobs)
  ├── src/skills/     → job_skills table      (dictionary-based skill detection)
  └── src/work_mode/  → job_work_mode table   (keyword-based work mode classification)
    │
    ▼
Analytics
  ├── src/analytics/  → CLI reports (python main.py)
  └── sql/views/      → BigQuery views → Looker Studio dashboard
```

The full pipeline (ETL → Enrichment → Analytics) runs as a single command via `main.py`, and is scheduled to run automatically once a day via GitHub Actions (`.github/workflows/daily-pipeline.yml`).

---

## Dashboard

Built in Looker Studio, backed directly by BigQuery views (not raw tables), across 5 pages:

| Page | Covers |
|---|---|
| **Overview** | Headline KPIs (total jobs, jobs this week, average salary, jobs posted today), 30-day hiring trend, top 5 skills |
| **Hiring Trends** | Top companies, cities, states, job titles, and category breakdown |
| **Salary Insights** | Salary distribution snapshot (P25/median/P75), average salary by role, highest-paying companies and cities, roles with missing salary data |
| **Contract & Work Mode** | Employment type breakdown (full-time/part-time), work mode breakdown among jobs that specified one |
| **Skills & Tech Stack** | Skill categories in demand (Languages, Cloud, ML & AI, Frameworks, DevOps & Infra, etc.), skills-per-job stats, skill detection coverage, and a role-filtered skills explorer |

Every page includes global filter controls (title search, city, state, date range) and a data-source / limitations footer.

---

## Key insights

A snapshot of what the data shows as of this writing (numbers update daily — see the live dashboard for current figures):

- **Python dominates demand**, appearing in more postings than any other tracked skill by a wide margin, followed by Machine Learning, AWS, SQL, and Azure — reflecting a market weighted toward data/ML-adjacent roles as much as traditional software development.
- **Hiring is heavily concentrated geographically**: Karnataka (driven almost entirely by Bangalore) and Maharashtra together account for a large share of all tracked postings, with Telangana (Hyderabad) a distant third.
- **IT roles dominate the categorized job pool** (~65%), with Engineering, Accounting & Finance, and Scientific/QA roles making up small remaining slices — this dataset is best understood as an IT/tech-services job market snapshot, not a general employment market view.
- **Full-time roles account for the large majority of postings** (~74% of jobs with a stated employment type), with part-time roles nearly nonexistent in this market segment.
- **Median disclosed salary sits around ₹10–11L/year**, with a wide spread (P25 ~₹7L, P75 ~₹15–16L) — and only about a third of postings disclose salary at all, so this should be read as directional, not comprehensive.
- **Explicit remote/hybrid/onsite signals are rare in postings** (~20% of jobs state one), but among those that do, the split is fairly even across Remote, Onsite, and Hybrid — suggesting no single work arrangement dominates when employers do specify.

---

## Project structure

```
.
├── main.py                      # Single-command orchestrator: ETL → Enrichment → Analytics
├── requirements.txt
├── sql/views/                   # BigQuery view definitions powering the Looker Studio dashboard
│   ├── v_hiring_trends.sql
│   ├── v_job_skills_expanded.sql
│   ├── v_salary_distribution.sql
│   └── v_top_skills.sql
├── config/
│   └── roles.py                 # List of job role search terms
├── .github/workflows/
│   └── daily-pipeline.yml       # Scheduled automation (daily, 9:00 AM IST)
├── src/
│   ├── api/                     # Adzuna API client
│   │   ├── clients.py
│   │   ├── config.py
│   │   └── endpoints.py
│   ├── etl/                     # Fetch → transform → validate
│   │   ├── pipeline.py
│   │   ├── transform.py
│   │   └── validate.py
│   ├── models/
│   │   └── job.py               # Job dataclass
│   ├── storage/
│   │   └── bronze.py            # Raw JSON snapshot storage (local, gitignored)
│   ├── warehouse/                # BigQuery client, schema, staging/merge logic
│   │   ├── client.py
│   │   ├── schema.py
│   │   ├── loader.py
│   │   └── merge.py
│   ├── skills/                  # Skill detection (dictionary + regex matching)
│   │   ├── dictionary.py
│   │   └── extract.py
│   ├── work_mode/                # Work mode classification (keyword matching)
│   │   ├── dictionary.py
│   │   └── classify.py
│   ├── analytics/                # CLI report queries and formatting
│   │   ├── queries.py
│   │   └── reports.py
│   └── config/
│       └── warehouse.py          # Dataset/table name constants
└── tests/                        # Standalone runner scripts
    ├── test_analytics.py         # Run all CLI analytics reports
    ├── test_extract.py           # Run skill extraction only
    └── test_classify.py          # Run work mode classification only
```

---

## Setup

**1. Clone and install dependencies**
```
git clone <repo-url>
cd tech-jobs-market-intelligence
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

**2. Configure environment variables**

Create a `.env` file in the project root:
```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
COUNTRY=in
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/gcp-service-account-key.json
```

You'll need:
- A free [Adzuna API](https://developer.adzuna.com/) account (app ID + key)
- A GCP project with BigQuery enabled, and a service account JSON key with **BigQuery Data Editor** and **BigQuery Job User** roles

**3. Run**
```
python main.py
```

Runs the full pipeline: ETL → skill/work-mode enrichment → all 5 analytics reports, printed to the console.

To run pieces individually:
```
python -m tests.test_analytics   # CLI analytics reports only
python -m tests.test_extract     # Skill extraction only
python -m tests.test_classify    # Work mode classification only
```

---

## Automation

The full pipeline runs automatically once a day (scheduled for 9:00 AM IST / 3:30 AM UTC) via GitHub Actions. Enrichment is **incremental** — each run only processes newly ingested jobs, not the full historical dataset, keeping runtime and cost low as the dataset grows.

Note: GitHub Actions doesn't guarantee scheduled runs fire at the exact minute — cron-scheduled workflows can be delayed, particularly during periods of high load across GitHub's infrastructure. In practice, this pipeline typically runs sometime between 9:00 and 10:30 AM IST.

Required GitHub repo secrets: `GCP_SA_KEY` (full service account JSON), `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `COUNTRY`.

---

## Known limitations

- **Job descriptions are truncated to ~500 characters** by the Adzuna API, which only returns excerpts rather than full postings. This directly limits skill detection (~50% of jobs have at least one skill detected) and work mode classification (~80% of jobs have no explicit work mode signal in the available text), since qualifications and work-arrangement details are often mentioned later in a posting, past the excerpt cutoff.
- **Adzuna's free tier caps at ~1,000 API calls/month** (~33/day). The pipeline currently uses close to that ceiling; sustained growth beyond the current dataset size would require either a paid tier or a reduced fetch scope.
- **Salary data is present for roughly a third of postings.** Salary figures below ₹1,00,000/year are treated as "not disclosed" rather than real values, based on an investigation into corrupted/placeholder salary data from the source.
- **Skill and work-mode detection are dictionary/keyword-based**, not NLP-driven — they catch known terms reliably but won't detect skills or phrasing outside the curated list.

## Roadmap

- Scrape full job descriptions from posting redirect URLs, to remove the 500-character excerpt ceiling
- Move skill extraction from dictionary-based matching to LLM-based extraction, once full descriptions are available
- Expand the skill dictionary and work-mode keyword list based on what full descriptions reveal

---

## Tech stack

**Data pipeline:** Python, Adzuna API, BigQuery
**Automation:** GitHub Actions
**Analytics:** SQL (BigQuery), pandas
**Dashboard:** Looker Studio

## License

MIT — see [LICENSE](LICENSE)
