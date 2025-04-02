def dfs(grafo, inicio, objetivo):
    # Pila para almacenar los nodos a explorar (último en entrar, primero en salir)
    pila = [(inicio, [inicio])]  # (nodo_actual, camino)
    # Conjunto para registrar nodos visitados (evita ciclos)
    visitados = set()

    while pila:
        nodo_actual, camino = pila.pop()  # Extrae el último nodo añadido (LIFO)

        if nodo_actual == objetivo:
            return camino  # Camino encontrado

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            # Añade vecinos no visitados a la pila (en orden inverso para explorar en orden)
            for vecino in reversed(grafo[nodo_actual]):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino]))

    return None  # No se encontró camino


# Ejemplo de grafo no dirigido (mismo que en BFS para comparar)
grafo = {
    'A': ['D', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Ejecutamos DFS desde 'A' hasta 'F'
inicio = 'A'
objetivo = 'F'
camino = dfs(grafo, inicio, objetivo)

if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print(f"No hay camino de {inicio} a {objetivo}")