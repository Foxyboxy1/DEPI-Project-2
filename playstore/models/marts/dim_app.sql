SELECT
    ROW_NUMBER() OVER (ORDER BY app) AS app_key,
    app AS app_id,
    ANY_VALUE(app_size) AS app_size,
    ANY_VALUE(current_ver) AS current_version,
    ANY_VALUE(android_ver) AS android_version
FROM {{ ref('stg_integrated_apps') }}
GROUP BY app