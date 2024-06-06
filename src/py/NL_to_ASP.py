# Imports
import sys
import requests
import json
from os import path
import re

# Constantes
AWANLLM_API_KEY = "59053288-c83e-4da7-bb4e-d0c0c1c885f9"
modelo = "Meta-Llama-3-8B-Instruct"
url = "https://api.awanllm.com/v1/chat/completions"
ASP_REGEX_LIGERO = r"(([a-z\_]+\(([a-z\_]+\,\s?[V])\)\s:-\s[a-z\_]+\([A-Z]\)\.?\s?)|(\s?[a-z\_]+\([0-9]+\.\.[0-9]+\)\.?\s?)|(\s?[a-z\_]+\((\s?[a-z\_]+\;?\s?)+\)\.?\s?)|(\s?[a-z\_]+\(([a-z\_0-9]+\s?\,?\s?)+\)\.?\s?))+"
ASP_REGEX_ESTRICTO_EINSTEIN = r"^((living_place\(([a-z\_]+\,\s?[V])\)\s:-\s[a-z\_]+\([V]\)\.?\s?)|(type\(([a-z\_]+\,\s?V)\)\s:-\s[a-z\_]+\(V\)\.?\s?)|(\s?[a-z\_]+\([0-9]+\.\.[0-9]+\)\.?\s?)|(\s?[a-z\_]+\((\s?[a-z\_]+\s?\;?\s?)+\)\.?\s?)|(\s?(living_place|image|left|right|next_to|same_place)\(([a-z\_0-9]+\s?\,?\s?)+\)\.?\s?))+$"

def NL_to_ASP(prompt : str = None, puzzle : str = None, llm_puro_flag : bool = False):
   
    ###  Preprocesado:
    # Sale con error si alguno de los args es nulo
    if ((prompt == None) or (puzzle == None)): return([1, "NL_to_ASP recibe una entrada con uno de los valores nulos."])

    # Flag de iteración con LLM Puro?
    if llm_puro_flag: 

        contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/einstein_puro.txt"))
        with open(contexto_zeroshot_path, 'r') as file: zeroshot = file.read()
        fewshot = "INPUT: "

    else:
        # Leemos /resources/ctx... para tener el contexto para few-shot learning
        match puzzle:
            case "Einstein":
                contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/zero_einstein_to_ASP.txt"))
                contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/einstein_to_ASP.txt"))
            case "Comensales":
                contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/comensales/zero_comensales_to_ASP.txt"))
                contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/comensales/comensales_to_ASP.txt"))
            case _:
                return([1, "En NL_to_ASP.py, se recibe un puzzle que no existe: "+ puzzle + ". Vigila que se pase bien."])
        
        # Construcción de prompt
        with open(contexto_zeroshot_path, 'r') as file: zeroshot = file.read()
        with open(contexto_path, 'r') as file: fewshot = file.read()

    contexto_fewshot = zeroshot + fewshot
    prompt_w_context = f"{contexto_fewshot} {prompt}\nOUTPUT: "


    ###  Petición al LLM
    payload = json.dumps({ 
                        "model": modelo, 
                        "messages": [{"role" : "user", "content" : prompt_w_context}],
                        "max_tokens": 1024,
                        "temperature": 0.7
                        })   
    headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {AWANLLM_API_KEY}" }
    response = requests.request("POST", url, headers=headers, data=payload).json()

    # Maneja la respuesta por si trae algún error por parte de servidor.
    try:
        salida_llm = response['choices'][0]['message']['content']
    except KeyError:
        return([1, "Error en el servidor del LLM: " + response['message']])
    except:
        return([1, "Error no manejado en la comunicación con el LLM para NL_to_ASP"])


    ###  Postprocesado:

    # Sale sin postprocesado si flag de iteración pura
    if(llm_puro_flag): return[1, salida_llm]

    # El modelo tiene tendencia a seguir los ejemplos con alucinaciones. Diga lo que diga, intento aprovechar la primera salida (previa al primer '\n', 'INPUT', 'Note'...)
    # Además, preprocesado de caracteres extraños que a veces el LLM mete por el medio con intención de ejemplificar.
    if (salida_llm.find("\\") != -1):
        salida_llm = salida_llm.strip().split("\\", 1)[0]
    if (salida_llm.find("INPUT:") != -1):
        salida_llm = salida_llm.strip().split("INPUT", 1)[0]
    if (salida_llm.find("output:") != -1):
        salida_llm = salida_llm.strip().split("output:", 1)[1]
    if (salida_llm.find("input:") != -1):
        salida_llm = salida_llm.strip().split("input:", 1)[1]
    if (salida_llm.find("Note") != -1):
        salida_llm = salida_llm.strip().split("Note", 1)[0]
    if (salida_llm.find("`") != -1):
        salida_llm = salida_llm.replace("`", "")
    if (salida_llm.find("),") != -1):
        salida_llm = salida_llm.replace("),", ").")
    if (salida_llm.find("type(person, V) :- person(V).") != -1):
        salida_llm = salida_llm.replace("type(person, V) :- person(V).", "")

    # A veces se olvida de poner el punto en el último predicado. Intento rescatarlo.
    salida_llm = salida_llm.strip()
    if (salida_llm[-1] != "."):
        salida_llm += "."

    # Comprobación de respuesta válida mediante REGEX con sintaxis ASP. Nota: REGEX en dos niveles para filtrar preámbulos y coletillas en nivel ligero y filtrar comandos erróneos en nivel estricto.

    match_regex_ligero = re.search(ASP_REGEX_LIGERO, salida_llm, flags=0).group()
    
    if(puzzle == "Einstein"):
        match_regex_estricto_einstein = re.search(ASP_REGEX_ESTRICTO_EINSTEIN, match_regex_ligero, flags=0).group()
        if match_regex_estricto_einstein == match_regex_ligero: 
            return([0, salida_llm])

    elif(puzzle == "Comensales" and match_regex_ligero):
        return([0, salida_llm])
        

    return([1, "Lo siento, no soy capaz de procesar esto. Por favor, reescribe tu puzzle explicando el estado de forma precisa o usando otras palabras. " + salida_llm])

        
# Logs para debug
#print("[Context]  " + contexto)
#print("[Prompt]  " +  prompt)
#print("[Answer]  " + json_res['choices'][0]['text'])
