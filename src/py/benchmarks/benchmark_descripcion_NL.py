# Test de generación de hechos: método automatizado de monitorización de tiempos para comprobar la generación de predicados por parte de la primera fase del LLM.
# Objetivo: Medir el rendimiento de la parte 
#

# Imports
import os
import sys
from os import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from AS_to_NL import AS_to_NL

# Archivos de I/O
log = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/txt/benchmark_descripcion.txt")), "a")


# Pruebas (en este caso, hay que ejecutarlas de forma manual)
prueba_1 = "Einstein | has(brittish,house,1)."
prueba_2 = "Einstein | has(brittish,house,1). has(german,house,2)."
prueba_3 = "Einstein | has(brittish,house,1). has(brittish,pet,snail). has(german,house,2). has(german,pet,zebra)."
prueba_4 = "Einstein | has(brittish,house,1). has(brittish,pet,snail). has(german,house,2). has(german,pet,zebra). has(swedish,house,3). has(swedish,pet,snake)."
prueba_5 = "Einstein | has(brittish,house,1). has(brittish,pet,snail). has(spanish,house,4). has(spanish,pet,dog). has(german,house,2). has(german,pet,zebra). has(swedish,house,3). has(swedish,pet,snake)."
prueba_6 = "Einstein | has(brittish,car,1). has(spanish,car,2). has(italian,car,3). has(brittish,color,yellow). has(spanish,color,cyan). has(italian,color,purple)."
prueba_7 = "Einstein | has(brittish,house,1). has(brittish,pet,snail). has(german,house,2). has(german,pet,zebra). has(swedish,house,3). has(swedish,pet,snake). has(brittish,phone,apple). has(german,phone,xiaomi). has(swedish,phone,samsung)."
prueba_8 = "Einstein | has(brittish,house,1). has(brittish,pet,snail). has(german,house,2). has(german,pet,zebra). has(swedish,house,3). has(swedish,pet,snake). has(brittish,phone,apple). has(german,phone,xiaomi). has(swedish,phone,samsung). has(chinese,house,4). has(chinese,pet,dog)."
prueba_9 = "Einstein | has(brittish,house,1). has(brittish,pet,snail). has(german,house,2). has(german,pet,zebra). has(swedish,house,3). has(swedish,pet,snake). has(brittish,phone,apple). has(german,phone,xiaomi). has(swedish,phone,samsung). has(chinese,house,4). has(chinese,pet,dog). has(chinese,phone,huawei). has(brittish,favourite_band,rolling_stones)."
prueba_10 = "Einstein | has(zimbabwean,house,16). has(zimbabwean,color,beige)."
prueba_11 = "Einstein | has(zimbabwean,house,16). has(zimbabwean,color,beige). has(greek,house,1). has(greek,drink,liquor)."
prueba_12 = "Einstein | has(zimbabwean,house,16). has(zimbabwean,color,beige). has(greek,house,1). has(greek,drink,liquor). has(zimbabwean,car,ford). has(greek,car,nissan)."
prueba_13 = "Einstein | has(zimbabwean,house,16). has(zimbabwean,color,beige). has(greek,house,1). has(greek,drink,liquor). has(zimbabwean,car,ford). has(greek,car,nissan). has(haitian,house,5). has(haitian,drink,soda). has(haitian,pet,horse). has(haitian,car,ford_focus)."
prueba_14 = "Einstein | has(japanese,house,1092385). has(peruvian,house,123596)."
prueba_15 = "Einstein | has(brittish,house,4). has(brittish,pet,bird). has(brittish,drink,beer). has(brittish,tobacco_brand,pall_mall). has(danish,house,2). has(danish,pet,horse). has(danish,drink,tea). has(danish,tobacco_brand,dunhill). has(german,house,1). has(german,pet,fish). has(german,drink,coffee). has(german,tobacco_brand,prince). has(norwegian,house,5). has(norwegian,pet,cat). has(norwegian,drink,water). has(norwegian,tobacco_brand,blends). has(swedish,house,3). has(swedish,pet,dog). has(swedish,drink,milk). has(swedish,tobacco_brand,blue_master)."
prueba_16 = "Comensales | seated(antonio,1)."
prueba_17 = "Comensales | seated(manuela,1). seated(abdhul,2)."
prueba_18 = "Comensales | seated(martina,2). seated(claudia,3). seated(pedro,1)."
prueba_19 = "Comensales | seated(jose,4). seated(martina,2). seated(claudia,3). seated(pedro,1)."
prueba_20 = "Comensales | seated(marta,5). seated(mohammed,4). seated(jose,2). seated(manuel,3). seated(pedro,1)."
prueba_21 = "Comensales | seated(marta,5). seated(mohammed,4). seated(jose,2). seated(manuel,3). seated(pedro,1). seated(roberto,6)."
prueba_22 = "Comensales | seated(marta,5). seated(mohammed,4). seated(carolina, 7). seated(jose,2). seated(manuel,3). seated(pedro,1). seated(roberto,6)."
prueba_23 = "Comensales | seated(marta,5). seated(mohammed,4). seated(carlos,8). seated(carolina,7). seated(jose,2). seated(manuel,3). seated(pedro,1). seated(roberto,6)."
prueba_24 = "Comensales | seated(marta,5). seated(mohammed,4). seated(carlos,8). seated(carolina,7). seated(maria,9). seated(jose,2). seated(manuel,3). seated(pedro,1). seated(roberto,6)."
prueba_25 = "Comensales | seated(alberto,1). seated(carlos,3). seated(carolina,6). seated(paco,10). seated(lucia,5). seated(antia,7). seated(jose,9). seated(martina,4). seated(claudia,2). seated(pedro,8)."
prueba_26 = "Comensales | seated(alberto,1). seated(carlos,3). seated(isabel,11). seated(carolina,6). seated(paco,10). seated(lucia,5). seated(antia,7). seated(jose,9). seated(martina,4). seated(claudia,2). seated(pedro,8)."
prueba_27 = "Comensales | seated(alberto,1). seated(carlos,3). seated(isabel,11). seated(juan,12). seated(carolina,6). seated(paco,10). seated(lucia,5). seated(antia,7). seated(jose,9). seated(martina,4). seated(claudia,2). seated(pedro,8)."
prueba_28 = "Comensales | seated(alberto,1). seated(carlos,3). seated(isabel,11). seated(juan,12). seated(carolina,6). seated(paco,10). seated(lucia,5). seated(antia,7). seated(jose,9). seated(martina,4). seated(claudia,2). seated(pedro,8). seated(javier,13). seated(julian,14). seated(herminia,15)."
prueba_29 = "Comensales | seated(eduardo,16). seated(amelia,17). seated(alberto,1). seated(ana,18). seated(elisa,19). seated(raul,20). seated(carlos,3). seated(isabel,11). seated(juan,12). seated(carolina,6). seated(paco,10). seated(lucia,5). seated(antia,7). seated(jose,9). seated(martina,4). seated(claudia,2). seated(pedro,8). seated(javier,13). seated(julian,14). seated(herminia,15)."
prueba_30 = "Comensales | seated(eduardo,16). seated(amelia,17). seated(alberto,1). seated(ana,18). seated(elisa,19). seated(raul,20). seated(carlos,3). seated(isabel,11). seated(juan,12). seated(carolina,6). seated(paco,10). seated(jesus,25). seated(amable,26). seated(dolores,27). seated(guillermo,28). seated(ivan,29). seated(sonia,30). seated(lucia,5). seated(antia,7). seated(jose,9). seated(marcos,21). seated(marcelino,22). seated(martina,4). seated(gabriel,23). seated(sergio,24). seated(claudia,2). seated(pedro,8). seated(javier,13). seated(julian,14). seated(herminia,15)."


# Proceso
prueba = prueba_30

puzzle, prompt = prueba.split("|")
puzzle = puzzle.strip()
prompt = prompt.strip()

log.write(f"###################################################\n")
log.write(f"[# Entrada] - {prompt}\n") 

# Llamada LLM. Si falla, se loguea error
try:
    estado, salida_llm = AS_to_NL(prompt, puzzle)
    print(f"[# Salida] - {salida_llm}\n")
    log.write(f"[# Salida] - {salida_llm} \n") 

except:
    log.write(f"[# Salida] - FALLO \n")