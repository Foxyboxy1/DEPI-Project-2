SELECT
    da.app_key,
    dc.category_key,
    dd.date_key,
    ANY_VALUE(s.installs) AS installs,
    COUNT(*) AS reviews_count,
    AVG(s.rating) AS avg_rating,                -- ✅ Must be included
    AVG(s.sentiment_polarity) AS sentiment_score -- ✅ Must be included
FROM {{ ref('stg_integrated_reviews') }} s
JOIN {{ ref('dim_app') }} da ON s.app = da.app_id
JOIN {{ ref('dim_category') }} dc ON s.category = dc.category_name
JOIN {{ ref('dim_date') }} dd ON s.last_updated = dd.full_date
WHERE s.rating IS NOT NULL
GROUP BY da.app_key, dc.category_key, dd.date_key