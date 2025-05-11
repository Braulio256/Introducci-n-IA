import random  # Importamos la librería random para generar un punto inicial aleatorio.


def funcion_objetivo(x):
    """
    Función objetivo a maximizar.
    En este caso es una parábola invertida con un máximo en x = 2.
    """
    return -x ** 2 + 4 * x + 10


def hill_climbing(funcion, x_inicial, paso=0.1, max_iter=1000):
    """
    Algoritmo de búsqueda por Ascensión de Colinas (Hill Climbing).

    Args:
        funcion: La función objetivo que se desea maximizar.
        x_inicial: El punto de partida en el espacio de búsqueda.
        paso: La distancia entre el punto actual y sus vecinos.
        max_iter: El número máximo de iteraciones permitidas.

    Returns:
        Una tupla (mejor_x, mejor_valor) donde:
        - mejor_x es el punto con la mejor evaluación encontrada.
        - mejor_valor es el valor de la función en ese punto.
    """
    x_actual = x_inicial  # Iniciamos en el punto dado.
    valor_actual = funcion(x_actual)  # Evaluamos la función en el punto inicial.

    for _ in range(max_iter):  # Iteramos hasta el máximo permitido.
        # Generamos dos vecinos: uno hacia la derecha y otro hacia la izquierda.
        vecinos = [x_actual + paso, x_actual - paso]

        # Inicializamos variables para registrar el mejor vecino encontrado.
        mejor_vecino = None
        mejor_valor_vecino = -float('inf')  # Valor muy bajo para iniciar comparación.

        # Evaluamos cada vecino generado.
        for vecino in vecinos:
            valor = funcion(vecino)
            if valor > mejor_valor_vecino:
                mejor_valor_vecino = valor
                mejor_vecino = vecino

        # Si ninguno de los vecinos mejora el valor actual, terminamos la búsqueda.
        if mejor_valor_vecino <= valor_actual:
            break

        # Actualizamos el punto actual al mejor vecino.
        x_actual = mejor_vecino
        valor_actual = mejor_valor_vecino

    # Devolvemos el mejor punto y su valor correspondiente.
    return x_actual, valor_actual


def imprimir_resultados(x_inicial, mejor_x, mejor_valor):
    """Imprime los resultados del algoritmo con formato."""
    print("=== Resultados de Hill Climbing ===")
    print(f"Inicio aleatorio: x = {x_inicial:.4f}, f(x) = {funcion_objetivo(x_inicial):.4f}")
    print(f"Máximo encontrado: x = {mejor_x:.4f}, f(x) = {mejor_valor:.4f}")


# --------------------- EJECUCIÓN ---------------------

# Generamos un punto inicial aleatorio entre -10 y 10.
x_inicial = random.uniform(-10, 10)

# Ejecutamos el algoritmo Hill Climbing.
mejor_x, mejor_valor = hill_climbing(funcion_objetivo, x_inicial)

# Imprimimos los resultados.
imprimir_resultados(x_inicial, mejor_x, mejor_valor)
