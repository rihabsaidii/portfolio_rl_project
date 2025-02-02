import os
import itertools
import json  # 📦 Pour la sauvegarde en JSON
from src.train import train  # Assurez-vous que MyAgent est défini dans train.py
from src.optimize import optimize_hyperparameters
from data.download_data import download_data
from models.q_learning import PortfolioAgent
import numpy as np
from models import markowitz

# 📂 Configuration du chemin de stockage
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(BASE_DIR, exist_ok=True)

# Définition des chemins des fichiers
RETURNS_FILE = os.path.join(BASE_DIR, 'returns.csv')
PRICES_FILE = os.path.join(BASE_DIR, 'prices.csv')
RESULTS_FILE = os.path.join(BASE_DIR, 'best_params.json')  # 📝 Fichier JSON pour les paramètres optimaux
WEIGHTS_FILE = os.path.join(BASE_DIR, 'optimal_weights.json')  # 📝 Fichier JSON pour les poids optimaux


def daily_run():
    # 🛠️ Téléchargement des données
    print("📥 Téléchargement des données...")
    returns, prices = download_data()
    print("✅ Données téléchargées avec succès !")

    returns.to_csv(RETURNS_FILE, index=True)
    prices.to_csv(PRICES_FILE, index=True)

    # 🛠️ Optimisation des hyperparamètres avec Q-Learning
    tickers = returns.columns
    all_combinations = list(itertools.combinations(tickers, 2)) + list(itertools.combinations(tickers, 3))

    comparison_results = {}
    all_best_params = {}  # Dictionnaire pour stocker les meilleurs hyperparamètres
    all_optimal_weights = {}  # Dictionnaire pour stocker les poids optimaux

    for combination in all_combinations:
        subset_returns = returns[list(combination)]
        mean_returns = subset_returns.mean()
        cov_matrix = subset_returns.cov()

        # ✅ Q-Learning Optimization
        best_params = optimize_hyperparameters(mean_returns, cov_matrix, 50)
        agent = PortfolioAgent(len(combination), **best_params)
        best_sharpe_q, best_weights_q, _ = train(agent, mean_returns, cov_matrix)

        # ✅ Markowitz Optimization
        markowitz_results = markowitz.optimize_portfolio(mean_returns, cov_matrix)

        # 🔄 Comparaison des résultats
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

    # Sauvegarde des résultats dans un fichier JSON
    with open(os.path.join(BASE_DIR, 'comparison_results.json'), 'w') as json_file:
        json.dump(comparison_results, json_file, default=str,
                  indent=4)  # Utilisation de 'default=str' pour d'autres types non sérialisables

    with open(RESULTS_FILE, 'w') as json_file:
        json.dump(all_best_params, json_file, default=str, indent=4)

    with open(WEIGHTS_FILE, 'w') as json_file:
        json.dump(all_optimal_weights, json_file, default=str, indent=4)

    print("🏁 Comparaison Markowitz vs Q-Learning terminée avec succès.")


# ✅ **Exécution principale**
if __name__ == "__main__":
    daily_run()






