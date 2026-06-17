from fastapi import FastAPI
import psycopg2
from env import *
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request



def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

app = FastAPI()

templates = Jinja2Templates(directory="templates")
print(templates)
print(type(templates))
print(templates.env)
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static") 
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
@app.get("/")
def home():
    return {"message": "API Working"}


@app.get("/api/overview")
def overview():

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT
        COUNT(*) AS total_jobs,
        MIN(date) AS data_from,
        MAX(date) AS data_to
    FROM main;
    """

    cur.execute(query)

    total_jobs, data_from , data_to = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_jobs": total_jobs,
        "data_from": str(data_from),
        "data_to" : str(data_to)
    }




@app.get("/api/momentum")
def monemtum():
    conn = get_connection()
    cur = conn.cursor()
    query = """
    WITH top_skills AS (
    SELECT skill
    FROM job_skills
    GROUP BY skill
    ORDER BY COUNT(*) DESC
    LIMIT 10
    ),

    max_day AS (
        SELECT MAX(day) AS latest_day
        FROM job_skills
    ),

    current_period AS (
        SELECT
            skill,
            COUNT(*) AS current_mentions
        FROM job_skills
        WHERE day >= (
            SELECT latest_day - INTERVAL '6 days'
            FROM max_day
        )
        GROUP BY skill
    ),

    previous_period AS (
        SELECT
            skill,
            COUNT(*) AS previous_mentions
        FROM job_skills
        WHERE day >= (
            SELECT latest_day - INTERVAL '13 days'
            FROM max_day
        )
        AND day < (
            SELECT latest_day - INTERVAL '6 days'
            FROM max_day
        )
        GROUP BY skill
    )

    SELECT
        c.skill,
        c.current_mentions,
        p.previous_mentions,
        ROUND(
            (
                (c.current_mentions - p.previous_mentions)
                * 100.0
                / NULLIF(p.previous_mentions, 0)
            )::numeric,
            2
        ) AS growth
    FROM current_period c
    JOIN previous_period p
        ON c.skill = p.skill
    WHERE c.skill IN (
        SELECT skill
        FROM top_skills
    )
    ORDER BY growth DESC;
"""

    cur.execute(query)
    rows = cur.fetchall()

    response = []

    for skill, current, previous, growth in rows:
        response.append({
            "skill": skill,
            "growth": float(growth)
        })

    cur.close()
    conn.close()

    return response




@app.get("/api/trends")
def trends():

    conn = get_connection()
    cur = conn.cursor()

    query = """
    WITH top_skills AS (
    SELECT skill
    FROM job_skills
    GROUP BY skill
    ORDER BY COUNT(*) DESC
    LIMIT 10
)

SELECT
    date_trunc('week', day) AS week,
    skill,
    COUNT(*) AS mentions
FROM job_skills
WHERE skill IN (SELECT skill FROM top_skills)
AND date_trunc('week', day) <
(
    SELECT date_trunc('week', MAX(day))
    FROM job_skills
)
GROUP BY week, skill
ORDER BY week;
    """

    cur.execute(query)

    rows = cur.fetchall()
    skills = set()
    weeks = {}

    for week, skill, mentions in rows:

        week = week.strftime("%Y-%m-%d")

        skills.add(skill)

        if week not in weeks:
            weeks[week] = {"week": week}

        weeks[week][skill] = mentions


    response = {
        "skills": sorted(list(skills)),
        "data": list(weeks.values())
    }

    

    cur.close()
    conn.close()
    return response
    


@app.get("/api/skill/{skill_name}")
def skill_details(skill_name: str):

    conn = get_connection()
    cur = conn.cursor()

    # -------------------
    # Total Jobs
    # -------------------
    cur.execute("""
        SELECT COUNT(DISTINCT job_id)
        FROM job_skills
        WHERE skill = %s
    """, (skill_name,))
    
    total_jobs = cur.fetchone()[0]

    # -------------------
    # Top Roles
    # -------------------
    cur.execute("""
        SELECT
            m.normalized_position,
            COUNT(*) AS jobs
        FROM job_skills js
        JOIN main m
            ON js.job_id = m.id
        WHERE js.skill = %s
        GROUP BY m.normalized_position
        ORDER BY jobs DESC
        LIMIT 5
    """, (skill_name,))
    
    roles = [
        {
            "role": role,
            "count": count
        }
        for role, count in cur.fetchall()
    ]

    # -------------------
    # Paired Skills
    # -------------------
    cur.execute("""
        SELECT
            js2.skill,
            COUNT(*) AS mentions
        FROM job_skills js1
        JOIN job_skills js2
            ON js1.job_id = js2.job_id
        WHERE js1.skill = %s
        AND js2.skill <> %s
        GROUP BY js2.skill
        ORDER BY mentions DESC
        LIMIT 10
    """, (skill_name, skill_name))

    paired_skills = [
        {
            "skill": skill,
            "count": count
        }
        for skill, count in cur.fetchall()
    ]

    cur.close()
    conn.close()

    return {
        "skill": skill_name,
        "total_jobs": total_jobs,
        "top_roles": roles,
        "paired_skills": paired_skills
    }