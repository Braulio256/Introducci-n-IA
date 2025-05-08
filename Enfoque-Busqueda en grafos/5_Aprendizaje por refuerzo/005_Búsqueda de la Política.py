import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import gym
import matplotlib.pyplot as plt

# 1. Configuración del Entorno
env = gym.make('CartPole-v1')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n


# 2. Construcción de la Política (Red Neuronal)
class PolicyNetwork(nn.Module):
    def __init__(self):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 24)
        self.fc2 = nn.Linear(24, 24)
        self.fc3 = nn.Linear(24, action_dim)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.softmax(self.fc3(x))
        return x


policy_net = PolicyNetwork()
optimizer = optim.Adam(policy_net.parameters(), lr=0.01)


# 3. Función para Generar Episodios
def generate_episode(policy_net, max_steps=1000):
    states, actions, rewards = [], [], []
    state = env.reset()

    # Manejo para diferentes versiones de Gym
    if isinstance(state, tuple):
        state = state[0]  # Para Gym v0.26+

    for _ in range(max_steps):
        # Convertir el estado a tensor correctamente
        state_tensor = torch.FloatTensor(np.array(state, dtype=np.float32))
        with torch.no_grad():
            action_probs = policy_net(state_tensor).numpy()
        action = np.random.choice(action_dim, p=action_probs)

        result = env.step(action)
        if len(result) == 4:  # Versiones antiguas de Gym
            next_state, reward, done, _ = result
        else:  # Versiones nuevas de Gym
            next_state, reward, terminated, truncated, _ = result
            done = terminated or truncated

        states.append(state)
        actions.append(action)
        rewards.append(reward)

        state = next_state
        if done:
            break

    return states, actions, rewards


# 4. Algoritmo REINFORCE (Gradiente de Política)
def reinforce(policy_net, episodes=500, gamma=0.99):
    episode_rewards = []

    for episode in range(episodes):
        # Generar episodio
        states, actions, rewards = generate_episode(policy_net)

        # Calcular retornos descontados
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        returns = np.array(returns, dtype=np.float32)
        returns = (returns - np.mean(returns)) / (np.std(returns) + 1e-9)  # Normalización

        # Convertir a tensores de PyTorch
        states = torch.FloatTensor(np.array(states, dtype=np.float32))
        actions = torch.LongTensor(np.array(actions))
        returns = torch.FloatTensor(returns)

        # Calcular pérdida
        action_probs = policy_net(states)
        selected_action_probs = action_probs.gather(1, actions.unsqueeze(1)).squeeze()
        loss = -torch.mean(torch.log(selected_action_probs) * returns)

        # Actualizar política
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Registrar progreso
        total_reward = sum(rewards)
        episode_rewards.append(total_reward)

        if (episode + 1) % 50 == 0:
            print(f"Episodio {episode + 1}: Recompensa = {total_reward}")

    return episode_rewards


# 5. Entrenamiento y Visualización
print("==== Entrenamiento con REINFORCE ====")
rewards_history = reinforce(policy_net, episodes=500)

# Gráfico de convergencia
plt.figure(figsize=(10, 5))
plt.plot(rewards_history)
plt.title("Búsqueda Directa de Política (REINFORCE)")
plt.xlabel("Episodio")
plt.ylabel("Recompensa Total")
plt.grid(True)
plt.show()


# 6. Demostración de la Política Aprendida
def demo_policy(policy_net, episodes=3):
    for episode in range(episodes):
        state = env.reset()
        if isinstance(state, tuple):
            state = state[0]
        done = False
        total_reward = 0

        while not done:
            env.render()
            state_tensor = torch.FloatTensor(np.array(state, dtype=np.float32))
            with torch.no_grad():
                action_probs = policy_net(state_tensor).numpy()
            action = np.argmax(action_probs)

            result = env.step(action)
            if len(result) == 4:
                state, reward, done, _ = result
            else:
                state, reward, terminated, truncated, _ = result
                done = terminated or truncated

            total_reward += reward

        print(f"Episodio de demo {episode + 1}: Recompensa = {total_reward}")
    env.close()


print("\n==== Demostración ====")
demo_policy(policy_net)