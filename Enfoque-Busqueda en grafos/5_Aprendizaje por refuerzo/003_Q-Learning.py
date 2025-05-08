import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import random


# ======================
# 1. Entorno Mejorado
# ======================
class AdvancedGridWorld:
    def __init__(self, size=5):
        self.size = size
        self.terminal = [(0, 0), (size - 1, size - 1)]
        self.actions = ['↑', '→', '↓', '←']
        self.rewards = {
            (0, 0): 5,
            (size - 1, size - 1): 50,
            (1, 1): -10,  # Obstáculo
            (2, 3): -5  # Penalización
        }
        self.obstacles = [(1, 1), (3, 2)]

    def reset(self):
        """Estado inicial evitando obstáculos/terminales"""
        while True:
            state = (random.randint(0, self.size - 1),
                     random.randint(0, self.size - 1))
            if state not in self.terminal and state not in self.obstacles:
                return state

    def step(self, state, action):
        if state in self.terminal:
            return state, 0, True

        # Movimiento estocástico mejorado
        prob = random.random()
        if prob < 0.7:  # 70% acción deseada
            move = action
        elif prob < 0.9:  # 20% aleatoria
            move = random.choice(self.actions)
        else:  # 10% opuesta
            opposites = {'↑': '↓', '→': '←', '↓': '↑', '←': '→'}
            move = opposites[action]

        # Aplicar movimiento
        move_effects = {'↑': (-1, 0), '→': (0, 1), '↓': (1, 0), '←': (0, -1)}
        new_state = (state[0] + move_effects[move][0],
                     state[1] + move_effects[move][1])

        # Limitar a los bordes
        new_state = (
            max(0, min(self.size - 1, new_state[0])),
            max(0, min(self.size - 1, new_state[1]))
        )

        # Verificar obstáculos
        if new_state in self.obstacles:
            return state, -10, False  # Rebote

        reward = self.rewards.get(new_state,
                                  -0.1 if new_state == state else -0.5)  # Costo por movimiento/estancamiento
        done = new_state in self.terminal

        return new_state, reward, done


# ======================
# 2. Q-Learning Mejorado
# ======================
class AdvancedQLearning:
    def __init__(self, env):
        self.env = env
        self.Q = defaultdict(lambda: np.zeros(len(env.actions)))
        self.action_map = {a: i for i, a in enumerate(env.actions)}
        self.reward_history = []
        self.steps_history = []

    def train(self, episodes=2000, alpha=0.1, gamma=0.95,
              epsilon_start=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        epsilon = epsilon_start

        for ep in range(episodes):
            state = self.env.reset()
            total_reward = 0
            steps = 0
            done = False

            while not done and steps < 100:  # Límite de pasos por episodio
                # Selección ε-greedy con decaimiento
                if random.random() < epsilon:
                    action = random.choice(self.env.actions)
                else:
                    action = self.env.actions[np.argmax(self.Q[state])]

                # Interacción con el entorno
                new_state, reward, done = self.env.step(state, action)
                total_reward += reward
                steps += 1

                # Actualización Q
                best_next = np.max(self.Q[new_state])
                td_target = reward + gamma * best_next * (not done)
                td_error = td_target - self.Q[state][self.action_map[action]]
                self.Q[state][self.action_map[action]] += alpha * td_error

                state = new_state

            # Decaimiento de ε
            epsilon = max(epsilon_min, epsilon * epsilon_decay)

            # Registro de métricas
            self.reward_history.append(total_reward)
            self.steps_history.append(steps)

            if ep % 100 == 0:
                print(f"Episodio {ep}: Recompensa={total_reward:.1f}, ε={epsilon:.3f}")

    def get_policy(self):
        return {s: self.env.actions[np.argmax(q)] for s, q in self.Q.items()}

    def visualize_learning(self):
        # Gráfico de convergencia
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(self.reward_history)
        plt.title("Recompensas por Episodio")
        plt.xlabel("Episodio")
        plt.ylabel("Recompensa Total")

        plt.subplot(1, 2, 2)
        plt.plot(self.steps_history)
        plt.title("Pasos por Episodio")
        plt.xlabel("Episodio")
        plt.ylabel("Pasos")

        plt.tight_layout()
        plt.show()


# ======================
# 3. Visualización Animada
# ======================
class QLearningVisualizer:
    def __init__(self, env, Q):
        self.env = env
        self.Q = Q
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xticks(np.arange(env.size))
        self.ax.set_yticks(np.arange(env.size))
        self.ax.grid(True)
        self.texts = []

    def draw_grid(self):
        self.ax.clear()
        q_grid = np.zeros((self.env.size, self.env.size))

        # Dibujar valores Q
        for (i, j), q in self.Q.items():
            q_grid[i, j] = np.max(q)
            for a_idx, val in enumerate(q):
                offset = 0.22
                offsets = [(0, offset), (offset, 0), (0, -offset), (-offset, 0)]
                self.ax.text(j + offsets[a_idx][0],
                             i + offsets[a_idx][1],
                             f"{val:.1f}", ha='center', va='center', fontsize=8)

        # Dibujar política
        policy = {s: np.argmax(q) for s, q in self.Q.items()}
        for (i, j), a_idx in policy.items():
            arrows = ['↑', '→', '↓', '←']
            self.ax.text(j, i, arrows[a_idx],
                         ha='center', va='center', fontsize=16, weight='bold')

        # Terminales y obstáculos
        for i, j in self.env.terminal:
            self.ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='green', alpha=0.3))
        for i, j in self.env.obstacles:
            self.ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='red', alpha=0.3))

        # Configuración visual
        im = self.ax.imshow(q_grid, cmap='viridis')
        plt.colorbar(im, ax=self.ax, label='Valor Q máximo')
        self.ax.set_title("Mapa de Valores Q y Política Óptima")


# ======================
# 4. Ejecución Completa
# ======================
env = AdvancedGridWorld()
q_learner = AdvancedQLearning(env)

print("==== Entrenamiento ====")
q_learner.train(episodes=1500)

print("\n==== Resultados ====")
policy = q_learner.get_policy()
print("\nPolítica óptima en (2,2):", policy[(2, 2)])
print("Valores Q en (2,2):", dict(zip(env.actions, q_learner.Q[(2, 2)])))
print("\nRecompensa promedio últimos 100 episodios:",
      np.mean(q_learner.reward_history[-100:]))

# Visualización
q_learner.visualize_learning()
visualizer = QLearningVisualizer(env, q_learner.Q)
visualizer.draw_grid()
plt.show()