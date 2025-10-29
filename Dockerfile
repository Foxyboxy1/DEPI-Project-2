FROM python:3.10-slim

WORKDIR /app
COPY . .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pymysql explicitly
RUN pip install pymysql

# Set Airflow environment variables
ENV AIRFLOW_HOME=/app/airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=mysql+pymysql://root:root@mysql:3306/playstore

EXPOSE 8080

# Run Airflow scheduler + webserver at runtime
CMD ["bash", "-c", "airflow db init && airflow scheduler & airflow webserver"]
