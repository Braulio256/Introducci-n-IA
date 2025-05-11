import heapq  # Importa la biblioteca heapq para usar una cola de prioridad (min-heap)
import networkx as nx  # Importa NetworkX para crear y manipular grafos
import matplotlib.pyplot as plt  # Importa matplotlib para graficar el camino

# Grafo de ejemplo (ciudades y conexiones)
grafo = {
    'A': {'B': 5, 'C': 10},  # Nodo A tiene conexiones a B (costo 5) y C (costo 10)
    'B': {'D': 3, 'E': 8},  # Nodo B tiene conexiones a D (costo 3) y E (costo 8)
    'C': {'F': 2},  # Nodo C tiene conexión a F (costo 2)
    'D': {'A': 6},  # Nodo D tiene conexión a A (costo 6)
    'E': {'G': 4},  # Nodo E tiene conexión a G (costo 4)
    'F': {'G': 5},  # Nodo F tiene conexión a G (costo 5)
    'G': {'B': 3, 'F': 4}  # Nodo G tiene conexiones a B (costo 3) y F (costo 4)
}

# Heurística (distancia estimada al objetivo 'G')
heuristicas = {
    'A': 6,   # Heurística para A
    'B': 4,   # Heurística para B
    'C': 5,   # Heurística para C
    'D': 3,   # Heurística para D
    'E': 2,   # Heurística para E
    'F': 1,   # Heurística para F
    'G': 7    # Heurística para G
}


# Función para verificar la validez de la heurística (debe ser admisible)
def es_heuristica_valida(heuristicas, grafo, objetivo):
    """
    Verifica si las heurísticas proporcionadas son válidas.
    La heurística debe ser admisible, es decir, no debe sobrestimar el costo al objetivo.
    """
    for nodo in grafo:
        if heuristicas[nodo] > heuristicas[
            objetivo]:  # Si la heurística de un nodo es mayor que la del objetivo, no es válida
            print(
                f"Advertencia: Heurística no válida para el nodo {nodo}")  # Advertir si se encuentra una heurística no válida
            return False  # Si la heurística no es válida, retorna False
    return True  # Si todas las heurísticas son válidas, retorna True


# Función de visualización del camino
def visualizar_camino(grafo, camino):
    """
    Visualiza el camino encontrado en el grafo usando NetworkX y matplotlib.
    El camino es resaltado en rojo.
    """
    G = nx.Graph()  # Crea un grafo vacío utilizando NetworkX
    for nodo, vecinos in grafo.items():  # Recorre el grafo para agregar las conexiones
        for vecino, _ in vecinos.items():  # Para cada vecino de un nodo
            G.add_edge(nodo, vecino)  # Agrega una arista entre el nodo y su vecino

    pos = nx.spring_layout(G)  # Calcula la disposición de los nodos para la visualización
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue")  # Dibuja el grafo con etiquetas
    edges = list(zip(camino[:-1], camino[1:]))  # Crea una lista de aristas del camino
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=2)  # Dibuja las aristas del camino en rojo
    plt.show()  # Muestra la visualización del grafo


# Función de búsqueda voraz primero el mejor
def busqueda_voraz(grafo, inicio, objetivo, heuristicas):
    """
    Implementa el algoritmo de búsqueda voraz primero el mejor.
    La prioridad es dada por la heurística de cada nodo.
    """
    # Verifica si la heurística es válida antes de proceder
    if not es_heuristica_valida(heuristicas, grafo, objetivo):
        print("La heurística no es válida, se recomienda ajustarla.")
        return None  # Si la heurística no es válida, termina la búsqueda

    # Cola de prioridad para almacenar los nodos a explorar, inicializada con el nodo de inicio
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (heuristicas[inicio], inicio, [inicio]))  # (heurística, nodo, camino)

    visitados = set()  # Conjunto para mantener los nodos visitados
    mejor_heuristica = {}  # Diccionario para almacenar la mejor heurística alcanzada para cada nodo

    while cola_prioridad:  # Mientras haya nodos en la cola de prioridad
        # Extrae el nodo con la menor heurística
        _, nodo_actual, camino = heapq.heappop(cola_prioridad)

        # Si el nodo actual es el objetivo, se ha encontrado el camino
        if nodo_actual == objetivo:
            visualizar_camino(grafo, camino)  # Visualiza el camino encontrado
            return camino  # Retorna el camino encontrado

        # Añadir el nodo a la lista de visitados solo después de explorar sus vecinos
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)  # Marca el nodo como visitado
            for vecino, _ in grafo[nodo_actual].items():  # Recorre los vecinos del nodo actual
                if vecino not in visitados:  # Si el vecino no ha sido visitado
                    # Solo seguimos el camino si no hemos encontrado una mejor heurística para ese vecino
                    if vecino not in mejor_heuristica or heuristicas[vecino] < mejor_heuristica[vecino]:
                        mejor_heuristica[vecino] = heuristicas[vecino]  # Actualiza la mejor heurística
                        # Agrega el vecino a la cola de prioridad con la heurística correspondiente
                        heapq.heappush(cola_prioridad, (heuristicas[vecino], vecino, camino + [vecino]))

    return None  # Si no se encontró un camino, retorna None


# Ejecución
inicio = 'A'  # Nodo de inicio
objetivo = 'G'  # Nodo objetivo
# Ejecuta la búsqueda voraz con el grafo, inicio, objetivo y heurísticas
camino = busqueda_voraz(grafo, inicio, objetivo, heuristicas)

# Si se encontró un camino, lo muestra, sino muestra que no se encontró
if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print(f"No se encontró un camino de {inicio} a {objetivo}.")
