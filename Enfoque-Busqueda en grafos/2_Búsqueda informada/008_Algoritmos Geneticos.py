import random  # Importamos el módulo random para operaciones aleatorias


#############################
# CONFIGURACIÓN INICIAL
#############################
POBLACION_SIZE = 300  # Número de individuos en la población
GENES = "01"  # Genes disponibles (para codificación binaria)
TARGET = "1011011011010"  # Solución objetivo que se desea alcanzar
MUTATION_RATE = 0.0000000001  # Probabilidad de mutación por gen
CROSSOVER_RATE = 0.03  # Probabilidad de realizar cruce
GENERATIONS = 1000  # Número máximo de generaciones


#############################
# FUNCIONES BASE
#############################
def crear_individuo(length):
    """
    Crea un individuo aleatorio con una secuencia binaria de longitud 'length'.
    """
    return ''.join(random.choice(GENES) for _ in range(length))


def crear_poblacion(size, length):
    """
    Inicializa una población con individuos aleatorios.

    Args:
        size: Número de individuos.
        length: Longitud de cada individuo (basada en el TARGET).
    """
    return [crear_individuo(length) for _ in range(size)]


#############################
# FUNCIONES DE EVALUACIÓN
#############################
def fitness(individuo):
    """
    Calcula la aptitud de un individuo comparándolo con el objetivo.
    Retorna el número de bits correctos.

    Args:
        individuo: Cadena binaria.

    Returns:
        Número de coincidencias con TARGET.
    """
    return sum(1 for i, j in zip(individuo, TARGET) if i == j)


def evaluar_poblacion(poblacion):
    """
    Evalúa la aptitud de todos los individuos en la población.

    Args:
        poblacion: Lista de individuos.

    Returns:
        Lista de valores de aptitud correspondientes.
    """
    return [fitness(ind) for ind in poblacion]


#############################
# OPERADORES GENÉTICOS
#############################
def seleccion(poblacion, fitnesses):
    """
    Selección por ruleta: selecciona dos individuos proporcionalmente a su aptitud.

    Args:
        poblacion: Lista de individuos.
        fitnesses: Lista de valores de aptitud.

    Returns:
        Dos individuos seleccionados como padres.
    """
    total = sum(fitnesses)
    if total == 0:
        # En caso de que todos tengan aptitud cero, se selecciona aleatoriamente
        return random.sample(poblacion, 2)
    probs = [f / total for f in fitnesses]
    return random.choices(poblacion, weights=probs, k=2)


def crossover(padre1, padre2):
    """
    Realiza cruce en un punto aleatorio con una cierta probabilidad.

    Args:
        padre1: Individuo padre.
        padre2: Individuo madre.

    Returns:
        Dos hijos (resultado del cruce o copia de padres).
    """
    if random.random() < CROSSOVER_RATE:
        punto = random.randint(1, len(TARGET) - 1)  # Punto de cruce no trivial
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2
    return padre1, padre2  # Si no hay cruce, se devuelven los padres sin cambios


def mutacion(individuo):
    """
    Aplica mutación aleatoria a un individuo con cierta probabilidad por gen.

    Args:
        individuo: Cadena binaria.

    Returns:
        Individuo mutado.
    """
    individuo = list(individuo)
    for i in range(len(individuo)):
        if random.random() < MUTATION_RATE:
            individuo[i] = random.choice(GENES)
    return ''.join(individuo)


#############################
# ALGORITMO PRINCIPAL
#############################
def algoritmo_genetico():
    """
    Ejecuta el algoritmo genético completo:
    - Inicializa la población
    - Itera generaciones realizando selección, cruce y mutación
    - Retorna el mejor individuo y su aptitud
    """
    poblacion = crear_poblacion(POBLACION_SIZE, len(TARGET))  # Población inicial
    mejor_aptitud = 0  # Almacena la mejor aptitud encontrada
    mejor_individuo = ""  # Almacena el mejor individuo

    for generacion in range(GENERATIONS):
        fitnesses = evaluar_poblacion(poblacion)  # Evaluar aptitud

        # Verificar y guardar el mejor individuo de la generación
        max_fitness = max(fitnesses)
        if max_fitness > mejor_aptitud:
            mejor_aptitud = max_fitness
            idx = fitnesses.index(max_fitness)
            mejor_individuo = poblacion[idx]
            print(f"Gen {generacion}: Mejor = {mejor_individuo} Aptitud = {mejor_aptitud}")

            # Si alcanzamos el objetivo perfecto, terminamos
            if mejor_aptitud == len(TARGET):
                break

        nueva_poblacion = []  # Lista para almacenar la siguiente generación

        while len(nueva_poblacion) < POBLACION_SIZE:
            padres = seleccion(poblacion, fitnesses)  # Selección de padres
            hijos = crossover(*padres)  # Cruce para generar hijos
            hijos = [mutacion(h) for h in hijos]  # Aplicar mutación a los hijos
            # Agregar los hijos generados (sin exceder el tamaño de población)
            nueva_poblacion.extend(hijos[:POBLACION_SIZE - len(nueva_poblacion)])

        poblacion = nueva_poblacion  # Reemplazar población actual con la nueva

    return mejor_individuo, mejor_aptitud  # Retornar la mejor solución


#############################
# EJECUCIÓN
#############################
if __name__ == "__main__":
    # Ejecutar el algoritmo y mostrar resultados finales
    mejor, aptitud = algoritmo_genetico()
    print(f"\nResultado Final:\nMejor Individuo: {mejor}\nAptitud: {aptitud}/{len(TARGET)}")
