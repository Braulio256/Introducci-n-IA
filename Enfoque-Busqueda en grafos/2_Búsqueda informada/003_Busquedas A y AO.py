import heapq  # Importamos la librería heapq para usar una cola de prioridad.

# Heurística común para ambos algoritmos (ahora incluye 'G')
def heuristica(nodo_actual, nodo_objetivo):
    # Coordenadas de cada nodo para calcular la heurística (distancia Manhattan).
    coordenadas = {
        'A': (0, 0), 'B': (1, 0), 'C': (0, 1),
        'D': (2, 0), 'E': (1, 1), 'F': (0, 2),
        'G': (2, 1)  # Coordenadas del nodo G.
    }
    x1, y1 = coordenadas[nodo_actual]
    x2, y2 = coordenadas[nodo_objetivo]
    # Calculamos la distancia Manhattan entre los nodos actual y objetivo.
    return abs(x1 - x2) + abs(y1 - y2)


# Función para mejorar la eficiencia de A* evitando duplicados
def expandir_nodos(cola, grafo, nodo, costo_real, camino, objetivo, heuristica, visitados):
    for vecino, costo in grafo[nodo].items():
        if vecino not in visitados:  # Solo expandimos nodos no visitados
            nuevo_costo = costo_real + costo
            heapq.heappush(cola, (
                nuevo_costo + heuristica(vecino, objetivo),  # f = g + h
                nuevo_costo,
                vecino,
                camino + [vecino]  # Extendemos el camino.
            ))


# Algoritmo A* optimizado
def a_star(grafo, inicio, objetivo, heuristica):
    cola = [(0 + heuristica(inicio, objetivo), 0, inicio, [inicio])]  # Iniciamos la cola de prioridad.
    visitados = set()  # Conjunto de nodos visitados.

    while cola:
        _, costo_real, nodo, camino = heapq.heappop(cola)  # Extraemos el nodo con el menor valor de f.

        if nodo == objetivo:
            return camino, costo_real  # Si encontramos el objetivo, devolvemos el camino y costo total.

        if nodo not in visitados:
            visitados.add(nodo)  # Marcamos el nodo como visitado.
            expandir_nodos(cola, grafo, nodo, costo_real, camino, objetivo, heuristica, visitados)  # Expandimos los nodos vecinos.

    return None, float('inf')  # Si no se encuentra un camino, devolvemos None.


# Función para expandir nodos en el algoritmo AO*
def expandir_nodos_ao(cola, grafo_and_or, nodo, costo_real, camino, objetivo, heuristica, visitados):
    if nodo in grafo_and_or['OR']:
        # Si el nodo es OR, expandimos un solo vecino a la vez.
        for vecino, costo in grafo_and_or['OR'][nodo].items():
            nuevo_g = costo_real + costo
            heapq.heappush(cola, (
                nuevo_g + heuristica(vecino, objetivo),  # f = g + h
                vecino,
                camino + [vecino],
                nuevo_g
            ))

    elif nodo in grafo_and_or['AND']:
        # Si el nodo es AND, expandimos todos sus hijos.
        hijos = grafo_and_or['AND'][nodo]
        nuevo_camino = camino.copy()
        nuevo_g = costo_real

        for hijo, costo in hijos.items():
            nuevo_g += costo
            nuevo_camino.append(hijo)

        # Estimamos el valor de f para el conjunto AND utilizando el último hijo.
        f_and = nuevo_g + heuristica(hijo, objetivo)
        heapq.heappush(cola, (
            f_and,
            hijo,  # Seguimos desde el último hijo.
            nuevo_camino,
            nuevo_g
        ))


# Algoritmo AO* optimizado
def ao_star(grafo_and_or, inicio, objetivo, heuristica):
    cola = [(heuristica(inicio, objetivo), inicio, [inicio], 0)]  # (f, nodo, camino, g)
    heapq.heapify(cola)  # Inicializamos la cola como un heap.
    visitados = set()  # Conjunto de nodos visitados.

    while cola:
        f_actual, nodo, camino, g_actual = heapq.heappop(cola)  # Extraemos el nodo con el menor valor de f.

        if nodo == objetivo:
            return camino, g_actual  # Si llegamos al objetivo, devolvemos el camino y costo total.

        if nodo not in visitados:
            visitados.add(nodo)  # Marcamos el nodo como visitado.
            expandir_nodos_ao(cola, grafo_and_or, nodo, g_actual, camino, objetivo, heuristica, visitados)

    return None, float('inf')  # Si no se encuentra un camino, devolvemos None.


# Grafo para A* (Grafo estándar)
grafo_estandar = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'D': 2, 'E': 5},
    'C': {'A': 4, 'F': 3},
    'D': {'B': 2},
    'E': {'B': 5, 'F': 1},
    'F': {'C': 3, 'E': 1}
}

# Grafo AND-OR para AO* (Contiene nodos AND y OR)
grafo_and_or = {
    'OR': {
        'A': {'B': 1, 'C': 4},
        'B': {'D': 2, 'E': 5},
        'C': {'F': 3},
        'E': {'F': 1}
    },
    'AND': {
        'D': {'G': 1},  # Para alcanzar D, necesitamos también G.
        'F': {'G': 2}  # Para alcanzar F, necesitamos también G.
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
