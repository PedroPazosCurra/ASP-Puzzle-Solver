# Test de ganancia de la aproximación neurosimbólica
# Objetivo: Medir la ventaja del sistema neurosimbólico frente a la solución del modelo de lenguaje puro.
#

# Imports
import os
import sys
from os import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from NL_to_ASP import NL_to_ASP
from resolver_ASP import resolver_ASP
from AS_to_NL import AS_to_NL

# Archivos de I/O
log = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/txt/benchmark_ganancia_aproximacion.txt")), "a")


# Pruebas (en este caso, hay que ejecutarlas de forma manual)
prueba_1 = "Einstein | There are two houses, and two people: a German and a English. One house is painted Red and the other one is colored Purple. The German lives in the Red house."
prueba_11 = "Comensales | "

# Proceso
prueba = prueba_1

puzzle, prompt = prueba.split("|")
puzzle = puzzle.strip()
prompt = prompt.strip()

log.write(f"###################################################\n")
log.write(f"[# Entrada] - {prompt}\n") 


# LLM Puro
#try:
[estado, salida_llm_puro] = NL_to_ASP(prompt, puzzle, True)

print(f"[# Salida Puro] - {salida_llm_puro}\n")
log.write(f"[# Salida Puro] - {salida_llm_puro} \n") 

#except:
#log.write(f"[# Salida Puro] - FALLO \n")


# Sistema neurosimbólico
#try:
[estado, salida_llm] = NL_to_ASP(prompt, puzzle, False)
[estado, salida_solver, _] = resolver_ASP(salida_llm, puzzle)
[estado, salida_llm_2] = AS_to_NL(salida_solver, puzzle)

print(f"[# Salida Sis. Neurosim.] - {salida_llm_2}\n")
log.write(f"[# Salida Sis. Neurosim. [1]] - {salida_llm} \n") 
log.write(f"[# Salida Sis. Neurosim. [2]] - {salida_solver} \n") 
log.write(f"[# Salida Sis. Neurosim. [3]] - {salida_llm_2} \n") 

#except:
#log.write(f"[# Salida Sis. Neurosim.] - FALLO \n")

