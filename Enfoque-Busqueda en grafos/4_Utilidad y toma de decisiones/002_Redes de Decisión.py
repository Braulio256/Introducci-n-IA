import matplotlib.pyplot as plt
import networkx as nx

# Crear la red de decisión (grafo dirigido)
red_decision = nx.DiGraph()

# Nodos:
# - Azar (Círculo): Variables aleatorias (incertidumbre).
# - Decisión (Rectángulo): Acciones del agente.
# - Utilidad (Diamante): Función de recompensa.

# Ejemplo: Decidir si llevar paraguas (acción) basado en el clima (azar)
red_decision.add_node("Clima", tipo="azar", dominio=["Lluvia", "Sol"])
red_decision.add_node("LlevarParaguas", tipo="decision", dominio=["Sí", "No"])
red_decision.add_node("Utilidad", tipo="utilidad")

# Aristas (dependencias):
red_decision.add_edge("Clima", "Utilidad")  # El clima afecta la utilidad
red_decision.add_edge("LlevarParaguas", "Utilidad")  # La decisión afecta la utilidad

# Probabilidades a priori (Clima)
prob_clima = {"Lluvia": 0.7, "Sol": 0.3}

# Tabla de utilidad (depende de Clima y LlevarParaguas)
tabla_utilidad = {
    ("Lluvia", "Sí"): 50,   # Llueve y llevas paraguas: alta utilidad
    ("Lluvia", "No"): -10,  # Llueve y no llevas paraguas: baja utilidad
    ("Sol", "Sí"): 20,      # Sol y llevas paraguas: utilidad moderada (molestia)
    ("Sol", "No"): 100      # Sol y no llevas paraguas: máxima utilidad
}

# Calcular utilidad esperada para cada decisión
def utilidad_esperada(decision):
    """
    Calcula la utilidad esperada dada una decisión.
    Args:
        decision (str): "Sí" o "No".
    Returns:
        float: Utilidad esperada.
    """
    utilidad = 0
    for clima, prob in prob_clima.items():
        utilidad += tabla_utilidad[(clima, decision)] * prob
    return utilidad

# Evaluar todas las decisiones
print("Utilidad Esperada para cada Decisión:")
for decision in ["Sí", "No"]:
    print(f"LlevarParaguas = {decision}: {utilidad_esperada(decision):.2f}")

# Decisión óptima (maximizar utilidad esperada)
decision_optima = max(["Sí", "No"], key=utilidad_esperada)
print(f"\nDecisión óptima: LlevarParaguas = {decision_optima}")

# Visualización del grafo (opcional)
pos = {"Clima": (0, 1), "LlevarParaguas": (0, -1), "Utilidad": (2, 0)}
node_colors = []
for node in red_decision.nodes():
    if red_decision.nodes[node]["tipo"] == "azar":
        node_colors.append("lightblue")
    elif red_decision.nodes[node]["tipo"] == "decision":
        node_colors.append("lightgreen")
    else:
        node_colors.append("yellow")

nx.draw(red_decision, pos, with_labels=True, node_color=node_colors, node_size=3000, node_shape="s")
plt.title("Red de Decisión: Llevar Paraguas")
plt.show()