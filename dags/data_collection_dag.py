from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.data_collection import fetch_data, save_data

DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 29),
}


ASSETS = ["AAPL", "PG", "XOM"]
START_DATE = "2022-01-01"
END_DATE = "2025-01-01"
INTERVAL = "1d"
OUTPUT_DIR = "data/raw"

dag = DAG(
    'data_collection_dag',
    default_args=DEFAULT_ARGS,
    description='Collecte des données boursières',
    schedule_interval=timedelta(days=1),
)

def collect_and_save_data():
    data = fetch_data(ASSETS, START_DATE, END_DATE, INTERVAL)
    save_data(data, OUTPUT_DIR)

collect_data_task = PythonOperator(
    task_id='collect_and_save_data_task',
    python_callable=collect_and_save_data,
    dag=dag,
)
