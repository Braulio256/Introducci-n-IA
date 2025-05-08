import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de estilos
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = [12, 6]

# =============================================
# 1. FILTRADO BAYESIANO DE SPAM (NORMALIZACIÓN)
# =============================================
print("\n1. Filtrado Bayesiano de Spam con Normalización")

# Datos de entrenamiento
data = {
    'Palabra': ['oferta', 'urgente', 'ganador', 'reunión', 'proyecto'],
    'P(Spam|Palabra)': [0.9, 0.85, 0.7, 0.3, 0.1],
    'Frecuencia_Spam': [0.4, 0.3, 0.2, 0.05, 0.02],
    'Frecuencia_NoSpam': [0.01, 0.02, 0.03, 0.1, 0.15]
}

df_spam = pd.DataFrame(data)

# Probabilidad a priori
p_spam = 0.3  # P(Spam)
p_no_spam = 0.7  # P(¬Spam)


# Cálculo de probabilidades condicionadas normalizadas
def bayes_spam(row, p_spam_prior):
    # P(Palabra|Spam)
    p_word_spam = row['Frecuencia_Spam']
    # P(Palabra|¬Spam)
    p_word_nospam = row['Frecuencia_NoSpam']

    # Numerador y denominador del teorema de Bayes
    numerator = p_word_spam * p_spam_prior
    denominator = (p_word_spam * p_spam_prior) + (p_word_nospam * (1 - p_spam_prior))

    return numerator / denominator


# Aplicar a todas las palabras
df_spam['P(Spam|Palabra)_Calc'] = df_spam.apply(bayes_spam, axis=1, p_spam_prior=p_spam)

print("\nTabla de Probabilidades de Spam:")
print(df_spam[['Palabra', 'P(Spam|Palabra)', 'P(Spam|Palabra)_Calc']].round(3))

# Visualización
plt.figure(figsize=(10, 5))
plt.bar(df_spam['Palabra'], df_spam['P(Spam|Palabra)'], alpha=0.6, label='Original')
plt.bar(df_spam['Palabra'], df_spam['P(Spam|Palabra)_Calc'], alpha=0.4, label='Calculada')
plt.title("Comparación de Probabilidades Condicionadas de Spam")
plt.ylabel("Probabilidad")
plt.legend()
plt.show()

# =============================================
# 2. DIAGNÓSTICO MÉDICO CON MÚLTIPLES SÍNTOMAS
# =============================================
print("\n\n2. Diagnóstico Médico con Múltiples Síntomas")

# Probabilidades a priori
p_enfermedad = 0.01  # Prevalencia
p_no_enfermedad = 1 - p_enfermedad

# Probabilidades condicionadas
sintomas = {
    'Fiebre': {'Enfermo': 0.8, 'Sano': 0.1},
    'Tos': {'Enfermo': 0.7, 'Sano': 0.2},
    'Dolor': {'Enfermo': 0.6, 'Sano': 0.1}
}


# Función para calcular probabilidad posterior
def diagnostico_bayes(sintomas_presentes):
    # Inicializar con la probabilidad a priori
    posterior = p_enfermedad

    # Aplicar teorema de Bayes para cada síntoma
    for sintoma in sintomas_presentes:
        likelihood = sintomas[sintoma]['Enfermo']
        marginal = (likelihood * p_enfermedad) + (sintomas[sintoma]['Sano'] * p_no_enfermedad)
        posterior = (likelihood * posterior) / marginal

    return posterior


# Casos de prueba
casos = [
    ['Fiebre'],
    ['Fiebre', 'Tos'],
    ['Fiebre', 'Tos', 'Dolor']
]

print("\nProbabilidad de enfermedad dado síntomas:")
for caso in casos:
    prob = diagnostico_bayes(caso)
    print(f"{', '.join(caso)}: {prob:.4f}")

# =============================================
# 3. NORMALIZACIÓN DE DISTRIBUCIONES
# =============================================
print("\n\n3. Normalización de Distribuciones de Probabilidad")

# Distribución no normalizada
scores = np.array([8.5, 7.2, 9.1, 6.3, 8.8])
prob_no_norm = np.exp(scores)  # Simular logits

# Normalización (softmax)
prob_norm = np.exp(scores) / np.sum(np.exp(scores))

# Crear DataFrame para comparación
df_norm = pd.DataFrame({
    'Elemento': ['A', 'B', 'C', 'D', 'E'],
    'Score': scores,
    'Prob_No_Norm': prob_no_norm,
    'Prob_Norm': prob_norm
})

print("\nTabla de Normalización:")
print(df_norm.round(4))

# Visualización
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.bar(df_norm['Elemento'], df_norm['Prob_No_Norm'])
ax1.set_title("Probabilidades No Normalizadas")
ax2.bar(df_norm['Elemento'], df_norm['Prob_Norm'])
ax2.set_title("Probabilidades Normalizadas (Softmax)")
plt.show()

# =============================================
# 4. MODELO GAUSSIANO CON NORMALIZACIÓN
# =============================================
print("\n\n4. Modelo Gaussiano con Normalización")

# Datos de altura de población
mu_hombres = 175  # cm
sigma_hombres = 7
mu_mujeres = 162  # cm
sigma_mujeres = 6

# Generar datos
np.random.seed(42)
hombres = norm.rvs(loc=mu_hombres, scale=sigma_hombres, size=1000)
mujeres = norm.rvs(loc=mu_mujeres, scale=sigma_mujeres, size=1000)

# Función de densidad de probabilidad (PDF)
altura = 170
pdf_hombre = norm.pdf(altura, mu_hombres, sigma_hombres)
pdf_mujer = norm.pdf(altura, mu_mujeres, sigma_mujeres)

# Normalización (P(Género|Altura))
p_hombre = 0.5  # Asumimos igual probabilidad a priori
p_mujer = 0.5

p_altura = (pdf_hombre * p_hombre) + (pdf_mujer * p_mujer)
p_hombre_altura = (pdf_hombre * p_hombre) / p_altura
p_mujer_altura = (pdf_mujer * p_mujer) / p_altura

print(f"\nProbabilidades para altura = {altura} cm:")
print(f"P(Hombre|Altura): {p_hombre_altura:.4f}")
print(f"P(Mujer|Altura): {p_mujer_altura:.4f}")

# Visualización
x = np.linspace(140, 200, 1000)
plt.figure(figsize=(10, 5))
plt.plot(x, norm.pdf(x, mu_hombres, sigma_hombres), label='Hombres')
plt.plot(x, norm.pdf(x, mu_mujeres, sigma_mujeres), label='Mujeres')
plt.axvline(altura, color='red', linestyle='--', label=f'Altura = {altura} cm')
plt.title("Distribución de Alturas por Género")
plt.xlabel("Altura (cm)")
plt.ylabel("Densidad de Probabilidad")
plt.legend()
plt.show()