import random

#############################
# FUNCIÓN OBJETIVO (PROBLEMA)
#############################
"""Función ejemplo que queremos maximizar: tiene un máximo en x=3 (valor=15)"""


def funcion_objetivo(x):
    return -(x - 3) ** 2 + 15


#############################
# GENERACIÓN DE VECINOS
#############################
"""Genera n_vecinos soluciones cercanas a x agregando ruido controlado por 'paso'"""


def generar_vecinos(x, paso=0.1, n_vecinos=5):
    return [x + random.uniform(-paso, paso) for _ in range(n_vecinos)]


#############################
# ALGORITMO PRINCIPAL
#############################
"""Implementación completa de la Búsqueda de Haz Local"""


def busqueda_haz_local(funcion, k=3, max_iter=100, paso=0.1):
    ##### INICIALIZACIÓN #####
    # Creamos un haz inicial con k soluciones aleatorias
    haz_actual = [random.uniform(0, 6) for _ in range(k)]

    ##### BÚSQUEDA PRINCIPAL #####
    for _ in range(max_iter):
        # Generación de todos los vecinos del haz actual
        vecinos = []
        for estado in haz_actual:
            vecinos.extend(generar_vecinos(estado, paso, n_vecinos=k))

        ##### SELECCIÓN #####
        # Ordenamos los vecinos de mejor a peor según la función objetivo
        vecinos.sort(key=lambda x: -funcion(x))
        # Nos quedamos solo con los k mejores
        haz_actual = vecinos[:k]

        ##### CONDICIÓN DE TERMINACIÓN (OPCIONAL) #####
        # Si todos los estados son muy similares, terminamos
        if all(abs(funcion(x) - funcion(haz_actual[0])) < 0.001 for x in haz_actual):
            break

    ##### RESULTADO FINAL #####
    # Devolvemos el mejor estado encontrado en el haz final
    mejor_estado = max(haz_actual, key=lambda x: funcion(x))
    return mejor_estado, funcion(mejor_estado)


#############################
# EJECUCIÓN Y DEMOSTRACIÓN
#############################
# Ejecutamos el algoritmo y mostramos resultados
mejor_x, mejor_valor = busqueda_haz_local(funcion_objetivo, k=3)
print(f"Mejor solución encontrada: x = {mejor_x:.2f}, f(x) = {mejor_valor:.2f}")