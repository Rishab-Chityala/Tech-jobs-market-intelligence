# Word-boundary regex patterns, matched case-insensitively.
# Ambiguous bare words (Go, R) are intentionally excluded or tightened
# to avoid false positives against common English words.

SKILL_PATTERNS = {
    # Languages
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b",
    "Java": r"\bjava\b",
    "JavaScript": r"\bjavascript\b",
    "TypeScript": r"\btypescript\b",
    "C++": r"c\+\+",
    "C#": r"c#",
    "Golang": r"\bgolang\b",

    # Cloud
    "AWS": r"\baws\b",
    "Azure": r"\bazure\b",
    "GCP": r"\bgcp\b|\bgoogle cloud\b",

    # DevOps / Infra
    "Docker": r"\bdocker\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "Terraform": r"\bterraform\b",
    "Jenkins": r"\bjenkins\b",
    "CI/CD": r"\bci[\/\- ]?cd\b",
    "Git": r"\bgit\b",
    "Linux": r"\blinux\b",

    # Data / Big Data
    "Spark": r"\bspark\b",
    "Kafka": r"\bkafka\b",
    "Hadoop": r"\bhadoop\b",
    "Airflow": r"\bairflow\b",

    # ML / AI
    "TensorFlow": r"\btensorflow\b",
    "PyTorch": r"\bpytorch\b",
    "GenAI": r"\bgen\s?ai\b|\bgenerative ai\b",
    "LangChain": r"\blangchain\b",
    "Scikit-learn": r"\bscikit-learn\b|\bsklearn\b",
    "NLP": r"\bnlp\b",
    "Machine Learning": r"\bmachine learning\b",
    "Deep Learning": r"\bdeep learning\b",

    # Databases
    "MongoDB": r"\bmongodb\b",
    "PostgreSQL": r"\bpostgresql\b|\bpostgres\b",
    "MySQL": r"\bmysql\b",
    "Snowflake": r"\bsnowflake\b",
    "Redis": r"\bredis\b",
    "Oracle": r"\boracle\b",

    # BI / Visualization
    "Power BI": r"\bpower\s?bi\b",
    "Tableau": r"\btableau\b",
    "Excel": r"\bexcel\b",

    # Frameworks
    "React": r"\breact(\.js)?\b",
    "Angular": r"\bangular\b",
    "Vue": r"\bvue(\.js)?\b",
    "Node.js": r"\bnode\.?js\b",
    "Django": r"\bdjango\b",
    "Flask": r"\bflask\b",
    "Spring Boot": r"\bspring\s?boot\b",
    ".NET": r"\.net\b|\bdotnet\b",

    # Other
    "GraphQL": r"\bgraphql\b",
    "REST API": r"\brest\s?api\b",
    "Agile": r"\bagile\b",
    "Scrum": r"\bscrum\b",
}