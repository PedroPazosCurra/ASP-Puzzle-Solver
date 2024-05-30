#  Imports 
import importlib
import importlib.util
spec = importlib.util.spec_from_file_location('src', 'src/py/resolver_ASP.py')
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)

resolver_ASP = getattr(modulo, 'resolver_ASP')

#  Variables
modelo_sat = "type(house,V) :- house(V). type(color,V) :- color(V). house(1). color(red). person(brittish). has(brittish, color, red). has(brittish, house, 1). image(dog, ruta_dog)."
modelo_unsat = "type(house, V) :- house(V). house(1..3). person(a). type(pet, V) :- pet(V). pet(dog; cat)."
modelo_invalido = ":-"
puzzle_valido = "Einstein"
puzzle_invalido = 'Puzzle_inventado'


# --------------------------------- Funciones de test ----------------------------------------


# Comprueba que devuelve estado de error y msg de error al recibir nulos en la entrada
def test_entradas_nulas():

    salida = resolver_ASP(None, None)
    assert (salida[0] == 1)
    assert (salida[1] == "resolver_ASP recibe una entrada con uno de los valores nulos.")
    assert (salida[2] == [])

    salida2 = resolver_ASP(None, puzzle_valido)
    assert (salida2[0] == 1)
    assert (salida2[1] == "resolver_ASP recibe una entrada con uno de los valores nulos.")
    assert (salida2[2] == [])

    salida3 = resolver_ASP('Hola que tal', None)
    assert (salida3[0] == 1)
    assert (salida3[1] == "resolver_ASP recibe una entrada con uno de los valores nulos.")
    assert (salida3[2] == [])
# Error si el puzzle dado no existe.
def test_puzzle_inexistente():
    assert (resolver_ASP(modelo_sat, puzzle_invalido) == [1, "En resolver_ASP.py, se recibe un puzzle que no existe. Vigila que se pase bien.", []])

# Insatisfacibilidad si se pasa un modelo lógico UNSAT
def test_modelo_unsat():
    assert (resolver_ASP(modelo_unsat, puzzle_valido) == [1, "El programa que he inferido en base a tu mensaje no es resoluble. Asegúrate de escribir todas las variables del sistema, aunque no estén relacionadas con ningún elemento.", []])

# Error en grounding si se pasa modelo con mala sintaxis 
def test_modelo_invalido():
    assert( resolver_ASP(modelo_invalido, puzzle_valido) == [1, "Ha habido un problema en el proceso de grounding ASP", []])

# Solución en caso de modelo resoluble y puzzle correcto
def test_modelo_sat():
    
    status, model, args_salida = resolver_ASP(modelo_sat, puzzle_valido)
    has_array, imagenes_array = args_salida

    # Status OK
    assert (status == 0)

    # Modelo no nulo
    assert (model != None and model != "")

    # Has array no vacío (imagenes_array sí puede serlo)
    assert(len(has_array) > 0)