import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, norm, entropy
import seaborn as sns

# Configuración estética
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = [12, 6]

# =============================================
# 1. Representación de Incertidumbre Discreta
# =============================================
print("\n1. Distribución Discreta (Lanzamiento de Dado Cargado)")
probs = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]  # Probabilidad de cada cara
dados = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']

# Muestreo de la distribución
muestras = np.random.choice(dados, size=1000, p=probs)
frecuencias = {dado: list(muestras).count(dado)/1000 for dado in dados}

print("Frecuencias relativas en 1000 lanzamientos:")
for dado, freq in frecuencias.items():
    print(f"{dado}: {freq:.3f}")

# Visualización
plt.subplot(2, 2, 1)
plt.bar(dados, probs, color='skyblue', alpha=0.7, label='Verdadero')
plt.bar(dados, list(frecuencias.values()), color='red', alpha=0.3, label='Muestreado')
plt.title("Distribución de Probabilidad Discreta")
plt.xlabel("Resultado")
plt.ylabel("Probabilidad")
plt.legend()

# =============================================
# 2. Distribución Continua (Incertidumbre en Medición)
# =============================================
print("\n2. Distribución Continua (Medición con Ruido)")
media_real = 5.0
desviacion = 1.5

# Generar datos con ruido gaussiano
datos_medicion = np.random.normal(media_real, desviacion, 1000)

# Ajustar distribución
x = np.linspace(0, 10, 1000)
pdf = norm.pdf(x, media_real, desviacion)

plt.subplot(2, 2, 2)
sns.histplot(datos_medicion, bins=30, kde=False, stat="density", color='lightgreen')
plt.plot(x, pdf, 'r-', lw=2, label=f'N(μ={media_real}, σ={desviacion})')
plt.title("Distribución Normal de Mediciones")
plt.xlabel("Valor Medido")
plt.ylabel("Densidad")
plt.legend()

# =============================================
# 3. Actualización Bayesiana (Distribución Beta)
# =============================================
print("\n3. Actualización Bayesiana (Prueba A/B)")
# Parámetros iniciales (creencia previa)
alpha_prior, beta_prior = 2, 2

# Datos observados (éxitos=15, fracasos=10)
exitos = 15
fracasos = 10

# Actualización
alpha_posterior = alpha_prior + exitos
beta_posterior = beta_prior + fracasos

# Visualización
x = np.linspace(0, 1, 1000)
plt.subplot(2, 2, 3)
plt.plot(x, beta.pdf(x, alpha_prior, beta_prior), 'b-', label='Previa')
plt.plot(x, beta.pdf(x, alpha_posterior, beta_posterior), 'r-', label='Posterior')
plt.title("Actualización de Creencia (Beta-Binomial)")
plt.xlabel("Probabilidad de Éxito")
plt.ylabel("Densidad")
plt.legend()

# =============================================
# 4. Medición de Incertidumbre (Entropía)
# =============================================
print("\n4. Medición de Incertidumbre (Entropía)")
def calcular_entropia(probs):
    return -np.sum(probs * np.log2(probs + 1e-10))  # +1e-10 para estabilidad

# Tres distribuciones diferentes
dist_uniforme = np.array([0.25, 0.25, 0.25, 0.25])
dist_segura = np.array([0.9, 0.03, 0.03, 0.04])
dist_confusa = np.array([0.4, 0.3, 0.2, 0.1])

entropias = {
    "Uniforme": calcular_entropia(dist_uniforme),
    "Segura": calcular_entropia(dist_segura),
    "Confusa": calcular_entropia(dist_confusa)
}

print("\nEntropía de diferentes distribuciones:")
for nombre, H in entropias.items():
    print(f"{nombre}: {H:.3f} bits")

plt.subplot(2, 2, 4)
plt.bar(entropias.keys(), entropias.values(), color=['blue', 'green', 'red'])
plt.title("Entropía como Medida de Incertidumbre")
plt.ylabel("Bits")

plt.tight_layout()
plt.show()