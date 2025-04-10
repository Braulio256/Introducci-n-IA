import random
import math


# Función objetivo de ejemplo (mínimo en x=2, y=3)
def funcion_objetivo(x, y):
    return (x - 2) ** 2 + (y - 3) ** 2 + 10


def temple_simulado(funcion, solucion_inicial, temperatura_inicial=1000, enfriamiento=0.95, iter_por_temp=100,
                    temp_minima=0.1):
    """
    Implementación del Temple Simulado.

    Args:
        funcion: Función a minimizar
        solucion_inicial: [x, y].
        temperatura_inicial: Temperatura inicial (controla la exploración).
        enfriamiento: Tasa de reducción de temperatura (0 < enfriamiento < 1).
        iter_por_temp: Iteraciones por temperatura.
        temp_minima: Temperatura mínima para detenerse.

    Returns:
        (mejor_solucion, mejor_valor)
    """
    solucion_actual = solucion_inicial.copy()
    mejor_solucion = solucion_actual.copy()
    temperatura = temperatura_inicial

    while temperatura > temp_minima:
        for _ in range(iter_por_temp):
            # Generar vecino aleatorio
            vecino = [
                solucion_actual[0] + random.uniform(-0.5, 0.5),
                solucion_actual[1] + random.uniform(-0.5, 0.5)
            ]

            # Calcular diferencia de energía
            delta = funcion(*vecino) - funcion(*solucion_actual)

            # Aceptar vecino si es mejor o con probabilidad Boltzmann
            if delta < 0 or random.random() < math.exp(-delta / temperatura):
                solucion_actual = vecino.copy()

            # Actualizar mejor solución
            if funcion(*solucion_actual) < funcion(*mejor_solucion):
                mejor_solucion = solucion_actual.copy()

        # Enfriar el sistema
        temperatura *= enfriamiento

    return mejor_solucion, funcion(*mejor_solucion)


# Ejemplo de uso
solucion_inicial = [random.uniform(0, 5), random.uniform(0, 5)]
mejor_sol, mejor_valor = temple_simulado(funcion_objetivo, solucion_inicial)

print(
    f"Solución inicial: x = {solucion_inicial[0]:.2f}, y = {solucion_inicial[1]:.2f}, f(x,y) = {funcion_objetivo(*solucion_inicial):.2f}")
print(f"Mejor solución encontrada: x = {mejor_sol[0]:.2f}, y = {mejor_sol[1]:.2f}, f(x,y) = {mejor_valor:.2f}")