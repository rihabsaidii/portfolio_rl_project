import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Ajouter le chemin vers le dossier 'dags' où se trouve 'scripts'
# sys.path.insert(0, '/home/rihab/airflow/dags')

# Importer les fonctions de 'scripts/data_collection'
from scripts.data_collection import fetch_data, save_data

# Paramètres par défaut pour Airflow
DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 29),
}

# Liste des symboles des actifs
ASSETS = ["AAPL", "PG", "XOM"]  # Mise à jour des actifs

# Utiliser la date d'aujourd'hui comme END_DATE
START_DATE = "2022-01-01"
END_DATE = datetime.today().strftime('%Y-%m-%d')  # Date actuelle

INTERVAL = "1d"
OUTPUT_DIR = "data/raw"

# Définir le DAG
dag = DAG(
    'data_collection_dag',
    default_args=DEFAULT_ARGS,
    description='Collecte des données ajustées de clôture',
    schedule_interval=timedelta(days=1),  # Exécuter tous les jours
)

def collect_and_save_data():
    # Collecte des données
    data = fetch_data(ASSETS, START_DATE, END_DATE, INTERVAL)
    # Sauvegarde des données
    save_data(data, OUTPUT_DIR)

# Définir la tâche Airflow
collect_data_task = PythonOperator(
    task_id='collect_and_save_data_task',
    python_callable=collect_and_save_data,
    dag=dag,
)

# Lancer la tâche
collect_data_task
