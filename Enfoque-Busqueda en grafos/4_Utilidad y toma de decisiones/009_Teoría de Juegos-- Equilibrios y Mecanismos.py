import numpy as np

# ======================
# 1. Definición del Juego
# ======================
# Jugadores: A, B
# Estrategias: Cooperar (C), Desertar (D)

# Matriz de pagos (recompensas)
# Formato: (Pago A, Pago B)
pagos = {
    ('C', 'C'): (-1, -1),  # Ambos cooperan: 1 año de cárcel
    ('C', 'D'): (-3, 0),  # A coopera, B deserta: A 3 años, B libre
    ('D', 'C'): (0, -3),  # A deserta, B coopera: A libre, B 3 años
    ('D', 'D'): (-2, -2)  # Ambos desertan: 2 años cada uno
}


# ======================
# 2. Encontrar Equilibrios de Nash
# ======================
def encontrar_equilibrios(pagos):
    equilibrios = []
    estrategias = ['C', 'D']

    # Verificar todas las combinaciones de estrategias puras
    for a_strat in estrategias:
        for b_strat in estrategias:
            es_equilibrio = True

            # Verificar si A puede mejorar desertando
            for a_dev in estrategias:
                if a_dev == a_strat:
                    continue
                if pagos[(a_dev, b_strat)][0] > pagos[(a_strat, b_strat)][0]:
                    es_equilibrio = False
                    break

            # Verificar si B puede mejorar desertando
            for b_dev in estrategias:
                if b_dev == b_strat:
                    continue
                if pagos[(a_strat, b_dev)][1] > pagos[(a_strat, b_strat)][1]:
                    es_equilibrio = False
                    break

            if es_equilibrio:
                equilibrios.append((a_strat, b_strat))

    return equilibrios


# Encontrar equilibrios en el juego original
equilibrios = encontrar_equilibrios(pagos)
print("Equilibrios de Nash (estrategias puras):", equilibrios)


# ======================
# 3. Mecanismo de Compensación
# ======================
def diseñar_mecanismo(pagos_originales, objetivo=('C', 'C')):
    """
    Diseña un mecanismo de compensación para hacer que el objetivo sea equilibrio de Nash.
    Devuelve los pagos modificados.
    """
    pagos_modificados = pagos_originales.copy()

    # Calcular incentivos necesarios
    # Para el jugador A:
    incentivo_A = max(0, pagos[('D', 'C')][0] - pagos[('C', 'C')][0] + 0.1)
    # Para el jugador B:
    incentivo_B = max(0, pagos[('C', 'D')][1] - pagos[('C', 'C')][1] + 0.1)

    # Aplicar compensaciones
    pagos_modificados[('C', 'C')] = (
        pagos_originales[('C', 'C')][0] + incentivo_A,
        pagos_originales[('C', 'C')][1] + incentivo_B
    )

    return pagos_modificados, (incentivo_A, incentivo_B)


# Diseñar mecanismo para hacer (C, C) equilibrio
pagos_compensados, incentivos = diseñar_mecanismo(pagos)
print("\nPagos compensados:", pagos_compensados)
print("Incentivos necesarios (A, B):", incentivos)

# Verificar nuevo equilibrio
nuevos_equilibrios = encontrar_equilibrios(pagos_compensados)
print("Nuevos equilibrios:", nuevos_equilibrios)


# ======================
# 4. Juegos Repetidos y Estrategias
# ======================
def jugar_repetido(pagos, rondas=10, estrategia_A='Tit-for-Tat', estrategia_B='Always_D'):
    historial = []
    accion_prev_A = None
    accion_prev_B = None

    for ronda in range(rondas):
        # Determinar acciones
        if estrategia_A == 'Tit-for-Tat':
            accion_A = 'C' if ronda == 0 else accion_prev_B
        elif estrategia_A == 'Always_C':
            accion_A = 'C'
        else:  # Always_D
            accion_A = 'D'

        if estrategia_B == 'Tit-for-Tat':
            accion_B = 'C' if ronda == 0 else accion_prev_A
        elif estrategia_B == 'Always_C':
            accion_B = 'C'
        else:  # Always_D
            accion_B = 'D'

        # Registrar resultados
        pago_A, pago_B = pagos[(accion_A, accion_B)]
        historial.append({
            'ronda': ronda + 1,
            'A': accion_A,
            'B': accion_B,
            'Pago_A': pago_A,
            'Pago_B': pago_B
        })

        accion_prev_A, accion_prev_B = accion_A, accion_B

    return historial


# Simular juego repetido
print("\nSimulación de juego repetido (Tit-for-Tat vs Always_D):")
historial = jugar_repetido(pagos, rondas=5)
for ronda in historial:
    print(f"Ronda {ronda['ronda']}: A={ronda['A']}, B={ronda['B']} | Pagos: A={ronda['Pago_A']}, B={ronda['Pago_B']}")

# ======================
# 5. Visualización
# ======================
import matplotlib.pyplot as plt

# Datos para gráfico de pagos
estrategias = ['C', 'D']
pagos_A = [[pagos[(a, b)][0] for b in estrategias] for a in estrategias]
pagos_B = [[pagos[(a, b)][1] for b in estrategias] for a in estrategias]

fig, ax = plt.subplots(figsize=(10, 4))
im = ax.imshow(pagos_A, cmap='coolwarm')

# Configurar gráfico
ax.set_xticks(np.arange(len(estrategias)))
ax.set_yticks(np.arange(len(estrategias)))
ax.set_xticklabels(estrategias)
ax.set_yticklabels(estrategias)
ax.set_xlabel('Estrategia B')
ax.set_ylabel('Estrategia A')
ax.set_title('Matriz de Pagos (Jugador A)')
plt.colorbar(im)
plt.show()