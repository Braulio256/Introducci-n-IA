import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo dirigido con utilidades en las aristas
grafo = nx.DiGraph()

# Añadir nodos (estados/decisiones)
grafo.add_nodes_from(["Inicio", "A", "B", "C", "Meta"])

# Añadir aristas con utilidades (representan acciones y sus recompensas)
grafo.add_edge("Inicio", "A", utilidad=5)
grafo.add_edge("Inicio", "B", utilidad=2)
grafo.add_edge("A", "C", utilidad=7)
grafo.add_edge("B", "C", utilidad=3)
grafo.add_edge("C", "Meta", utilidad=10)
grafo.add_edge("B", "Meta", utilidad=1)


# Función para calcular la utilidad de un camino
def utilidad_camino(camino):
    """
    Calcula la utilidad total de un camino (suma de utilidades de las aristas).

    Args:
        camino (list): Lista de nodos en orden (ej. ["Inicio", "A", "C", "Meta"]).

    Returns:
        int: Utilidad total del camino.
    """
    utilidad_total = 0
    for i in range(len(camino) - 1):
        utilidad_total += grafo[camino[i]][camino[i + 1]]["utilidad"]
    return utilidad_total


# Encontrar todos los caminos posibles desde "Inicio" hasta "Meta"
caminos_posibles = list(nx.all_simple_paths(grafo, "Inicio", "Meta"))

# Evaluar cada camino según su utilidad
print("Caminos posibles y sus utilidades:")
for idx, camino in enumerate(caminos_posibles):
    print(f"Camino {idx + 1}: {camino} -> Utilidad = {utilidad_camino(camino)}")

# Seleccionar el camino con máxima utilidad (decisión óptima)
mejor_camino = max(caminos_posibles, key=utilidad_camino)
print(f"\nMejor camino según teoría de utilidad: {mejor_camino} (Utilidad = {utilidad_camino(mejor_camino)})")

# Visualización del grafo (opcional)
pos = nx.spring_layout(grafo)
nx.draw(grafo, pos, with_labels=True, node_color="skyblue", node_size=1000)
edge_labels = nx.get_edge_attributes(grafo, "utilidad")
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)
plt.title("Grafo de Decisiones con Utilidades")
plt.show()