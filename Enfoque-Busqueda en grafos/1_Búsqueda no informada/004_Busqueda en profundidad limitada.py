def dls(grafo, nodo, objetivo, limite_profundidad, camino=None, visitados=None):
    # Inicializa la lista del camino si es la primera llamada
    if camino is None:
        camino = []
    # Inicializa el conjunto de nodos visitados si es la primera llamada
    if visitados is None:
        visitados = set()

    camino.append(nodo)           # Agrega el nodo actual al camino
    visitados.add(nodo)           # Marca el nodo como visitado

    if nodo == objetivo:
        return camino             # Si se encuentra el objetivo, retorna el camino actual

    # Verifica si se alcanzó el límite de profundidad
    if len(camino) - 1 >= limite_profundidad:  # -1 porque el nodo inicial cuenta como nivel 0
        camino.pop()            # Elimina el nodo actual para retroceder (backtracking)
        return None

    # Recorre los vecinos no visitados
    for vecino in grafo[nodo]:
        if vecino not in visitados:
            # Llama recursivamente a DLS para el vecino
            resultado = dls(grafo, vecino, objetivo, limite_profundidad, camino, visitados)
            if resultado is not None:
                return resultado  # Si se encuentra un camino válido, lo retorna

    camino.pop()                # Retrocede si no se encontró el objetivo en esta rama
    return None                 # Retorna None si no hay solución dentro del límite

# Ejemplo de grafo no dirigido (diccionario de listas)
grafo = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': ['F'],
    'E': ['F'],
    'F': []
}

# Parámetros de búsqueda
inicio = 'A'                  # Nodo inicial de búsqueda
objetivo = 'F'                # Nodo objetivo a encontrar
limite_profundidad = 3       # Límite máximo de profundidad permitido

# Validación inicial
if inicio not in grafo or objetivo not in grafo:
    print("Error: Nodo inicial o final no está en el grafo.")
else:
    # Ejecutar búsqueda en profundidad limitada
    camino = dls(grafo, inicio, objetivo, limite_profundidad)

    if camino:  # Si se encontró un camino dentro del límite
        print(f"Camino encontrado de {inicio} a {objetivo} (límite {limite_profundidad}): {' -> '.join(camino)}")
    else:
        print(f"No se encontró un camino de {inicio} a {objetivo} dentro del límite de profundidad {limite_profundidad}.")
