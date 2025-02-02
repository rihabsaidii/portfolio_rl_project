import numpy as np
import random

np.random.seed(42)  # Fixer la graine pour NumPy
random.seed(42)     # Fixer la graine pour Python

class PortfolioAgent:
    def __init__(self, num_assets=3, learning_rate=0.1, discount_factor=0.95, epsilon=0.1, step_size=0.1):
        self.num_assets = num_assets
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.step_size = step_size

        self.action_space = self.generate_all_weight_combinations()
        self.q_table = np.zeros((len(self.action_space), len(self.action_space)))

    # import numpy as np

    def generate_all_weight_combinations(self, step_size=0.1):
        """
        Génère toutes les combinaisons possibles de poids pour un nombre donné d'actifs,
        de manière à ce que la somme des poids soit égale à 1, avec un pas de discretisation
        spécifié par `step_size`, en excluant les combinaisons contenant 0 ou 1.
        """
        # Créer un ensemble de valeurs discrètes sans inclure 0 et 1
        possible_weights = np.arange(step_size, 1, step_size)

        # Liste pour stocker les combinaisons valides
        valid_combinations = []

        # Fonction récursive pour générer toutes les combinaisons
        def generate_combinations(current_combination, remaining_assets, remaining_weight):
            if remaining_assets == 1:
                # Pour le dernier actif, le poids est déterminé par le poids restant
                if step_size <= remaining_weight < 1:  # Exclure 0 et 1
                    new_combination = current_combination + [remaining_weight]
                    if 0 not in new_combination and 1 not in new_combination:
                        valid_combinations.append(new_combination)
            else:
                # Pour les autres actifs, on explore toutes les possibilités
                for weight in possible_weights:
                    if sum(current_combination) + weight <= 1:
                        generate_combinations(current_combination + [weight], remaining_assets - 1,
                                              remaining_weight - weight)

        # Démarrer la génération des combinaisons avec un poids restant de 1
        generate_combinations([], self.num_assets, 1)

        return np.array(valid_combinations)

    # def generate_all_weight_combinations(self, step_size=0.1):
    #     """
    #     Génère toutes les combinaisons possibles de poids pour un nombre donné d'actifs,
    #     de manière à ce que la somme des poids soit égale à 1, avec un pas de discretisation
    #     spécifié par `step_size`.
    #     """
    #     # Créer un ensemble de valeurs discrètes (par exemple, [0, 0.1, 0.2, ..., 1])
    #     possible_weights = np.arange(0, 1 + step_size, step_size)
    #
    #     # Liste pour stocker les combinaisons valides
    #     valid_combinations = []
    #
    #     # Fonction récursive pour générer toutes les combinaisons
    #     def generate_combinations(current_combination, remaining_assets, remaining_weight):
    #         if remaining_assets == 1:
    #             # Pour le dernier actif, le poids est déterminé par le poids restant
    #             if 0 <= remaining_weight <= 1:
    #                 valid_combinations.append(current_combination + [remaining_weight])
    #         else:
    #             # Pour les autres actifs, on explore toutes les possibilités
    #             for weight in possible_weights:
    #                 if sum(current_combination) + weight <= 1:
    #                     generate_combinations(current_combination + [weight], remaining_assets - 1,
    #                                           remaining_weight - weight)
    #
    #     # Démarrer la génération des combinaisons avec un poids restant de 1
    #     generate_combinations([], self.num_assets, 1)
    #
    #     return np.array(valid_combinations)


    def sharpe_ratio(self, weights, mean_returns, cov_matrix, risk_free_rate=0):
        """
        Calcul du ratio de Sharpe d'un portefeuille.
        """
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return (portfolio_return - risk_free_rate) / portfolio_volatility

    def select_action(self, state):
        """
        Sélectionner une action selon la stratégie epsilon-greedy.
        """
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.randint(0, len(self.action_space))  # Exploration
        else:
            return np.argmax(self.q_table[state])  # Exploitation

    def update_q_table(self, state, action, reward, next_state):
        """
        Mise à jour de la Q-table avec la règle de Q-learning.
        """
        max_future_q = np.max(self.q_table[next_state])
        current_q = self.q_table[state, action]
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        self.q_table[state, action] = new_q

