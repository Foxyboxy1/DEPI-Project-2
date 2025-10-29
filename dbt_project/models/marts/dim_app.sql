{{ config(
    materialized='view',
    tags=['marts', 'dimension']
) }}

WITH apps_base AS (
    SELECT * FROM {{ ref('stg_apps') }}
),

apps_with_keys AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY App) AS app_key,
        App AS app_id,
        CASE 
            WHEN Size < 10 THEN 'Small (<10MB)'
            WHEN Size < 50 THEN 'Medium (10-50MB)'
            WHEN Size < 100 THEN 'Large (50-100MB)'
            ELSE 'Very Large (>100MB)'
        END AS app_size,
        Current_Ver AS current_version,
        Android_Ver AS android_version,
        CURRENT_TIMESTAMP() AS created_at,
        CURRENT_TIMESTAMP() AS updated_at
    FROM apps_base
    WHERE App IS NOT NULL
)

SELECT 
    app_key,
    app_id,
    app_size,
    current_version,
    android_version,
    created_at,
    updated_at
FROM apps_with_keys
