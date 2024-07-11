# Test de generación de hechos: método automatizado de monitorización de tiempos para comprobar la generación de predicados por parte de la primera fase del LLM.
# Objetivo: Medir con métricas de learning: Precision, Recall, F1 Score
#
# Precision (Valor Predictivo Positivo):    VP / VP + FP
# Recall (sensibilidad):                    VP / VP + FN
# F1-Score:                                 2VP / (2VP + FP + FN)

# Imports
import os
import sys
import clingo
from os import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from NL_to_ASP import NL_to_ASP

vp, vn, fp, fn = [0,0,0,0]
reglas_einstein = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/asp/einstein.lp"))
reglas_comensales = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/asp/comensales.lp"))
lineas_count = 0
fail_count = 0

as_prueba_unsat = "living_place(house, V) :- house(V). type(color, V) :- color(V). color(red; blue; purple). person(spanish; english; chinese). type(pet, V) :- pet(V). pet(dog; cat; duck). same_place(spanish, red). same_place(english, blue). same_place(chinese, purple). same_place(spanish, dog). same_place(chinese, tea). type(tobacco_brand, V) :- tobacco_brand(V). tobacco_brand(ducados). same_place(spanish, ducados)."
#as_prueba_sat = 

# Archivos de I/O
log = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/txt/benchmark_predicados.txt")), "a")
tests = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/benchmark_tests/generacion_predicados.txt")), "r")

# Bucle
for line in tests.readlines():

    if (line[0] == "#") or (line.__len__ == 0):  # Comentario o linea vacía -> ignorar
        continue


    num_seats, puzzle, sat,  prompt = line.split("|")
    num_seats = int(num_seats.strip())
    puzzle = puzzle.strip()
    unique_sat_expected = (sat.strip() == "SAT")
    prompt = prompt.strip()

    # Llamada LLM. Si falla, se salta la iteración
    estado, salida_llm = NL_to_ASP(prompt, puzzle, False)
    if estado != 0:
        #print(salida_llm)
        fail_count += 1
        continue 

    print(f"Salida: {salida_llm}\n")

    cc = clingo.Control(["--warn=none", "--models=0"])

    # Se carga el programa ASP según el puzzle elegido
    match puzzle:
        case "Einstein":
            cc.load(reglas_einstein)
        case "Comensales":
            cc.load(reglas_comensales)

    # Se añade el modelo recibido de LLM al código ASP + se hace grounding
    try:
        cc.add('base', [], salida_llm)
        cc.ground([('base',[])])

    except:
        continue

    # ¿SAT?
    try:
        solve_handle = cc.solve(yield_= True)
    except:
        if unique_sat_expected:
            fn += 1
            continue
        else:
            vn += 1
            continue

    # ¿Modelos? Si > 1 diferentes, está mal
    unique_models = set()

    for modelo in solve_handle:
        unique_models.add(modelo)

    for i, modelo in enumerate(unique_models):
        print(f"Modelo {i}: {modelo}")

    model_count = len(unique_models)

    # En comensales, hay num_seats modelos válidos para cada solución única.
    if(puzzle == "Comensales" and model_count == num_seats):
        model_count = 1
    
    print(f"Numero de modelos: {model_count}")

    if model_count == 1:        # Positivo: modelos == 1
        if unique_sat_expected: 
            vp += 1
        else:
            fp += 1
    else:                       # Negativo: modelos != 1
        if unique_sat_expected:
            fn += 1
        else:
            vn += 1

    lineas_count += 1

# Cálculo de métricas
try:
    precision = vp / (vp + fp)
    recall = vp / (vp + fn)
    f1_score = 2*vp / (2*vp + fp + fn)

except ZeroDivisionError:
    precision = 0
    recall = 0
    f1_score = 0

# Log resultados
log.write(f"{lineas_count} muestras probadas ({fail_count} fallos). [VP FP FN VN] = [{vp} {fp} {fn} {vn}]  precision: {precision}, recall: {recall}, F1: {f1_score}\n")


            