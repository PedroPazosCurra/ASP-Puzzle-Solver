# En este documento se lleva a cabo la tarea central de procesar el mensaje en lenguaje natural recibido del front-end

# Imports
import sys
import requests
import json
from os import path
import re
import clingo
from NL_to_ASP import NL_to_ASP
# from ASP_to_NL import ASP_to_NL
from resolver_ASP import resolver_ASP

def comprueba_error(array_salida):

    # Si falla, no pasa a la siguiente fase y devuelve el mensaje de error al front-end
    if(array_salida[0] == 1):

        return(array_salida[1])

    else:
        return array_salida[1]


# Prompt y puzzle recibidos por argumento
prompt_usuario = sys.argv[1]
puzzle_elegido = sys.argv[2]

# Pasa el NL a ASP
modelo_asp = comprueba_error(NL_to_ASP(prompt_usuario, puzzle_elegido))

# Pasa el ASP a Answer Set (resuelve ASP)
#answer_set = comprueba_error(resolver_ASP(modelo_asp, puzzle_elegido))

# Pasa Answer Set a NL
# ASP_to_NL(...)

# Devuelve al front-end
print(modelo_asp)
