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
        self.grafo = {
            'A': {'B': 1, 'C': 3},  # Ejemplo: De 'A' a 'B' cuesta 1
            'B': {'A': 1, 'D': 2},
            'C': {'A': 3, 'D': 1},
            'D': {'B': 2, 'C': 1, 'E': 4},
            'E': {'D': 4}  # Nodo objetivo
        }
        self.objetivo = 'E'

    def obtener_vecinos(self, nodo):
        """
        Devuelve los nodos vecinos y sus costos.
        Simula cómo un agente percibe el entorno en tiempo real.
        """
        return self.grafo.get(nodo, {}).items()

    def es_objetivo(self, nodo):
        """Verifica si el nodo actual es el objetivo"""
        return nodo == self.objetivo


###############################
# ALGORITMO LRTA* (BÚSQUEDA ONLINE)
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
    # 1. INICIALIZACIÓN
    camino = [inicio]  # Registra el camino seguido
    costo_total = 0
    h = {}  # Diccionario de heurísticas (se actualiza durante la búsqueda)
    nodo_actual = inicio

    # 2. BÚSQUEDA PRINCIPAL
    for _ in range(max_iter):
        # Condición de término: ¿Llegamos al objetivo?
        if entorno.es_objetivo(nodo_actual):
            break

        # 2.1 INICIALIZAR HEURÍSTICA SI ES NECESARIO
        if nodo_actual not in h:
            h[nodo_actual] = 0  # Valor inicial (puede ajustarse)

        # 2.2 OBTENER INFORMACIÓN LOCAL (VECINOS)
        vecinos = list(entorno.obtener_vecinos(nodo_actual))

        if not vecinos:  # Si no hay vecinos, terminamos
            break

        # 2.3 SELECCIÓN DEL MEJOR VECINO
        mejor_vecino = None
        mejor_valor = float('inf')  # Inicializamos con infinito

        for vecino, costo in vecinos:
            # Inicializar heurística para nodos nuevos
            if vecino not in h:
                h[vecino] = 0
                # Calcular valor f(n) = costo + h(n)
            valor = costo + h[vecino]
            # Actualizar mejor opción
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_vecino = vecino

        # 2.4 ACTUALIZAR HEURÍSTICA (APRENDIZAJE)
        h[nodo_actual] = mejor_valor

        # 2.5 MOVERSE AL SIGUIENTE NODO
        # Calculamos el costo real del movimiento
        costo_real = next(c for (v, c) in vecinos if v == mejor_vecino)
        costo_total += costo_real
        nodo_actual = mejor_vecino
        camino.append(nodo_actual)

    # 3. RESULTADOS
    return camino, costo_total


###############################
# EJEMPLO DE USO
###############################
if __name__ == "__main__":
    # Crear entorno y ejecutar búsqueda
    entorno = EntornoDinamico()
    camino, costo = busqueda_online_lrta(entorno, 'A')

    # Mostrar resultados
    print(f"Camino encontrado: {' → '.join(camino)}")
    print(f"Costo total: {costo}")
    print("Nota: Los costos pueden variar por las heurísticas dinámicas")