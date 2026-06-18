UPDATE jobs
	SET description = NULL
	WHERE TRIM(description) = '';
	
DELETE FROM jobs
WHERE description IS NULL;

DELETE FROM jobs
WHERE ctid not in( SELECT min(CTID) FROM jobs GROUP BY URL);

select * 
from jobs;

DELETE FroM jobs
WHERE position is NULL;	

INSERT INTO MAIN 
SELECT *
FROM jobs;

INSERT INTO MAIN_backup 
SELECT *
FROM jobs;




-- ALTER TABLE main
-- ADD COLUMN normalized_position TEXT;

UPDATE main
SET normalized_position =
CASE

    WHEN LOWER(position) LIKE '%data engineer%' THEN 'Data Engineer'

    WHEN LOWER(position) LIKE '%data scientist%' THEN 'Data Scientist'

    WHEN LOWER(position) LIKE '%data analyst%' THEN 'Data Analyst'

    WHEN LOWER(position) LIKE '%machine learning engineer%'
      OR LOWER(position) LIKE '%ml engineer%'
      THEN 'ML Engineer'

    WHEN LOWER(position) LIKE '%ai engineer%'
      OR LOWER(position) LIKE '%genai%'
      THEN 'AI Engineer'

    WHEN LOWER(position) LIKE '%backend%'
      THEN 'Backend Developer'

    WHEN LOWER(position) LIKE '%full stack%'
      OR LOWER(position) LIKE '%fullstack%'
      THEN 'Full Stack Developer'

    WHEN LOWER(position) LIKE '%cloud engineer%'
      THEN 'Cloud Engineer'

    WHEN LOWER(position) LIKE '%devops%'
      THEN 'DevOps Engineer'

    ELSE position

END;

SELECT
    normalized_position,
    COUNT(*)
FROM main
GROUP BY normalized_position
ORDER BY COUNT(*) DESC
LIMIT 20;



INSERT INTO job_skills (job_id, day, skill)
SELECT
    id,
    date::date,
    TRIM(skill)
FROM main,
LATERAL unnest(string_to_array(description, ',')) AS skill;


INSERT INTO MAIN_backup 
SELECT *
FROM jobs;

TRUNCATE jobs;