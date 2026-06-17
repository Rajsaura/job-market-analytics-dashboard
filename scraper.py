from operator import pos
import random
import time
import psycopg2
from datetime import date
from bs4 import BeautifulSoup
from list import skills, NORMALIZATION_MAP
from env import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)



# naukri job scraping 
url_naukri = "https://www.naukri.com/data-scientist-jobs-"
headers = {
    "user-agent" : "Mozilla/5.0"
}

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    company VARCHAR(255),   
                    position VARCHAR(255),
                    location VARCHAR(255),
                    date VARCHAR(255),
                    url TEXT,
                    description TEXT
                                )""")


target_jobs = [
    "data-scientist",
    "data-analyst"
    # "data-engineer",
    # "machine-learning-engineer",
    # "python-developer",
    # "backend-developer",
    # "devops-engineer"
]
for target in target_jobs:
    stop = False
    time.sleep(random.uniform(5,10))
    driver.get(f"https://www.naukri.com/{target}-jobs")
    time.sleep(random.uniform(5,10))

    sort_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='filter-sort']")))

    sort_button.click()
    time.sleep(10)
    date_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Date']")))
    date_option.click()
    time.sleep(5)
    
    
    for page in range(1, 10):
        time.sleep(10)
        web_naukri = driver.page_source
        soup_naukri = BeautifulSoup(web_naukri, "html.parser")
        job_cards = soup_naukri.find_all("div", class_="srp-jobtuple-wrapper" )
        safety = ["just now", "today" ,"few hours ago" ]

        time.sleep(random.uniform(5,10))
        for job in job_cards:
            p = job.find("span", class_="job-post-day").text.lower()
            if p in safety:
                k = job.get_text(" ", strip=True).lower()
                
                for old, new in NORMALIZATION_MAP.items():
                    k = k.replace(old, new)
                k = k.split()
                
                skill = []
                job_naukri_list = []
                for word in k:     
                    if(word in skills):
                        skill.append(word)
                skill = list(set(skill))
                try:
                    company_tag = job.find("a", class_="comp-name mw-25")
                except AttributeError:
                    company_tag = None
                try:
                    position_tag = job.find("a", class_="title")
                except AttributeError:
                    position_tag = None
                try:
                    location_tag = job.find("span", class_="locWdth")
                except AttributeError:
                    location_tag = None
                try:
                    date_tag = job.find("span", class_="job-post-day")
                except AttributeError:
                    date_tag = None

                if company_tag:
                    company = company_tag.text.strip()
                else:
                    company = None
       


                job_naukri_list.append({
                    "company": company,
                    "position": position_tag.text.strip() if position_tag else None,
                    "location": location_tag.text.strip() if location_tag else None,
                    "date": date.today().strftime("%Y-%m-%d"),
                    "url": job.find("a", class_="title")['href'],
                    "description": skill
                })
                            
                for job in job_naukri_list: 
                
                    cursor.execute("""
                                INSERT INTO jobs (
                                    company,
                                    position,
                                    location,
                                    date,
                                    url,
                                    description
                                )
                                VALUES (%s, %s, %s, %s, %s, %s)
                                
                            """, (
                                job['company'],
                                job['position'],
                                job['location'],
                                job['date'],
                                job['url'],
                                ', '.join(job['description'])
                            ))
                try:
                    conn.commit()
                except Exception as e:
                    print(e)
            else:
                try:
                    conn.commit()
                except Exception as e:
                    print(e)
                stop = True
                break;
        if page <= 10 and not stop:

            next_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[text()='Next']")
                )
            )

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                next_button
            )

            time.sleep(1)

            driver.execute_script(
                "arguments[0].click();",
                next_button
            )

            time.sleep(random.uniform(3,5))


try:
    conn.commit()
except Exception as e:
    print(e)
finally:
    cursor.close()
    conn.close()
    driver.quit()
