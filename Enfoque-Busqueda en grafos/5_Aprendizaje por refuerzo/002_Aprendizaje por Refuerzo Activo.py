import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


# ======================
# 1. Entorno GridWorld
# ======================
class GridWorld:
    def __init__(self, size=4):
        self.size = size
        self.terminal = [(0, 0), (size - 1, size - 1)]  # Estados terminales
        self.actions = ['↑', '→', '↓', '←']
        self.rewards = {(0, 0): 1, (3, 3): 10}  # Recompensas en terminales

    def reset(self):
        """Estado inicial aleatorio (no terminal)"""
        while True:
            state = (np.random.randint(self.size), np.random.randint(self.size))
            if state not in self.terminal:
                return state

    def step(self, state, action):
        """Transición de estado con recompensa"""
        if state in self.terminal:
            return state, 0, True

        # Movimiento estocástico (80% deseado, 20% aleatorio)
        if np.random.random() < 0.8:
            move = action
        else:
            move = np.random.choice(self.actions)

        # Diccionario de movimientos
        moves = {
            '↑': (-1, 0),
            '→': (0, 1),
            '↓': (1, 0),
            '←': (0, -1)
        }

        # Nuevo estado
        new_state = (
            max(0, min(self.size - 1, state[0] + moves[move][0])),
            max(0, min(self.size - 1, state[1] + moves[move][1]))
        )

        # Recompensa
        reward = self.rewards.get(new_state, 0)
        done = new_state in self.terminal

        return new_state, reward, done


# ======================
# 2. Algoritmo Q-Learning
# ======================
def q_learning(env, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    Q = defaultdict(lambda: np.zeros(len(env.actions)))
    action_idx = {a: i for i, a in enumerate(env.actions)}

    for _ in range(episodes):
        state = env.reset()
        done = False

        while not done:
            # Selección de acción ε-greedy
            if np.random.random() < epsilon:
                action = np.random.choice(env.actions)
            else:
                action = env.actions[np.argmax(Q[state])]

            # Paso en el entorno
            new_state, reward, done = env.step(state, action)

            # Actualización Q-Learning
            best_next_action = np.argmax(Q[new_state])
            td_target = reward + gamma * Q[new_state][best_next_action] * (not done)
            td_error = td_target - Q[state][action_idx[action]]
            Q[state][action_idx[action]] += alpha * td_error

            state = new_state

    # Extraer política óptima
    policy = {s: env.actions[np.argmax(q)] for s, q in Q.items()}

    return Q, policy


# ======================
# 3. Entrenamiento y Visualización
# ======================
env = GridWorld()
Q, policy = q_learning(env, episodes=5000)


# Función para mostrar resultados
def print_results(Q, policy, env):
    print("\nPolítica óptima:")
    for i in range(env.size):
        for j in range(env.size):
            state = (i, j)
            print(f"{state}: {policy.get(state, '?')}", end="  ")
        print()

    print("\nValores Q para (2,2):")
    for a, v in zip(env.actions, Q[(2, 2)]):
        print(f"{a}: {v:.2f}")


# Visualización
def plot_q_values(Q, env):
    q_grid = np.zeros((env.size, env.size))
    for (i, j), q in Q.items():
        q_grid[i, j] = np.max(q)

    plt.figure(figsize=(8, 6))
    plt.imshow(q_grid, cmap='viridis')
    plt.colorbar(label='Valor Q máximo')
    plt.title("Valores Q Máximos por Estado")
    plt.xticks(range(env.size))
    plt.yticks(range(env.size))
    for i in range(env.size):
        for j in range(env.size):
            plt.text(j, i, f"{q_grid[i, j]:.1f}", ha='center', va='center', color='w')
    plt.show()


print_results(Q, policy, env)
plot_q_values(Q, env)