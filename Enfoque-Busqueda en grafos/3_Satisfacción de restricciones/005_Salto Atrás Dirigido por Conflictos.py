class CSP:
    def __init__(self, variables, dominios, restricciones):
        """
        Inicializa un problema CSP.

        Args:
            variables: Lista de variables (ej: ['A', 'B', 'C'])
            dominios: Diccionario {variable: lista_de_valores}
            restricciones: Diccionario {(var1, var2): función_restricción}
        """
        self.variables = variables
        self.dominios = dominios.copy()
        self.restricciones = restricciones

    def es_consistente(self, var, valor, asignacion):
        """Verifica si una asignación es consistente"""
        for (v1, v2), restriccion in self.restricciones.items():
            if v1 == var and v2 in asignacion:
                if not restriccion(valor, asignacion[v2]):
                    return False
            elif v2 == var and v1 in asignacion:
                if not restriccion(asignacion[v1], valor):
                    return False
        return True


def conflict_directed_backjumping(csp):
    """
    Implementación del algoritmo CBJ para CSP.

    Args:
        csp: Objeto CSP definido previamente

    Returns:
        Una solución válida o None si no existe
    """
    asignacion = {}
    conflict_set = {v: set() for v in csp.variables}
    return cbj_recursivo(csp, asignacion, 0, conflict_set)


def cbj_recursivo(csp, asignacion, nivel, conflict_set):
    """
    Función recursiva principal para CBJ.
    """
    if len(asignacion) == len(csp.variables):
        return asignacion.copy()

    var = seleccionar_variable(csp, asignacion)

    for valor in ordenar_valores(csp, var, asignacion):
        if csp.es_consistente(var, valor, asignacion):
            asignacion[var] = valor
            resultado = cbj_recursivo(csp, asignacion, nivel + 1, conflict_set)
            if resultado is not None:
                return resultado
            del asignacion[var]
        else:
            # Actualizar conjunto de conflictos
            for v in asignacion:
                if not csp.es_consistente(var, valor, {v: asignacion[v]}):
                    conflict_set[var].add(v)

    # Salto atrás dirigido por conflictos
    if nivel > 0:
        conflicto_union = set()
        for v in conflict_set:
            if v not in asignacion:
                conflicto_union.update(conflict_set[v])

        if conflicto_union:
            max_nivel = max([csp.variables.index(v) for v in conflicto_union])
            # Saltar atrás al nivel del conflicto más reciente
            vars_a_eliminar = [v for v in asignacion if csp.variables.index(v) >= max_nivel]
            for v in vars_a_eliminar:
                del asignacion[v]
            return None

    return None


def seleccionar_variable(csp, asignacion):
    """Selecciona la próxima variable a asignar (MRV)"""
    no_asignadas = [v for v in csp.variables if v not in asignacion]
    return min(no_asignadas, key=lambda v: len(csp.dominios[v]))


def ordenar_valores(csp, var, asignacion):
    """Ordena valores usando heurística LCV"""
    return csp.dominios[var]


# Ejemplo de uso
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
dominios = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}
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

problema = CSP(variables, dominios, restricciones)
solucion = conflict_directed_backjumping(problema)
print("Solución encontrada:", solucion)