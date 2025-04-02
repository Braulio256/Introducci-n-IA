import heapq


def ucs(grafo, inicio, objetivo):
    # Cola de prioridad: (costo_acumulado, nodo_actual, camino)
    cola = [(0, inicio, [inicio])]
    # Diccionario para registrar los nodos visitados y su costo mínimo
    visitados = {inicio: 0}

    while cola:
        costo_acumulado, nodo_actual, camino = heapq.heappop(cola)

        # Si encontramos el objetivo, retornamos el camino y el costo
        if nodo_actual == objetivo:
            return camino, costo_acumulado

        # Exploramos los nodos vecinos
        for vecino, costo in grafo[nodo_actual].items():
            nuevo_costo = costo_acumulado + costo
            # Si el vecino no ha sido visitado o encontramos un camino más barato
            if vecino not in visitados or nuevo_costo < visitados[vecino]:
                visitados[vecino] = nuevo_costo
                heapq.heappush(cola, (nuevo_costo, vecino, camino + [vecino]))

    return None, float('inf')  # No se encontró camino


# Ejemplo de grafo ponderado (representado como diccionario de diccionarios)
grafo = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'D': 2, 'E': 5},
    'C': {'A': 4, 'F': 3},
    'D': {'B': 2, 'E': 5},
    'E': {'B': 5, 'F': 1},
    'F': {'C': 3, 'E': 1}
}

# Ejecutamos UCS desde 'A' hasta 'F'
inicio = 'C'
objetivo = 'D'
camino, costo = ucs(grafo, inicio, objetivo)

if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
    print(f"Costo total: {costo}")
else:
    print(f"No hay camino de {inicio} a {objetivo}")