SELECT
    App AS app,
    Category AS category,
    CAST(Rating AS DECIMAL(3,1)) AS rating,
    CAST(Reviews AS INTEGER) AS reviews,
    CAST(REPLACE(REPLACE(Installs, ',', ''), '+', '') AS BIGINT) AS installs,
    Size AS app_size,
    Type AS type,
    -- 👇 THIS MUST EXIST
    CASE 
        WHEN Price IN ('0', 'Free') THEN 0.0
        WHEN Price LIKE '$%' THEN CAST(REPLACE(Price, '$', '') AS DECIMAL(10,2))
        ELSE NULL
    END AS price_clean,
    "Content Rating" AS content_rating,
    Genres AS genres,
    -- Date parsing (as fixed earlier)
    CASE
        WHEN "Last Updated" SIMILAR TO '[A-Za-z]+ [0-9]+, [0-9]{4}' THEN
            TRY_CAST(STRPTIME("Last Updated", '%B %d, %Y') AS DATE)
        WHEN "Last Updated" SIMILAR TO '[A-Za-z]+ [0-9]+ [0-9]{4}' THEN
            TRY_CAST(STRPTIME("Last Updated", '%b %d %Y') AS DATE)
        ELSE
            TRY_CAST("Last Updated" AS DATE)
    END AS last_updated,
    "Current Ver" AS current_ver,
    "Android Ver" AS android_ver,
    CAST(Sentiment_Polarity AS FLOAT) AS sentiment_score
FROM {{ source('integrated', 'integrated_data') }}
WHERE App IS NOT NULL AND Rating IS NOT NULL