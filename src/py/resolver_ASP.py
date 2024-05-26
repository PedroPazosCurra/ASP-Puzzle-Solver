# Imports
import sys
import clingo
from os import path

# Variables y Constantes
answer_sets = ""    # has(brittish,house,1). has(brittish,pet,dog).
has_atoms = []      # [['norwegian', 'beverage', 'coffee'], ['english', 'house', '1']]
image_routes = []   # [['coffee', 'ruta/coffee.png']]
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

    # En caso de que haya modelos, se recogen los átomos en listas.
    for model in solve_handle:
        answer_sets = (str(model).replace(" ", ". ") + ".")
        for atom in model.symbols(atoms=True):
            if(atom.name == "has" and len(atom.arguments) == 3):
                has_atoms.append([atom.arguments[0].name, atom.arguments[1].name, atom.arguments[2]])
            elif(atom.name == "image" and len(atom.arguments) == 2):
                image_routes.append([atom.arguments[0].name, atom.arguments[1]])

    # ¿Tiene solución?
    if (len(answer_sets) >= 1):
        return([0, answer_sets, has_atoms, image_routes])
    else:
        return([1, "El programa que he inferido en base a tu mensaje no es resoluble. Asegúrate de escribir todas las variables del sistema, aunque no estén relacionadas con ningún elemento."])

# Debug:

#status, ans_sets, has, imageroutes = (resolver_ASP("has(brittish, color, red). has(brittish, house, 1). image(dog, ruta_dog).", "Einstein"))
#print(f"Answer sets:\t{ans_sets}\nHas:\t{has}\nRutas:\t{image_routes}")