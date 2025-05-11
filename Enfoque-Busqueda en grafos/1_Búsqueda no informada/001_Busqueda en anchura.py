from collections import deque  # Importa deque para usar una cola eficiente (FIFO)

def bfs(grafo, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        return None  # Retorna None si el nodo de inicio o el objetivo no existen en el grafo

    cola = deque([inicio])  # Inicializa la cola con el nodo de inicio
    visitados = {inicio: None}  # Diccionario para registrar nodos visitados y su predecesor

    while cola:
        nodo_actual = cola.popleft()  # Extrae el primer nodo de la cola (FIFO)

        if nodo_actual == objetivo:  # Si se alcanza el objetivo, se reconstruye el camino
            return reconstruir_camino(visitados, objetivo)  # Llama a función para construir el camino

        for vecino in grafo[nodo_actual]:  # Itera sobre los vecinos del nodo actual
            if vecino not in visitados:  # Si el vecino no ha sido visitado
                cola.append(vecino)  # Lo agrega a la cola para explorar
                visitados[vecino] = nodo_actual  # Guarda el nodo actual como su predecesor

    return None  # Retorna None si no se encuentra un camino al objetivo

def reconstruir_camino(visitados, objetivo):
    camino = []  # Lista para almacenar el camino desde el objetivo al inicio
    while objetivo is not None:  # Retrocede desde el objetivo hasta el inicio
        camino.append(objetivo)  # Agrega el nodo actual al camino
        objetivo = visitados[objetivo]  # Se mueve al predecesor
    return camino[::-1]  # Retorna el camino invertido (desde inicio hasta objetivo)

# Ejemplo de grafo no dirigido con más claridad estructural
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

inicio = 'A'  # Nodo de inicio para la búsqueda
objetivo = 'F'  # Nodo objetivo que se desea alcanzar
camino = bfs(grafo, inicio, objetivo)  # Llama a la función de búsqueda en anchura

if camino:  # Si se encontró un camino válido
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")  # Imprime el camino
else:
    print(f"No hay camino de {inicio} a {objetivo}")  # Mensaje si no se encontró camino
