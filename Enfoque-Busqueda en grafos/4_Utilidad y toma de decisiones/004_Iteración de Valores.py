import matplotlib.pyplot as plt

# Definición del MDP (Proceso de Decisión de Markov)
# Estados: 0 (Inicio), 1 (Estado intermedio), 2 (Meta)
# Acciones: A (Izquierda), B (Derecha)
# Recompensas: R(s, a, s')
recompensas = {
    0: {"A": {0: 0, 1: 5}, "B": {1: 0}},  # Desde estado 0
    1: {"A": {0: 0, 2: 10}, "B": {2: 0}},  # Desde estado 1
    2: {}  # Estado terminal (Meta)
}

# Probabilidades de transición (determinista en este caso)
transiciones = {
    0: {"A": {0: 0.2, 1: 0.8}, "B": {1: 1.0}},  # Desde estado 0
    1: {"A": {0: 0.3, 2: 0.7}, "B": {2: 1.0}},  # Desde estado 1
    2: {}  # Estado terminal
}

# Parámetros del algoritmo
gamma = 0.9  # Factor de descuento
epsilon = 0.01  # Criterio de convergencia
estados = [0, 1, 2]
acciones = ["A", "B"]

# Inicialización de valores
V = {s: 0 for s in estados}  # Valores iniciales (cero)

# Algoritmo de Iteración de Valores
def value_iteration():
    iteracion = 0
    while True:
        delta = 0
        V_nuevo = V.copy()
        for s in estados[:-1]:  # Ignorar estado terminal
            if not transiciones[s]:  # Si no hay acciones posibles (terminal)
                continue
            # Calcular el valor para cada acción posible
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
        # Actualizar valores
        V.update(V_nuevo)
        iteracion += 1
        print(f"Iteración {iteracion}: Valores = {V}")
        if delta < epsilon:
            break
    return V

# Ejecutar el algoritmo
V_optimo = value_iteration()

# Extraer política óptima
def extraer_politica(V):
    politica = {}
    for s in estados[:-1]:
        if not transiciones[s]:
            continue
        valores_acciones = {}
        for a in acciones:
            if a not in transiciones[s]:
                continue
            valor = 0
            for s_prima, prob in transiciones[s][a].items():
                valor += prob * (recompensas[s][a].get(s_prima, 0) + gamma * V[s_prima])
            valores_acciones[a] = valor
        if valores_acciones:
            politica[s] = max(valores_acciones, key=valores_acciones.get)
    return politica

politica_optima = extraer_politica(V_optimo)
print(f"\nPolítica óptima: {politica_optima}")

# Gráfico de convergencia de valores
estados_grafico = [0, 1]
plt.plot([V_optimo[s] for s in estados_grafico], marker="o")
plt.xticks(range(len(estados_grafico)), estados_grafico)
plt.xlabel("Estado")
plt.ylabel("Valor Óptimo (V)")
plt.title("Convergencia de los Valores por Estado")
plt.grid()
plt.show()