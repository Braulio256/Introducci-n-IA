from collections import defaultdict
import itertools


class CSP:
    def __init__(self, variables, dominios, restricciones):
        """
        Inicializa un problema CSP.

        Args:
            variables: Lista de variables
            dominios: Diccionario {variable: valores_posibles}
            restricciones: Diccionario {(var1, var2): función}
        """
        self.variables = variables
        self.dominios = dominios.copy()
        self.restricciones = restricciones
        self.grafo = self._construir_grafo()

    def _construir_grafo(self):
        """Construye el grafo de restricciones"""
        grafo = defaultdict(set)
        for (v1, v2) in self.restricciones:
            grafo[v1].add(v2)
            grafo[v2].add(v1)
        return grafo


def encontrar_corte(grafo):
    """
    Encuentra un conjunto de corte mínimo (aproximado).
    Implementación simplificada usando eliminación de nodos de alto grado.
    """
    grafo = {k: set(v) for k, v in grafo.items()}
    corte = set()

    while True:
        if not grafo:
            break

        # Seleccionar nodo con mayor grado
        nodo = max(grafo.keys(), key=lambda x: len(grafo[x]))
        corte.add(nodo)

        # Eliminar nodo del grafo
        for vecino in grafo[nodo]:
            grafo[vecino].remove(nodo)
        del grafo[nodo]

    return corte


def cutset_conditioning(csp):
    """
    Algoritmo principal de Acondicionamiento del Corte.
    """
    # 1. Encontrar conjunto de corte
    corte = encontrar_corte(csp.grafo)
    variables_arbol = [v for v in csp.variables if v not in corte]

    # 2. Generar todas las posibles asignaciones para el corte
    asignaciones_corte = itertools.product(
        *[csp.dominios[v] for v in corte]
    )

    # 3. Para cada asignación del corte, resolver el subproblema en árbol
    for asignacion_corte in asignaciones_corte:
        asignacion_actual = dict(zip(corte, asignacion_corte))

        # Verificar consistencia de la asignación del corte
        if not all(
                csp.restricciones.get((v1, v2), lambda x, y: True)(asignacion_actual.get(v1), asignacion_actual.get(v2))
                for v1 in corte for v2 in corte if (v1, v2) in csp.restricciones
        ):
            continue

        # Resolver el subproblema en árbol (backtracking simple)
        resultado = backtracking_arbol(csp, variables_arbol, asignacion_actual)
        if resultado is not None:
            return resultado

    return None


def backtracking_arbol(csp, variables, asignacion):
    """
    Backtracking para componentes en forma de árbol.
    """
    if len(asignacion) == len(csp.variables):
        return asignacion

    var = next(v for v in variables if v not in asignacion)

    for valor in csp.dominios[var]:
        nueva_asignacion = asignacion.copy()
        nueva_asignacion[var] = valor

        # Verificar consistencia solo con variables ya asignadas
        consistente = True
        for (v1, v2), restriccion in csp.restricciones.items():
            if v1 in nueva_asignacion and v2 in nueva_asignacion:
                if not restriccion(nueva_asignacion[v1], nueva_asignacion[v2]):
                    consistente = False
                    break

        if consistente:
            resultado = backtracking_arbol(csp, variables, nueva_asignacion)
            if resultado is not None:
                return resultado

    return None


# Ejemplo: Problema de colorear un grafo en forma de "reloj"
variables = ['A', 'B', 'C', 'D', 'E', 'F']
dominios = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}
restricciones = {
    ('A', 'B'): lambda a, b: a != b,
    ('B', 'C'): lambda a, b: a != b,
    ('C', 'D'): lambda a, b: a != b,
    ('D', 'E'): lambda a, b: a != b,
    ('E', 'F'): lambda a, b: a != b,
    ('F', 'A'): lambda a, b: a != b,
    ('A', 'D'): lambda a, b: a != b  # Este arco crea un ciclo
}

# Resolver
problema = CSP(variables, dominios, restricciones)
solucion = cutset_conditioning(problema)

print("Solución encontrada:")
for variable, valor in solucion.items():
    print(f"{variable}: {valor}")