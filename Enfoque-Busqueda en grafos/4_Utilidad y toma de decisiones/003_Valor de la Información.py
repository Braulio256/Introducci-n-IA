import numpy as np
import matplotlib.pyplot as plt

# --- Definición del problema ---
# Decisión: Llevar paraguas (Sí/No)
# Estado incierto: Clima (Lluvia o Sol)
prob_clima = {"Lluvia": 0.3, "Sol": 0.7}  # Probabilidades a priori

# Tabla de utilidad (clima, decisión) -> utilidad
tabla_utilidad = {
    ("Lluvia", "Sí"): 50,   # Llevar paraguas cuando llueve: alta utilidad
    ("Lluvia", "No"): -10,  # No llevarlo cuando llueve: baja utilidad
    ("Sol", "Sí"): 20,      # Llevarlo cuando hay sol: utilidad moderada
    ("Sol", "No"): 100      # No llevarlo cuando hay sol: máxima utilidad
}

# --- Utilidad esperada sin información adicional ---
def utilidad_esperada(decision, prob_clima):
    """Calcula la utilidad esperada dada una decisión y distribución del clima."""
    return sum(tabla_utilidad[(clima, decision)] * prob for clima, prob in prob_clima.items())

# Decisión óptima sin información
decision_sin_info = max(["Sí", "No"], key=lambda d: utilidad_esperada(d, prob_clima))
utilidad_sin_info = utilidad_esperada(decision_sin_info, prob_clima)
print(f"Decisión óptima sin información: {decision_sin_info} (Utilidad esperada: {utilidad_sin_info:.2f})")

# --- Utilidad esperada con información perfecta (VOI) ---
# Suponemos que podemos conocer el clima con certeza antes de decidir
utilidad_con_info = 0
for clima, prob in prob_clima.items():
    # Elegimos la mejor decisión para cada clima posible
    mejor_decision = max(["Sí", "No"], key=lambda d: tabla_utilidad[(clima, d)])
    utilidad_con_info += tabla_utilidad[(clima, mejor_decision)] * prob

# Valor de la Información (VOI) = Utilidad con info - Utilidad sin info
voi = utilidad_con_info - utilidad_sin_info
print(f"\nUtilidad esperada con información perfecta: {utilidad_con_info:.2f}")
print(f"Valor de la Información (VOI): {voi:.2f}")

# --- Caso con información imperfecta (Ejemplo: Pronóstico con 90% de precisión) ---
precision_pronostico = 0.9  # P(pronóstico=Lluvia | Lluvia_real)
prob_pronostico = {
    "Pronóstico_Lluvia": prob_clima["Lluvia"] * precision_pronostico + prob_clima["Sol"] * (1 - precision_pronostico),
    "Pronóstico_Sol": prob_clima["Sol"] * precision_pronostico + prob_clima["Lluvia"] * (1 - precision_pronostico)
}

# Probabilidades posteriores (Teorema de Bayes)
def prob_posterior(pronostico):
    """Calcula P(Lluvia | pronóstico) y P(Sol | pronóstico)."""
    if pronostico == "Pronóstico_Lluvia":
        p_lluvia = (prob_clima["Lluvia"] * precision_pronostico) / prob_pronostico["Pronóstico_Lluvia"]
        return {"Lluvia": p_lluvia, "Sol": 1 - p_lluvia}
    else:
        p_sol = (prob_clima["Sol"] * precision_pronostico) / prob_pronostico["Pronóstico_Sol"]
        return {"Lluvia": 1 - p_sol, "Sol": p_sol}

# Utilidad esperada con pronóstico
utilidad_con_pronostico = 0
for pronostico, prob in prob_pronostico.items():
    posterior = prob_posterior(pronostico)
    mejor_decision = max(["Sí", "No"], key=lambda d: utilidad_esperada(d, posterior))
    utilidad_con_pronostico += utilidad_esperada(mejor_decision, posterior) * prob

voi_imperfecto = utilidad_con_pronostico - utilidad_sin_info
print(f"\nUtilidad con pronóstico (90% precisión): {utilidad_con_pronostico:.2f}")
print(f"VOI (Información imperfecta): {voi_imperfecto:.2f}")

# Comparación de VOI en diferentes precisiones de pronóstico
precisiones = np.linspace(0.5, 1.0, 10)
vois = []
for p in precisiones:
    prob_pronostico_p = {
        "Pronóstico_Lluvia": prob_clima["Lluvia"] * p + prob_clima["Sol"] * (1 - p),
        "Pronóstico_Sol": prob_clima["Sol"] * p + prob_clima["Lluvia"] * (1 - p)
    }
    utilidad_p = 0
    for pronostico, prob in prob_pronostico_p.items():
        posterior = prob_posterior(pronostico) if p != 0.5 else prob_clima  # Evitar división por cero
        mejor_decision = max(["Sí", "No"], key=lambda d: utilidad_esperada(d, posterior))
        utilidad_p += utilidad_esperada(mejor_decision, posterior) * prob
    vois.append(utilidad_p - utilidad_sin_info)

plt.plot(precisiones, vois, marker="o")
plt.xlabel("Precisión del Pronóstico")
plt.ylabel("Valor de la Información (VOI)")
plt.title("VOI vs. Precisión de la Información")
plt.grid()
plt.show()