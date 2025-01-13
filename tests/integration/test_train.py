import unittest
import numpy as np
from models.q_learning import PortfolioAgent
from src.train import train

class TestTrain(unittest.TestCase):

    def setUp(self):
        self.mean_returns = np.array([0.1, 0.2, 0.15])
        self.cov_matrix = np.array([[0.1, 0.02, 0.01],
                                     [0.02, 0.08, 0.03],
                                     [0.01, 0.03, 0.09]])
        self.agent = PortfolioAgent(num_assets=3, learning_rate=0.1, discount_factor=0.95, epsilon=0.1, step_size=0.1)

    def test_train_convergence(self):
        best_sharpe, best_weights, max_q = train(self.agent, self.mean_returns, self.cov_matrix, num_episodes=100)
        self.assertGreater(best_sharpe, 0, "Le ratio de Sharpe obtenu doit être positif.")
        self.assertAlmostEqual(np.sum(best_weights), 1.0, places=5, msg="Les poids obtenus doivent sommer à 1.")

if __name__ == '__main__':
    unittest.main()