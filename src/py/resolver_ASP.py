# Imports
import sys
import clingo
from os import path

# Variables y Constantes
DEBUG = False

answer_sets = ""    # has(brittish,house,1). has(brittish,pet,dog).
has_atoms = []      # [['norwegian', 'beverage', 'coffee'], ['english', 'house', '1']]
image_routes = []   # [['coffee', 'ruta/coffee.png']]
reglas_einstein = path.abspath(path.join(path.dirname(__file__), "..", "../resources/asp/asp_einstein.lp"))



###########################################   Funciones   ##########################################


# Función auxiliar para procesar los argumentos de los átomos
def procesa_atom_arguments(atom_args):

    lista_args = []
    arg_listo = ""

    # Procesa los argumentos según su tipo
    for atom_arg in atom_args:
        match atom_arg.type:
            case clingo.SymbolType.Function:    arg_listo = atom_arg.name
            case clingo.SymbolType.Number:      arg_listo = atom_arg.number  
            case clingo.SymbolType.String:      arg_listo = atom_arg.string
            case _:                             arg_listo = atom_arg

        lista_args.append(arg_listo)
    
    return lista_args


# Función a exportar: resolver_ASP
#
#   Dada la salida de NL_to_ASP, que devuelve un conjunto de declaraciones, devuelve un estado, Answer Set y argumentos posteriores
def resolver_ASP(modelo : str = None, puzzle : str = None, clingo_args : list = ["--warn=none"]):

    answer_sets = ""
    has_atoms = []
    image_routes = []

    # Sale con error si alguno de los args es nulo
    if ((modelo == None) or (puzzle == None)): return([1, "resolver_ASP recibe una entrada con uno de los valores nulos.", []])

    cc = clingo.Control(clingo_args)
    answer_sets = ""

    # Se carga el programa ASP según el puzzle elegido
    match puzzle:
        case "Einstein":
            cc.load(reglas_einstein)
        case _:
            return([1, "En resolver_ASP.py, se recibe un puzzle que no existe. Vigila que se pase bien.", []])

    # Se añade el modelo recibido de LLM al código ASP + se hace grounding
    try:
        cc.add('base', [], modelo)
        cc.ground([('base',[])])

    except:
        return([1, "Ha habido un problema en el proceso de grounding ASP", []])

    # Se devuelve el set si el programa es SAT y un error si no.

    try:
        solve_handle = cc.solve(yield_= True)
    except:
        return([1, "Ha habido un problema en el proceso de solving ASP", []])


    # En caso de que haya modelos, se recogen los átomos en listas.
    for model in solve_handle:
        answer_sets = (str(model).replace(" ", ". ") + ".")
        for atom in model.symbols(atoms=True):

            match puzzle:
                case "Einstein":
                    if(atom.name == "has" and len(atom.arguments) == 3):
                        # Toma los 3 argumentos del has(X,Y,Z)
                        has_arg_1, has_arg_2, has_arg_3 = procesa_atom_arguments(atom.arguments)  
                        has_atoms.append([has_arg_1, has_arg_2, has_arg_3])

                    elif(atom.name == "image" and len(atom.arguments) == 2):

                        # Toma 2 args del image(X,Y)
                        img_arg_1, img_arg_2 = procesa_atom_arguments(atom.arguments)
                        image_routes.append([img_arg_1, img_arg_2])
                case _:
                    return([1, "En resolver_ASP.py, se recibe un puzzle que no existe. Vigila que se pase bien.", []])

    # ¿Tiene solución?
    if (len(answer_sets) >= 1):
        return([0, answer_sets, [has_atoms, image_routes]])
    else:
        return([1, "El programa que he inferido en base a tu mensaje no es resoluble. Asegúrate de escribir todas las variables del sistema, aunque no estén relacionadas con ningún elemento.", []])

# Debug:
if (DEBUG):
    modelo_sat = "type(house,V) :- house(V). type(color,V) :- color(V). house(1). color(red). person(brittish). has(brittish, color, red). has(brittish, house, 1). image(dog, ruta_dog)."
    #modelo_unsat = "type(house, V) :- house(V). house(1..3). person(a). type(pet, V) :- pet(V). pet(dog; cat)."
    #modelo_invalido = ":-"
    status, ans_sets, [has, imageroutes] = resolver_ASP(modelo_sat, "Einstein")
    print(f"Answer sets:\t{ans_sets}\nHas:\t{has}\nRutas:\t{image_routes}")