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
from matplotlib import pyplot as plt
from NL_to_ASP import NL_to_ASP
from AS_to_NL import AS_to_NL
from resolver_ASP import resolver_ASP
from einstein_grafico import einstein_grafico
from tiempos_plot import tiempos_plot


# Constantes
AHORA = time.localtime()
HORA_STRING = f"[{str(AHORA.tm_hour)}:{str(AHORA.tm_min)}]"
LOG_HEADER = f"\n############ {HORA_STRING} LOG ############:\n"

# Flags
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
prompt_usuario = "There are three houses. There are a spanish, an english and a chinese. There are three drinks: tea, milk and soda. The spanish man drinks soda. Represent soda with the image \"cocacola\". There's a dog, a cat and a horse. The spanish keeps the cat, while the english man has a dog. The horse is represented by the image called \"horse\". The cat is represented by \"https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg\" The spanish man has a red house. The chinese man, on the other hand, lives in a purple house."
puzzle_elegido = "Einstein"
salida = "# "
array_tiempos = []

# Funcion auxiliar imprimir_salida()
def imprimir_salida(estado, msg, tiempos : list):

    print(f"{str(estado)}|{msg}", flush= True)
    log.write(msg)
    log.close

    tiempos_plot(tiempos)

    exit(0)

# Prompt y puzzle recibidos por argumento (adaptado para debug directo sin pasar por frontend)
if (num_args >= 3): _, prompt_usuario, puzzle_elegido = args

######### PROCESO: 1 -> 2 -> 3. Si falla, no pasa a la siguiente fase y devuelve el mensaje de error al front-end (vía stdout). ###########
#
#       1 - NL_to_ASP(prompt, puzzle) ->    [estado, msg] 
#       2 - resolver_ASP(modelo, puzzle) -> [estado, modelo, array_has, array_rutas_img]
#       3 - ASP_to_NL(answerset, puzzle) -> [estado, msg]
#

# Start
log.write(LOG_HEADER)
tiempo_comienzo_total = time.perf_counter()


####  1º - Pasa el mensaje del usuario a declaraciones ASP. ####
tiempo_comienzo_nl_to_asp = time.perf_counter()

estado, modelo_asp = NL_to_ASP(prompt_usuario, puzzle_elegido)

tiempo_nl_to_asp = time.perf_counter() - tiempo_comienzo_nl_to_asp
array_tiempos.append(tiempo_nl_to_asp)

salida += f"Modelo ASP sacado: \n\t{modelo_asp}\n"

## Fallo en NL_to_ASP (1)
if (estado != 0): imprimir_salida(estado, salida, array_tiempos)

# Si modo LLM Puro, se sale ya.
if (USAR_LLM_PURO): imprimir_salida(estado, salida, array_tiempos)


####  2º - Pasa el ASP al solver para obtener el Answer Set solución. ####
tiempo_comienzo_resolver_asp = time.perf_counter()

estado, answer_set, predicados_has, rutas_imagenes = resolver_ASP(modelo_asp, puzzle_elegido)

tiempo_resolver_asp = time.perf_counter() - tiempo_comienzo_resolver_asp
array_tiempos.append(tiempo_resolver_asp)

salida += f"# Answer set resuelto: \n\t{answer_set}\n"

##   Fallo en resolver_ASP (2)
if(estado != 0): imprimir_salida(estado, salida, array_tiempos)


####  3º - Pasa el Answer Set a Lenguaje Natural y lo devuelve. ####
tiempo_comienzo_as_to_nl = time.perf_counter()


estado, nl_salida = AS_to_NL(answer_set, puzzle_elegido)

tiempo_as_to_nl = time.perf_counter() - tiempo_comienzo_as_to_nl
array_tiempos.append(tiempo_as_to_nl)

salida += f"# Explicación LN: {nl_salida}\n"

##   Fallo en AS_to_NL (3)
if(estado != 0): imprimir_salida(estado, salida, array_tiempos)


####  4º Caso optimista: Todo OK - Representación gráfica ####
tiempo_comienzo_modulo_grafico = time.perf_counter()

if(puzzle_elegido == "Einstein"):
    estado, msg_grafico = einstein_grafico(predicados_has, rutas_imagenes)

tiempo_grafico = time.perf_counter() - tiempo_comienzo_modulo_grafico
array_tiempos.append(tiempo_grafico)

salida += f"# Módulo gráfico: {msg_grafico}\n"

tiempo_total = time.perf_counter() - tiempo_comienzo_total

imprimir_salida(estado, salida, array_tiempos)

if(DEBUG):

    # Salida
    #msg = f"modelo nl_to_asp : {modelo_asp} >>>>>>>>\nanswer sets : {answer_set} ///\n has : {predicados_has} ///\n imgs : {rutas_imagenes} >>>>>>>\nexplicacion: {nl_salida}"

    # Tiempo
    print(f"########### TIEMPO TOTAL ###########:      {tiempo_total}:\n\tNL_to_ASP:\t\t{tiempo_nl_to_asp}\n\tresolver_ASP:\t\t{tiempo_resolver_asp}\n\tAS_to_NL:\t\t{tiempo_as_to_nl}\n\tMódulo gráfico:\t\t{tiempo_grafico}")
    
    
