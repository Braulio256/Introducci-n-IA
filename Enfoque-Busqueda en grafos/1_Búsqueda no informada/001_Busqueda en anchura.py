from collections import deque


def bfs(grafo, inicio, objetivo):
    # Cola para almacenar los nodos a explorar
    cola = deque([inicio])
    # Diccionario para registrar los nodos visitados y su padre (evitar ciclos)
    visitados = {inicio: None}

    while cola:
        nodo_actual = cola.popleft()  # Extrae el primer nodo de la cola (FIFO)

        # Si encontramos el objetivo, reconstruimos el camino
        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = visitados[nodo_actual]
            return camino[::-1]  # Invertimos el camino (del inicio al objetivo)

        # Exploramos los nodos vecinos no visitados
        for vecino in grafo[nodo_actual]:
            if vecino not in visitados:
                cola.append(vecino)
                visitados[vecino] = nodo_actual  # Registramos el padre del vecino

    return None  # Si no se encuentra el objetivo


# Ejemplo de grafo no dirigido (representado como diccionario de listas de adyacencia)
grafo = {
    'A': ['E', 'C'],
    'B': ['A', 'F', 'E'],
    'C': ['E', 'F'],
    'D': ['B', 'C'],
    'E': ['A', 'F'],
    'F': ['C', 'E']
}

# Ejecutamos BFS desde 'A' hasta 'F'
inicio = 'A'
objetivo = 'F'
camino = bfs(grafo, inicio, objetivo)

if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print(f"No hay camino de {inicio} a {objetivo}")