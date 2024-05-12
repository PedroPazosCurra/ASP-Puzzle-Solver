# proceso.py
#
# Descripción:  En este documento se lleva a cabo la tarea central de procesar el
#                mensaje en lenguaje natural recibido del front-end
#
# -*- coding: utf-8 -*-

# Imports
import sys
import requests
import json
from os import path
import re
import clingo
from NL_to_ASP import NL_to_ASP
from AS_to_NL import AS_to_NL
from resolver_ASP import resolver_ASP

# Variables
modelo_asp = ""
answer_set = ""
nl_salida = ""
estado = 0

# Prompt y puzzle recibidos por argumento
prompt_usuario = sys.argv[1]
puzzle_elegido = sys.argv[2]

# PROCESO: 1 -> 2 -> 3. Si falla, no pasa a la siguiente fase y devuelve el mensaje de error al front-end.
#
#       1 - NL_to_ASP(prompt, puzzle) ->    [estado, msg] 
#       2 - resolver_ASP(modelo, puzzle) -> [estado, msg]
#       3 - ASP_to_NL(answerset, puzzle) -> [estado, msg]
#

# 1º - Pasa el mensaje del usuario a declaraciones ASP.
[estado, modelo_asp] = NL_to_ASP(prompt_usuario, puzzle_elegido)

## Fallo en LLM
if (estado != 0):
    print(modelo_asp)
    exit(0)


# 2º - Pasa el ASP al solver para obtener el Answer Set solución.
[estado, answer_set] = resolver_ASP(modelo_asp, puzzle_elegido)

##   Fallo en ASP
if(estado != 0):
    print("modelo ASP sacado: \n\f" + modelo_asp + "\n Answer set resuelto: \n\f" + answer_set)
    exit(0)


# 3º - Pasa el Answer Set a Lenguaje Natural y lo devuelve.
[estado, nl_salida] = AS_to_NL(answer_set, puzzle_elegido)

##   Fallo en LLM
if(estado != 0):
    print("modelo ASP sacado: \n\f" + modelo_asp + "\n Answer set resuelto: \n\f" + answer_set + "Explicación LN: \n\f" + nl_salida)
    exit(0)


# Caso optimista: Todo OK
print("modelo ASP sacado: \n\f" + modelo_asp + "\n Answer set resuelto: \n\f" + answer_set + "Explicación LN: \n\f" + nl_salida)
