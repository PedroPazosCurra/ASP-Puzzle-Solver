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
import time
from NL_to_ASP import NL_to_ASP
from AS_to_NL import AS_to_NL
from resolver_ASP import resolver_ASP
from einstein_grafico import einstein_grafico


# Variables
now = time.localtime()
hora_string = "[" + str(now.tm_hour) + ":" + str(now.tm_min) + "]"
log_header = "############ " + hora_string + " LOG ############:\n"
modelo_asp = ""
answer_set = ""
nl_salida = ""
predicados_has = []
rutas_imagenes = []
estado = 0
num_args = len(args)
prompt_usuario = "There are three houses. There are a spanish, an english and a chinese."
puzzle_elegido = "Einstein"
log = open(path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/log.txt")), "a")

# Prompt y puzzle recibidos por argumento (adaptado para debug directo sin pasar por frontend)
if (num_args >= 3): _, prompt_usuario, puzzle_elegido = args

# Vacía la carpeta de salidas temporales del módulo de imagen usadas previamente
carpeta_tmp = glob('..../resources/tmp')
for imagen in carpeta_tmp: remove(imagen)

# PROCESO: 1 -> 2 -> 3. Si falla, no pasa a la siguiente fase y devuelve el mensaje de error al front-end.
#
#       1 - NL_to_ASP(prompt, puzzle) ->    [estado, msg] 
#       2 - resolver_ASP(modelo, puzzle) -> [estado, msg]
#       3 - ASP_to_NL(answerset, puzzle) -> [estado, msg]
#

log.write(log_header)

# 1º - Pasa el mensaje del usuario a declaraciones ASP.
estado, modelo_asp = NL_to_ASP(prompt_usuario, puzzle_elegido)

## Fallo en LLM
if (estado != 0):
    print("1|" + modelo_asp)
    log.write("# Modelo ASP sacado: \n\f" + modelo_asp)
    log.close
    exit(0)


# 2º - Pasa el ASP al solver para obtener el Answer Set solución.
estado, answer_set, predicados_has, rutas_imagenes = resolver_ASP(modelo_asp, puzzle_elegido)

##   Fallo en ASP
if(estado != 0):
    print("1|# Modelo ASP sacado:" + modelo_asp + "\n# Answer set resuelto: \n\t" + answer_set, flush=True)
    log.write("# Modelo ASP sacado: \n" + modelo_asp + "\n# Answer set resuelto: \n" + answer_set)
    log.close
    exit(0)


# 3º - Pasa el Answer Set a Lenguaje Natural y lo devuelve.
estado, nl_salida = AS_to_NL(answer_set, puzzle_elegido)

##   Fallo en LLM
if(estado != 0):
    print("1|# Modelo ASP sacado: " + modelo_asp + "\n# Answer set resuelto: " + answer_set + "# Explicación LN: " + nl_salida, flush=True)
    log.write("# Modelo ASP sacado: " + modelo_asp + "\n# Answer set resuelto: " + answer_set + "# Explicación LN: " + nl_salida)
    log.close
    exit(0)


# Caso optimista: Todo OK
einstein_grafico(predicados_has, rutas_imagenes)
log.write("# Modelo ASP sacado: " + modelo_asp + "\n# Answer set resuelto: " + answer_set + "# Explicación LN: " + nl_salida)
log.close
print("0|" + nl_salida, flush= True)
