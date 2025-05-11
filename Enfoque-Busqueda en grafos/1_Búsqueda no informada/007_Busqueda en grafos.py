from collections import deque  # Importa deque para estructuras de cola eficientes
import heapq  # Importa heapq para implementar colas de prioridad (necesarias para UCS)


# Búsqueda por anchura (Breadth-First Search)
def bfs(grafo, inicio, objetivo):
    cola = deque([(inicio, [inicio])])  # Cola con tuplas (nodo actual, camino recorrido)
    visitados = set()  # Conjunto para llevar registro de nodos ya visitados
    while cola:
        nodo, camino = cola.popleft()  # Extrae el primer nodo de la cola
        if nodo == objetivo:
            return camino  # Si es el objetivo, devuelve el camino
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)  # Marca el vecino como visitado
                cola.append((vecino, camino + [vecino]))  # Añade el vecino con el camino actualizado
    return None  # Si no se encuentra el objetivo


# Búsqueda por profundidad (Depth-First Search)
def dfs(grafo, inicio, objetivo):
    pila = [(inicio, [inicio])]  # Pila con tuplas (nodo actual, camino recorrido)
    visitados = set()  # Conjunto de nodos visitados
    while pila:
        nodo, camino = pila.pop()  # Extrae el último nodo de la pila
        if nodo == objetivo:
            return camino  # Devuelve el camino si se encuentra el objetivo
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in reversed(grafo[nodo]):  # Recorre vecinos en orden inverso para mantener el orden
                pila.append((vecino, camino + [vecino]))  # Añade vecino con el camino actualizado
    return None


# Búsqueda de costo uniforme (Uniform Cost Search)
def ucs(grafo, inicio, objetivo):
    cola = [(0, inicio, [inicio])]  # Cola de prioridad con tuplas (costo acumulado, nodo, camino)
    visitados = set()
    while cola:
        costo, nodo, camino = heapq.heappop(cola)  # Extrae el nodo con menor costo
        if nodo == objetivo:
            return camino, costo  # Devuelve camino y costo si se encuentra el objetivo
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino, c in grafo[nodo]:  # Para cada vecino y su costo
                heapq.heappush(cola, (costo + c, vecino, camino + [vecino]))  # Inserta en la cola con costo actualizado
    return None, float('inf')  # Si no se encuentra el camino, retorna costo infinito

# Búsqueda bidireccional: busca simultáneamente desde el inicio y el objetivo
def busqueda_bidireccional(grafo, inicio, objetivo):
    if inicio == objetivo:
        return [inicio]  # Si inicio y objetivo son iguales, el camino es trivial

    # Inicializa colas para ambas búsquedas
    cola_inicio = deque([inicio])  # Cola desde el inicio
    cola_objetivo = deque([objetivo])  # Cola desde el objetivo

    # Diccionarios para reconstruir el camino desde ambas direcciones
    padres_inicio = {inicio: None}  # Rastro de nodos desde el inicio
    padres_objetivo = {objetivo: None}  # Rastro de nodos desde el objetivo

    interseccion = None  # Nodo donde ambas búsquedas se encuentran

    # Ejecuta mientras ambas colas tengan nodos y no se haya encontrado la intersección
    while cola_inicio and cola_objetivo and not interseccion:
        # Expande nodo desde el inicio
        nodo_actual = cola_inicio.popleft()
        for vecino in grafo[nodo_actual]:
            if vecino not in padres_inicio:
                padres_inicio[vecino] = nodo_actual  # Guarda el padre
                cola_inicio.append(vecino)
                if vecino in padres_objetivo:  # Si el vecino ya fue visto desde el objetivo
                    interseccion = vecino  # Se encontró un nodo común
                    break

        # Si aún no hay intersección, expande desde el objetivo
        if not interseccion:
            nodo_actual = cola_objetivo.popleft()
            for vecino in grafo[nodo_actual]:
                if vecino not in padres_objetivo:
                    padres_objetivo[vecino] = nodo_actual
                    cola_objetivo.append(vecino)
                    if vecino in padres_inicio:  # Nodo encontrado desde el otro lado
                        interseccion = vecino
                        break

    # Si se encontró intersección, se reconstruye el camino completo
    if interseccion:
        camino_inicio = []  # Reconstrucción desde inicio hasta intersección
        nodo = interseccion
        while nodo is not None:
            camino_inicio.append(nodo)
            nodo = padres_inicio[nodo]
        camino_inicio.reverse()  # Invierte para obtener orden correcto

        camino_objetivo = []  # Reconstrucción desde intersección hasta objetivo
        nodo = padres_objetivo[interseccion]
        while nodo is not None:
            camino_objetivo.append(nodo)
            nodo = padres_objetivo[nodo]

        return camino_inicio + camino_objetivo  # Une ambos caminos
    return None  # Si no se encontró conexión entre inicio y objetivo

# Grafo 1: No dirigido, altamente conectado
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

# Grafo 2: No dirigido, menos conexiones, más lineal
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

# Función que ejecuta todos los algoritmos de búsqueda sobre un grafo dado
def ejecutar_pruebas(grafo, inicio, objetivo, nombre_grafo):
    print(f"\n--- Pruebas en {nombre_grafo} ({inicio} -> {objetivo}) ---")

    # Ejecuta búsqueda BFS
    camino_bfs = bfs(grafo, inicio, objetivo)
    print(
        f"BFS: Camino más corto (pasos) = {camino_bfs}, Longitud = {len(camino_bfs) - 1 if camino_bfs else 'No encontrado'}")

    # Ejecuta búsqueda DFS
    camino_dfs = dfs(grafo, inicio, objetivo)
    print(
        f"DFS: Camino encontrado = {camino_dfs}, Longitud = {len(camino_dfs) - 1 if camino_dfs else 'No encontrado'}")

    # Ejecuta búsqueda bidireccional
    camino_bb = busqueda_bidireccional(grafo, inicio, objetivo)
    print(
        f"Búsqueda bidireccional: Camino = {camino_bb}, Longitud = {len(camino_bb) - 1 if camino_bb else 'No encontrado'}")

    # Convierte el grafo a ponderado para UCS (todos los costos valen 1)
    grafo_ponderado = {nodo: [(vecino, 1) for vecino in vecinos] for nodo, vecinos in grafo.items()}

    # Ejecuta búsqueda UCS
    camino_ucs, costo_ucs = ucs(grafo_ponderado, inicio, objetivo)
    print(f"UCS: Camino = {camino_ucs}, Costo = {costo_ucs}")

# Ejecuta pruebas en el grafo 1
ejecutar_pruebas(grafo_1, 'A', 'P', "Grafo 1 (Altamente conectado)")

# Ejecuta pruebas en el grafo 2
ejecutar_pruebas(grafo_2, 'A', 'P', "Grafo 2 (Conectividad media)")
