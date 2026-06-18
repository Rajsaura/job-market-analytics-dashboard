import psycopg2
from env import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)

cursor = conn.cursor()

with open("sql/cleaning.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor.execute(sql)

conn.commit()

cursor.close()
conn.close()

print("Cleaning completed successfully.")