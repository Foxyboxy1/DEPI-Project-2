# Star Schema: App Analytics Warehouse

## Fact Table: `fact_app_metrics`
| Column | Type | Description |
|--------|------|-------------|
| app_key | INTEGER | FK → dim_app |
| category_key | INTEGER | FK → dim_category |
| date_key | INTEGER | FK → dim_date |
| installs | BIGINT | Cleaned numeric installs |
| reviews_count | INTEGER | Total reviews |
| sentiment_score | FLOAT | Avg sentiment from reviews |

## Dimension Tables

### `dim_app`
- `app_key` (PK)
- `app_id` (natural key = app name)
- `app_size`, `current_version`, `android_version`

### `dim_category`
- `category_key` (PK)
- `category_name`

### `dim_date`
- `date_key` (PK, format: YYYYMMDD)
- `full_date`, `year`, `month`, `day`
