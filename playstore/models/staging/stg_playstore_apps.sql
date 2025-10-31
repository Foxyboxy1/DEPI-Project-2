-- Read the integrated, cleaned dataset from Member 3
SELECT
    app,
    category,
    rating,
    reviews,
    installs,
    size,
    type,
    price,
    "Content Rating" AS content_rating,
    genres,
    "Last Updated" AS last_updated,
    "Current Ver" AS current_ver,
    "Android Ver" AS android_ver,
    "Sentiment_Polarity" AS sentiment_score
FROM {{ source('integrated', 'integrated_data') }}
WHERE app IS NOT NULL