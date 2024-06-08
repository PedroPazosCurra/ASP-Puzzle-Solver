# proceso.py
#
# Descripción:  En este documento se lleva a cabo la tarea central de procesar el
#                mensaje en lenguaje natural recibido del front-end
#
# -*- coding: utf-8 -*-

# Imports
from sys import argv as args
from os import path
import time
from NL_to_ASP import NL_to_ASP
from AS_to_NL import AS_to_NL
from resolver_ASP import resolver_ASP
from modulo_grafico.modulo_grafico import modulo_grafico
from utils.tiempos_plot import tiempos_plot


# Constantes
AHORA = time.localtime()
HORA_STRING = f"[{str(AHORA.tm_hour)}:{str(AHORA.tm_min)}]"
LOG_HEADER = f"\n############ {HORA_STRING} LOG ############:\n"
MAX_REINTENTOS = 4

# Flags
USAR_LLM_PURO = False
DEBUG = False

# Variables
log = open(path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/log.txt")), "a")


# Funcion auxiliar imprimir_salida()
def imprimir_salida(estado, msg : str, prompt,  puzzle_elegido, tiempos : list, intento : int, contador_tiempo_total):

    # Modo LLM puro -> Sale
    if(USAR_LLM_PURO): 
        log.write(msg)
        log.close

    # Fallo sin máximo alcanzado -> reintento
    if(estado != 0 and intento < MAX_REINTENTOS):
        log.write(msg)
        proceso(prompt, puzzle_elegido, intento + 1, contador_tiempo_total)

    else:
        # Fin de proceso
        tiempo_total = time.perf_counter() - contador_tiempo_total
        
        # Sal con el mensaje
        print(f"{str(estado)}|{msg}", flush= True)
        log.write(msg)
        log.close
        tiempos_plot(tiempos, tiempo_total, intento)

    exit(0)


######### PROCESO: 1 -> 2 -> 3. Si falla, no pasa a la siguiente fase y reintenta o devuelve el mensaje de error al front-end (vía stdout). ###########
#
#       1 - NL_to_ASP(prompt, puzzle) ->    [estado, msg] 
#       2 - resolver_ASP(modelo, puzzle) -> [estado, modelo, [args_solver]]
#       3 - ASP_to_NL(answerset, puzzle) -> [estado, msg]
#       4 - Módulo gráfico ([args_solver], puzzle) -> [estado, msg]
#
def proceso(prompt_usuario, puzzle_elegido, n_intento, contador_tiempo_total):

    # Variables
    modelo_asp = ""
    answer_set = ""
    nl_salida = ""
    msg_grafico = ""
    salida_solver = [{},{}]
    array_tiempos = []
    salida = "# "
    estado = 0

    # Inicio
    log.write(LOG_HEADER)
    log.write(f"\n### Intento {n_intento} de {MAX_REINTENTOS}  ###\n")
    if(n_intento == 0): contador_tiempo_total = time.perf_counter()


    ########    1º - Pasa el mensaje del usuario a declaraciones ASP.           ########
    tiempo_comienzo_nl_to_asp = time.perf_counter()

    estado, modelo_asp = NL_to_ASP(prompt_usuario, puzzle_elegido, USAR_LLM_PURO)

    tiempo_nl_to_asp = time.perf_counter() - tiempo_comienzo_nl_to_asp
    array_tiempos.append(tiempo_nl_to_asp)

    salida += f"# Modelo ASP sacado: \n\t{modelo_asp}\n"

    ## Fallo en NL_to_ASP (1) o modo LLM Puro
    if ((estado != 0) or USAR_LLM_PURO): imprimir_salida(estado, salida, prompt_usuario, puzzle_elegido, array_tiempos, n_intento, contador_tiempo_total)


    ########    2º - Pasa el ASP al solver para obtener el Answer Set solución. ########
    tiempo_comienzo_resolver_asp = time.perf_counter()

    [estado, answer_set, salida_solver] = resolver_ASP(modelo_asp, puzzle_elegido)

    tiempo_resolver_asp = time.perf_counter() - tiempo_comienzo_resolver_asp
    array_tiempos.append(tiempo_resolver_asp)

    ##   Fallo en resolver_ASP (2)
    if(estado != 0): imprimir_salida(estado, salida, prompt_usuario, puzzle_elegido, array_tiempos, n_intento, contador_tiempo_total)


    ########    3º - Pasa el Answer Set a Lenguaje Natural y lo devuelve.       ########
    tiempo_comienzo_as_to_nl = time.perf_counter()

    estado, nl_salida = AS_to_NL(answer_set, puzzle_elegido)

    tiempo_as_to_nl = time.perf_counter() - tiempo_comienzo_as_to_nl
    array_tiempos.append(tiempo_as_to_nl)

    salida += f"# Explicación LN: {nl_salida}\n"

    ##   Fallo en AS_to_NL (3)
    if(estado != 0): imprimir_salida(estado, salida, prompt_usuario, puzzle_elegido, array_tiempos, n_intento, contador_tiempo_total)


    ########    4º Caso optimista: Todo OK - Representación gráfica             ########
    tiempo_comienzo_modulo_grafico = time.perf_counter()

    [estado, msg_grafico] = modulo_grafico(salida_solver, puzzle_elegido)

    tiempo_grafico = time.perf_counter() - tiempo_comienzo_modulo_grafico
    array_tiempos.append(tiempo_grafico)

    if (estado != 0) : salida += f"# Módulo gráfico: {msg_grafico}\n"

    # Fin
    imprimir_salida(estado, salida, prompt_usuario, puzzle_elegido, array_tiempos, n_intento, contador_tiempo_total)

    if(DEBUG):

        pass

        # Salida
        #msg = f"modelo nl_to_asp : {modelo_asp} >>>>>>>>\nanswer sets : {answer_set} ///\n has : {predicados_has} ///\n imgs : {rutas_imagenes} >>>>>>>\nexplicacion: {nl_salida}"

        # Tiempo
        #print(f"########### TIEMPO TOTAL ###########:      {tiempo_total}:\n\tNL_to_ASP:\t\t{tiempo_nl_to_asp}\n\tresolver_ASP:\t\t{tiempo_resolver_asp}\n\tAS_to_NL:\t\t{tiempo_as_to_nl}\n\tMódulo gráfico:\t\t{tiempo_grafico}")
        
##############################################################  Ejecución  #############################################################################

# Default
prompt = "There are three houses. There are a spanish, an english and a chinese. There are three drinks: tea, milk and soda. The spanish man drinks soda. Represent soda with the image \"cocacola\". There's a dog, a cat and a horse. The spanish keeps the cat, while the english man has a dog. The horse is represented by the image called \"horse\". The cat is represented by \"https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg\" The spanish man has a red house. The chinese man, on the other hand, lives in a purple house."
puzzle = "Einstein"
n_intento = 0

# Prompt y puzzle recibidos por argumento (adaptado para debug directo sin pasar por frontend)
num_args = len(args)
if (num_args >= 3): _, prompt, puzzle, n_intento = args

proceso(prompt, puzzle, int(n_intento), None)