import matplotlib.pyplot as plt
import networkx as nx

###############################
# CLASE DEL ENTORNO DINÁMICO
###############################
class EntornoDinamico:
    def __init__(self):
        """
        Simula un entorno dinámico con:
        - grafo: Diccionario que representa conexiones entre nodos y sus costos
        - objetivo: Nodo destino (en este caso 'E')
        """
        # Representación de un grafo donde las claves son nodos y los valores son diccionarios
        # que indican los nodos vecinos y el costo para llegar a ellos.
        self.grafo = {
            'A': {'B': 1, 'C': 3},
            'B': {'A': 1, 'D': 2},
            'C': {'A': 3, 'D': 1},
            'D': {'B': 2, 'C': 1, 'E': 4},
            'E': {'D': 4}  # Nodo objetivo
        }
        # El objetivo del agente es llegar al nodo 'E'
        self.objetivo = 'E'

    def obtener_vecinos(self, nodo):
        """
        Obtiene los vecinos de un nodo y sus costos de transición.
        Simula cómo un agente percibe el entorno en tiempo real.
        """
        # Retorna los vecinos del nodo en forma de lista de tuplas (vecino, costo)
        return self.grafo.get(nodo, {}).items()

    def es_objetivo(self, nodo):
        """Verifica si el nodo actual es el objetivo"""
        # Verifica si el nodo proporcionado es el objetivo
        return nodo == self.objetivo


###############################
# FUNCIÓN DE VISUALIZACIÓN
###############################
def dibujar_grafo(entorno, camino):
    """
    Dibuja el grafo y destaca el camino recorrido por el agente en color rojo.
    Utiliza la librería NetworkX y Matplotlib.
    """
    G = nx.Graph()  # Crea un grafo vacío
    # Añade las conexiones entre nodos al grafo
    for nodo, vecinos in entorno.grafo.items():
        for vecino, costo in vecinos.items():
            G.add_edge(nodo, vecino, weight=costo)  # Añadir una arista con su peso

    # Posicionamiento de los nodos utilizando el layout de spring
    pos = nx.spring_layout(G)
    # Obtener las etiquetas de las aristas (costos)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Dibuja el grafo con etiquetas y nodos de color azul claro
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000)
    # Dibuja las etiquetas de los costos en las aristas
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Dibuja el camino recorrido en color rojo
    path_edges = list(zip(camino, camino[1:]))  # Zips los nodos consecutivos en el camino
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    # Título del gráfico
    plt.title("Camino recorrido por LRTA*")
    plt.show()


###############################
# ALGORITMO LRTA* MEJORADO
###############################
def busqueda_online_lrta(entorno, inicio, max_iter=100):
    """
    Implementación de LRTA* (Learning Real-Time A*):
    - Aprende heurísticas mientras explora
    - Toma decisiones basadas en información local

    Args:
        entorno: Objeto que simula el entorno dinámico
        inicio: Nodo inicial (ej: 'A')
        max_iter: Límite de pasos para evitar bucles infinitos

    Returns:
        camino: Lista de nodos visitados
        costo_total: Costo acumulado del camino
    """
    # Inicializa el camino con el nodo de inicio
    camino = [inicio]
    # Inicializa el costo total en 0
    costo_total = 0
    # Diccionario para almacenar las heurísticas de cada nodo
    h = {}
    # Nodo actual del agente
    nodo_actual = inicio
    # Conjunto de nodos ya visitados para detectar bucles
    visitados = set()

    for paso in range(max_iter):
        # Imprime el estado actual del paso en la búsqueda
        print(f"\nPaso {paso + 1}: Nodo actual = {nodo_actual}")

        # Si llegamos al objetivo, terminamos la búsqueda
        if entorno.es_objetivo(nodo_actual):
            print("¡Objetivo alcanzado!")
            break

        # Inicializa la heurística para el nodo actual si no está definida
        if nodo_actual not in h:
            h[nodo_actual] = 0

        # Obtiene los vecinos del nodo actual
        vecinos = list(entorno.obtener_vecinos(nodo_actual))
        if not vecinos:
            # Si no hay vecinos, terminamos la búsqueda
            print("No hay vecinos disponibles. Fin de búsqueda.")
            break

        # Selección del mejor vecino
        mejor_vecino = None
        mejor_valor = float('inf')  # Comienza con un valor infinito

        for vecino, costo in vecinos:
            # Si el vecino no tiene heurística, inicializa a 0
            if vecino not in h:
                h[vecino] = 0
            # Calcula el valor f(n) = costo + heurística
            valor = costo + h[vecino]
            # Imprime la evaluación del vecino
            print(f"Evaluando vecino {vecino}: costo = {costo}, h = {h[vecino]}, total = {valor}")
            # Si es el mejor valor, selecciona el vecino
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_vecino = vecino

        # Imprime el mejor vecino seleccionado
        print(f"Mejor vecino seleccionado: {mejor_vecino} con valor {mejor_valor}")
        # Actualiza la heurística del nodo actual
        h[nodo_actual] = mejor_valor
        print(f"Heurística actualizada: h({nodo_actual}) = {h[nodo_actual]}")

        # Calcula el costo real de la transición al mejor vecino
        costo_real = next(c for (v, c) in vecinos if v == mejor_vecino)
        # Acumula el costo total
        costo_total += costo_real
        # Mueve al agente al mejor vecino
        nodo_actual = mejor_vecino

        # Detecta posibles repeticiones en el camino (bucle)
        if nodo_actual in camino:
            print("Advertencia: Se ha detectado una posible repetición en el camino.")
        # Añade el nuevo nodo al camino recorrido
        camino.append(nodo_actual)

    return camino, costo_total, h


###############################
# EJEMPLO DE USO
###############################
if __name__ == "__main__":
    # Crear el entorno dinámico
    entorno = EntornoDinamico()
    # Ejecutar la búsqueda LRTA* desde el nodo 'A'
    camino, costo, heuristica = busqueda_online_lrta(entorno, 'A')

    # Mostrar el resultado de la búsqueda
    print("\n==========================")
    print(f"Camino encontrado: {' → '.join(camino)}")
    print(f"Costo total del camino: {costo}")
    print("Heurísticas finales aprendidas:")
    for nodo in heuristica:
        print(f"  h({nodo}) = {heuristica[nodo]}")

    # Visualizar el camino sobre el grafo
    dibujar_grafo(entorno, camino)
