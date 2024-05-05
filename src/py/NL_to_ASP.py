# Imports
import sys
import requests
import json
from os import path
import re

# Constantes
AWANLLM_API_KEY = "cee74e0e-35c6-46b0-b4d5-071396a48e32"
modelo = "Meta-Llama-3-8B-Instruct-Dolfin-v0.1"
url = "https://api.awanllm.com/v1/completions"
ASP_REGEX = "([a-z]*\((([a-z]*(,\s)?)*|([a-z]*(;\s)?)*)\)\.)+"
REINTENTOS_MAX = 5

# Prompt y puzzle recibidos por argumento
prompt_usuario = sys.argv[1]
puzzle_elegido = sys.argv[2]



# Cadenas de contexto
contexto_zeroshot = "### I want to translate sentences to facts expressed as atomic logical predicates. Do not reply with a sentence, only with the logical atoms. Don't explain the result and don't say anything else than the result. Process only one iteration in each step. ###\n"

# Leemos /resources/txt/contexto_einstein.txt para tener el contexto few-shot
contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/ctx_einstein_to_ASP.txt"))

with open(contexto_path, 'r') as file:
    fewshot = file.read()

contexto_fewshot = contexto_zeroshot + fewshot

# Variables usadas?
prompt = prompt_usuario
contexto = contexto_fewshot

# Construcción de prompt completo
prompt_w_context = contexto + prompt +"\nOutput: "

# Bucle para reintentar petición si salida incorrecta
salida_valida = False
intentos = 0

while (not salida_valida):

    # Petición a la LLM (Actualmente, modelo pequeño para probar)
    payload = json.dumps({ "model": modelo, "prompt": prompt_w_context })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {AWANLLM_API_KEY}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    salida_llm = response.json()['choices'][0]['text']

    # Comprobación de respuesta mediante REGEX
    if (re.search(ASP_REGEX, salida_llm) != None ):

        salida_valida = True
        print(salida_llm)

    else:

        intentos = intentos + 1
        if intentos >= REINTENTOS_MAX:
            print("Lo siento, no soy capaz de procesar esto. Por favor, reescribe tu puzzle explicando el estado de forma precisa o usando otras palabras.")
            break


# Envío al solver ASP
#


# Logs para debug
#print("[Context]  " + contexto)
#print("[Prompt]  " +  prompt)
#print("[Answer]  " + json_res['choices'][0]['text'])
