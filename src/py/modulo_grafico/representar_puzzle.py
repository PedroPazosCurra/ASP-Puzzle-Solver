from modulo_grafico.einstein_grafico import einstein
from modulo_grafico.comensales_grafico import comensales

# Función pequeña encargada de segregar el programa para generar imágenes según el puzzle, abstrayendo a proceso.py de esta labor. 
def representar(args : list, puzzle : str):

    match puzzle:
        case "Einstein": return einstein(args)
        case "Comensales": return comensales(args)
        case _: return [1, f"El módulo gráfico recibe un puzzle que no existe: {puzzle}."]