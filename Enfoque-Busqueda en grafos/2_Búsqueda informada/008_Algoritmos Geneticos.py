import random

#############################
# CONFIGURACIÓN INICIAL
#############################
POBLACION_SIZE = 50
GENES = "01"  # Para problemas binarios
TARGET = "10011010011"  # Solución objetivo
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.7
GENERATIONS = 100


#############################
# FUNCIONES BASE
#############################
def crear_individuo(length):
    """Crea un individuo aleatorio"""
    return ''.join(random.choice(GENES) for _ in range(length))


def crear_poblacion(size, length):
    """Inicializa una población"""
    return [crear_individuo(len(TARGET)) for _ in range(size)]


#############################
# FUNCIONES DE EVALUACIÓN
#############################
def fitness(individuo):
    """Calcula la aptitud (mayor es mejor)"""
    return sum(1 for i, j in zip(individuo, TARGET) if i == j)


def evaluar_poblacion(poblacion):
    """Evalúa toda la población"""
    return [fitness(ind) for ind in poblacion]


#############################
# OPERADORES GENÉTICOS
#############################
def seleccion(poblacion, fitnesses):
    """Selección por ruleta"""
    total = sum(fitnesses)
    probs = [f / total for f in fitnesses]
    return random.choices(poblacion, weights=probs, k=2)


def crossover(padre1, padre2):
    """Cruza en un punto"""
    if random.random() < CROSSOVER_RATE:
        punto = random.randint(1, len(TARGET) - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2
    return padre1, padre2


def mutacion(individuo):
    """Aplica mutaciones aleatorias"""
    individuo = list(individuo)
    for i in range(len(individuo)):
        if random.random() < MUTATION_RATE:
            individuo[i] = random.choice(GENES)
    return ''.join(individuo)


#############################
# ALGORITMO PRINCIPAL
#############################
def algoritmo_genetico():
    # Inicialización
    poblacion = crear_poblacion(POBLACION_SIZE, len(TARGET))
    mejor_aptitud = 0
    mejor_individuo = ""

    for generacion in range(GENERATIONS):
        # Evaluación
        fitnesses = evaluar_poblacion(poblacion)

        # Encontrar el mejor
        max_fitness = max(fitnesses)
        if max_fitness > mejor_aptitud:
            mejor_aptitud = max_fitness
            idx = fitnesses.index(max_fitness)
            mejor_individuo = poblacion[idx]
            print(f"Gen {generacion}: Mejor = {mejor_individuo} Aptitud = {mejor_aptitud}")

            # Condición de término
            if mejor_aptitud == len(TARGET):
                break

        # Nueva generación
        nueva_poblacion = []

        while len(nueva_poblacion) < POBLACION_SIZE:
            # Selección
            padres = seleccion(poblacion, fitnesses)

            # Cruzamiento
            hijos = crossover(*padres)

            # Mutación
            hijos = [mutacion(h) for h in hijos]

            nueva_poblacion.extend(hijos[:POBLACION_SIZE - len(nueva_poblacion)])

        poblacion = nueva_poblacion

    return mejor_individuo, mejor_aptitud


#############################
# EJECUCIÓN
#############################
if __name__ == "__main__":
    mejor, aptitud = algoritmo_genetico()
    print(f"\nResultado Final:\nMejor Individuo: {mejor}\nAptitud: {aptitud}/{len(TARGET)}")