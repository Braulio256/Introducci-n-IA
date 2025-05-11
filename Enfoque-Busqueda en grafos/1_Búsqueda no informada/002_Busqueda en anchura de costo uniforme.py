import heapq  # Importa heapq para utilizar una cola de prioridad basada en montículo (min-heap)

def ucs(grafo, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        return None, float('inf')  # Valida que los nodos existan en el grafo

    # Inicializa la cola de prioridad con una tupla (costo acumulado, nodo actual, camino recorrido)
    cola = [(0, inicio, [inicio])]
    # Diccionario que almacena el menor costo conocido para cada nodo
    visitados = {inicio: 0}

    while cola:
        # Extrae el nodo con menor costo acumulado de la cola de prioridad
        costo_acumulado, nodo_actual, camino = heapq.heappop(cola)

        if nodo_actual == objetivo:  # Si se llega al nodo objetivo
            return camino, costo_acumulado  # Retorna el camino y su costo total

        # Itera sobre los vecinos del nodo actual y sus costos asociados
        for vecino, costo in grafo[nodo_actual].items():
            nuevo_costo = costo_acumulado + costo  # Calcula el nuevo costo acumulado

            # Si el vecino no ha sido visitado o se encuentra un camino más barato
            if vecino not in visitados or nuevo_costo < visitados[vecino]:
                visitados[vecino] = nuevo_costo  # Actualiza el menor costo al vecino
                # Agrega el nuevo camino con su costo a la cola de prioridad
                heapq.heappush(cola, (nuevo_costo, vecino, camino + [vecino]))

    return None, float('inf')  # Retorna None si no se encuentra un camino al objetivo

# Grafo ponderado que permite mostrar decisiones de caminos con diferentes costos
grafo = {
    'A': {'B': 2, 'C': 5},
    'B': {'A': 2, 'D': 1, 'E': 4},
    'C': {'A': 5, 'F': 2},
    'D': {'B': 1, 'E': 1},
    'E': {'B': 4, 'D': 1, 'F': 3},
    'F': {'C': 2, 'E': 3}
}

inicio = 'A'  # Nodo desde donde comienza la búsqueda
objetivo = 'F'  # Nodo que se desea alcanzar
camino, costo = ucs(grafo, inicio, objetivo)  # Ejecuta búsqueda de costo uniforme

if camino:  # Verifica si se encontró un camino
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")  # Imprime el camino
    print(f"Costo total: {costo}")  # Imprime el costo total del camino
else:
    print(f"No hay camino de {inicio} a {objetivo}")  # Mensaje si no se encontró camino
