# Importa la biblioteca heapq para usar colas de prioridad (min-heaps)
import heapq

# Importa funciones matemáticas necesarias para calcular la distancia Haversine
from math import radians, sin, cos, sqrt, atan2

# Define el grafo como un diccionario de ciudades con sus conexiones y costos reales de distancia
grafo = {
    'CDMX': {'Puebla': 120, 'Querétaro': 200, 'Toluca': 60},
    'Puebla': {'CDMX': 120, 'Oaxaca': 300},
    'Querétaro': {'CDMX': 200, 'San Luis Potosí': 150, 'Guadalajara': 250},
    'Toluca': {'CDMX': 60, 'Morelia': 180},
    'Oaxaca': {'Puebla': 300},
    'San Luis Potosí': {'Querétaro': 150, 'Monterrey': 350},
    'Guadalajara': {'Querétaro': 250, 'Morelia': 200},
    'Morelia': {'Toluca': 180, 'Guadalajara': 200},
    'Monterrey': {'San Luis Potosí': 350}
}

# Coordenadas geográficas aproximadas de cada ciudad en formato (latitud, longitud)
coordenadas = {
    'CDMX': (19.4326, -99.1332),
    'Puebla': (19.0414, -98.2063),
    'Querétaro': (20.5881, -100.3881),
    'Toluca': (19.2925, -99.6532),
    'Oaxaca': (17.0732, -96.7266),
    'San Luis Potosí': (22.1565, -100.9855),
    'Guadalajara': (20.6597, -103.3496),
    'Morelia': (19.7069, -101.1925),
    'Monterrey': (25.6866, -100.3161)
}


# Calcula la distancia aproximada en línea recta entre dos ciudades usando la fórmula de Haversine
def heuristica(ciudad_actual, ciudad_objetivo):
    lat1, lon1 = coordenadas[ciudad_actual]  # Coordenadas de la ciudad actual
    lat2, lon2 = coordenadas[ciudad_objetivo]  # Coordenadas de la ciudad objetivo
    R = 6371  # Radio de la Tierra en kilómetros

    # Diferencias angulares entre latitudes y longitudes (convertidas a radianes)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    # Fórmula de Haversine para calcular la distancia sobre la superficie terrestre
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Devuelve la distancia en km como valor heurístico


# Implementación del algoritmo A* que combina costo real + heurística
def a_star(grafo, inicio, objetivo):
    # Cola de prioridad que contiene tuplas: (costo total estimado, costo real, ciudad actual, camino recorrido)
    cola = [(0 + heuristica(inicio, objetivo), 0, inicio, [inicio])]
    visitados = set()  # Conjunto de ciudades ya visitadas

    # Mientras haya nodos por explorar
    while cola:
        _, costo_real, ciudad, camino = heapq.heappop(cola)  # Extrae el nodo con menor costo estimado

        # Si llegamos al objetivo, devolvemos el camino y el costo real
        if ciudad == objetivo:
            return camino, costo_real

        # Si la ciudad no ha sido visitada aún
        if ciudad not in visitados:
            visitados.add(ciudad)  # Marca la ciudad como visitada

            # Itera sobre todos los vecinos de la ciudad actual
            for vecino, costo in grafo[ciudad].items():
                # Calcula el costo real acumulado y el costo total estimado
                heapq.heappush(cola, (
                    costo_real + costo + heuristica(vecino, objetivo),  # f(n) = g(n) + h(n)
                    costo_real + costo,  # g(n): costo real acumulado
                    vecino,
                    camino + [vecino]  # Actualiza el camino
                ))

    # Si no se encontró un camino, se devuelve None
    return None, float('inf')


# Búsqueda informada Greedy: solo considera la heurística (no el costo real)
def greedy(grafo, inicio, objetivo):
    # Cola de prioridad que contiene tuplas: (heurística, ciudad actual, camino recorrido)
    cola = [(heuristica(inicio, objetivo), inicio, [inicio])]
    visitados = set()  # Ciudades ya visitadas

    # Mientras haya nodos por explorar
    while cola:
        _, ciudad, camino = heapq.heappop(cola)  # Extrae el nodo con menor heurística

        # Si llegamos al objetivo, devolvemos el camino
        if ciudad == objetivo:
            return camino

        # Si la ciudad no ha sido visitada aún
        if ciudad not in visitados:
            visitados.add(ciudad)  # Marca como visitada

            # Explora vecinos y calcula únicamente la heurística
            for vecino in grafo[ciudad]:
                heapq.heappush(cola, (
                    heuristica(vecino, objetivo),  # Solo se usa h(n), no g(n)
                    vecino,
                    camino + [vecino]
                ))

    # Si no se encuentra el camino
    return None

# Define el punto de inicio y el destino
inicio = 'CDMX'
objetivo = 'Monterrey'

# Ejecuta A*
camino_a_star, costo_a_star = a_star(grafo, inicio, objetivo)

# Ejecuta búsqueda Greedy
camino_greedy = greedy(grafo, inicio, objetivo)

# Imprime los resultados
print(f"\n--- Búsqueda Informada: {inicio} -> {objetivo} ---")
print(f"A*: Camino = {camino_a_star}, Costo real = {costo_a_star} km")
print(f"Greedy: Camino = {camino_greedy}")
