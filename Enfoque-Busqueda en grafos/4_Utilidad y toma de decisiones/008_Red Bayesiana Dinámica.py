# -*- coding: utf-8 -*-
"""
Red Bayesiana Dinámica (DBN) - Versión corregida
Ejemplo: Sistema de falla-mantenimiento-alarma
"""
from pgmpy.models import DynamicBayesianNetwork as DBN
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import DBNInference

# ===========================================
# 1. Definición CORRECTA de la estructura DBN
# ===========================================
dbn = DBN()
dbn.add_edges_from([
    (('F', 0), ('A', 0)),  # Falla en t afecta alarma en t
    (('F', 0), ('F', 1)),  # Falla en t afecta falla en t+1
    (('M', 0), ('F', 1))  # Mantenimiento en t afecta falla en t+1
])

# ===========================================
# 2. Definición CORRECTA de las CPDs
# ===========================================
# Variable ('F', 0): Falla en tiempo 0
cpd_F0 = TabularCPD(('F', 0), 2, [[0.9], [0.1]])  # P(F_0)

# Variable ('A', 0): Alarma en tiempo 0
cpd_A0 = TabularCPD(
    ('A', 0), 2,
    [[0.95, 0.2],  # P(A=0|F=0), P(A=0|F=1)
     [0.05, 0.8]],  # P(A=1|F=0), P(A=1|F=1)
    evidence=[('F', 0)],
    evidence_card=[2]
)

# Variable ('M', 0): Mantenimiento en tiempo 0
cpd_M0 = TabularCPD(('M', 0), 2, [[0.7], [0.3]])  # P(M_0)

# Variable ('F', 1): Falla en tiempo 1
cpd_F1 = TabularCPD(
    ('F', 1), 2,
    [[0.99, 0.6, 0.3, 0.1],  # P(F_1=0|F_0=0,M_0=0), P(F_1=0|F_0=0,M_0=1), etc.
     [0.01, 0.4, 0.7, 0.9]],
    evidence=[('F', 0), ('M', 0)],
    evidence_card=[2, 2]
)

# Añadir TODAS las CPDs al modelo
dbn.add_cpds(cpd_F0, cpd_A0, cpd_M0, cpd_F1)

# Verificar modelo
print("¿El modelo es válido?", dbn.check_model())

# ===========================================
# 3. Inferencia CORRECTA
# ===========================================
try:
    dbn_infer = DBNInference(dbn)

    # Consulta de ejemplo: P(F_1 | A_0=1)
    resultado = dbn_infer.forward_inference([('F', 1)], {('A', 0): 1})
    print("\nProbabilidad de falla en t=1 dado A_0=1:")
    print(resultado[('F', 1)].values)

except Exception as e:
    print("\nError durante la inferencia:", str(e))

# ===========================================
# 4. Visualización (opcional)
# ===========================================
try:
    from pgmpy.utils import get_example_model
    from pgmpy.utils import plot_dbn

    # Ejemplo con un modelo predefinido (si falla la visualización personalizada)
    modelo_ejemplo = get_example_model('dbn')
    plot_dbn(modelo_ejemplo)

except ImportError:
    print("\nAdvertencia: No se pudo cargar el módulo de visualización")