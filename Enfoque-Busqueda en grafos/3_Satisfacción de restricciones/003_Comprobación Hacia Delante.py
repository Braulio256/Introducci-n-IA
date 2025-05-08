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
        self.dominios = dominios.copy()  # Copia para no modificar el original
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


def forward_checking(csp, asignacion, var, valor):
    """
    Realiza la comprobación hacia delante después de asignar un valor.

    Args:
        csp: Instancia del problema CSP
        asignacion: Asignación actual
        var: Variable recién asignada
        valor: Valor asignado a la variable

    Returns:
        dominios_actualizados: Dominios reducidos o None si se detecta inconsistencia
    """
    dominios_actualizados = {v: list(csp.dominios[v]) for v in csp.variables if v not in asignacion}

    # Corrección clave: Obtener vecinos correctamente
    vecinos = []
    for (v1, v2) in csp.restricciones:
        if v1 == var and v2 not in asignacion:
            vecinos.append(v2)
        elif v2 == var and v1 not in asignacion:
            vecinos.append(v1)

    for vecino in vecinos:
        for val_vecino in list(dominios_actualizados[vecino]):
            # Verificar compatibilidad con la nueva asignación
            if (var, vecino) in csp.restricciones:
                if not csp.restricciones[(var, vecino)](valor, val_vecino):
                    dominios_actualizados[vecino].remove(val_vecino)
            elif (vecino, var) in csp.restricciones:
                if not csp.restricciones[(vecino, var)](val_vecino, valor):
                    dominios_actualizados[vecino].remove(val_vecino)

            # Si un dominio queda vacío, la asignación es inválida
            if not dominios_actualizados[vecino]:
                return None
    return dominios_actualizados


def backtracking_con_fc(csp, asignacion=None):
    """
    Backtracking con Forward Checking.

    Args:
        csp: Instancia del CSP
        asignacion: Asignación parcial (inicia vacía)

    Returns:
        Solución completa o None si no hay solución
    """
    if asignacion is None:
        asignacion = {}

    # Caso base: solución completa
    if len(asignacion) == len(csp.variables):
        return asignacion

    # Selección de variable (MRV)
    var = min([v for v in csp.variables if v not in asignacion],
              key=lambda v: len(csp.dominios[v]))

    for valor in list(csp.dominios[var]):
        if csp.es_consistente(var, valor, asignacion):
            # Hacer asignación temporal
            asignacion[var] = valor

            # Guardar estado anterior de dominios
            dominios_originales = {v: list(csp.dominios[v]) for v in csp.variables}

            # Aplicar Forward Checking
            dominios_fc = forward_checking(csp, asignacion, var, valor)

            if dominios_fc is not None:
                # Actualizar dominios temporalmente
                for v in dominios_fc:
                    csp.dominios[v] = dominios_fc[v]

                # Llamada recursiva
                resultado = backtracking_con_fc(csp, asignacion)
                if resultado is not None:
                    return resultado

                # Restaurar dominios después de la recursión
                for v in dominios_fc:
                    csp.dominios[v] = dominios_originales[v]

            # Deshacer asignación
            del asignacion[var]

    return None


# Ejemplo: Problema de colorear Australia
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

# Resolución
problema = CSP(variables, dominios, restricciones)
solucion = backtracking_con_fc(problema)
print("Solución con Forward Checking:", solucion)