SELECT
    App AS app,
    Category AS category,
    CAST(Rating AS DECIMAL(3,1)) AS rating,
    CAST(Reviews AS INTEGER) AS reviews,
    CAST(REPLACE(REPLACE(Installs, ',', ''), '+', '') AS BIGINT) AS installs,
    Size AS app_size,          -- ✅ Correct name
    Type AS type,
    CASE 
        WHEN Price = '0' THEN 0.0
        WHEN Price LIKE '$%' THEN CAST(REPLACE(Price, '$', '') AS DECIMAL(10,2))
        ELSE CAST(Price AS DECIMAL(10,2))
    END AS price_clean,
    "Content Rating" AS content_rating,
    Genres AS genres,
    TRY_CAST("Last Updated" AS DATE) AS last_updated,
    "Current Ver" AS current_ver,
    "Android Ver" AS android_ver,
    CAST(Sentiment_Polarity AS FLOAT) AS sentiment_score
FROM {{ source('integrated', 'integrated_data') }}
WHERE App IS NOT NULL AND Rating IS NOT NULL