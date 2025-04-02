def dfs_limitado(grafo, nodo, objetivo, limite, camino, visitados):
    camino.append(nodo)
    visitados.add(nodo)

    if nodo == objetivo:
        return camino

    if len(camino) - 1 >= limite:  # -1 para contar desde 0
        camino.pop()
        return None

    for vecino in grafo[nodo]:
        if vecino not in visitados:
            resultado = dfs_limitado(grafo, vecino, objetivo, limite, camino, visitados)
            if resultado is not None:
                return resultado

    camino.pop()  # Backtracking
    return None


def ids(grafo, inicio, objetivo, max_profundidad=10):
    for limite in range(max_profundidad + 1):  # Incrementa el límite desde 0
        visitados = set()
        camino = []
        resultado = dfs_limitado(grafo, inicio, objetivo, limite, camino, visitados)
        if resultado is not None:
            return resultado
    return None


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
objetivo = 'F'
camino = ids(grafo, inicio, objetivo)

if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print(f"No hay camino de {inicio} a {objetivo} en la profundidad máxima explorada.")