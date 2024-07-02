# Imports
import clingo
from os import path

# Variables y Constantes
DEBUG = False

reglas_einstein = path.abspath(path.join(path.dirname(__file__), "..", "../resources/asp/einstein.lp"))
reglas_comensales = path.abspath(path.join(path.dirname(__file__), "..", "../resources/asp/comensales.lp"))


###########################################   Funciones   ##########################################


# Función auxiliar para procesar los argumentos de los átomos
def procesa_argumentos_atomo(atom_args):

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
#   Nota: En la lista de argumentos podríamos añadir "--models=0" para enumerar todos los modelos encontrados, pero sirve con el primero que encuentre (+ rendimiento)
def resolver_ASP(modelo : str = None, puzzle : str = None, clingo_args : list = ["--warn=none"]):

    answer_sets = ""    # has(brittish,house,1). has(brittish,pet,dog).
    has_atoms = []      # [['norwegian', 'beverage', 'coffee'], ['english', 'house', '1']]
    seated_atoms = []
    speaks_atoms = []
    representation_atoms = []

    # Sale con error si alguno de los args es nulo
    if ((modelo == None) or (puzzle == None)): return([1, "resolver_ASP recibe una entrada con uno de los valores nulos.", []])

    cc = clingo.Control(clingo_args)
    answer_sets = ""

    # Se carga el programa ASP según el puzzle elegido
    match puzzle:
        case "Einstein":
            cc.load(reglas_einstein)
        case "Comensales":
            cc.load(reglas_comensales)
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
    for modelo in solve_handle:
        answer_sets = (str(modelo).replace(" ", ". ") + ".")
        for atomo in modelo.symbols(atoms=True):

            # Átomos de representación
            if(atomo.name == "show_graphic" or atomo.name == "show_description"):
                representation_atoms.append(atomo.name)

            match puzzle:

                case "Einstein":

                    # has(X, Y, Z)
                    if(atomo.name == "has" and len(atomo.arguments) == 3):
                        has_arg_1, has_arg_2, has_arg_3 = procesa_argumentos_atomo(atomo.arguments)  
                        has_atoms.append([has_arg_1, has_arg_2, has_arg_3])

                case "Comensales":

                    # seated(X, Y)
                    if(atomo.name == "seated" and len(atomo.arguments) == 2):
                        seated_arg_1, seated_arg_2 = procesa_argumentos_atomo(atomo.arguments)
                        seated_atoms.append([seated_arg_1, seated_arg_2])

                    # speaks(X, Y)
                    elif(atomo.name == "speaks" and len(atomo.arguments) == 2):
                        speaks_arg_1, speaks_arg_2 = procesa_argumentos_atomo(atomo.arguments)
                        speaks_atoms.append([speaks_arg_1, speaks_arg_2])

                case _:
                    return([1, "En resolver_ASP.py, se recibe un puzzle que no existe. Vigila que se pase bien.", []])
        
        # Si no se indica representación, se representa de ambas formas
        if representation_atoms == []:
            representation_atoms = ["show_graphic", "show_description"]

    # ¿Tiene solución?
    if (len(answer_sets) >= 1):
        match puzzle:
            case "Einstein":
                return([0, answer_sets, [representation_atoms, has_atoms]])
            case "Comensales":
                return([0, answer_sets, [representation_atoms, seated_atoms, speaks_atoms]])
            case _:
                return([1, "En resolver_ASP.py, se recibe un puzzle que no existe. Vigila que se pase bien.", []])

    else:
        return([1, "El programa que he inferido en base a tu mensaje no es resoluble. Asegúrate de escribir todas las variables del sistema, aunque no estén relacionadas con ningún elemento.", []])

# Debug:
if (DEBUG):
    modelo_sat = "living_place(house, V) :- house(V). type(color,V) :- color(V). house(1). color(red). person(brittish). same_place(brittish, red). same_place(brittish, 1). show_graphic."
    modelo_unsat = "type(house, V) :- house(V). house(1..3). person(a). type(pet, V) :- pet(V). pet(dog; cat)."
    modelo_invalido = ":-"
    status, ans_sets, args = resolver_ASP(modelo_sat, "Einstein")

    print(status, ans_sets, args)