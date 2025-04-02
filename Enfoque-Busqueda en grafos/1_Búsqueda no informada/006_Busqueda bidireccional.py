from collections import deque

def busqueda_bidireccional(grafo, inicio, objetivo):
    if inicio == objetivo:
        return [inicio]

    # Colas para las dos búsquedas (desde inicio y objetivo)
    cola_inicio = deque([inicio])
    cola_objetivo = deque([objetivo])

    # Diccionarios para registrar padres y nodos visitados
    padres_inicio = {inicio: None}
    padres_objetivo = {objetivo: None}

    # Nodo de intersección (cuando las dos búsquedas se encuentran)
    interseccion = None

    while cola_inicio and cola_objetivo and not interseccion:
        # BFS desde el inicio
        nodo_actual_inicio = cola_inicio.popleft()
        for vecino in grafo[nodo_actual_inicio]:
            if vecino not in padres_inicio:
                padres_inicio[vecino] = nodo_actual_inicio
                cola_inicio.append(vecino)
                if vecino in padres_objetivo:  # Intersección encontrada
                    interseccion = vecino
                    break

        # BFS desde el objetivo (si no se ha encontrado intersección)
        if not interseccion:
            nodo_actual_objetivo = cola_objetivo.popleft()
            for vecino in grafo[nodo_actual_objetivo]:
                if vecino not in padres_objetivo:
                    padres_objetivo[vecino] = nodo_actual_objetivo
                    cola_objetivo.append(vecino)
                    if vecino in padres_inicio:  # Intersección encontrada
                        interseccion = vecino
                        break

    # Reconstruir el camino si hay intersección
    if interseccion:
        camino_inicio = []
        nodo = interseccion
        while nodo is not None:
            camino_inicio.append(nodo)
            nodo = padres_inicio[nodo]
        camino_inicio.reverse()  # Ordenar desde inicio hasta intersección

        camino_objetivo = []
        nodo = padres_objetivo[interseccion]  # Evita duplicar la intersección
        while nodo is not None:
            camino_objetivo.append(nodo)
            nodo = padres_objetivo[nodo]

        return camino_inicio + camino_objetivo

    return None  # No hay camino

# Grafo de ejemplo (no dirigido)
grafo = {
    'A': ['D', 'C'],
    'B': ['A', 'D', 'C'],
    'C': ['A', 'E'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Ejecución
inicio = 'A'
objetivo = 'E'
camino = busqueda_bidireccional(grafo, inicio, objetivo)

if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print(f"No hay camino de {inicio} a {objetivo}.")