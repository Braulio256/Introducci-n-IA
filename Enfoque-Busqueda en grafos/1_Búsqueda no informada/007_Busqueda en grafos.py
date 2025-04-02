from collections import deque
import heapq


# Definición de los 4 algoritmos solicitados
def bfs(grafo, inicio, objetivo):
    cola = deque([(inicio, [inicio])])
    visitados = set()
    while cola:
        nodo, camino = cola.popleft()
        if nodo == objetivo:
            return camino
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
    return None


def dfs(grafo, inicio, objetivo):
    pila = [(inicio, [inicio])]
    visitados = set()
    while pila:
        nodo, camino = pila.pop()
        if nodo == objetivo:
            return camino
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in reversed(grafo[nodo]):  # reversed para orden natural
                pila.append((vecino, camino + [vecino]))
    return None


def ucs(grafo, inicio, objetivo):
    cola = [(0, inicio, [inicio])]
    visitados = set()
    while cola:
        costo, nodo, camino = heapq.heappop(cola)
        if nodo == objetivo:
            return camino, costo
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino, c in grafo[nodo]:
                heapq.heappush(cola, (costo + c, vecino, camino + [vecino]))
    return None, float('inf')


def busqueda_bidireccional(grafo, inicio, objetivo):
    if inicio == objetivo:
        return [inicio]

    # Colas y diccionarios para ambas direcciones
    cola_inicio = deque([inicio])
    cola_objetivo = deque([objetivo])
    padres_inicio = {inicio: None}
    padres_objetivo = {objetivo: None}
    interseccion = None

    while cola_inicio and cola_objetivo and not interseccion:
        # Búsqueda desde inicio
        nodo_actual = cola_inicio.popleft()
        for vecino in grafo[nodo_actual]:
            if vecino not in padres_inicio:
                padres_inicio[vecino] = nodo_actual
                cola_inicio.append(vecino)
                if vecino in padres_objetivo:
                    interseccion = vecino
                    break

        # Búsqueda desde objetivo (si no hay intersección)
        if not interseccion:
            nodo_actual = cola_objetivo.popleft()
            for vecino in grafo[nodo_actual]:
                if vecino not in padres_objetivo:
                    padres_objetivo[vecino] = nodo_actual
                    cola_objetivo.append(vecino)
                    if vecino in padres_inicio:
                        interseccion = vecino
                        break

    # Reconstruir camino si hay intersección
    if interseccion:
        camino_inicio = []
        nodo = interseccion
        while nodo is not None:
            camino_inicio.append(nodo)
            nodo = padres_inicio[nodo]
        camino_inicio.reverse()

        camino_objetivo = []
        nodo = padres_objetivo[interseccion]
        while nodo is not None:
            camino_objetivo.append(nodo)
            nodo = padres_objetivo[nodo]

        return camino_inicio + camino_objetivo
    return None


# Grafos no dirigidos extensos (con múltiples caminos)
grafo_1 = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E', 'F'],
    'C': ['A', 'F', 'G'],
    'D': ['A', 'H'],
    'E': ['B', 'I'],
    'F': ['B', 'C', 'J'],
    'G': ['C', 'K'],
    'H': ['D', 'L'],
    'I': ['E', 'M'],
    'J': ['F', 'N'],
    'K': ['G', 'O'],
    'L': ['H', 'P'],
    'M': ['I', 'N'],
    'N': ['J', 'M', 'O'],
    'O': ['K', 'N', 'P'],
    'P': ['L', 'O']
}

grafo_2 = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B', 'H'],
    'E': ['B', 'I'],
    'F': ['C', 'J'],
    'G': ['C', 'K'],
    'H': ['D', 'L'],
    'I': ['E', 'M'],
    'J': ['F', 'N'],
    'K': ['G', 'O'],
    'L': ['H', 'P'],
    'M': ['I', 'N'],
    'N': ['J', 'M', 'O'],
    'O': ['K', 'N', 'P'],
    'P': ['L', 'O']
}


# Función para ejecutar pruebas
def ejecutar_pruebas(grafo, inicio, objetivo, nombre_grafo):
    print(f"\n--- Pruebas en {nombre_grafo} ({inicio} -> {objetivo}) ---")

    # BFS
    camino_bfs = bfs(grafo, inicio, objetivo)
    print(
        f"BFS: Camino más corto (pasos) = {camino_bfs}, Longitud = {len(camino_bfs) - 1 if camino_bfs else 'No encontrado'}")

    # DFS
    camino_dfs = dfs(grafo, inicio, objetivo)
    print(f"DFS: Camino encontrado = {camino_dfs}, Longitud = {len(camino_dfs) - 1 if camino_dfs else 'No encontrado'}")

    # Búsqueda bidireccional
    camino_bb = busqueda_bidireccional(grafo, inicio, objetivo)
    print(
        f"Búsqueda bidireccional: Camino = {camino_bb}, Longitud = {len(camino_bb) - 1 if camino_bb else 'No encontrado'}")

    # UCS (convertimos el grafo a ponderado con costos = 1)
    grafo_ponderado = {nodo: [(vecino, 1) for vecino in vecinos] for nodo, vecinos in grafo.items()}
    camino_ucs, costo_ucs = ucs(grafo_ponderado, inicio, objetivo)
    print(f"UCS: Camino = {camino_ucs}, Costo = {costo_ucs}")


# Ejecutar pruebas
ejecutar_pruebas(grafo_1, 'A', 'P', "Grafo 1 (Altamente conectado)")
ejecutar_pruebas(grafo_2, 'A', 'P', "Grafo 2 (Conectividad media)")