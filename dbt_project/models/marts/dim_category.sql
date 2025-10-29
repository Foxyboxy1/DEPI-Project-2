{{ config(
    materialized='view',
    tags=['marts', 'dimension']
) }}

WITH categories_base AS (
    SELECT DISTINCT category
    FROM {{ ref('stg_apps') }}
    WHERE category IS NOT NULL
),

categories_with_keys AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY category) AS category_key,
        category AS category_name,
        CURRENT_TIMESTAMP() AS created_at
    FROM categories_base
)

SELECT
    category_key,
    category_name,
    created_at
FROM categories_with_keys
