from models.q_learning import PortfolioAgent
import numpy as np
from src.train import train
import optuna



def objective(trial, mean_returns, cov_matrix):

    # Définir les plages d'hyperparamètres
    epsilon = trial.suggest_float('epsilon', 0, 1)  # Augmenter l'epsilon pour plus d'exploration
    discount_factor = trial.suggest_float('discount_factor', 0.8, 0.999)  # Essayer des valeurs légèrement plus petites
    learning_rate = trial.suggest_float('learning_rate', 0.0001, 0.01)

    # Initialiser l'agent avec les hyperparamètres proposés
    agent = PortfolioAgent(
        num_assets=mean_returns.shape[0],  # Ajuster au nombre d'actifs
        learning_rate=learning_rate,
        discount_factor=discount_factor,
        epsilon=epsilon
    )

    # Entraîner et évaluer l'agent avec les données
    performance, _, _ = train(agent, mean_returns, cov_matrix)
    return performance




# Fonction pour gérer l'early stopping dans l'optimisation
def early_stopping(study, patience=10):
    best_performance = -np.inf
    trials_since_improvement = 0

    for trial in study.trials:
        if trial.state == optuna.trial.TrialState.COMPLETE:
            performance = trial.value
            if performance > best_performance:
                best_performance = performance
                trials_since_improvement = 0
            else:
                trials_since_improvement += 1

            if trials_since_improvement >= patience:
                print(f"Early stopping: La performance n'a pas augmenté depuis {patience} essais.")
                return True
    return False


# Fonction d'optimisation avec EarlyStopping intégré
def optimize_hyperparameters(mean_returns, cov_matrix, n_trials, patience=10):
    study = optuna.create_study(direction='maximize')

    for trial in range(n_trials):
        study.optimize(lambda trial: objective(trial, mean_returns, cov_matrix), n_trials=1)

        if early_stopping(study, patience=patience):
            break

    print("\n✅ **Meilleurs Hyperparamètres trouvés :**")
    print(f"Performance : {study.best_value}")

    return study.best_params

