from einstein_grafico import einstein_grafico
from comensales_grafico import comensales_grafico

# Función pequeña encargada de segregar el programa para generar imágenes según el puzzle, abstrayendo a proceso.py de esta labor. 
def modulo_grafico(args : list, puzzle : str):

    match puzzle:
        case "Einstein": return einstein_grafico(args)
        case "Comensales": return comensales_grafico(args)
        case _: return [1, f"El módulo gráfico recibe un puzzle que no existe: {puzzle}."]