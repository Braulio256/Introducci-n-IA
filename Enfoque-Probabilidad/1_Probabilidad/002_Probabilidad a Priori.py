import numpy as np
from scipy.stats import beta, binom
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuración estética moderna
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 12

# =============================================
# 1. DIAGNÓSTICO MÉDICO (PREVALENCIA COMO PRIOR)
# =============================================
print("\n1. Diagnóstico Médico (Prevalencia como Prior)")

prevalencia = 0.01
sensibilidad = 0.95
especificidad = 0.90


def teorema_bayes(prior, likeli, marginal):
    return (prior * likeli) / marginal


# Paciente con prueba positiva
prob_prior = prevalencia
likeli_pos = sensibilidad
marginal_pos = (prevalencia * sensibilidad) + ((1 - prevalencia) * (1 - especificidad))
prob_posterior = teorema_bayes(prob_prior, likeli_pos, marginal_pos)

print(f"• Probabilidad a priori: {prevalencia:.3f}")
print(f"• Probabilidad posterior: {prob_posterior:.3f}")

# Visualización
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs[0, 0].bar(['Prior', 'Posterior'], [prob_prior, prob_posterior],
              color=['blue', 'red'], alpha=0.7)
axs[0, 0].set_title("Actualización de Creencia en Diagnóstico Médico")
axs[0, 0].set_ylabel("Probabilidad")
axs[0, 0].set_ylim(0, 0.2)

# =============================================
# 2. FILTRADO BAYESIANO DE SPAM
# =============================================
print("\n2. Filtrado Bayesiano de Spam")

spam_total = 120
palabra_spam = 90
no_spam_total = 300
palabra_no_spam = 15

alpha_prior = 1
beta_prior = 1
alpha_post = alpha_prior + palabra_spam
beta_post = beta_prior + (spam_total - palabra_spam)

x = np.linspace(0, 1, 1000)
axs[0, 1].plot(x, beta.pdf(x, alpha_prior, beta_prior), 'b-', label='Prior (Uniforme)')
axs[0, 1].plot(x, beta.pdf(x, alpha_post, beta_post), 'r-', label='Posterior')
axs[0, 1].set_title("Distribución para Palabra 'oferta' en Spam")
axs[0, 1].set_xlabel("Probabilidad")
axs[0, 1].legend()

# =============================================
# 3. COMPARACIÓN DE DIFERENTES PRIORS
# =============================================
print("\n3. Comparación de Diferentes Priors")
priors = {
    'Fuerte creencia baja': beta(2, 20),
    'Uniforme': beta(1, 1),
    'Fuerte creencia alta': beta(20, 2)
}

exitos = 15
fracasos = 5

for nombre, prior in priors.items():
    posterior = beta(prior.args[0] + exitos, prior.args[1] + fracasos)
    axs[1, 0].plot(x, posterior.pdf(x), label=nombre)

axs[1, 0].set_title("Efecto del Prior en la Posterior")
axs[1, 0].legend()

# =============================================
# 4. SIMULACIÓN MONTE CARLO
# =============================================
print("\n4. Simulación Monte Carlo con Prior")

prior_theta = beta(8, 4)
theta_samples = prior_theta.rvs(10000)
n_experimentos = 20
datos_simulados = binom.rvs(n=n_experimentos, p=theta_samples)

axs[1, 1].hist(datos_simulados, bins=range(22), density=True, alpha=0.6)
axs[1, 1].set_title(f"Distribución Predictiva Prior\n(Beta(8,4) + Binomial(n={n_experimentos}))")

plt.tight_layout()
plt.show()

# =============================================
# TABLA COMPARATIVA
# =============================================
print("\nTabla Comparativa de Priors")
data = {
    'Prior': list(priors.keys()),
    'Media Prior': [p.mean() for p in priors.values()],
    'Media Posterior': [beta(a + exitos, b + fracasos).mean()
                        for a, b in [p.args for p in priors.values()]],
    'Prob > 0.7': [1 - beta(a + exitos, b + fracasos).cdf(0.7)
                   for a, b in [p.args for p in priors.values()]]
}

df = pd.DataFrame(data)
print(df.round(3))