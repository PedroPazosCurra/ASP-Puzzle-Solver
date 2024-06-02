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
ASP_REGEX = "((type\(([a-z\_]+\,\s?[A-Z])\)\s:-\s[a-z\_]+\([A-Z]\)\.?\s?)|(\s?[a-z]+\([0-9]+\.\.[0-9]+\)\.?\s?)|(\s?[a-z]+\((\s?[a-z]+\;?\s?)+\)\.?\s?)|(\s?[a-z\_]+\(([a-z\_]+\s?\,?\s?)+\)\.?\s?))+"

def NL_to_ASP(prompt = None, puzzle = None):

    # Contexto sin ejemplos (Zero-Shot)
    contexto_zeroshot = "### You must turn natural language sentences into atomic logical predicates.\
    Instanciate every new atom different than 'person(P)' as a type with the format: 'type(new_type, V) :- new_type(V1;...;Vn).'.\
    For example: 'type(pet, V) :- pet(V). pet(dog; cat; horse).'\
    Also, you can use the predicates 'image(X, Y).' to indicate a image route, 'left(X, Y).' to indicate atom X is to the left of atom Y, 'right(X, Y).' to indicate atom X is to the right of atom Y and 'next_to(X, Y)' to indicate that a person X and a person Y are neighbors.\
    Besides, the predicate 'same_place(X,Y).' says that the atom X and the atom Y are on the same place or grouped together, for example 'John lives in the house number 3' is 'same_place(john, 3).', while 'Water is drunk in the house where Camel is smoked' would be 'same_place(water, camel).'\
    You will be penalized if you write anything in natural language. You will be penalized if you make any kind of note or clarification.\
    You will be penalized if you're verbose and convoluted. Complete only the last iteration. ###\n"
   
    # Sale con error si alguno de los args es nulo
    if ((prompt == None) or (puzzle == None)): return([1, "NL_to_ASP recibe una entrada con uno de los valores nulos."])
    

    # Leemos /resources/txt/ctx... para tener el contexto para few-shot learning
    match puzzle:
        case "Einstein":
            contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/ctx_einstein_to_ASP.txt"))
        case _:
            return([1, "En NL_to_ASP.py, se recibe un puzzle que no existe: "+ puzzle + ". Vigila que se pase bien."])
    
    # Construcción de prompt
    with open(contexto_path, 'r') as file: fewshot = file.read()
    contexto_fewshot = contexto_zeroshot + fewshot
    prompt_w_context = contexto_fewshot + prompt +"\nOUTPUT: "

    # Petición a la LLM (Actualmente, modelo pequeño para probar).
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

    # Comprobación de respuesta válida mediante REGEX con sintaxis ASP.
    match_regex = re.search(ASP_REGEX, salida_llm, flags=0)

    if (match_regex): 
        return([0, salida_llm])
    else:
        return([1, "Lo siento, no soy capaz de procesar esto. Por favor, reescribe tu puzzle explicando el estado de forma precisa o usando otras palabras." + salida_llm])


# Logs para debug
#print("[Context]  " + contexto)
#print("[Prompt]  " +  prompt)
#print("[Answer]  " + json_res['choices'][0]['text'])
