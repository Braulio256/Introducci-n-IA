"""
Proceso de Decisión de Markov (MDP) completo con:
1. Definición de estados, acciones, recompensas y transiciones
2. Algoritmo de Iteración de Valores
3. Visualización de resultados
"""
from matplotlib import pyplot as plt

# ======================
# 1. Definición del MDP
# ======================
# Estados: 0 (Inicio), 1 (Peligro), 2 (Meta)
# Acciones: A (Arriba), B (Derecha), C (Abajo), D (Izquierda)

# Recompensas: R(s, a, s')
recompensas = {
    0: {"A": {0: -1, 1: 5},  # Desde estado 0, acción A
        "B": {1: 0}},  # Desde estado 0, acción B
    1: {"A": {1: -1, 2: 10},  # Desde estado 1, acción A
        "B": {2: 0}},  # Desde estado 1, acción B
    2: {}  # Estado terminal (Meta)
}

# Probabilidades de transición: P(s'|s,a)
transiciones = {
    0: {"A": {0: 0.2, 1: 0.8},  # Desde 0, A tiene 20% de fallar
        "B": {1: 1.0}},  # Desde 0, B siempre funciona
    1: {"A": {1: 0.3, 2: 0.7},  # Desde 1, A tiene 30% de fallar
        "B": {2: 1.0}},  # Desde 1, B siempre funciona
    2: {}
}

# Parámetros
gamma = 0.9  # Factor de descuento
epsilon = 1e-5  # Criterio de convergencia
estados = [0, 1, 2]
acciones = ["A", "B"]


# ======================
# 2. Algoritmo de Iteración de Valores
# ======================
def value_iteration():
    # Inicialización de valores
    V = {s: 0 for s in estados}
    historia_V = [V.copy()]  # Para guardar historial

    iteracion = 0
    while True:
        delta = 0
        V_nuevo = V.copy()

        for s in estados[:-1]:  # Excluir estado terminal
            if not transiciones[s]:  # Si no hay acciones
                continue

            # Calcular valor para cada acción posible
            valores_acciones = {}
            for a in acciones:
                if a not in transiciones[s]:
                    continue

                valor_accion = 0
                for s_prima, prob in transiciones[s][a].items():
                    valor_accion += prob * (recompensas[s][a].get(s_prima, 0) + gamma * V[s_prima])
                valores_acciones[a] = valor_accion

            # Actualizar valor del estado (máximo sobre acciones)
            if valores_acciones:
                V_nuevo[s] = max(valores_acciones.values())
                delta = max(delta, abs(V_nuevo[s] - V[s]))

        V = V_nuevo
        historia_V.append(V.copy())
        iteracion += 1

        print(f"Iteración {iteracion}: Delta = {delta:.6f}, Valores = {V}")

        if delta < epsilon:
            break

    # Extraer política óptima
    politica = {}
    for s in estados[:-1]:
        if not transiciones[s]:
            continue

        valores_acciones = {}
        for a in acciones:
            if a not in transiciones[s]:
                continue

            valor = sum(prob * (recompensas[s][a].get(s_prima, 0) + gamma * V[s_prima])
                        for s_prima, prob in transiciones[s][a].items())
            valores_acciones[a] = valor

        if valores_acciones:
            politica[s] = max(valores_acciones, key=valores_acciones.get)

    return V, politica, historia_V


# ======================
# 3. Ejecución y Visualización
# ======================
print("=== Ejecutando Iteración de Valores ===")
V_optimo, politica_optima, historia_V = value_iteration()

print("\n=== Resultados ===")
print(f"Valores óptimos: {V_optimo}")
print(f"Política óptima: {politica_optima}")

# Gráfico de convergencia
plt.figure(figsize=(10, 5))
for s in estados[:-1]:
    valores_s = [v[s] for v in historia_V]
    plt.plot(valores_s, label=f"Estado {s}")

plt.xlabel("Iteraciones")
plt.ylabel("Valor")
plt.title("Convergencia de los Valores por Estado")
plt.legend()
plt.grid()
plt.show()