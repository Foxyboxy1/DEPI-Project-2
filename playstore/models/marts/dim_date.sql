WITH dates AS (
    SELECT DISTINCT last_updated AS full_date
    FROM {{ ref('stg_integrated_apps') }}
    WHERE last_updated IS NOT NULL
)
SELECT
    CAST(STRFTIME('%Y%m%d', full_date) AS INTEGER) AS date_key,
    full_date,
    YEAR(full_date) AS year,
    MONTH(full_date) AS month,
    DAY(full_date) AS day
FROM dates