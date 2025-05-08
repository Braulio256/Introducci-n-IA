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
        self.dominios = dominios
        self.restricciones = restricciones

    def es_consistente(self, asignacion):
        """Verifica si una asignación parcial cumple todas las restricciones."""
        for (var1, var2), restriccion in self.restricciones.items():
            if var1 in asignacion and var2 in asignacion:
                if not restriccion(asignacion[var1], asignacion[var2]):
                    return False
        return True


# Ejemplo: Problema de colorear Australia (3 colores)
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
dominios = {var: ['Rojo', 'Verde', 'Azul'] for var in variables}
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


def backtracking_csp(csp, asignacion={}):
    """
    Resuelve un CSP usando backtracking recursivo.

    Args:
        csp: Objeto CSP definido previamente.
        asignacion: Asignación parcial actual (inicia vacía).

    Returns:
        Asignación completa o None si no hay solución.
    """
    # Caso base: asignación completa
    if len(asignacion) == len(csp.variables):
        return asignacion

    # Seleccionar variable no asignada (heurística: MRV)
    var_no_asignadas = [v for v in csp.variables if v not in asignacion]
    var = min(var_no_asignadas, key=lambda v: len(csp.dominios[v]))

    for valor in csp.dominios[var]:
        asignacion_actual = asignacion.copy()
        asignacion_actual[var] = valor

        if csp.es_consistente(asignacion_actual):
            resultado = backtracking_csp(csp, asignacion_actual)
            if resultado is not None:
                return resultado

    return None  # No se encontró solución


# Ejecución
solucion = backtracking_csp(problema)
print("Solución CSP (colores):", solucion)