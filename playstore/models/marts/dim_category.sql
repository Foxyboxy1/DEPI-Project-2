SELECT
    ROW_NUMBER() OVER (ORDER BY category) AS category_key,
    category AS category_name
FROM (
    SELECT DISTINCT category
    FROM {{ ref('stg_integrated_apps') }}
    WHERE category IS NOT NULL
)