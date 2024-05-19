# proceso.py
#
# Descripción:  En este documento se lleva a cabo la tarea central de procesar el
#                mensaje en lenguaje natural recibido del front-end
#
# -*- coding: utf-8 -*-

# Imports
from sys import argv as args
from os import path, remove
from glob import glob
import re
import clingo
from NL_to_ASP import NL_to_ASP
from AS_to_NL import AS_to_NL
from resolver_ASP import resolver_ASP
from einstein_grafico import einstein_grafico

# Variables
modelo_asp = ""
answer_set = ""
nl_salida = ""
estado = 0
num_args = len(args)
prompt_usuario = "There are three houses. In them live a spanish, an english and a chinese."
puzzle_elegido = "Einstein"

# Prompt y puzzle recibidos por argumento (adaptado para debug directo sin pasar por frontend)
if (num_args >= 3): _, prompt_usuario, puzzle_elegido = args



# Vacía la carpeta de salidas temporales del módulo de imagen usadas previamente
carpeta_tmp = glob('..../resources/tmp/*')
for imagen in carpeta_tmp: remove(imagen)

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
    print("1|" + modelo_asp)
    exit(0)


# 2º - Pasa el ASP al solver para obtener el Answer Set solución.
[estado, answer_set] = resolver_ASP(modelo_asp, puzzle_elegido)

##   Fallo en ASP
if(estado != 0):
    print("1|modelo ASP sacado: \n\f" + modelo_asp + "\n Answer set resuelto: \n\f" + answer_set, flush=True)
    exit(0)


# 3º - Pasa el Answer Set a Lenguaje Natural y lo devuelve.
[estado, nl_salida] = AS_to_NL(answer_set, puzzle_elegido)

##   Fallo en LLM
if(estado != 0):
    print("1|modelo ASP sacado: \n\f" + modelo_asp + "\n Answer set resuelto: \n\f" + answer_set + "Explicación LN: \n\f" + nl_salida, flush=True)
    exit(0)


# Caso optimista: Todo OK
einstein_grafico(answer_set)
print("0|modelo ASP sacado: \n\f" + modelo_asp + "\n Answer set resuelto: \n\f" + answer_set + "Explicación LN: \n\f" + nl_salida, flush= True)
