import random
import numpy as np


# Función objetivo de ejemplo (mínimo en x=2, y=3)
def funcion_objetivo(x, y):
    return (x - 2) ** 2 + (y - 3) ** 2 + 10


def generar_vecino(solucion_actual, paso=0.1):
    """Genera una solución vecina aleatoria."""
    return [
        solucion_actual[0] + random.uniform(-paso, paso),
        solucion_actual[1] + random.uniform(-paso, paso)
    ]


def busqueda_tabu(funcion, solucion_inicial, max_iter=100, tamano_lista_tabu=5, paso=0.1):
    """
    Implementación de Búsqueda Tabú.

    Args:
        funcion: Función a minimizar.
        solucion_inicial: Punto inicial [x, y].
        max_iter: Iteraciones máximas.
        tamano_lista_tabu: Tamaño de la lista tabú.
        paso: Tamaño del paso para vecinos.

    Returns:
        Mejor solución encontrada y su valor.
    """
    solucion_actual = solucion_inicial.copy()
    mejor_solucion = solucion_actual.copy()
    lista_tabu = []

    for _ in range(max_iter):
        # Generar vecinos y evaluarlos
        vecinos = [generar_vecino(solucion_actual, paso) for _ in range(10)]
        vecinos = [v for v in vecinos if v not in lista_tabu]  # Filtrar movimientos tabú

        if not vecinos:
            break  # Todos los vecinos están en la lista tabú

        # Seleccionar el mejor vecino no tabú
        mejor_vecino = min(vecinos, key=lambda v: funcion(v[0], v[1]))
        valor_actual = funcion(solucion_actual[0], solucion_actual[1])
        valor_vecino = funcion(mejor_vecino[0], mejor_vecino[1])

        # Actualizar la mejor solución global
        if valor_vecino < funcion(mejor_solucion[0], mejor_solucion[1]):
            mejor_solucion = mejor_vecino.copy()

        # Mover a la nueva solución (aunque sea peor)
        solucion_actual = mejor_vecino.copy()

        # Actualizar lista tabú (FIFO)
        lista_tabu.append(solucion_actual.copy())
        if len(lista_tabu) > tamano_lista_tabu:
            lista_tabu.pop(0)

    return mejor_solucion, funcion(mejor_solucion[0], mejor_solucion[1])


# Ejemplo de uso
solucion_inicial = [random.uniform(0, 5), random.uniform(0, 5)]
mejor_sol, mejor_valor = busqueda_tabu(funcion_objetivo, solucion_inicial)

print(
    f"Solución inicial: x = {solucion_inicial[0]:.2f}, y = {solucion_inicial[1]:.2f}, f(x,y) = {funcion_objetivo(*solucion_inicial):.2f}")
print(f"Mejor solución: x = {mejor_sol[0]:.2f}, y = {mejor_sol[1]:.2f}, f(x,y) = {mejor_valor:.2f}")