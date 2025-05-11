# Función auxiliar: Búsqueda en profundidad limitada con backtracking
def dfs_limitado(grafo, nodo, objetivo, limite, camino, visitados):
    camino.append(nodo)            # Agrega el nodo al camino actual

    if nodo == objetivo:
        return camino              # Si se alcanza el objetivo, retorna el camino

    if len(camino) - 1 >= limite:  # Verifica si se alcanzó el límite de profundidad
        camino.pop()
        return None

    # Explora vecinos del nodo actual
    for vecino in grafo[nodo]:
        if vecino not in visitados:
            visitados.add(vecino)  # Marca como visitado en esta rama
            resultado = dfs_limitado(grafo, vecino, objetivo, limite, camino, visitados)
            if resultado is not None:
                return resultado
            visitados.remove(vecino)  # Limpia visitados locales tras backtracking

    camino.pop()                   # Retrocede si no se encuentra el objetivo
    return None

# Función principal: Búsqueda en profundidad iterativa
def ids(grafo, inicio, objetivo, max_profundidad=10):
    for limite in range(max_profundidad + 1):
        camino = []
        visitados = set([inicio])  # Solo se marca el nodo inicial al principio
        resultado = dfs_limitado(grafo, inicio, objetivo, limite, camino, visitados)
        if resultado is not None:
            print(f"Profundidad en la que se encontró la solución: {limite}")
            return resultado
    return None

# Grafo no dirigido representado como diccionario de listas
grafo = {
    'A': ['D', 'C'],
    'B': ['A', 'D', 'C'],
    'C': ['A', 'E'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Parámetros de búsqueda
inicio = 'A'
objetivo = 'F'

# Ejecutar IDDFS
camino = ids(grafo, inicio, objetivo)

# Mostrar resultado
if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print(f"No hay camino de {inicio} a {objetivo} en la profundidad máxima explorada.")
