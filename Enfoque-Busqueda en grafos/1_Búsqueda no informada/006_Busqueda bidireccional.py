from collections import deque  # Importa deque para usar colas eficientes (doble extremo)

def reconstruir_camino(padres_desde_inicio, padres_desde_objetivo, nodo_interseccion):
    # Reconstruye el camino desde el nodo inicial hasta la intersección
    camino_desde_inicio = []  # Lista para guardar el camino desde el inicio
    nodo = nodo_interseccion  # Comienza desde la intersección
    while nodo is not None:
        camino_desde_inicio.append(nodo)  # Agrega el nodo al camino
        nodo = padres_desde_inicio[nodo]  # Retrocede al nodo padre
    camino_desde_inicio.reverse()  # Invierte la lista para obtener el orden correcto

    # Reconstruye el camino desde la intersección hasta el objetivo
    camino_desde_objetivo = []  # Lista para el segundo tramo del camino
    nodo = padres_desde_objetivo[nodo_interseccion]  # Comienza desde el padre de la intersección
    while nodo is not None:
        camino_desde_objetivo.append(nodo)  # Agrega nodo al camino
        nodo = padres_desde_objetivo[nodo]  # Retrocede al nodo padre

    # Une ambos caminos (inicio → intersección → objetivo)
    return camino_desde_inicio + camino_desde_objetivo

def busqueda_bidireccional(grafo, inicio, objetivo):
    if inicio == objetivo:
        return [inicio]  # Si el nodo de inicio y objetivo son iguales, devuelve una lista con ese nodo

    # Inicializa las colas de búsqueda para ambos extremos
    cola_inicio = deque([inicio])     # Cola desde el nodo inicial
    cola_objetivo = deque([objetivo]) # Cola desde el nodo objetivo

    # Diccionarios para rastrear los padres de cada nodo (para reconstruir camino)
    padres_inicio = {inicio: None}     # Padres desde el nodo de inicio
    padres_objetivo = {objetivo: None} # Padres desde el nodo objetivo

    # Bucle principal: continúa mientras ambas colas no estén vacías
    while cola_inicio and cola_objetivo:
        # Paso de expansión desde el nodo de inicio
        if cola_inicio:
            nodo_actual = cola_inicio.popleft()  # Extrae el primer nodo de la cola de inicio
            for vecino in grafo[nodo_actual]:    # Itera sobre los vecinos del nodo actual
                if vecino not in padres_inicio:  # Si el vecino no ha sido visitado desde el inicio
                    padres_inicio[vecino] = nodo_actual  # Registra su padre
                    cola_inicio.append(vecino)           # Agrega el vecino a la cola
                    if vecino in padres_objetivo:        # Si el vecino ya fue visitado desde el objetivo
                        return reconstruir_camino(padres_inicio, padres_objetivo, vecino)  # Camino encontrado

        # Paso de expansión desde el nodo objetivo
        if cola_objetivo:
            nodo_actual = cola_objetivo.popleft()  # Extrae el primer nodo de la cola del objetivo
            for vecino in grafo[nodo_actual]:      # Itera sobre sus vecinos
                if vecino not in padres_objetivo:  # Si el vecino no ha sido visitado desde el objetivo
                    padres_objetivo[vecino] = nodo_actual  # Registra su padre
                    cola_objetivo.append(vecino)           # Agrega el vecino a la cola
                    if vecino in padres_inicio:            # Si el vecino ya fue visitado desde el inicio
                        return reconstruir_camino(padres_inicio, padres_objetivo, vecino)  # Camino encontrado

    return None  # Si se termina el bucle sin encontrar intersección, no hay camino

# Grafo de ejemplo (no dirigido)
grafo = {
    'A': ['D', 'C'],      # Nodo A está conectado con D y C
    'B': ['A', 'D', 'C'], # Nodo B está conectado con A, D y C
    'C': ['A', 'E'],      # Nodo C está conectado con A y E
    'D': ['B'],           # Nodo D está conectado con B
    'E': ['B', 'F'],      # Nodo E está conectado con B y F
    'F': ['C', 'E']       # Nodo F está conectado con C y E
}

# Parámetros de ejecución
inicio = 'A'     # Nodo inicial
objetivo = 'E'   # Nodo objetivo

# Llamada a la función de búsqueda bidireccional
camino = busqueda_bidireccional(grafo, inicio, objetivo)

# Mostrar resultado por consola
if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print(f"No hay camino de {inicio} a {objetivo}.")
