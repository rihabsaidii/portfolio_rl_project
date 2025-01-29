import unittest
import numpy as np
from models.markowitz import optimize_portfolio, sharpe_ratio

class TestMarkowitz(unittest.TestCase):

    def setUp(self):
        self.mean_returns = np.array([0.1, 0.2, 0.15])
        self.cov_matrix = np.array([[0.1, 0.02, 0.01],
                                     [0.02, 0.08, 0.03],
                                     [0.01, 0.03, 0.09]])

    def test_sharpe_ratio(self):
        weights = np.array([0.4, 0.4, 0.2])
        sharpe = sharpe_ratio(weights, self.mean_returns, self.cov_matrix)
        self.assertIsInstance(sharpe, float, "Le ratio de Sharpe doit être un float.")
        self.assertLess(sharpe, 0, "Le ratio de Sharpe doit être négatif car la fonction retourne le négatif pour maximisation.")

    def test_optimize_portfolio(self):
        optimized_weights, optimized_sharpe = optimize_portfolio(self.mean_returns, self.cov_matrix)
        self.assertAlmostEqual(np.sum(optimized_weights), 1.0, places=5, msg="Les poids optimaux doivent sommer à 1.")
        self.assertGreater(optimized_sharpe, 0, "Le ratio de Sharpe optimisé doit être positif.")

if __name__ == '__main__':
    unittest.main()