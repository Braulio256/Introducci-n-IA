class CSP:
    """
    CLASE PRINCIPAL PARA DEFINIR UN PROBLEMA CSP

    Atributos:
        variables: Lista de variables del problema
        dominios: Diccionario con valores posibles para cada variable
        restricciones: Diccionario con restricciones entre pares de variables
    """

    def __init__(self, variables, dominios, restricciones):
        # Inicialización de las componentes básicas del CSP
        self.variables = variables  # Ej: ['WA', 'NT', 'SA', ...]
        self.dominios = dominios  # Ej: {'WA': ['Rojo', 'Verde', 'Azul'], ...}
        self.restricciones = restricciones  # Ej: {('WA','NT'): lambda a,b: a!=b, ...}

    def es_consistente(self, variable, valor, asignacion):
        """
        VERIFICADOR DE CONSISTENCIA PARA ASIGNACIONES PARCIALES

        Args:
            variable: Variable que se quiere asignar
            valor: Valor propuesto para la variable
            asignacion: Diccionario con asignaciones actuales

        Returns:
            True si la asignación es consistente, False si viola restricciones
        """
        # Revisa todas las restricciones que involucran a la variable
        for (var1, var2), restriccion in self.restricciones.items():
            # Caso donde var1 es la variable actual y var2 ya está asignada
            if var1 == variable and var2 in asignacion:
                if not restriccion(valor, asignacion[var2]):
                    return False
            # Caso donde var2 es la variable actual y var1 ya está asignada
            elif var2 == variable and var1 in asignacion:
                if not restriccion(asignacion[var1], valor):
                    return False
        return True


def seleccionar_variable_no_asignada(csp, asignacion):
    """
    HEURÍSTICA MRV (MÍNIMOS VALORES RESTANTES)

    Selecciona la variable con menos valores posibles en su dominio,
    para reducir el factor de ramificación.
    """
    # Filtra variables no asignadas
    variables_no_asignadas = [v for v in csp.variables if v not in asignacion]
    # Elige la variable con el dominio más pequeño
    return min(variables_no_asignadas, key=lambda v: len(csp.dominios[v]))


def ordenar_valores(csp, variable, asignacion):
    """
    HEURÍSTICA LCV (VALOR QUE MENOS RESTRINGE)

    Ordena los valores del dominio de la variable según cuánto
    limitan las opciones de las variables vecinas no asignadas.
    """

    def contar_conflictos(valor):
        # Cuenta cuántas restricciones violaría este valor
        return sum(1 for (var1, var2), restriccion in csp.restricciones.items()
                   if (var1 == variable and var2 not in asignacion and
                       not restriccion(valor, csp.dominios[var2][0])))

    # Ordena valores de menos a más conflictivos
    return sorted(csp.dominios[variable], key=contar_conflictos)


def backtracking(csp, asignacion=None):
    """
    ALGORITMO PRINCIPAL DE BACKTRACKING

    Args:
        csp: Objeto CSP con el problema a resolver
        asignacion: Asignación parcial actual (inicia vacía)

    Returns:
        Asignación completa solución o None si no hay solución
    """
    # Inicialización para primera llamada recursiva
    if asignacion is None:
        asignacion = {}

    # CASO BASE: solución completa encontrada
    if len(asignacion) == len(csp.variables):
        return asignacion

    # 1. SELECCIÓN DE VARIABLE (usando MRV)
    variable = seleccionar_variable_no_asignada(csp, asignacion)

    # 2. ORDENACIÓN DE VALORES (usando LCV)
    for valor in ordenar_valores(csp, variable, asignacion):
        # 3. VERIFICACIÓN DE CONSISTENCIA
        if csp.es_consistente(variable, valor, asignacion):
            # 4. ASIGNACIÓN TEMPORAL
            asignacion[variable] = valor

            # 5. LLAMADA RECURSIVA
            resultado = backtracking(csp, asignacion)

            # 6. VERIFICACIÓN DE SOLUCIÓN
            if resultado is not None:
                return resultado

            # 7. BACKTRACK (eliminar asignación si no llevó a solución)
            del asignacion[variable]

    # 8. RETORNO SIN SOLUCIÓN (para esta rama)
    return None


# =============================================================================
# EJEMPLO: PROBLEMA DE COLOREO DE MAPA (AUSTRALIA)
# =============================================================================

# Definición de variables (regiones)
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

# Dominios posibles (colores disponibles)
dominios = {var: ['Rojo', 'Verde', 'Azul'] for var in variables}

# Restricciones: regiones adyacentes no pueden tener el mismo color
restricciones = {
    ('WA', 'NT'): lambda a, b: a != b,
    ('WA', 'SA'): lambda a, b: a != b,
    ('NT', 'SA'): lambda a, b: a != b,
    ('NT', 'Q'): lambda a, b: a != b,
    ('SA', 'Q'): lambda a, b: a != b,
    ('SA', 'NSW'): lambda a, b: a != b,
    ('SA', 'V'): lambda a, b: a != b,
    ('Q', 'NSW'): lambda a, b: a != b,
    ('NSW', 'V'): lambda a, b: a != b
}

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

# 1. Crear instancia del problema CSP
problema = CSP(variables, dominios, restricciones)

# 2. Resolver usando backtracking
solucion = backtracking(problema)

# 3. Mostrar resultados
print("\nSOLUCIÓN ENCONTRADA:")
for variable, valor in solucion.items():
    print(f"{variable}: {valor}")
print("\nNota: Los colores pueden variar entre ejecuciones por el orden de exploración")