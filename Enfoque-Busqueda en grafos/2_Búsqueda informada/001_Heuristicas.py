import heapq
from math import radians, sin, cos, sqrt, atan2

# Datos del grafo (ciudades y conexiones con costos reales)
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

# Coordenadas aproximadas de las ciudades (lat, lon)
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

# Heurística: Distancia en línea recta (Haversine)
def heuristica(ciudad_actual, ciudad_objetivo):
    lat1, lon1 = coordenadas[ciudad_actual]
    lat2, lon2 = coordenadas[ciudad_objetivo]
    R = 6371  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Algoritmo A*
def a_star(grafo, inicio, objetivo):
    cola = [(0 + heuristica(inicio, objetivo), 0, inicio, [inicio])]
    visitados = set()
    while cola:
        _, costo_real, ciudad, camino = heapq.heappop(cola)
        if ciudad == objetivo:
            return camino, costo_real
        if ciudad not in visitados:
            visitados.add(ciudad)
            for vecino, costo in grafo[ciudad].items():
                heapq.heappush(cola, (
                    costo_real + costo + heuristica(vecino, objetivo),
                    costo_real + costo,
                    vecino,
                    camino + [vecino]
                ))
    return None, float('inf')

# Algoritmo Greedy Best-First Search
def greedy(grafo, inicio, objetivo):
    cola = [(heuristica(inicio, objetivo), inicio, [inicio])]
    visitados = set()
    while cola:
        _, ciudad, camino = heapq.heappop(cola)
        if ciudad == objetivo:
            return camino
        if ciudad not in visitados:
            visitados.add(ciudad)
            for vecino in grafo[ciudad]:
                heapq.heappush(cola, (
                    heuristica(vecino, objetivo),
                    vecino,
                    camino + [vecino]
                ))
    return None

# Ejecución
inicio = 'CDMX'
objetivo = 'Monterrey'

camino_a_star, costo_a_star = a_star(grafo, inicio, objetivo)
camino_greedy = greedy(grafo, inicio, objetivo)

print(f"\n--- Búsqueda Informada: {inicio} -> {objetivo} ---")
print(f"A*: Camino = {camino_a_star}, Costo real = {costo_a_star} km")
print(f"Greedy: Camino = {camino_greedy}")