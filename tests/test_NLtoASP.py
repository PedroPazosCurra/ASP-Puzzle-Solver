import importlib
import importlib.util
spec = importlib.util.spec_from_file_location('src', 'src/py/NL_to_ASP.py')
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)

NL_to_ASP = getattr(modulo, 'NL_to_ASP')

# Comprueba que devuelve estado de error y msg de error al recibir nulos en la entrada
def test_entradas_nulas():

    salida = NL_to_ASP(None, None)
    assert (salida[0] == 1)
    assert (salida[1] == "NL_to_ASP recibe una entrada con uno de los valores nulos.")

    salida2 = NL_to_ASP(None, 'Einstein')
    assert (salida2[0] == 1)
    assert (salida2[1] == "NL_to_ASP recibe una entrada con uno de los valores nulos.")

    salida3 = NL_to_ASP('Hola que tal', None)
    assert (salida3[0] == 1)
    assert (salida3[1] == "NL_to_ASP recibe una entrada con uno de los valores nulos.")

# Comprueba fallo si el puzzle dado no existe.
def test_puzzle_inexistente():
    assert (NL_to_ASP('hola que tal', 'Puzzle_inventado') == [1, "En NL_to_ASP.py, se recibe un puzzle que no existe: Puzzle_inventado. Vigila que se pase bien."])
