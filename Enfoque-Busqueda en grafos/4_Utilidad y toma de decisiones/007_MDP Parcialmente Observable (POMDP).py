# -*- coding: utf-8 -*-
"""
Implementación básica de un POMDP (Proceso de Decisión de Markov Parcialmente Observable)
con algoritmo de Filtrado de Bayes para actualizar creencias.
"""
import numpy as np
from matplotlib import pyplot as plt

# ======================
# 1. Definición del POMDP
# ======================
# Estados: 0 (Inicio), 1 (Peligro), 2 (Meta)
# Acciones: A (Arriba), B (Derecha)
# Observaciones: 'limpio', 'sucio', 'meta'

# Matriz de transición: P(s'|s,a)
transiciones = {
    0: {"A": {0: 0.2, 1: 0.8},  # Desde 0, acción A
        "B": {1: 1.0}},  # Desde 0, acción B
    1: {"A": {1: 0.3, 2: 0.7},  # Desde 1, acción A
        "B": {2: 1.0}},  # Desde 1, acción B
    2: {"A": {2: 1.0}, "B": {2: 1.0}}  # Estado terminal
}

# Matriz de observación: P(o|s')
observaciones = {
    0: {"limpio": 0.8, "sucio": 0.2},  # En estado 0
    1: {"limpio": 0.3, "sucio": 0.7},  # En estado 1
    2: {"meta": 1.0}  # En estado 2
}

# Recompensas: R(s,a,s')
recompensas = {
    0: {"A": {0: -1, 1: 5}, "B": {1: 0}},
    1: {"A": {1: -1, 2: 10}, "B": {2: 0}},
    2: {"A": {2: 0}, "B": {2: 0}}
}

# Parámetros
gamma = 0.9  # Factor de descuento
estados = [0, 1, 2]
acciones = ["A", "B"]
obs_posibles = ["limpio", "sucio", "meta"]


# ======================
# 2. Filtrado de Bayes
# ======================
def actualizar_creencia(creencia_anterior, accion, observacion):
    """
    Actualiza la distribución de creencia usando el filtro de Bayes.

    Args:
        creencia_anterior: np.array con P(s)
        accion: Acción tomada
        observacion: Observación recibida

    Returns:
        np.array: Nueva distribución de creencia P(s')
    """
    nueva_creencia = np.zeros(len(estados))

    for s_prima in estados:
        # P(s'|a,o) ∝ P(o|s') * Σ_s P(s'|s,a)P(s)
        prob_obs = observaciones[s_prima].get(observacion, 0)
        suma = 0
        for s in estados:
            suma += transiciones[s][accion].get(s_prima, 0) * creencia_anterior[s]
        nueva_creencia[s_prima] = prob_obs * suma

    # Normalizar
    if np.sum(nueva_creencia) > 0:
        nueva_creencia /= np.sum(nueva_creencia)
    else:
        nueva_creencia = np.ones(len(estados)) / len(estados)

    return nueva_creencia


# ======================
# 3. Simulación POMDP
# ======================
def simular_pomdp(politica, pasos=10):
    """
    Simula la ejecución del POMDP bajo una política dada.

    Args:
        politica: Función que mapea creencias a acciones
        pasos: Número de pasos a simular
    """
    # Creencia inicial (uniforme)
    creencia = np.array([1 / len(estados)] * len(estados))
    estado_real = np.random.choice(estados)  # Estado real oculto

    historial = {
        'creencia': [creencia.copy()],
        'estado_real': [estado_real],
        'acciones': [],
        'observaciones': []
    }

    for _ in range(pasos):
        # Seleccionar acción basada en la creencia
        accion = politica(creencia)

        # Transición de estado real (oculto)
        prob_trans = [transiciones[estado_real][accion].get(s, 0) for s in estados]
        nuevo_estado = np.random.choice(estados, p=prob_trans)

        # Generar observación
        prob_obs = list(observaciones[nuevo_estado].values())
        obs_keys = list(observaciones[nuevo_estado].keys())
        observacion = np.random.choice(obs_keys, p=prob_obs)

        # Actualizar creencia
        creencia = actualizar_creencia(creencia, accion, observacion)

        # Guardar historial
        historial['estado_real'].append(nuevo_estado)
        historial['creencia'].append(creencia.copy())
        historial['acciones'].append(accion)
        historial['observaciones'].append(observacion)

        estado_real = nuevo_estado

        # Terminar si llegamos a la meta
        if estado_real == 2:
            break

    return historial


# ======================
# 4. Política Simple
# ======================
def politica_simple(creencia):
    """Política que siempre elige la acción A"""
    return "A"


# ======================
# 5. Ejecución y Visualización
# ======================
print("=== Simulación POMDP ===")
historial = simular_pomdp(politica_simple, pasos=10)

# Mostrar resultados
print("\nEstado real:", historial['estado_real'])
print("Acciones:", historial['acciones'])
print("Observaciones:", historial['observaciones'])
print("\nEvolución de la creencia:")
for i, creencia in enumerate(historial['creencia']):
    print(f"Paso {i}: Estado={historial['estado_real'][i]}, Creencia={np.round(creencia, 2)}")

# Gráfico de evolución de creencias
plt.figure(figsize=(10, 5))
for s in estados:
    creencias_s = [c[s] for c in historial['creencia']]
    plt.plot(creencias_s, label=f"Creencia estado {s}", marker='o')

plt.xlabel("Paso de tiempo")
plt.ylabel("Probabilidad")
plt.title("Evolución de la Distribución de Creencia")
plt.legend()
plt.grid()
plt.show()