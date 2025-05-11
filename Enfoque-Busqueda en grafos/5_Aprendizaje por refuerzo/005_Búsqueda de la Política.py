# -*- coding: utf-8 -*-
"""
Búsqueda de Política con Gradiente de Política (REINFORCE)
Entorno: CartPole-v1 de OpenAI Gym
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import gym
import matplotlib.pyplot as plt

# 1. Configuración del Entorno
env = gym.make('CartPole-v1')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n


# 2. Construcción de la Política (Red Neuronal)
class PolicyNetwork(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = layers.Dense(24, activation='relu')
        self.dense2 = layers.Dense(24, activation='relu')
        self.output_layer = layers.Dense(action_dim, activation='softmax')

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return self.output_layer(x)


policy_net = PolicyNetwork()
optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)


# 3. Función para Generar Episodios
def generate_episode(policy_net, max_steps=1000):
    states, actions, rewards = [], [], []
    state = env.reset()

    for _ in range(max_steps):
        state = np.array(state, dtype=np.float32)
        action_probs = policy_net(state[np.newaxis, :]).numpy()[0]
        action = np.random.choice(action_dim, p=action_probs)

        next_state, reward, done, _ = env.step(action)

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
        with tf.GradientTape() as tape:
            # Generar episodio
            states, actions, rewards = generate_episode(policy_net)

            # Calcular retornos descontados
            returns = []
            G = 0
            for r in reversed(rewards):
                G = r + gamma * G
                returns.insert(0, G)

            returns = np.array(returns)
            returns = (returns - np.mean(returns)) / (np.std(returns) + 1e-9)  # Normalización

            # Convertir a tensores
            states = tf.convert_to_tensor(np.array(states), dtype=tf.float32)
            actions = tf.convert_to_tensor(np.array(actions), dtype=tf.int32)
            returns = tf.convert_to_tensor(returns, dtype=tf.float32)

            # Calcular pérdida
            action_probs = policy_net(states)
            selected_action_probs = tf.reduce_sum(
                action_probs * tf.one_hot(actions, action_dim), axis=1)
            loss = -tf.reduce_mean(tf.math.log(selected_action_probs) * returns)

            # Actualizar política
            grads = tape.gradient(loss, policy_net.trainable_variables)
            optimizer.apply_gradients(zip(grads, policy_net.trainable_variables))

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
        done = False
        total_reward = 0

        while not done:
            env.render()
            action_probs = policy_net(np.array([state], dtype=np.float32)).numpy()[0]
            action = np.argmax(action_probs)
            state, reward, done, _ = env.step(action)
            total_reward += reward

        print(f"Episodio de demo {episode + 1}: Recompensa = {total_reward}")
    env.close()


print("\n==== Demostración ====")
demo_policy(policy_net)