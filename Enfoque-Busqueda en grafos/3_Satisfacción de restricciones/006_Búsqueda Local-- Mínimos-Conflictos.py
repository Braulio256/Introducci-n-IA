import random


class CSP:
    def __init__(self, variables, dominios, restricciones):
        """
        Inicializa un problema CSP.

        Args:
            variables: Lista de variables (ej: ['A', 'B', 'C'])
            dominios: Diccionario {variable: lista_de_valores_posibles}
            restricciones: Diccionario {(var1, var2): función_restricción}
        """
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones

    def contar_conflictos(self, variable, valor, asignacion):
        """Calcula cuántas restricciones viola un valor para una variable"""
        conflictos = 0
        for (v1, v2), restriccion in self.restricciones.items():
            if v1 == variable and v2 in asignacion:
                if not restriccion(valor, asignacion[v2]):
                    conflictos += 1
            elif v2 == variable and v1 in asignacion:
                if not restriccion(asignacion[v1], valor):
                    conflictos += 1
        return conflictos


def minimos_conflictos(csp, max_iter=1000):
    """
    Implementación del algoritmo de mínimos conflictos.

    Args:
        csp: Objeto CSP definido previamente
        max_iter: Máximo de iteraciones permitidas

    Returns:
        Asignación solución o None si no converge
    """
    # 1. Inicialización aleatoria
    asignacion = {var: random.choice(csp.dominios[var]) for var in csp.variables}

    for _ in range(max_iter):
        # 2. Verificar si es solución
        conflictos_totales = sum(
            csp.contar_conflictos(var, asignacion[var], asignacion)
            for var in csp.variables
        )
        if conflictos_totales == 0:
            return asignacion

        # 3. Seleccionar variable conflictiva aleatoria
        var_conflictiva = random.choice([
            var for var in csp.variables
            if csp.contar_conflictos(var, asignacion[var], asignacion) > 0
        ])

        # 4. Elegir valor que minimice conflictos
        mejor_valor = min(
            csp.dominios[var_conflictiva],
            key=lambda v: csp.contar_conflictos(var_conflictiva, v, asignacion)
        )

        # 5. Actualizar asignación
        asignacion[var_conflictiva] = mejor_valor

    return None  # No se encontró solución en max_iter


# Ejemplo: Problema de las 8 reinas (adaptado)
variables = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8']
dominios = {r: range(8) for r in variables}  # Columnas (0-7)


def restriccion_reinas(a, b):
    """Verifica que dos reinas no se ataquen"""
    return a != b  # Simplificado para ejemplo


restricciones = {
    (f'R{i}', f'R{j}'): restriccion_reinas
    for i in range(1, 9) for j in range(i + 1, 9)
}

# Resolver
problema = CSP(variables, dominios, restricciones)
solucion = minimos_conflictos(problema, max_iter=10000)

print("Solución encontrada:")
for reina, columna in sorted(solucion.items()):
    print(f"{reina}: Columna {columna}")