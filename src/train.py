import random
import numpy as np
np.random.seed(42)  # Fixer la graine pour NumPy
random.seed(42)

def train(agent, mean_returns, cov_matrix, num_episodes=5000, max_steps=100, convergence_threshold=1e-3, patience=100):
    """
    Entraîne l'agent avec Q-learning et s'arrête si les différences entre Q-values consécutives se stabilisent.

    Args:
        agent: Instance de PortfolioAgent.
        mean_returns: Moyenne des rendements des actifs.
        cov_matrix: Matrice de covariance des rendements.
        num_episodes: Nombre maximum d'épisodes.
        max_steps: Nombre maximum d'étapes par épisode.
        convergence_threshold: Seuil de variation pour détecter la stabilité.
        patience: Nombre d'épisodes consécutifs pour vérifier la stabilité.
    """
    rewards_per_episode = []
    max_q_per_episode = []
    stable_count = 0

    prev_q_table = None  # Stocke la Q-table du précédent épisode

    for episode in range(num_episodes):
        state = random.randint(0, len(agent.action_space) - 1)
        total_reward = 0

        for step in range(max_steps):
            action = agent.select_action(state)
            reward = agent.sharpe_ratio(agent.action_space[action], mean_returns, cov_matrix)
            next_state = random.randint(0, len(agent.action_space) - 1)
            agent.update_q_table(state, action, reward, next_state)

            total_reward += reward
            state = next_state

        rewards_per_episode.append(total_reward)
        current_max_q = np.max(agent.q_table)
        max_q_per_episode.append(current_max_q)

        # 🔄 **Vérification de la stabilité avec les Q-values consécutives**
        if prev_q_table is not None:
            q_diff = np.max(np.abs(agent.q_table - prev_q_table))  # Différence maximale entre Q-values consécutives
            if q_diff < convergence_threshold:
                stable_count += 1
            else:
                stable_count = 0  # Réinitialiser si la condition n'est pas remplie

            if stable_count >= patience:
                print(f"⚠️ Convergence détectée après {episode + 1} épisodes. Différence max: {q_diff:.6f}")
                break

        # Stocker la Q-table actuelle comme précédente
        prev_q_table = np.copy(agent.q_table)

        # Affichage périodique
        if episode % 100 == 0:
            print(f"Episode {episode}, Total Reward: {total_reward:.4f}")

    best_action = np.argmax(agent.q_table.sum(axis=0))
    best_weights = agent.action_space[best_action]
    best_sharpe_ratio = agent.sharpe_ratio(best_weights, mean_returns, cov_matrix)

    print(f"\n✅ Meilleure pondération après {episode + 1} épisodes : {best_weights}")
    print(f"✅ Ratio de Sharpe : {best_sharpe_ratio:.4f}")

    return best_sharpe_ratio, best_weights, max_q_per_episode



