def dfs(grafo, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        return None  # Retorna None si los nodos no existen en el grafo

    # Pila para explorar nodos (último en entrar, primero en salir - LIFO)
    pila = [(inicio, [inicio])]  # Cada elemento contiene (nodo_actual, camino_recorrido)
    # Conjunto para registrar los nodos ya visitados (evita ciclos)
    visitados = set()

    while pila:
        nodo_actual, camino = pila.pop()  # Extrae el nodo más recientemente añadido

        if nodo_actual == objetivo:
            return camino  # Si se llega al objetivo, retorna el camino

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)  # Marca el nodo como visitado
            # Itera sobre los vecinos en orden inverso para mantener exploración predecible
            for vecino in reversed(grafo[nodo_actual]):
                if vecino not in visitados:
                    # Agrega el vecino a la pila con el camino actualizado
                    pila.append((vecino, camino + [vecino]))

    return None  # Retorna None si no se encuentra un camino al objetivo

# Grafo no dirigido con múltiples caminos para mostrar el comportamiento de DFS
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

inicio = 'A'  # Nodo inicial desde donde empieza la búsqueda
objetivo = 'F'  # Nodo que se desea alcanzar
camino = dfs(grafo, inicio, objetivo)  # Ejecuta DFS desde el nodo inicial al objetivo

if camino:  # Verifica si se encontró un camino
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")  # Imprime el camino encontrado
else:
    print(f"No hay camino de {inicio} a {objetivo}")  # Imprime mensaje si no hay camino
