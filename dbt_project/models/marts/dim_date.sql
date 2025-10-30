{{ config(
    materialized='table',
    tags=['marts', 'dimension']
) }}

WITH date_spine AS (
    -- Generate dates for the last 5 years
    SELECT 
        DATE_ADD('2020-01-01', INTERVAL n DAY) AS full_date
    FROM (
        SELECT a.N + b.N * 10 + c.N * 100 + d.N * 1000 AS n
        FROM 
            (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
             UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
            (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
             UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b,
            (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
             UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) c,
            (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) d
    ) numbers
    WHERE DATE_ADD('2020-01-01', INTERVAL n DAY) <= CURRENT_DATE()
),

dates_with_keys AS (
    SELECT
        -- Primary Key
        CAST(DATE_FORMAT(full_date, '%Y%m%d') AS UNSIGNED) AS date_key,
        
        -- Full Date
        full_date,
        
        -- Date Parts
        YEAR(full_date) AS year,
        MONTH(full_date) AS month,
        DAY(full_date) AS day,
        QUARTER(full_date) AS quarter,
        DAYOFWEEK(full_date) AS day_of_week,
        DAYNAME(full_date) AS day_name,
        MONTHNAME(full_date) AS month_name,
        WEEK(full_date) AS week_of_year,
        
        -- Flags
        CASE WHEN DAYOFWEEK(full_date) IN (1, 7) THEN 1 ELSE 0 END AS is_weekend
        
    FROM date_spine
)

SELECT * FROM dates_with_keys