import importlib
import importlib.util
spec = importlib.util.spec_from_file_location('src', 'src/py/AS_to_NL.py')
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)

AS_to_NL = getattr(modulo, 'AS_to_NL')

# Comprueba que devuelve estado de error y msg de error al recibir nulos en la entrada
def test_entradas_nulas():

    salida = AS_to_NL(None, None)
    assert (salida[0] == 1)
    assert (salida[1] == "AS_to_NL recibe una entrada con uno de los valores nulos.")

    salida2 = AS_to_NL(None, 'Einstein')
    assert (salida2[0] == 1)
    assert (salida2[1] == "AS_to_NL recibe una entrada con uno de los valores nulos.")

    salida3 = AS_to_NL('Hola que tal', None)
    assert (salida3[0] == 1)
    assert (salida3[1] == "AS_to_NL recibe una entrada con uno de los valores nulos.")

# Comprueba fallo si el puzzle dado no existe.
def test_puzzle_inexistente():
    assert (AS_to_NL('hola que tal', 'Puzzle_inventado') == [1, "En AS_to_NL.py, se recibe un puzzle que no existe: Puzzle_inventado. Vigila que se pase bien."])