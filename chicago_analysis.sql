-- Active: 1691852189968@@127.0.0.1@5432@ChicagoData
SELECT COUNT(*) FROM crime_data

SELECT * FROM cencus_data
WHERE income_per_capita < 11000

SELECT case_number, crime_description FROM crime_data
WHERE crime_description LIKE '%CHILD%'

SELECT case_number, primary_type, crime_description FROM crime_data
WHERE primary_type = 'KIDNAPPING' AND crime_description LIKE '%CHILD%'

SELECT DISTINCT(primary_type) FROM crime_data
WHERE location_description LIKE '%SCHOOL%'

SELECT school_type, AVG(safety_score) as avg_safety_score FROM public_school
GROUP BY school_type

SELECT comm_area_name, below_poverty FROM cencus_data
ORDER BY below_poverty DESC LIMIT 5

SELECT comm_area_id, COUNT(case_number) AS total_case FROM crime_data
WHERE comm_area_id IS NOT NULL
GROUP BY comm_area_id
ORDER BY total_case DESC LIMIT 1

SELECT comm_area_name, hardship_index FROM cencus_data
WHERE hardship_index = (SELECT MAX(hardship_index) FROM cencus_data)

SELECT CE.comm_area_name, COUNT(CR.case_number) AS total_case
FROM cencus_data CE RIGHT OUTER JOIN crime_data CR
ON CE.comm_area_id = CR.comm_area_id
GROUP BY CE.comm_area_name 
HAVING CE.comm_area_name IS NOT NULL
ORDER BY total_case DESC LIMIT 1

SELECT PU.school_name, CE.comm_area_name, PU.student_attendance, CE.hardship_index
FROM cencus_data CE LEFT OUTER JOIN public_school PU
ON CE.comm_area_id = PU.comm_area_id
WHERE CE.hardship_index = 98;

SELECT CR.case_number, CR.primary_type, CE.comm_area_name, CR.location_description
FROM cencus_data CE RIGHT OUTER JOIN crime_data CR
ON CE.comm_area_id = CR.comm_area_id
WHERE CR.location_description LIKE '%SCHOOL%'

CREATE VIEW leader_data
AS SELECT school_name, leader_icon
FROM public_school;
SELECT * FROM leader_data

CREATE OR REPLACE PROCEDURE update_leader_score(IN in_school_id INTEGER, IN in_leader_score INTEGER)
LANGUAGE plpgsql
AS $$

BEGIN

    UPDATE public_school
    SET leader_score = in_leader_score
    WHERE school_id = in_school_id;

    IF in_leader_score BETWEEN 80 AND 99 THEN
        UPDATE public_school
        SET leader_icon = 'Very Strong'
        WHERE school_id = in_school_id;

    ELSEIF in_leader_score BETWEEN 60 AND 79 THEN
        UPDATE public_school
        SET leader_icon = 'Strong'
        WHERE school_id = in_school_id;

    ELSEIF in_leader_score BETWEEN 40 AND 59 THEN
        UPDATE public_school
        SET leader_icon = 'Average'
        WHERE school_id = in_school_id;

    ELSEIF in_leader_score BETWEEN 20 AND 39 THEN
        UPDATE public_school
        SET leader_icon = 'Weak'
        WHERE school_id = in_school_id;

    ELSEIF in_leader_score BETWEEN 0 AND 19 THEN
        UPDATE public_school
        SET leader_icon = 'Very Weak'
        WHERE school_id = in_school_id;

    ELSEIF in_leader_score IS NULL THEN
        UPDATE public_school
        SET leader_icon = NULL
        WHERE school_id = in_school_id;

    ELSE
        ROLLBACK;

    END IF;

    COMMIT;

END;
$$;

CALL update_leader_score(609951, 20);