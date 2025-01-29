import numpy as np
from scipy.optimize import minimize


# Fonction pour calculer le ratio de Sharpe
def sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0):
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return -(portfolio_return - risk_free_rate) / portfolio_volatility  # Négatif pour maximisation


# Fonction de contrainte : les poids doivent sommer à 1
def weight_constraint(weights):
    return np.sum(weights) - 1


# Fonction principale pour optimiser le portefeuille
def optimize_portfolio(mean_returns, cov_matrix, risk_free_rate=0):
    num_assets = len(mean_returns)
    initial_weights = np.ones(num_assets) / num_assets
    bounds = tuple((0, 1) for _ in range(num_assets))
    constraints = ({'type': 'eq', 'fun': weight_constraint})

    result = minimize(
        sharpe_ratio,
        initial_weights,
        args=(mean_returns, cov_matrix, risk_free_rate),
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    if result.success:
        optimized_weights = result.x
        optimized_sharpe = -result.fun
        return optimized_weights, optimized_sharpe
    else:
        raise ValueError('optimisation échoué: ', result.message)


