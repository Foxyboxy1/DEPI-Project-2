SELECT
    App AS app,
    Category AS category,
    CAST(Rating AS DECIMAL(3,1)) AS rating,
    CAST(REPLACE(REPLACE(Installs, ',', ''), '+', '') AS BIGINT) AS installs,
    Size AS app_size,
    Type AS type,
    CASE 
        WHEN Price = '0' THEN 0.0
        WHEN Price LIKE '$%' THEN CAST(REPLACE(Price, '$', '') AS DECIMAL(10,2))
        ELSE CAST(Price AS DECIMAL(10,2))
    END AS price,
    "Content Rating" AS content_rating,
    Genres AS genres,
    TRY_CAST("Last Updated" AS DATE) AS last_updated,
    "Current Ver" AS current_ver,
    "Android Ver" AS android_ver,
    Sentiment_Polarity AS sentiment_polarity
FROM read_csv('../data/processed/integrated_data.csv', header=true, auto_detect=true)
WHERE App IS NOT NULL AND Rating IS NOT NULL