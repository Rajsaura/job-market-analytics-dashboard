from dotenv import load_dotenv
load_dotenv()

import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "jobs_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_PORT = int(os.getenv("DB_PORT", 5432))

