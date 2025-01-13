import os
import json
import unittest

# Définir les chemins des fichiers JSON
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEST_PARAMS_FILE = os.path.join(BASE_DIR, "data", "best_params.json")
OPTIMAL_WEIGHTS_FILE = os.path.join(BASE_DIR, "data", "optimal_weights.json")
COMPARISON_RESULTS_FILE = os.path.join(BASE_DIR, "data", "comparison_results.json")

class TestJSONFiles(unittest.TestCase):

    def test_best_params_json(self):
        # Vérifier l'existence du fichier
        self.assertTrue(os.path.exists(BEST_PARAMS_FILE), f"Le fichier {BEST_PARAMS_FILE} est introuvable.")

        # Charger et valider le contenu
        with open(BEST_PARAMS_FILE, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict, "Le fichier best_params.json doit contenir un dictionnaire.")
            for key, params in data.items():
                self.assertIn("epsilon", params, f"Clé 'epsilon' manquante pour {key}.")
                self.assertIn("discount_factor", params, f"Clé 'discount_factor' manquante pour {key}.")
                self.assertIn("learning_rate", params, f"Clé 'learning_rate' manquante pour {key}.")

    def test_optimal_weights_json(self):
        # Vérifier l'existence du fichier
        self.assertTrue(os.path.exists(OPTIMAL_WEIGHTS_FILE), f"Le fichier {OPTIMAL_WEIGHTS_FILE} est introuvable.")

        # Charger et valider le contenu
        with open(OPTIMAL_WEIGHTS_FILE, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict, "Le fichier optimal_weights.json doit contenir un dictionnaire.")
            for key, weights in data.items():
                self.assertIsInstance(weights, list, f"Les poids pour {key} doivent être une liste.")
                self.assertAlmostEqual(sum(weights), 1.0, places=5, msg=f"La somme des poids pour {key} doit être égale à 1.")

    def test_comparison_results_json(self):
        # Vérifier l'existence du fichier
        self.assertTrue(os.path.exists(COMPARISON_RESULTS_FILE), f"Le fichier {COMPARISON_RESULTS_FILE} est introuvable.")

        # Charger et valider le contenu
        with open(COMPARISON_RESULTS_FILE, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict, "Le fichier comparison_results.json doit contenir un dictionnaire.")
            for key, results in data.items():
                self.assertIn("Q-Learning", results, f"Résultats 'Q-Learning' manquants pour {key}.")
                self.assertIn("Markowitz", results, f"Résultats 'Markowitz' manquants pour {key}.")
                self.assertIn("sharpe_ratio", results["Q-Learning"], f"'sharpe_ratio' manquant pour Q-Learning dans {key}.")
                self.assertIn("weights", results["Q-Learning"], f"'weights' manquant pour Q-Learning dans {key}.")

if __name__ == "__main__":
    unittest.main()
