# Imports
import sys
import clingo
from os import path

# Constantes
reglas_einstein = path.abspath(path.join(path.dirname(__file__), "..", "../resources/asp/asp_einstein.lp"))

# Función a exportar: resolver_ASP
#
#   Dada la salida de NL_to_ASP, que devuelve un conjunto de declaraciones, devuelve un Answer Set con la solución
def resolver_ASP(modelo, puzzle, clingo_args = []):

    cc = clingo.Control(clingo_args)

    match puzzle:
        case "Einstein":
            cc.load(reglas_einstein)
        case _:
            return([1, "En resolver_ASP.py, se recibe un puzzle que no existe. Vigila que se esté pasando bien."])
        
    cc.load(reglas_einstein)

    try:
        cc.add('base', [], modelo)
        cc.ground([("base",[])])
    except:
        return([1, "Ha habido un problema en el grounding"])

    def onmodel(modelo):
        return([0, modelo])
    
    def on_unsat():
        return([1, "El programa lógico que he inferido en base a tu explicación no tiene solución."])

    cc.solve(on_model=onmodel, on_unsat=on_unsat)

    return([1, "cc.solve no pasa por alguna razón"])