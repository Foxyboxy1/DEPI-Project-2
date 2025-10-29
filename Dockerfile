# استخدام صورة Python بدلاً من Airflow مباشرة
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create airflow user
RUN useradd -m -u 50000 -s /bin/bash airflow

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Upgrade pip and install requirements
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=airflow:airflow . .

# Switch to airflow user
USER airflow

# Configure environment
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=mysql+pymysql://root:root@mysql:3306/playstore
ENV DBT_PROFILES_DIR=/app/dbt_project
ENV PYTHONPATH=/app:$PYTHONPATH

# Create Airflow directories
RUN mkdir -p ${AIRFLOW_HOME}/dags ${AIRFLOW_HOME}/logs ${AIRFLOW_HOME}/plugins

EXPOSE 8080

# Startup command
CMD ["bash", "-c", "airflow db init && airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com || true && airflow scheduler & airflow webserver"]