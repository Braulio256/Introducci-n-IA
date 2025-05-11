import random  # Para generar números aleatorios
import math    # Para funciones matemáticas como exp()


# Función objetivo de ejemplo: mínimo en x=2, y=3, valor mínimo = 10
def funcion_objetivo(x, y):
    return (x - 2) ** 2 + (y - 3) ** 2 + 10


def temple_simulado(funcion, solucion_inicial, temperatura_inicial=1000, enfriamiento=0.95,
                    iter_por_temp=100, temp_minima=0.1, paso=0.5):
    """
    Implementación del algoritmo de Temple Simulado para minimizar una función.

    Args:
        funcion: Función objetivo a minimizar.
        solucion_inicial: Lista [x, y] con el punto de partida.
        temperatura_inicial: Temperatura inicial para la simulación.
        enfriamiento: Factor de reducción de temperatura por ciclo (0 < enfriamiento < 1).
        iter_por_temp: Iteraciones internas por temperatura.
        temp_minima: Temperatura mínima para detener el algoritmo.
        paso: Tamaño máximo de cambio al generar un vecino.

    Returns:
        Tupla con la mejor solución encontrada y su valor.
    """
    # Validación básica de parámetros
    if not isinstance(solucion_inicial, list) or len(solucion_inicial) != 2:
        raise ValueError("La solución inicial debe ser una lista de dos elementos [x, y].")
    if not (0 < enfriamiento < 1):
        raise ValueError("El parámetro 'enfriamiento' debe estar entre 0 y 1.")

    # Inicialización de variables
    solucion_actual = solucion_inicial.copy()                  # Solución actual
    mejor_solucion = solucion_actual.copy()                    # Mejor solución encontrada
    temperatura = temperatura_inicial                          # Temperatura inicial
    historial = [solucion_actual.copy()]                       # Historial de soluciones

    mejor_valor = funcion(*mejor_solucion)                     # Valor de la mejor solución
    valor_actual = mejor_valor                                 # Valor de la solución actual

    # Bucle principal del algoritmo
    while temperatura > temp_minima:
        for _ in range(iter_por_temp):
            # Generar un vecino aleatorio cercano a la solución actual
            vecino = [
                solucion_actual[0] + random.uniform(-paso, paso),
                solucion_actual[1] + random.uniform(-paso, paso)
            ]

            # Evaluar la función objetivo para el vecino
            valor_vecino = funcion(*vecino)

            # Calcular la diferencia de "energía" (valor)
            delta = valor_vecino - valor_actual

            # Criterio de aceptación:
            # - Si el vecino es mejor, se acepta
            # - Si es peor, se acepta con una probabilidad basada en la temperatura
            if delta < 0 or random.random() < math.exp(-delta / temperatura):
                solucion_actual = vecino.copy()
                valor_actual = valor_vecino  # Actualizar valor actual también
                historial.append(solucion_actual.copy())  # Registrar en el historial

                # Si es la mejor solución encontrada hasta ahora, actualizar
                if valor_actual < mejor_valor:
                    mejor_solucion = solucion_actual.copy()
                    mejor_valor = valor_actual

        # Reducir la temperatura según el factor de enfriamiento
        temperatura *= enfriamiento

    return mejor_solucion, mejor_valor


# --- Ejemplo de uso ---

# Generar una solución inicial aleatoria dentro del rango [0, 5] para x e y
solucion_inicial = [random.uniform(0, 5), random.uniform(0, 5)]

# Ejecutar el algoritmo de temple simulado
mejor_sol, mejor_valor = temple_simulado(funcion_objetivo, solucion_inicial)

# Mostrar resultados en consola
print(f"Solución inicial: x = {solucion_inicial[0]:.2f}, y = {solucion_inicial[1]:.2f}, "
      f"f(x,y) = {funcion_objetivo(*solucion_inicial):.2f}")
print(f"Mejor solución encontrada: x = {mejor_sol[0]:.2f}, y = {mejor_sol[1]:.2f}, "
      f"f(x,y) = {mejor_valor:.2f}")
