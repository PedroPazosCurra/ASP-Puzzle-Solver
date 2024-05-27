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

# Constantes
AHORA = time.localtime()
HORA_STRING = f"[{str(AHORA.tm_hour)}:{str(AHORA.tm_min)}]"
LOG_HEADER = f"\n############ {HORA_STRING} LOG ############:\n"
USAR_LLM_PURO = False
DEBUG = True

# Variables
modelo_asp = ""
answer_set = ""
nl_salida = ""
predicados_has = []
rutas_imagenes = []
estado = 0
num_args = len(args)
log = open(path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/log.txt")), "a")

# Debug
prompt_usuario = "There are three houses. There are a spanish, an english and a chinese. There are three drinks: tea, milk and soda. The spanish man drinks soda. Represent soda with the image 'cocacola'. There's a dog, a cat and a horse. The spanish keeps the cat, while the english man has a dog. The horse is represented by the image called horse."
puzzle_elegido = "Einstein"



# Prompt y puzzle recibidos por argumento (adaptado para debug directo sin pasar por frontend)
if (num_args >= 3): _, prompt_usuario, puzzle_elegido = args

# Vacía la carpeta de salidas temporales del módulo de imagen usadas previamente
for imagen in glob('..../resources/tmp'): remove(imagen)

# PROCESO: 1 -> 2 -> 3. Si falla, no pasa a la siguiente fase y devuelve el mensaje de error al front-end.
#
#       1 - NL_to_ASP(prompt, puzzle) ->    [estado, msg] 
#       2 - resolver_ASP(modelo, puzzle) -> [estado, msg]
#       3 - ASP_to_NL(answerset, puzzle) -> [estado, msg]
#

# Start
log.write(LOG_HEADER)
tiempo_comienzo_total = time.perf_counter()
tiempo_comienzo_nl_to_asp = time.perf_counter()


# 1º - Pasa el mensaje del usuario a declaraciones ASP.
estado, modelo_asp = NL_to_ASP(prompt_usuario, puzzle_elegido)

tiempo_nl_to_asp = time.perf_counter() - tiempo_comienzo_nl_to_asp
tiempo_comienzo_resolver_asp = time.perf_counter()

## Fallo en NL_to_ASP (1)
if (estado != 0):
    print("1|" + modelo_asp)
    log.write("# Modelo ASP sacado: \n\f" + modelo_asp)
    log.close
    exit(0)

# Si modo LLM Puro, se sale ya.
if(USAR_LLM_PURO):
    print("0|" + modelo_asp)

# 2º - Pasa el ASP al solver para obtener el Answer Set solución.
estado, answer_set, predicados_has, rutas_imagenes = resolver_ASP(modelo_asp, puzzle_elegido)

tiempo_resolver_asp = time.perf_counter() - tiempo_comienzo_resolver_asp
tiempo_comienzo_as_to_nl = time.perf_counter()

##   Fallo en resolver_ASP (2)
if(estado != 0):
    print("1|# Modelo ASP sacado:" + modelo_asp + "\n# Answer set resuelto: \n\t" + answer_set, flush=True)
    log.write("# Modelo ASP sacado: \n" + modelo_asp + "\n# Answer set resuelto: \n" + answer_set)
    log.close
    exit(0)


# 3º - Pasa el Answer Set a Lenguaje Natural y lo devuelve.
estado, nl_salida = AS_to_NL(answer_set, puzzle_elegido)

tiempo_as_to_nl = time.perf_counter() - tiempo_comienzo_as_to_nl
tiempo_comienzo_modulo_grafico = time.perf_counter()

##   Fallo en LLM
if(estado != 0):
    print("1|# Modelo ASP sacado: " + modelo_asp + "\n# Answer set resuelto: " + answer_set + "# Explicación LN: " + nl_salida, flush=True)
    log.write("# Modelo ASP sacado: " + modelo_asp + "\n# Answer set resuelto: " + answer_set + "# Explicación LN: " + nl_salida)
    log.close
    exit(0)


# Caso optimista: Todo OK
if(puzzle_elegido == "Einstein"):
    einstein_grafico(predicados_has, rutas_imagenes)

tiempo_grafico = time.perf_counter() - tiempo_comienzo_modulo_grafico
tiempo_total = time.perf_counter() - tiempo_comienzo_total

# Logs, debugs, etc.    
log.write("# Modelo ASP sacado: " + modelo_asp + "\n# Answer set resuelto: " + answer_set + "# Explicación LN: " + nl_salida)
log.close

if(DEBUG):

    # Salida
    print("0|" + nl_salida, flush= True)

    # Tiempo
    print(f"########### TIEMPO TOTAL ###########:{tiempo_total}:\n\tNL_to_ASP:\t{tiempo_nl_to_asp}\n\tresolver_ASP:\t{tiempo_resolver_asp}\n\tAS_to_NL:\t{tiempo_as_to_nl}\n\tMódulo gráfico:\t{tiempo_grafico}")

