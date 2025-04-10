import random


def funcion_objetivo(x):
    """Función de ejemplo: -x^2 + 4x + 10 (tiene un máximo en x=2)"""
    return -x ** 2 + 4 * x + 10


def hill_climbing(funcion, x_inicial, paso=0.1, max_iter=1000):
    """
    Implementación de Ascensión de Colinas para maximizar una función.

    Args:
        funcion: Función a maximizar.
        x_inicial: Punto de inicio.
        paso: Tamaño del paso para generar vecinos.
        max_iter: Número máximo de iteraciones.

    Returns:
        Tupla con (mejor_x, mejor_valor)
    """
    x_actual = x_inicial
    valor_actual = funcion(x_actual)

    for _ in range(max_iter):
        # Generar vecinos (izquierda y derecha)
        vecinos = [x_actual + paso, x_actual - paso]

        # Evaluar vecinos
        mejor_vecino = None
        mejor_valor_vecino = -float('inf')

        for vecino in vecinos:
            valor = funcion(vecino)
            if valor > mejor_valor_vecino:
                mejor_valor_vecino = valor
                mejor_vecino = vecino

        # Si no hay mejora, terminar
        if mejor_valor_vecino <= valor_actual:
            break

        # Moverse al mejor vecino
        x_actual = mejor_vecino
        valor_actual = mejor_valor_vecino

    return x_actual, valor_actual


# Ejecución
x_inicial = random.uniform(-10, 10)  # Punto inicial aleatorio
mejor_x, mejor_valor = hill_climbing(funcion_objetivo, x_inicial)

print(f"Inicio: x = {x_inicial:.2f}, f(x) = {funcion_objetivo(x_inicial):.2f}")
print(f"Mejor encontrado: x = {mejor_x:.2f}, f(x) = {mejor_valor:.2f}")