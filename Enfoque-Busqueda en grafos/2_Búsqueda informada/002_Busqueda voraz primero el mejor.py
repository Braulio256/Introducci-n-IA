import heapq

# Grafo de ejemplo (ciudades y conexiones)
grafo = {
    'A': {'B': 5, 'C': 10},
    'B': {'D': 3, 'E': 8},
    'C': {'F': 2},
    'D': {'A': 6},
    'E': {'G': 4},
    'F': {'G': 5},
    'G': {'B': 3, 'F': 4}
}

# Heurística (distancia estimada al objetivo 'G')
heuristicas = {
    'A': 15,
    'B': 10,
    'C': 8,
    'D': 7,
    'E': 5,
    'F': 3,
    'G': 0  # El objetivo tiene heurística 0
}


def busqueda_voraz(grafo, inicio, objetivo, heuristicas):
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (heuristicas[inicio], inicio, [inicio]))  # (heurística, nodo, camino)
    visitados = set()

    while cola_prioridad:
        _, nodo_actual, camino = heapq.heappop(cola_prioridad)

        if nodo_actual == objetivo:
            return camino  # ¡Objetivo encontrado!

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            for vecino, _ in grafo[nodo_actual].items():  # Ignoramos el costo real (solo usamos heurística)
                heapq.heappush(cola_prioridad, (heuristicas[vecino], vecino, camino + [vecino]))

    return None  # No se encontró el objetivo


# Ejecución
inicio = 'B'
objetivo = 'F'
camino = busqueda_voraz(grafo, inicio, objetivo, heuristicas)

if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print(f"No se encontró un camino de {inicio} a {objetivo}.")