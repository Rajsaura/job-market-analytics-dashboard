NORMALIZATION_MAP = {

    # =========================
    # Python / AI / ML
    # =========================
    "python": "python",
    "python3": "python",
    "pyhton": "python",

    "pytorch": "pytorch",
    "py torch": "pytorch",
    "tensorflow": "tensorflow",
    "keras": "keras",
    "scikit learn": "scikitlearn",
    "scikit-learn": "scikitlearn",
    "sklearn": "scikitlearn",

    "machine learning": "machinelearning",
    "deep learning": "deeplearning",
    "artificial intelligence": "ai",
    "generative ai": "genai",
    "large language model": "llm",
    "llm": "llm",
    "langchain": "langchain",
    "rag": "rag",
    "retrieval augmented generation": "rag",

    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",

    # =========================
    # Data Engineering / Big Data
    # =========================
    "pyspark": "pyspark",
    "spark": "spark",
    "apache spark": "spark",

    "hadoop": "hadoop",
    "etl": "etl",
    "etl pipelines": "etl",

    "data engineering": "dataengineering",
    "data engineer": "dataengineering",

    "data modeling": "datamodeling",
    "data ingestion": "dataingestion",
    "data pipeline": "datapipeline",

    "databricks": "databricks",
    "data bricks": "databricks",

    "snowflake": "snowflake",

    # =========================
    # SQL / Databases
    # =========================
    "sql": "sql",
    "mysql": "mysql",

    "postgres": "postgresql",
    "postgresql": "postgresql",

    "mongodb": "mongodb",
    "mongo db": "mongodb",

    "sqlite": "sqlite",
    "redis": "redis",

    "sql server": "mssql",
    "mssql": "mssql",
    "microsoft sql server": "mssql",

    # =========================
    # Cloud
    # =========================
    "aws": "aws",
    "amazon web services": "aws",

    "gcp": "gcp",
    "google cloud": "gcp",
    "google cloud platform": "gcp",

    "azure": "azure",

    # =========================
    # Azure Data Stack
    # =========================
    "azure data factory": "adf",
    "adf": "adf",

    "azure synapse": "synapse",
    "synapse analytics": "synapse",

    "microsoft fabric": "fabric",
    "fabric": "fabric",

    "power bi": "powerbi",

    "bigquery": "bigquery",

    # =========================
    # Web / Backend
    # =========================
    "javascript": "javascript",
    "typescript": "typescript",

    "react": "react",
    "react.js": "react",

    "node.js": "nodejs",
    "node js": "nodejs",

    "express.js": "expressjs",
    "express js": "expressjs",

    "next.js": "nextjs",

    "html": "html",
    "css": "css",

    "tailwind css": "tailwind",
    "bootstrap": "bootstrap",

    # =========================
    # DevOps
    # =========================
    "docker": "docker",
    "kubernetes": "kubernetes",
    "terraform": "terraform",

    "git": "git",
    "github": "github",

    # =========================
    # BI / Analytics
    # =========================
    "tableau": "tableau",
    "excel": "excel",

    # =========================
    # APIs
    # =========================
    "rest api": "restapi",
    "restful api": "restapi",
    "api": "api"
}
skills = set(NORMALIZATION_MAP.values())
