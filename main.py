# import os
# import itertools
# import json  # 📦 Pour la sauvegarde en JSON
# from src.train import train  # Assurez-vous que MyAgent est défini dans train.py
# from src.optimize import optimize_hyperparameters
# from data.download_data import download_data
# from models.q_learning import PortfolioAgent
# import numpy as np
# from models import markowitz
#
# # 📂 Configuration du chemin de stockage
# BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# os.makedirs(BASE_DIR, exist_ok=True)
#
# # Définition des chemins des fichiers
# RETURNS_FILE = os.path.join(BASE_DIR, 'returns.csv')
# PRICES_FILE = os.path.join(BASE_DIR, 'prices.csv')
# RESULTS_FILE = os.path.join(BASE_DIR, 'best_params.json')  # 📝 Fichier JSON pour les paramètres optimaux
# WEIGHTS_FILE = os.path.join(BASE_DIR, 'optimal_weights.json')  # 📝 Fichier JSON pour les poids optimaux
#
#
# def daily_run():
#     # 🛠️ Téléchargement des données
#     print("📥 Téléchargement des données...")
#     returns, prices = download_data()
#     print("✅ Données téléchargées avec succès !")
#
#     returns.to_csv(RETURNS_FILE, index=True)
#     prices.to_csv(PRICES_FILE, index=True)
#
#     # 🛠️ Optimisation des hyperparamètres avec Q-Learning
#     tickers = returns.columns
#     all_combinations = list(itertools.combinations(tickers, 2)) + list(itertools.combinations(tickers, 3))
#
#     comparison_results = {}
#     all_best_params = {}  # Dictionnaire pour stocker les meilleurs hyperparamètres
#     all_optimal_weights = {}  # Dictionnaire pour stocker les poids optimaux
#
#     for combination in all_combinations:
#         subset_returns = returns[list(combination)]
#         mean_returns = subset_returns.mean()
#         cov_matrix = subset_returns.cov()
#
#         # ✅ Q-Learning Optimization
#         best_params = optimize_hyperparameters(mean_returns, cov_matrix, 50)
#         agent = PortfolioAgent(len(combination), **best_params)
#         best_sharpe_q, best_weights_q, _ = train(agent, mean_returns, cov_matrix)
#
#         # ✅ Markowitz Optimization
#         markowitz_results = markowitz.optimize_portfolio(mean_returns, cov_matrix)
#
#         # 🔄 Comparaison des résultats
#         comparison_results[','.join(combination)] = {
#             "Q-Learning": {
#                 "sharpe_ratio": best_sharpe_q,
#                 "weights": best_weights_q.tolist() if isinstance(best_weights_q, np.ndarray) else best_weights_q
#             },
#             "Markowitz": {
#                 "sharpe_ratio": markowitz_results[1],
#                 "weights": markowitz_results[0]  # Assurez-vous ici aussi que markowitz_results[0] est sérialisable
#             }
#         }
#
#         # Stockage des meilleurs hyperparamètres et des poids optimaux
#         all_best_params[','.join(combination)] = best_params
#         all_optimal_weights[','.join(combination)] = best_weights_q.tolist() if isinstance(best_weights_q,
#                                                                                            np.ndarray) else best_weights_q
#
#         print(f"Comparaison pour {','.join(combination)} terminée.")
#
#     # Sauvegarde des résultats dans un fichier JSON
#     with open(os.path.join(BASE_DIR, 'comparison_results.json'), 'w') as json_file:
#         json.dump(comparison_results, json_file, default=str,
#                   indent=4)  # Utilisation de 'default=str' pour d'autres types non sérialisables
#
#     with open(RESULTS_FILE, 'w') as json_file:
#         json.dump(all_best_params, json_file, default=str, indent=4)
#
#     with open(WEIGHTS_FILE, 'w') as json_file:
#         json.dump(all_optimal_weights, json_file, default=str, indent=4)
#
#     print("🏁 Comparaison Markowitz vs Q-Learning terminée avec succès.")
#
#
# # ✅ **Exécution principale**
# if __name__ == "__main__":
#     daily_run()
# import os
# import csv
# import itertools
# import json
# import dvc.api
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# from models.q_learning import PortfolioAgent
# from models import markowitz
# from src.train import train  # Assurez-vous que MyAgent est défini dans train.py
# from src.optimize import optimize_hyperparameters
# import numpy as np
#
# # 📂 Configuration du chemin de stockage
# BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# os.makedirs(BASE_DIR, exist_ok=True)
# print(BASE_DIR)
# # Définition des chemins des fichiers
# MARKET_DATA_FILE = os.path.join(BASE_DIR, 'raw', 'market_data.csv')
# RETURNS_FILE = os.path.join(BASE_DIR, 'raw', 'returns.csv')
# # PRICES_FILE = os.path.join(BASE_DIR, 'prices.csv')
# RESULTS_FILE = os.path.join(BASE_DIR, 'best_params.json')
# WEIGHTS_FILE = os.path.join(BASE_DIR, 'optimal_weights.json')
#
#
# def load_market_data():
#     """Charge les données du fichier CSV et extrait les tickers (actifs)."""
#     with open(MARKET_DATA_FILE, 'r') as f:
#         reader = csv.reader(f)
#         # Ignore la première ligne (l'en-tête)
#         print(reader)
#
#         header = next(reader)
#         print(header)
#         market_data = list(reader)
#
#     # Extraction des tickers uniques à partir des colonnes suivantes (en excluant la première colonne de dates)
#     tickers = header[1:]  # Les tickers sont dans les colonnes suivantes après la date
#     print('market_data', market_data)
#     print('tickers', tickers)
#     return market_data, tickers
#
#
# def calculate_returns(prices):
#     """Calcule les rendements quotidiens à partir des prix."""
#     returns = []
#     for i in range(1, len(prices)):
#         daily_return = (prices[i] - prices[i - 1]) / prices[i - 1]
#         returns.append(daily_return)
#     print('returns', returns)
#     return returns
#
#
# def process_data():
#     """Processus principal pour charger les données, calculer les rendements et sauvegarder."""
#     print("📥 Chargement des données depuis DVC...")
#
#     # Télécharger les données à partir de DVC
#     dvc.api.get_url(path='data/raw/market_data.csv', rev='main',
#                     repo='https://github.com/rihabsaidii/portfolio_rl_project')
#
#     # Charger et traiter les données
#     market_data, tickers = load_market_data()
#
#     # Calcul des rendements pour chaque ticker
#     asset_returns = {}
#     for ticker in tickers:
#         # Assurez-vous que vous récupérez les prix dans la bonne colonne en fonction de votre structure de données
#         prices = []
#         for row in market_data:
#             # Supposons que row[0] est la date et que les prix des actifs sont dans les colonnes suivantes
#             ticker_prices = row[1:]  # Cela prend les prix pour tous les tickers pour cette ligne de données
#             if len(ticker_prices) > 0:
#                 # Trouvez l'indice du ticker dans la liste des tickers
#                 ticker_index = tickers.index(ticker)
#                 prices.append(float(ticker_prices[ticker_index]))  # Extraire le prix pour le ticker spécifique
#
#         # Calcul des rendements pour ce ticker
#         returns = calculate_returns(prices)
#         asset_returns[ticker] = returns
#
#     # Sauvegarde des rendements dans un fichier CSV
#     with open(RETURNS_FILE, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(["Ticker", "Return"])
#         for ticker, returns in asset_returns.items():
#             for r in returns:
#                 writer.writerow([ticker, r])
#
#     print("✅ Rendements calculés et sauvegardés !")
#
#
# # def process_data():
# #     """Processus principal pour charger les données, calculer les rendements et sauvegarder."""
# #     print("📥 Chargement des données depuis DVC...")
# #     # Télécharger les données à partir de DVC
# #     dvc.api.get_url(path='data/raw/market_data.csv', rev='main', repo='https://github.com/rihabsaidii/portfolio_rl_project')
# #
# #     # Charger et traiter les données
# #     market_data, tickers = load_market_data()
# #
# #     # Calcul des rendements pour chaque ticker
# #     asset_returns = {}
# #     for ticker in tickers:
# #         prices = [float(row[1]) for row in market_data if row[0] == ticker]  # Prix des actifs
# #         returns = calculate_returns(prices)
# #         asset_returns[ticker] = returns
# #
# #     # Sauvegarde des rendements dans un fichier CSV
# #     with open(RETURNS_FILE, 'w', newline='') as file:
# #         writer = csv.writer(file)
# #         writer.writerow(["Ticker", "Return"])
# #         for ticker, returns in asset_returns.items():
# #             for r in returns:
# #                 writer.writerow([ticker, r])
# #
# #     print("✅ Rendements calculés et sauvegardés !")
#
#
# def optimize_portfolio():
#     """Optimisation du portefeuille avec Q-Learning et Markowitz."""
#     # Charger les rendements
#     returns_data = {}
#     with open(RETURNS_FILE, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Ignorer l'en-tête
#         for row in reader:
#             ticker, daily_return = row
#             if ticker not in returns_data:
#                 returns_data[ticker] = []
#             returns_data[ticker].append(float(daily_return))
#
#     # Optimisation pour chaque combinaison d'actifs
#     all_combinations = list(itertools.combinations(returns_data.keys(), 2)) + list(itertools.combinations(returns_data.keys(), 3))
#     comparison_results = {}
#
#     all_best_params = {}
#     all_optimal_weights = {}
#
#     for combination in all_combinations:
#         # Sélection des rendements des actifs pour chaque combinaison
#         subset_returns = [returns_data[ticker] for ticker in combination]
#         mean_returns = [sum(r) / len(r) for r in subset_returns]  # Moyenne des rendements
#         cov_matrix = [[1 if i == j else 0 for i in range(len(combination))] for j in
#                       range(len(combination))]  # Matrice de covariance simplifiée
#         print('mean & cov_matrix', mean_returns, cov_matrix)
#         best_params = optimize_hyperparameters(mean_returns, cov_matrix, 50)
#         agent = PortfolioAgent(len(combination), **best_params)
#         best_sharpe_q, best_weights_q, _ = train(agent, mean_returns, cov_matrix)
#         # Optimisation avec Q-Learning
#         # agent = PortfolioAgent(len(combination), **best_params)
#         # best_sharpe_q, best_weights_q, _ = agent.train(mean_returns, cov_matrix)
#
#         # Optimisation avec Markowitz
#         markowitz_results = markowitz.optimize_portfolio(mean_returns, cov_matrix)
#         comparison_results[','.join(combination)] = {
#             "Q-Learning": {
#                 "sharpe_ratio": best_sharpe_q,
#                 "weights": best_weights_q.tolist() if isinstance(best_weights_q, np.ndarray) else best_weights_q
#             },
#             "Markowitz": {
#                 "sharpe_ratio": markowitz_results[1],
#                 "weights": markowitz_results[0]  # Assurez-vous ici aussi que markowitz_results[0] est sérialisable
#             }
#         }
#
#         # Stockage des meilleurs hyperparamètres et des poids optimaux
#         all_best_params[','.join(combination)] = best_params
#         # all_optimal_weights[','.join(combination)] = best_weights_q.tolist() if isinstance(best_weights_q,
#         #                                                                                    np.ndarray) else best_weights_q
#         #
#         # Sauvegarde des résultats
#         all_best_params[','.join(combination)] = best_params
#         all_optimal_weights[','.join(combination)] = best_weights_q
#
#         print(f"Optimisation pour {','.join(combination)} terminée.")
#
#     # Sauvegarde des résultats dans des fichiers JSON
#     with open(RESULTS_FILE, 'w') as json_file:
#         json.dump(all_best_params, json_file, indent=4)
#
#     with open(WEIGHTS_FILE, 'w') as json_file:
#         json.dump(all_optimal_weights, json_file, indent=4)
#
#     print("🏁 Optimisation terminée avec succès.")
#
# print(process_data())
# print(optimize_portfolio())
#
# # # DAG Airflow
# # default_args = {
# #     'owner': 'airflow',
# #     'retries': 1,
# #     'retry_delay': timedelta(minutes=5),
# # }
# #
# # dag = DAG(
# #     'portfolio_optimization',
# #     default_args=default_args,
# #     description='DAG pour l\'optimisation de portefeuille avec Q-Learning et Markowitz',
# #     schedule=timedelta(days=1),  # Exécution quotidienne
# #     start_date=datetime(2025, 1, 30),  # Date de démarrage
# #     catchup=False,
# # )
# #
# # # Tâches Airflow
# # process_data_task = PythonOperator(
# #     task_id='process_data',
# #     python_callable=process_data,
# #     dag=dag,
# # )
# #
# # optimize_portfolio_task = PythonOperator(
# #     task_id='optimize_portfolio',
# #     python_callable=optimize_portfolio,
# #     dag=dag,
# # )
# #
# # # Dépendances des tâches
# # process_data_task >> optimize_portfolio_task
import os
import itertools
import json
import dvc.api  # 📦 Pour charger les données via DVC
from src.train import train  # Assurez-vous que MyAgent est défini dans train.py
from src.optimize import optimize_hyperparameters
from models.q_learning import PortfolioAgent
import numpy as np
from models import markowitz
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import gdrivefs
print(dir(gdrivefs))
# 📂 Configuration du chemin de stockage
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(BASE_DIR, exist_ok=True)

# Définition des chemins des fichiers
RETURNS_FILE = os.path.join(BASE_DIR, 'returns.csv')
# PRICES_FILE = os.path.join(BASE_DIR, 'prices.csv')
RESULTS_FILE = os.path.join(BASE_DIR, 'best_params.json')  # 📝 Fichier JSON pour les paramètres optimaux
WEIGHTS_FILE = os.path.join(BASE_DIR, 'optimal_weights.json')  # 📝 Fichier JSON pour les poids optimaux
COMPARISON_RESULTS_FILE = os.path.join(BASE_DIR, 'comparison_results.json')  # 📝 Fichier JSON pour les comparaisons

# #     dvc.api.get_url(path='data/raw/market_data.csv', rev='main', repo='https://github.com/rihabsaidii/portfolio_rl_project')

# def download_data_from_dvc():
#     """Télécharge les données des prix depuis DVC"""
#     # Téléchargez les fichiers de prix à partir du remote DVC
#     PRICES_FILE = dvc.api.get_url(path='data/raw/market_data.csv', rev='main', repo='https://github.com/rihabsaidii/portfolio_rl_project')
#     prices = pd.read_csv(PRICES_FILE)  # Lire les fichiers de données
#     return prices
import gdown
import pandas as pd


def download_data_from_dvc():
    """Télécharge les données des prix depuis Google Drive via gdown"""

    # ID du fichier Google Drive (remplace ceci par l'ID réel du fichier)
    file_id = '1s3PZMpJypoSJ7Zs7PtTTaMHuMJ-TkTMQ'  # ID à remplacer par le vrai ID de ton fichier
    url = f'https://drive.google.com/uc?id={file_id}'

    # Télécharger le fichier depuis Google Drive
    output = 'data/raw/market_data.csv'  # Où tu veux sauvegarder le fichier téléchargé
    gdown.download(url, output, quiet=False)

    # Lire les données dans le fichier CSV
    prices = pd.read_csv(output)

    return prices

def calculate_returns(prices):
    """Calcule les rendements à partir des prix"""
    prices_numeric = prices.set_index("Date")  # Définit la colonne Date comme index
    returns = prices_numeric.pct_change().dropna()
    returns.to_csv(RETURNS_FILE, index=True)
    return returns

# def calculate_returns(prices):
#     """Calcule les rendements à partir des prix"""
#     returns = prices.pct_change().dropna()
#     returns.to_csv(RETURNS_FILE, index=True)
#     return returns


def run_optimization(returns):
    """Optimise les poids avec Q-Learning et Markowitz"""
    tickers = returns.columns
    all_combinations = list(itertools.combinations(tickers, 2)) + list(itertools.combinations(tickers, 3))
    print(all_combinations)
    comparison_results = {}
    all_best_params = {}  # Dictionnaire pour stocker les meilleurs hyperparamètres
    all_optimal_weights = {}  # Dictionnaire pour stocker les poids optimaux

    for combination in all_combinations:
        subset_returns = returns[list(combination)]
        mean_returns = subset_returns.mean()
        cov_matrix = subset_returns.cov()

        # Q-Learning Optimization
        best_params = optimize_hyperparameters(mean_returns, cov_matrix, 50)
        agent = PortfolioAgent(len(combination), **best_params)
        best_sharpe_q, best_weights_q, _ = train(agent, mean_returns, cov_matrix)

        # Markowitz Optimization
        markowitz_results = markowitz.optimize_portfolio(mean_returns, cov_matrix)

        # Comparaison des résultats
        comparison_results[','.join(combination)] = {
            "Q-Learning": {
                "sharpe_ratio": best_sharpe_q,
                "weights": best_weights_q.tolist() if isinstance(best_weights_q, np.ndarray) else best_weights_q
            },
            "Markowitz": {
                "sharpe_ratio": markowitz_results[1],
                "weights": markowitz_results[0]  # Assurez-vous ici aussi que markowitz_results[0] est sérialisable
            }
        }

        # Stockage des meilleurs hyperparamètres et des poids optimaux
        all_best_params[','.join(combination)] = best_params
        all_optimal_weights[','.join(combination)] = best_weights_q.tolist() if isinstance(best_weights_q,
                                                                                           np.ndarray) else best_weights_q

        print(f"Comparaison pour {','.join(combination)} terminée.")

    # Sauvegarde dans DVC
    with open(COMPARISON_RESULTS_FILE, 'w') as json_file:
        json.dump(comparison_results, json_file, default=str, indent=4)
    with open(RESULTS_FILE, 'w') as json_file:
        json.dump(all_best_params, json_file, default=str, indent=4)
    with open(WEIGHTS_FILE, 'w') as json_file:
        json.dump(all_optimal_weights, json_file, default=str, indent=4)

    # # Ajouter les fichiers DVC
    # os.system(f"dvc add {COMPARISON_RESULTS_FILE} {RESULTS_FILE} {WEIGHTS_FILE}")
    # os.system("git add .")  # Ajoute les fichiers DVC ajoutés et les changements Git
    # os.system("git commit -m 'Ajout des résultats optimaux et comparatifs dans DVC'")  # Commit des fichiers
    # os.system("dvc push")  # Pousse les fichiers vers le remote DVC
    # print("Résultats sauvegardés dans DVC.")
    # print("🏁 Comparaison Markowitz vs Q-Learning terminée avec succès.")

import os

#Liste des fichiers à gérer dans DVC
files = [COMPARISON_RESULTS_FILE, RESULTS_FILE, WEIGHTS_FILE]

#Vérifier si les fichiers existent
missing_files = [file for file in files if not os.path.exists(file)]
if missing_files:
    print(f"Erreur : Les fichiers suivants n'existent pas et ne peuvent pas être ajoutés à DVC : {missing_files}")
    exit(1)

# Vérifier si les fichiers sont déjà suivis par DVC
tracked_files = os.popen("dvc list --dvc-only").read().splitlines()
files_to_add = [file for file in files if os.path.basename(file) not in tracked_files]

if files_to_add:
    os.system(f"dvc add {' '.join(files_to_add)}")
else:
    print("Tous les fichiers sont déjà suivis par DVC.")

# Ajouter les fichiers et commit uniquement si des changements existent
os.system("git add .")

if os.system("git diff --cached --quiet") != 0:  # Vérifier si des modifications existent
    os.system('git commit -m "Mise à jour quotidienne des résultats DVC"')
    os.system("dvc push")  # Pousser les nouveaux fichiers vers le remote
    print(" Résultats sauvegardés dans DVC.")
else:
    print(" Aucun changement détecté, pas de commit effectué.")

def daily_run():
    """Exécute le pipeline complet : téléchargement, calcul, optimisation et sauvegarde"""
    # 1. Téléchargement des données
    print(" Téléchargement des données...")
    prices = download_data_from_dvc()
    # prices = prices.apply(pd.to_numeric, errors='coerce')

    print(prices)
    print(" Données téléchargées avec succès !")

    # 2. Calcul des rendements
    returns = calculate_returns(prices)
    print(" Rendements calculés.")

    # 3. Optimisation des poids et comparaison
    run_optimization(returns)

daily_run()