### 👩‍💻 Person 3 – Data Integration Developer

**Responsibility:**  
Integrate data from MySQL (Google Play Store CSV) and MongoDB (User Reviews JSON) into one clean dataset for later use in DuckDB and dbt.

**Tasks Done:**
1. Loaded both datasets using `pandas` (CSV + JSON).
2. Renamed columns to match on the key `App`.
3. Merged both datasets into one DataFrame.
4. Exported the final file `integrated_data.csv` inside the `data/` folder.

**Output:**
- 📄 `integrated_data.csv` → Final merged dataset ready for DuckDB team.  
- 🐍 `integration_script.py` → Python code for data merging and export.  

**Example for DuckDB Team:**
```sql
SELECT * FROM 'data/integrated_data.csv' LIMIT 10;
