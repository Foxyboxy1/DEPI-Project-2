SELECT
    da.app_key,
    dc.category_key,
    dd.date_key,
    ANY_VALUE(s.installs) AS installs,
    COUNT(*) AS reviews_count,
    AVG(s.rating) AS avg_rating,
    AVG(s.price_clean) AS avg_price,          -- ✅ Comma at end of previous line!
    AVG(s.sentiment_score) AS sentiment_score
FROM {{ ref('stg_playstore_apps') }} s
JOIN {{ ref('dim_app') }} da ON s.app = da.app_id
JOIN {{ ref('dim_category') }} dc ON s.category = dc.category_name
JOIN {{ ref('dim_date') }} dd ON s.last_updated = dd.full_date
GROUP BY da.app_key, dc.category_key, dd.date_key