# 📊 App Performance & User Retention Analytics Platform

A complete ELT pipeline that transforms raw Google Play Store data into actionable insights using **MySQL**, **MongoDB**, **DuckDB**, **dbt**, **Airflow**, and **Dash**.

Built by the AppPulse Data Engineering Team for DEPI Project 2.

---

## 🎯 Project Overview

This platform helps app developers and investors understand:
- Top-rated and top-installed apps by category  
- Category growth over time  
- Correlation between price, rating, and installs  
- User sentiment from reviews  

**Data Sources**:
- `googleplaystore.csv` → App metadata (loaded into **MySQL**)  
- `user_reviews.json` → User reviews & sentiment (loaded into **MongoDB**)

---

## 🏗️ Architecture

```mermaid
flowchart LR
    A[CSV] -->|Ingestion| B(MySQL)
    C[JSON] -->|Ingestion| D(MongoDB)
    B -->|Extract| E[DuckDB Warehouse]
    D -->|Extract| E
    E -->|dbt Transform| F[Star Schema]
    F -->|Airflow DAG| G[Automated Refresh]
    F -->|Dash| H[Interactive Dashboard]
