import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, poisson, norm, expon, beta
import seaborn as sns
import pandas as pd

# Configuración estética
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [14, 8]
plt.rcParams['font.size'] = 12
colors = sns.color_palette("husl", 8)

# =============================================
# 1. DISTRIBUCIÓN BINOMIAL
# =============================================
print("\n1. Distribución Binomial (Éxitos en n intentos)")

n, p = 20, 0.4
x_binom = np.arange(0, n+1)
prob_binom = binom.pmf(x_binom, n, p)

plt.subplot(2, 3, 1)
plt.bar(x_binom, prob_binom, color=colors[0], alpha=0.7)
plt.title(f"Binomial(n={n}, p={p})")
plt.xlabel("Número de éxitos")
plt.ylabel("Probabilidad")

# =============================================
# 2. DISTRIBUCIÓN DE POISSON
# =============================================
print("\n2. Distribución Poisson (Eventos en intervalo)")

mu = 3.5
x_poisson = np.arange(0, 15)
prob_poisson = poisson.pmf(x_poisson, mu)

plt.subplot(2, 3, 2)
plt.bar(x_poisson, prob_poisson, color=colors[1], alpha=0.7)
plt.title(f"Poisson(μ={mu})")
plt.xlabel("Número de eventos")
plt.ylabel("Probabilidad")

# =============================================
# 3. DISTRIBUCIÓN NORMAL
# =============================================
print("\n3. Distribución Normal (Variables continuas)")

mu, sigma = 170, 8
x_norm = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
pdf_norm = norm.pdf(x_norm, mu, sigma)

plt.subplot(2, 3, 3)
plt.plot(x_norm, pdf_norm, color=colors[2], linewidth=2)
plt.title(f"Normal(μ={mu}, σ={sigma})")
plt.xlabel("Valor")
plt.ylabel("Densidad")

# =============================================
# 4. DISTRIBUCIÓN EXPONENCIAL
# =============================================
print("\n4. Distribución Exponencial (Tiempos entre eventos)")

lambda_ = 0.5
x_expon = np.linspace(0, 10, 1000)
pdf_expon = expon.pdf(x_expon, scale=1/lambda_)

plt.subplot(2, 3, 4)
plt.plot(x_expon, pdf_expon, color=colors[3], linewidth=2)
plt.title(f"Exponencial(λ={lambda_})")
plt.xlabel("Tiempo")
plt.ylabel("Densidad")

# =============================================
# 5. DISTRIBUCIÓN BETA
# =============================================
print("\n5. Distribución Beta (Probabilidad de probabilidades)")

alpha, beta_ = 8, 2
x_beta = np.linspace(0, 1, 1000)
pdf_beta = beta.pdf(x_beta, alpha, beta_)

plt.subplot(2, 3, 5)
plt.plot(x_beta, pdf_beta, color=colors[4], linewidth=2)
plt.title(f"Beta(α={alpha}, β={beta_})")
plt.xlabel("Probabilidad")
plt.ylabel("Densidad")

# =============================================
# 6. COMPARACIÓN ENTRE DISTRIBUCIONES (CORREGIDO)
# =============================================
plt.subplot(2, 3, 6)
x_comp = np.linspace(-4, 4, 100)
plt.plot(x_comp, norm.pdf(x_comp), label='Normal(0,1)')

# Corrección aquí: separar los argumentos correctamente
x_poisson_comp = np.arange(0, 20)
plt.plot(x_poisson_comp, poisson.pmf(x_poisson_comp, 3), 'o-', label='Poisson(3)')

x_binom_comp = np.arange(20)
plt.plot(x_binom_comp, binom.pmf(x_binom_comp, 20, 0.3), 's-', label='Binomial(20,0.3)')

plt.title("Comparación entre Distribuciones")
plt.legend()
plt.xlabel("Valor")
plt.ylabel("Densidad/Probabilidad")

plt.tight_layout()
plt.show()

# =============================================
# TABLA RESUMEN DE PROPIEDADES
# =============================================
distributions = [
    ["Binomial", "Discreta", "n, p", "Éxitos en intentos", "Spam detection"],
    ["Poisson", "Discreta", "μ", "Eventos raros", "Visitas web"],
    ["Normal", "Continua", "μ, σ", "Variables continuas", "Puntuaciones"],
    ["Exponencial", "Continua", "λ", "Tiempos entre eventos", "Tiempos de espera"],
    ["Beta", "Continua", "α, β", "Proporciones", "CTR anuncios"]
]

df = pd.DataFrame(distributions,
                 columns=["Distribución", "Tipo", "Parámetros", "Uso", "Aplicación IA"])
print("\nResumen de Distribuciones Clave:")
print(df.to_markdown(index=False))