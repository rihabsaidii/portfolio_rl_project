import unittest
import numpy as np
from models.q_learning import PortfolioAgent

class TestPortfolioAgent(unittest.TestCase):

    def setUp(self):
        """Initialisation avant chaque test."""
        self.agent = PortfolioAgent(num_assets=3, learning_rate=0.1, discount_factor=0.95, epsilon=0.1, step_size=0.1)
        self.mean_returns = np.array([0.1, 0.2, 0.15])
        self.cov_matrix = np.array([[0.1, 0.02, 0.01],
                                     [0.02, 0.08, 0.03],
                                     [0.01, 0.03, 0.09]])

    def test_action_space(self):
        """Test que l'espace des actions contient les bonnes combinaisons de poids."""
        action_space = self.agent.action_space
        self.assertTrue(len(action_space) > 0, "L'espace des actions doit contenir des combinaisons.")
        self.assertAlmostEqual(np.sum(action_space[0]), 1.0, places=5, msg="La somme des poids doit être égale à 1.")

    def test_sharpe_ratio(self):
        """Test que le calcul du ratio de Sharpe est correct."""
        weights = np.array([0.4, 0.4, 0.2])
        sharpe = self.agent.sharpe_ratio(weights, self.mean_returns, self.cov_matrix)
        self.assertIsInstance(sharpe, float, "Le ratio de Sharpe doit être un float.")
        self.assertGreater(sharpe, 0, "Le ratio de Sharpe doit être positif pour des données positives.")

    def test_q_table_update(self):
        """Test que la Q-table est mise à jour correctement."""
        state = 0
        action = 1
        reward = 1.0
        next_state = 2
        initial_q_value = self.agent.q_table[state, action]

        self.agent.update_q_table(state, action, reward, next_state)
        updated_q_value = self.agent.q_table[state, action]
        self.assertGreater(updated_q_value, initial_q_value, "La valeur Q doit augmenter après une mise à jour.")

if __name__ == '__main__':
    unittest.main()
