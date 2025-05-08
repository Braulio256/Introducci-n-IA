import numpy as np
import matplotlib.pyplot as plt


# ======================
# 1. Definición del Entorno
# ======================
class GridWorld:
    def __init__(self, size=4):
        self.size = size
        self.states = [(i, j) for i in range(size) for j in range(size)]
        self.terminal = [(0, 0), (size - 1, size - 1)]  # Estados terminales
        self.actions = ['↑', '→', '↓', '←']
        self.rewards = {(0, 0): 1, (3, 3): 10}  # Recompensas en terminales

    def move(self, state, action):
        """Simula el movimiento en la grilla con política aleatoria"""
        if state in self.terminal:
            return state, 0  # No hay movimiento desde terminales

        # Mapeo de acciones a movimientos
        movement = {
            '↑': (-1, 0),
            '→': (0, 1),
            '↓': (1, 0),
            '←': (0, -1)
        }

        # Aplicar movimiento con transición estocástica (80% deseado, 20% aleatorio)
        if np.random.random() < 0.8:
            new_state = (state[0] + movement[action][0], state[1] + movement[action][1])
        else:
            new_state = (state[0] + movement[np.random.choice(self.actions)][0],
                         state[1] + movement[np.random.choice(self.actions)][1])

        # Mantener dentro de los límites
        new_state = (
            max(0, min(self.size - 1, new_state[0])),
            max(0, min(self.size - 1, new_state[1]))
        )

        # Recompensa solo al llegar a terminales
        reward = self.rewards.get(new_state, 0)
        return new_state, reward


# ======================
# 2. Política a Evaluar (Ejemplo: Siempre ↑)
# ======================
def policy(state):
    """Política fija que siempre elige ↑ (puede modificarse)"""
    return '↑'


# ======================
# 3. Evaluación Directa de la Política
# ======================
def evaluate_policy(env, policy, episodes=1000, gamma=0.9):
    V = {s: 0 for s in env.states}  # Valores iniciales
    returns = {s: [] for s in env.states}  # Listas de retornos por estado

    for _ in range(episodes):
        state = env.states[np.random.randint(len(env.states))]  # Estado inicial aleatorio
        episode = []

        # Generar episodio
        while True:
            action = policy(state)
            new_state, reward = env.move(state, action)
            episode.append((state, reward))
            state = new_state
            if state in env.terminal:
                break

        # Calcular retornos descontados
        G = 0
        for t in reversed(range(len(episode))):
            state, reward = episode[t]
            G = gamma * G + reward
            if state not in [x[0] for x in episode[:t]]:  # Primera visita
                returns[state].append(G)

    # Calcular valores como promedio de retornos
    for s in env.states:
        if returns[s]:
            V[s] = np.mean(returns[s])

    return V


# ======================
# 4. Ejecución y Visualización
# ======================
env = GridWorld()
V = evaluate_policy(env, policy)

print("Valores estimados de la política:")
for i in range(env.size):
    for j in range(env.size):
        print(f"{V[(i, j)]:6.2f}", end=" ")
    print()

# Visualización
plt.figure(figsize=(8, 6))
values = np.array([V[(i, j)] for i in range(env.size) for j in range(env.size)]).reshape(env.size, env.size)
plt.imshow(values, cmap='viridis')
plt.colorbar(label='Valor')
plt.title("Mapa de Valores de la Política (Siempre ↑)")
plt.xticks([])
plt.yticks([])
for i in range(env.size):
    for j in range(env.size):
        plt.text(j, i, f"{V[(i, j)]:.1f}", ha='center', va='center', color='w')
plt.show()