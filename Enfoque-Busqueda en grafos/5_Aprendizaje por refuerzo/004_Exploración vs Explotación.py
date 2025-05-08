import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import random


# 1. Entorno de prueba
class ExplorationGridWorld:
    def __init__(self):
        self.size = 5
        self.terminal = [(0, 0), (4, 4)]
        self.actions = ['↑', '→', '↓', '←']
        self.rewards = {(0, 0): 1, (4, 4): 10, (2, 2): -5}
        self.reset()

    def reset(self):
        self.state = (2, 0)  # Estado inicial fijo
        return self.state

    def step(self, action):
        if self.state in self.terminal:
            return self.state, 0, True

        move_map = {'↑': (-1, 0), '→': (0, 1), '↓': (1, 0), '←': (0, -1)}
        new_state = (self.state[0] + move_map[action][0],
                     self.state[1] + move_map[action][1])

        new_state = (
            max(0, min(self.size - 1, new_state[0])),
            max(0, min(self.size - 1, new_state[1]))
        )

        reward = self.rewards.get(new_state, 0)
        done = new_state in self.terminal
        self.state = new_state
        return new_state, reward, done


# 2. Estrategias corregidas
def epsilon_greedy(Q, state, epsilon=0.1, **kwargs):
    if random.random() < epsilon:
        return random.choice(list(Q[state].keys()))
    return max(Q[state], key=Q[state].get)


def boltzmann_exploration(Q, state, temp=0.5, **kwargs):
    actions = list(Q[state].keys())
    q_values = np.array([Q[state][a] for a in actions])
    probs = np.exp(q_values / temp) / np.sum(np.exp(q_values / temp))
    return actions[np.random.choice(len(actions), p=probs)]


def decaying_epsilon_greedy(Q, state, episode, total_episodes=500, **kwargs):
    epsilon = 0.5 * (1 - episode / total_episodes)
    return epsilon_greedy(Q, state, epsilon)


def optimistic_initialization(Q, state, **kwargs):
    if sum(Q[state].values()) == 0:
        return random.choice(list(Q[state].keys()))
    return max(Q[state], key=Q[state].get)


# 3. Función de entrenamiento corregida
def compare_strategies(episodes=500, runs=5):
    strategies = {
        "ε-Greedy (ε=0.1)": epsilon_greedy,
        "Boltzmann (T=0.5)": boltzmann_exploration,
        "ε-Decay": decaying_epsilon_greedy,
        "Optimistic Init": optimistic_initialization
    }

    results = {name: [] for name in strategies}

    for strategy_name, strategy in strategies.items():
        print(f"\nEvaluando estrategia: {strategy_name}")
        run_rewards = []

        for _ in range(runs):
            env = ExplorationGridWorld()
            Q = defaultdict(lambda: {a: 1.0 if 'Optimistic' in strategy_name else 0 for a in env.actions})
            reward_history = []

            for episode in range(episodes):
                state = env.reset()
                total_reward = 0
                done = False

                while not done:
                    # Llamada corregida a la estrategia
                    if strategy_name == "ε-Decay":
                        action = strategy(Q, state, episode=episode)
                    else:
                        action = strategy(Q, state)

                    new_state, reward, done = env.step(action)
                    total_reward += reward

                    # Actualización Q-Learning
                    max_next = max(Q[new_state].values())
                    alpha = 0.1
                    gamma = 0.9
                    Q[state][action] += alpha * (reward + gamma * max_next * (not done) - Q[state][action])
                    state = new_state

                reward_history.append(total_reward)

            run_rewards.append(reward_history)

        results[strategy_name] = np.mean(run_rewards, axis=0)

    return results


# 4. Visualización (sin cambios)
def plot_results(results):
    plt.figure(figsize=(12, 6))

    for name, rewards in results.items():
        smoothed = np.convolve(rewards, np.ones(20) / 20, mode='valid')
        plt.plot(smoothed, label=name, linewidth=2)

    plt.title("Comparación de Estrategias de Exploración-Explotación", fontsize=14)
    plt.xlabel("Episodios", fontsize=12)
    plt.ylabel("Recompensa Promedio (suavizada)", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# Ejecución corregida
if __name__ == "__main__":
    print("==== Experimento Exploración vs Explotación ====")
    results = compare_strategies(episodes=500, runs=5)
    plot_results(results)