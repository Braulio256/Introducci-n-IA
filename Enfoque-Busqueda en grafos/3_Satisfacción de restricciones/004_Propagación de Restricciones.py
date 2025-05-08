from collections import deque


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
        self.dominios = {v: list(dominios[v]) for v in variables}  # Copia los dominios
        self.restricciones = restricciones
        self.arcos = self._obtener_arcos()  # Precomputa todos los arcos

    def _obtener_arcos(self):
        """Genera todos los arcos bidireccionales del grafo de restricciones"""
        arcos = []
        for (xi, xj) in self.restricciones:
            arcos.append((xi, xj))
            arcos.append((xj, xi))  # Restricciones son bidireccionales
        return arcos


def AC3(csp):
    """
    Implementación del algoritmo AC-3 para propagación de restricciones.

    Args:
        csp: Objeto CSP definido previamente

    Returns:
        True si se logra consistencia de arcos, False si se detecta inconsistencia
    """
    cola = deque(csp.arcos)  # Usamos una cola FIFO

    while cola:
        (xi, xj) = cola.popleft()

        # Paso clave: Revisar y reducir dominios
        if revisar(csp, xi, xj):
            if not csp.dominios[xi]:  # Dominio vacío -> inconsistencia
                return False

            # Agregar arcos (xk, xi) para revisión posterior
            for (xk, _) in csp.arcos:
                if xk == xi:
                    continue
                cola.append((xk, xi))

    return True  # Consistencia lograda


def revisar(csp, xi, xj):
    """
    Elimina valores inconsistentes del dominio de xi respecto a xj.

    Args:
        csp: Objeto CSP
        xi: Variable cuyo dominio se revisará
        xj: Variable vecina

    Returns:
        True si se modificó el dominio de xi, False en caso contrario
    """
    modificado = False

    for x in list(csp.dominios[xi]):
        # Verificar si existe algún valor en xj que satisfaga la restricción
        satisfacible = any(
            csp.restricciones.get((xi, xj), lambda a, b: True)(x, y) or
            csp.restricciones.get((xj, xi), lambda a, b: True)(y, x)
            for y in csp.dominios[xj]
        )

        if not satisfacible:
            csp.dominios[xi].remove(x)
            modificado = True

    return modificado


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

# Crear y resolver CSP
problema = CSP(variables, dominios, restricciones)
consistente = AC3(problema)

print("¿Consistencia lograda?", consistente)
print("Dominios resultantes:")
for variable, dominio in problema.dominios.items():
    print(f"{variable}: {dominio}")