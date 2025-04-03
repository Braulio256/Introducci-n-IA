import heapq
from collections import defaultdict


# Heurística común para ambos algoritmos (ahora incluye 'G')
def heuristica(nodo_actual, nodo_objetivo):
    coordenadas = {
        'A': (0, 0), 'B': (1, 0), 'C': (0, 1),
        'D': (2, 0), 'E': (1, 1), 'F': (0, 2),
        'G': (2, 1)  # Agregamos coordenadas para el nodo G
    }
    x1, y1 = coordenadas[nodo_actual]
    x2, y2 = coordenadas[nodo_objetivo]
    return abs(x1 - x2) + abs(y1 - y2)


# Algoritmo A*
def a_star(grafo, inicio, objetivo, heuristica):
    cola = [(0 + heuristica(inicio, objetivo), 0, inicio, [inicio])]
    visitados = set()

    while cola:
        _, costo_real, nodo, camino = heapq.heappop(cola)

        if nodo == objetivo:
            return camino, costo_real

        if nodo not in visitados:
            visitados.add(nodo)
            for vecino, costo in grafo[nodo].items():
                nuevo_costo = costo_real + costo
                heapq.heappush(cola, (
                    nuevo_costo + heuristica(vecino, objetivo),
                    nuevo_costo,
                    vecino,
                    camino + [vecino]
                ))
    return None, float('inf')


# Algoritmo AO*
def ao_star(grafo_and_or, inicio, objetivo, heuristica):
    cola = [(heuristica(inicio, objetivo), inicio, [inicio], 0)]  # (f, nodo, camino, g)
    heapq.heapify(cola)
    visitados = set()

    while cola:
        f_actual, nodo, camino, g_actual = heapq.heappop(cola)

        if nodo == objetivo:
            return camino, g_actual

        if nodo not in visitados:
            visitados.add(nodo)

            if nodo in grafo_and_or['OR']:
                for vecino, costo in grafo_and_or['OR'][nodo].items():
                    nuevo_g = g_actual + costo
                    heapq.heappush(cola, (
                        nuevo_g + heuristica(vecino, objetivo),
                        vecino,
                        camino + [vecino],
                        nuevo_g
                    ))

            elif nodo in grafo_and_or['AND']:
                # Para nodos AND, debemos expandir todos los hijos
                hijos = grafo_and_or['AND'][nodo]
                nuevo_camino = camino.copy()
                nuevo_g = g_actual

                # Calculamos el costo total de los hijos AND
                for hijo, costo in hijos.items():
                    nuevo_g += costo
                    nuevo_camino.append(hijo)

                # Estimamos f para el conjunto AND
                f_and = nuevo_g + heuristica(hijo, objetivo)  # Usamos el último hijo como referencia
                heapq.heappush(cola, (
                    f_and,
                    hijo,  # Seguimos desde el último hijo
                    nuevo_camino,
                    nuevo_g
                ))

    return None, float('inf')


# Grafo para A*
grafo_estandar = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'D': 2, 'E': 5},
    'C': {'A': 4, 'F': 3},
    'D': {'B': 2},
    'E': {'B': 5, 'F': 1},
    'F': {'C': 3, 'E': 1}
}

# Grafo AND-OR para AO*
grafo_and_or = {
    'OR': {
        'A': {'B': 1, 'C': 4},
        'B': {'D': 2, 'E': 5},
        'C': {'F': 3},
        'E': {'F': 1}
    },
    'AND': {
        'D': {'G': 1},  # Para alcanzar D, necesitamos también G
        'F': {'G': 2}  # Para alcanzar F, necesitamos también G
    }
}

# Ejecutando A*
print("=== Algoritmo A* ===")
camino_a_estrella, costo_a_estrella = a_star(grafo_estandar, 'A', 'F', heuristica)
print(f"Camino encontrado: {camino_a_estrella}")
print(f"Costo total: {costo_a_estrella}\n")

# Ejecutando AO*
print("=== Algoritmo AO* ===")
camino_ao_star, costo_ao_star = ao_star(grafo_and_or, 'A', 'G', heuristica)
print(f"Camino encontrado: {camino_ao_star}")
print(f"Costo total: {costo_ao_star}")