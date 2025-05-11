import random  # Usamos esta librería para generar números aleatorios.


def funcion_objetivo(x, y):
    """
    Función objetivo a minimizar.
    Es una parábola con mínimo en el punto (2, 3) y valor mínimo 10.
    """
    return (x - 2) ** 2 + (y - 3) ** 2 + 10


def generar_vecino(solucion_actual, paso=0.1):
    """
    Genera un vecino aleatorio cercano a la solución actual.

    Args:
        solucion_actual: Lista con dos elementos [x, y].
        paso: Rango máximo de desplazamiento en cada dirección.

    Returns:
        Una nueva lista [x', y'] como vecino de la solución actual.
    """
    return [
        solucion_actual[0] + random.uniform(-paso, paso),  # Nuevo x dentro del rango
        solucion_actual[1] + random.uniform(-paso, paso)   # Nuevo y dentro del rango
    ]


def busqueda_tabu(funcion, solucion_inicial, max_iter=100, tamano_lista_tabu=5, paso=0.1):
    """
    Implementa el algoritmo de búsqueda tabú para minimizar una función.

    Args:
        funcion: Función objetivo a minimizar.
        solucion_inicial: Punto inicial [x, y].
        max_iter: Número máximo de iteraciones.
        tamano_lista_tabu: Tamaño de la lista tabú (memoria).
        paso: Tamaño del paso para generar vecinos.

    Returns:
        Una tupla con la mejor solución encontrada y su valor: ([x, y], f(x, y)).
    """
    solucion_actual = solucion_inicial.copy()  # Copiamos la solución inicial para no modificar la original.
    mejor_solucion = solucion_actual.copy()    # Inicialmente, la mejor solución es la actual.
    lista_tabu = []  # Lista tabú vacía al inicio.

    for _ in range(max_iter):
        # Generamos 10 vecinos aleatorios de la solución actual.
        vecinos = [generar_vecino(solucion_actual, paso) for _ in range(10)]

        # Filtramos los vecinos que están en la lista tabú.
        vecinos = [v for v in vecinos if v not in lista_tabu]

        # Si todos los vecinos están en la lista tabú, detenemos la búsqueda.
        if not vecinos:
            break

        # Seleccionamos el vecino con el menor valor de la función objetivo (mejor).
        mejor_vecino = min(vecinos, key=lambda v: funcion(v[0], v[1]))

        # Evaluamos la solución actual y el mejor vecino.
        valor_actual = funcion(solucion_actual[0], solucion_actual[1])
        valor_vecino = funcion(mejor_vecino[0], mejor_vecino[1])

        # Si el mejor vecino es mejor que la mejor solución global, lo actualizamos.
        if valor_vecino < funcion(mejor_solucion[0], mejor_solucion[1]):
            mejor_solucion = mejor_vecino.copy()

        # Nos movemos al mejor vecino, incluso si es peor (comportamiento típico de tabú).
        solucion_actual = mejor_vecino.copy()

        # Añadimos la nueva solución a la lista tabú.
        lista_tabu.append(solucion_actual.copy())

        # Si la lista tabú supera el tamaño permitido, eliminamos el más antiguo (FIFO).
        if len(lista_tabu) > tamano_lista_tabu:
            lista_tabu.pop(0)

    # Devolvemos la mejor solución encontrada y su evaluación.
    return mejor_solucion, funcion(mejor_solucion[0], mejor_solucion[1])


# --------------------- EJECUCIÓN ---------------------

# Generamos una solución inicial aleatoria con x e y entre 0 y 5.
solucion_inicial = [random.uniform(0, 5), random.uniform(0, 5)]

# Ejecutamos el algoritmo de búsqueda tabú.
mejor_sol, mejor_valor = busqueda_tabu(funcion_objetivo, solucion_inicial)

# Imprimimos los resultados con formato.
print("=== Resultados de Búsqueda Tabú ===")
print(f"Solución inicial: x = {solucion_inicial[0]:.2f}, y = {solucion_inicial[1]:.2f}, f(x, y) = {funcion_objetivo(*solucion_inicial):.2f}")
print(f"Mejor solución:   x = {mejor_sol[0]:.2f}, y = {mejor_sol[1]:.2f}, f(x, y) = {mejor_valor:.2f}")
