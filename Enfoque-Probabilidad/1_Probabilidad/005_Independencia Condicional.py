import numpy as np
import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
import matplotlib.pyplot as plt
import networkx as nx

# Configuración de visualización
plt.rcParams['figure.figsize'] = [14, 7]
plt.rcParams['font.size'] = 12

# =============================================
# 1. EJEMPLO MÉDICO (CORREGIDO)
# =============================================
print("\n1. Red Bayesiana Médica (Síntomas dada la Enfermedad)")

# Crear modelo
modelo_medico = DiscreteBayesianNetwork([
    ('Enfermedad', 'Fiebre'),
    ('Enfermedad', 'Tos'),
    ('Enfermedad', 'Dolor')
])

# Definir CPDs (sin cambios)
cpd_enfermedad = TabularCPD(
    variable='Enfermedad',
    variable_card=2,
    values=[[0.98], [0.02]],
    state_names={'Enfermedad': ['No', 'Si']}
)

cpd_fiebre = TabularCPD(
    variable='Fiebre',
    variable_card=2,
    values=[
        [0.95, 0.2],
        [0.05, 0.8]
    ],
    evidence=['Enfermedad'],
    evidence_card=[2],
    state_names={
        'Fiebre': ['No', 'Si'],
        'Enfermedad': ['No', 'Si']
    }
)

cpd_tos = TabularCPD(
    variable='Tos',
    variable_card=2,
    values=[
        [0.9, 0.3],
        [0.1, 0.7]
    ],
    evidence=['Enfermedad'],
    evidence_card=[2],
    state_names={
        'Tos': ['No', 'Si'],
        'Enfermedad': ['No', 'Si']
    }
)

cpd_dolor = TabularCPD(
    variable='Dolor',
    variable_card=2,
    values=[
        [0.85, 0.1],
        [0.15, 0.9]
    ],
    evidence=['Enfermedad'],
    evidence_card=[2],
    state_names={
        'Dolor': ['No', 'Si'],
        'Enfermedad': ['No', 'Si']
    }
)

# Añadir CPDs al modelo
modelo_medico.add_cpds(cpd_enfermedad, cpd_fiebre, cpd_tos, cpd_dolor)

# Verificar independencia condicional
print("\nVerificación de independencia condicional:")
print("¿Fiebre y Tos son independientes dada Enfermedad?:",
      modelo_medico.is_dconnected('Fiebre', 'Tos', observed=['Enfermedad']))
print("¿Fiebre y Dolor son independientes sin condicionar?:",
      modelo_medico.is_dconnected('Fiebre', 'Dolor'))

# Convertir a grafo NetworkX para visualización
G_medico = nx.DiGraph()
G_medico.add_edges_from(modelo_medico.edges())

# Visualización
plt.subplot(1, 2, 1)
nx.draw(G_medico,
        with_labels=True,
        node_size=2000,
        node_color='skyblue',
        font_size=12,
        arrowsize=20)
plt.title("Red Bayesiana Médica")

# =============================================
# 2. FILTRADO DE SPAM (CORREGIDO)
# =============================================
print("\n\n2. Modelo Naive Bayes para Spam")

# Crear modelo
modelo_spam = DiscreteBayesianNetwork([
    ('Spam', 'Oferta'),
    ('Spam', 'Urgente'),
    ('Spam', 'Ganador')
])

# Probabilidades (sin cambios)
cpd_spam = TabularCPD(
    variable='Spam',
    variable_card=2,
    values=[[0.7], [0.3]],
    state_names={'Spam': ['No', 'Si']}
)

cpd_oferta = TabularCPD(
    variable='Oferta',
    variable_card=2,
    values=[
        [0.99, 0.4],
        [0.01, 0.6]
    ],
    evidence=['Spam'],
    evidence_card=[2],
    state_names={
        'Oferta': ['No', 'Si'],
        'Spam': ['No', 'Si']
    }
)

cpd_urgente = TabularCPD(
    variable='Urgente',
    variable_card=2,
    values=[
        [0.98, 0.3],
        [0.02, 0.7]
    ],
    evidence=['Spam'],
    evidence_card=[2],
    state_names={
        'Urgente': ['No', 'Si'],
        'Spam': ['No', 'Si']
    }
)

cpd_ganador = TabularCPD(
    variable='Ganador',
    variable_card=2,
    values=[
        [0.95, 0.2],
        [0.05, 0.8]
    ],
    evidence=['Spam'],
    evidence_card=[2],
    state_names={
        'Ganador': ['No', 'Si'],
        'Spam': ['No', 'Si']
    }
)

# Añadir CPDs
modelo_spam.add_cpds(cpd_spam, cpd_oferta, cpd_urgente, cpd_ganador)

# Verificar independencia
print("\nVerificación para palabras en spam:")
print("¿Oferta y Urgente son independientes dado Spam?:",
      modelo_spam.is_dconnected('Oferta', 'Urgente', observed=['Spam']))

# Convertir a grafo NetworkX
G_spam = nx.DiGraph()
G_spam.add_edges_from(modelo_spam.edges())

# Visualización
plt.subplot(1, 2, 2)
nx.draw(G_spam,
        with_labels=True,
        node_size=2000,
        node_color='lightgreen',
        font_size=12,
        arrowsize=20)
plt.title("Modelo Naive Bayes para Spam")

plt.tight_layout()
plt.show()

# =============================================
# 3. DEMOSTRACIÓN NUMÉRICA (SIN CAMBIOS)
# =============================================
print("\n\n3. Cálculo Numérico de Independencia Condicional")

def calcular_joint(enfermedad, fiebre, tos, dolor):
    p_e = cpd_enfermedad.values[enfermedad]
    p_f_e = cpd_fiebre.values[fiebre, enfermedad]
    p_t_e = cpd_tos.values[tos, enfermedad]
    p_d_e = cpd_dolor.values[dolor, enfermedad]
    return p_e * p_f_e * p_t_e * p_d_e

p_fiebre_tos_enfermo = calcular_joint(1, 1, 1, 1) + calcular_joint(1, 1, 1, 0)
p_fiebre_enfermo = cpd_fiebre.values[1, 1]
p_tos_enfermo = cpd_tos.values[1, 1]
producto = p_fiebre_enfermo * p_tos_enfermo

print(f"\nP(Fiebre, Tos | Enfermedad=Si): {p_fiebre_tos_enfermo:.4f}")
print(f"P(Fiebre|Enfermedad=Si) * P(Tos|Enfermedad=Si): {producto:.4f}")
print(f"¿Son iguales?: {np.isclose(p_fiebre_tos_enfermo, producto)}")

# =============================================
# 4. TABLA COMPARATIVA (SIN CAMBIOS)
# =============================================
data = {
    'Variable 1': ['Fiebre', 'Fiebre', 'Oferta', 'Oferta'],
    'Variable 2': ['Tos', 'Dolor', 'Urgente', 'Ganador'],
    'Independientes': [False, False, False, False],
    'Condicionalmente Independientes': [True, True, True, True],
    'Dado': ['Enfermedad', 'Enfermedad', 'Spam', 'Spam']
}

df = pd.DataFrame(data)
print("\nTabla de Independencia Condicional:")
print(df.to_markdown(index=False))