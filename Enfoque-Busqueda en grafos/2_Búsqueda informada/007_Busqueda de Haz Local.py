import random  # Importa el módulo para generar números aleatorios


#############################
# FUNCIÓN OBJETIVO (PROBLEMA)
#############################
def funcion_objetivo(x):
    """
    Función objetivo que queremos maximizar.
    Tiene un máximo en x = 3 con valor = 15.
    """
    return -(x - 3) ** 2 + 15


#############################
# GENERACIÓN DE VECINOS
#############################
def generar_vecinos(x, paso=0.1, n_vecinos=5):
    """
    Genera vecinos aleatorios cercanos a una solución x.

    Args:
        x: Valor actual.
        paso: Tamaño máximo del cambio.
        n_vecinos: Número de vecinos a generar.

    Returns:
        Lista de vecinos generados.
    """
    return [x + random.uniform(-paso, paso) for _ in range(n_vecinos)]


#############################
# ALGORITMO PRINCIPAL
#############################
def busqueda_haz_local(funcion, k=3, max_iter=100, paso=0.1):
    """
    Implementación del algoritmo de Búsqueda de Haz Local.

    Args:
        funcion: Función a maximizar.
        k: Número de elementos en el haz.
        max_iter: Máximo número de iteraciones.
        paso: Magnitud del cambio al generar vecinos.

    Returns:
        La mejor solución encontrada y su valor.
    """

    # Validación básica de parámetros
    if k <= 0 or max_iter <= 0:
        raise ValueError("Los parámetros 'k' y 'max_iter' deben ser mayores que cero.")

    # Inicialización del haz con k soluciones aleatorias dentro del dominio [0, 6]
    haz_actual = [random.uniform(0, 6) for _ in range(k)]

    # Historial de soluciones (opcional)
    historial = [haz_actual.copy()]

    # Bucle principal de iteración
    for _ in range(max_iter):
        vecinos = []  # Lista donde se almacenan los vecinos generados

        # Para cada estado en el haz actual, generar k vecinos
        for estado in haz_actual:
            vecinos.extend(generar_vecinos(estado, paso=paso, n_vecinos=k))

        # Ordenar los vecinos de mejor a peor según la función objetivo
        vecinos.sort(key=lambda x: -funcion(x))  # Negativo porque es maximización

        # Actualizar el haz con los k mejores vecinos encontrados
        haz_actual = vecinos[:k]

        # Registrar el nuevo haz (opcional)
        historial.append(haz_actual.copy())

        # Condición de convergencia: si todos los estados tienen valores similares, detenemos
        if all(abs(funcion(x) - funcion(haz_actual[0])) < 0.001 for x in haz_actual):
            break

    # Seleccionar la mejor solución final del haz
    mejor_estado = max(haz_actual, key=funcion)
    mejor_valor = funcion(mejor_estado)

    return mejor_estado, mejor_valor


#############################
# EJECUCIÓN Y DEMOSTRACIÓN
#############################
# Ejecutamos el algoritmo con un haz de tamaño k = 3
mejor_x, mejor_valor = busqueda_haz_local(funcion_objetivo, k=3)

# Imprimir la mejor solución encontrada
print(f"Mejor solución encontrada: x = {mejor_x:.2f}, f(x) = {mejor_valor:.2f}")
