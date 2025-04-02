def dls(grafo, nodo, objetivo, limite_profundidad, camino=None, visitados=None):
    if camino is None:
        camino = []
    if visitados is None:
        visitados = set()

    camino.append(nodo)
    visitados.add(nodo)

    if nodo == objetivo:
        return camino

    if len(camino) - 1 >= limite_profundidad:  # -1 porque camino incluye al nodo inicial
        camino.pop()  # Retroceder (backtracking)
        return None

    for vecino in grafo[nodo]:
        if vecino not in visitados:
            resultado = dls(grafo, vecino, objetivo, limite_profundidad, camino, visitados)
            if resultado is not None:
                return resultado

    camino.pop()  # Retroceder si no se encontró el objetivo en esta rama
    return None

# Ejemplo de grafo no dirigido
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
limite_profundidad = 4  # Profundidad máxima permitida

# Ejecutar DLS
camino = dls(grafo, inicio, objetivo, limite_profundidad)

if camino:
    print(f"Camino encontrado de {inicio} a {objetivo} (límite {limite_profundidad}): {' -> '.join(camino)}")
else:
    print(f"No se encontró un camino de {inicio} a {objetivo} dentro del límite de profundidad {limite_profundidad}.")