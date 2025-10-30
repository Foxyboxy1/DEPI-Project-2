-- models/staging/stg_reviews.sql
with raw as (
    select *
    from {{ source('raw', 'user_reviews_raw') }}
)

select
    app_id,
    translated_review,
    sentiment,
    sentiment_polarity,
    sentiment_subjectivity
from raw
