-- models/staging/stg_apps.sql
with raw as (
    select *
    from {{ source('raw', 'apps_raw') }}
)

select
    App,
    Category,
    `Type`,
    CAST(REPLACE(Price, '$', '') AS DECIMAL(10,2)) as Price,
    Rating,
    Reviews,
    Size,
    Installs,
    `Content Rating` as Content_Rating,
    Genres,
    `Last Updated` as Last_Updated,
    `Current Ver` as Current_Ver,
    `Android Ver` as Android_Ver
from raw
