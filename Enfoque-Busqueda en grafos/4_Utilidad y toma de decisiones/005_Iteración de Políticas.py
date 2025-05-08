import numpy as np

# ======================
# Definición del MDP
# ======================
recompensas = {
    0: {"A": {1: 5}, "B": {1: 0}},  # Desde estado 0
    1: {"A": {2: 10}, "B": {2: 0}},  # Desde estado 1
    2: {}  # Estado terminal
}

transiciones = {
    0: {"A": {1: 1.0}, "B": {1: 1.0}},  # Transiciones deterministas
    1: {"A": {2: 1.0}, "B": {2: 1.0}},
    2: {}
}

# Parámetros
gamma = 0.9  # Factor de descuento
epsilon = 0.01  # Criterio de convergencia
estados = [0, 1, 2]
acciones = ["A", "B"]

# ======================
# Inicialización
# ======================
politica = {0: np.random.choice(acciones),
            1: np.random.choice(acciones),
            2: None}
V = {s: 0 for s in estados}


# ======================
# Algoritmo Principal
# ======================
def policy_iteration():
    global politica, V
    politica_estable = False
    iteracion = 0

    while not politica_estable:
        # ------------------------------------
        # Paso 1: Evaluación de la Política
        # ------------------------------------
        while True:
            delta = 0
            V_old = V.copy()

            for s in estados[:-1]:  # Excluir estado terminal
                if politica[s] is None:
                    continue

                a = politica[s]
                # Calculamos el nuevo valor para el estado s
                nuevo_valor = 0
                for s_prima, prob in transiciones[s][a].items():
                    recompensa = recompensas[s][a].get(s_prima, 0)
                    nuevo_valor += prob * (recompensa + gamma * V_old[s_prima])

                delta = max(delta, abs(nuevo_valor - V_old[s]))
                V[s] = nuevo_valor

            if delta < epsilon:
                break

        # ------------------------------------
        # Paso 2: Mejora de la Política
        # ------------------------------------
        politica_estable = True

        for s in estados[:-1]:  # Excluir estado terminal
            if not transiciones[s]:
                continue

            # Calculamos el valor de cada acción posible
            valores_acciones = {}
            for a in acciones:
                if a not in transiciones[s]:
                    continue

                valor_accion = 0
                for s_prima, prob in transiciones[s][a].items():
                    recompensa = recompensas[s][a].get(s_prima, 0)
                    valor_accion += prob * (recompensa + gamma * V[s_prima])
                valores_acciones[a] = valor_accion

            # Seleccionamos la mejor acción
            mejor_accion = max(valores_acciones, key=valores_acciones.get)

            # Actualizamos la política si es necesario
            if mejor_accion != politica[s]:
                politica[s] = mejor_accion
                politica_estable = False

        iteracion += 1
        print(f"\nIteración {iteracion}:")
        print(f"Política: {politica}")
        print(f"Valores: {V}")

    return politica, V


# ======================
# Ejecución
# ======================
print("=== Inicio de Iteración de Políticas ===")
politica_optima, valores_optimos = policy_iteration()

print("\n=== Resultados Finales ===")
print(f"Política óptima: {politica_optima}")
print(f"Valores óptimos: {valores_optimos}")