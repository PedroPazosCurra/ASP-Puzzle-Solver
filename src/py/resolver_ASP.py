# Imports
import sys
import clingo
from os import path

# Constantes
reglas_einstein = path.abspath(path.join(path.dirname(__file__), "..", "../resources/asp/asp_einstein.lp"))

# Función a exportar: resolver_ASP
#
#   Dada la salida de NL_to_ASP, que devuelve un conjunto de declaraciones, devuelve un Answer Set con la solución
def resolver_ASP(modelo, puzzle, clingo_args = ["--warn=none"]):

    cc = clingo.Control(clingo_args)

    # Se carga el programa ASP según el puzzle elegido
    match puzzle:
        case "Einstein":
            cc.load(reglas_einstein)
        case _:
            return([1, "En resolver_ASP.py, se recibe un puzzle que no existe. Vigila que se pase bien."])

    # Se añade el modelo recibido de LLM al código ASP + se hace grounding
    try:
        cc.add('base', [], modelo)
        cc.ground([("base",[])])

    except:
        return([1, "Ha habido un problema en el proceso de grounding ASP"])

    # Se devuelve el set si el programa es SAT y un error si no.

    solve_handle = cc.solve(yield_= True)

    # En caso de que haya modelos, se toma el primero, preprocesado de answer set para separar los predicados por puntos y return.
    for model in solve_handle:

        answer_sets = str(model).replace(" ", ". ") + "."
        return([0, answer_sets])

    return([1, "El programa que he inferido en base a tu mensaje no es resoluble. Asegúrate de escribir todas las variables del sistema, aunque no estén relacionadas con ningún elemento."])