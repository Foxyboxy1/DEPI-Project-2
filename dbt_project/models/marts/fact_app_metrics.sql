{{ config(
    materialized='table',
    tags=['marts', 'fact']
) }}

WITH apps AS (
    SELECT * FROM {{ ref('stg_apps') }}
),

reviews AS (
    SELECT * FROM {{ ref('stg_reviews') }}
),

dim_app AS (
    SELECT * FROM {{ ref('dim_app') }}
),

dim_category AS (
    SELECT * FROM {{ ref('dim_category') }}
),

dim_date AS (
    SELECT * FROM {{ ref('dim_date') }}
),

-- Join apps with their reviews
apps_with_reviews AS (
    SELECT
        a.App,
        a.Category,
        a.Installs,
        a.Reviews AS reviews_count,
        a.Last_Updated,
        COALESCE(r.sentiment_polarity, 0) AS sentiment_score
    FROM apps a
    LEFT JOIN reviews r ON a.App = r.app_id
),

-- Add dimension keys
fact_table AS (
    SELECT
        da.app_key,
        dc.category_key,
        dd.date_key,
        awr.Installs,
        awr.reviews_count,
        awr.sentiment_score,
        CURRENT_TIMESTAMP() AS loaded_at
    FROM apps_with_reviews awr
    INNER JOIN dim_app da 
        ON awr.App = da.app_id
    INNER JOIN dim_category dc 
        ON awr.Category = dc.category_name
    INNER JOIN dim_date dd 
        ON dd.full_date = awr.Last_Updated
)

SELECT 
    app_key,
    category_key,
    date_key,
    installs,
    reviews_count,
    sentiment_score,
    loaded_at
FROM fact_table
