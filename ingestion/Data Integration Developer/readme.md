# Google Play Store Data Integration & DuckDB Extraction

This project integrates Google Play Store app data with user reviews into one clean dataset and prepares it for use in DuckDB or other analytical tools.

## Overview

The project performs two main tasks:

- **Merging Datasets**: Combines `googleplaystore.csv` and `googleplaystore_user_reviews.csv` using the `App` column.
- **Extracting Data for DuckDB**: Allows you to filter and export specific subsets of data for analysis.

## Requirements

Before running the script, make sure you have Python installed and install the required library:

```bash
pip install pandas
```

## How to Use

### 1. Run the Merge Script

This will merge both CSV files and create `integrated_data.csv`.

**Output:**
```
Integration complete! Merged file saved in folder.
```

### 2. Extract Data for DuckDB

You can filter specific data from the merged file using the provided function:

```python
from merge_duckdb_extract import extract_for_duckdb

# Extract apps in the "GAME" category
extract_for_duckdb(filter_col="Category", filter_val="GAME")
