# Imports
import sys
import requests
import json
from os import path
import re

# Constantes
AWANLLM_API_KEY = "59053288-c83e-4da7-bb4e-d0c0c1c885f9"
modelo = "Meta-Llama-3-8B-Instruct-Dolfin-v0.1"
url = "https://api.awanllm.com/v1/completions"
ASP_REGEX = "^\s?([a-z\_]*\((([a-z\_]+(,\s?)?)+|([a-z\_]+(;\s?)?)*|([0-9]+\.\.[0-9]+))\)\.\s?)+$"
REINTENTOS_MAX = 5

def NL_to_ASP(prompt, puzzle):

    # Contexto sin ejemplos (Zero-Shot)
    contexto_zeroshot = "### I want to translate sentences to facts expressed as atomic logical predicates. Do not reply with a sentence, only with the logical atoms. Don't explain the result and don't say anything else than the result. Process only one iteration in each step. ###\n"

    # Leemos /resources/txt/contexto_einstein.txt para tener el contexto para few-shot learning
    contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/ctx_einstein_to_ASP.txt"))
    with open(contexto_path, 'r') as file: fewshot = file.read()

    contexto_fewshot = contexto_zeroshot + fewshot

    # Zero-shot o Few-shot?
    contexto = contexto_fewshot

    # Construcción de prompt completo
    prompt_w_context = contexto + prompt +"\nOutput: "

    # Bucle para reintentar petición si salida incorrecta
    intentos = 0

    while (intentos <= REINTENTOS_MAX):

        # Petición a la LLM (Actualmente, modelo pequeño para probar)
        payload = json.dumps({ "model": modelo, "prompt": prompt_w_context })
        headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {AWANLLM_API_KEY}" }
        response = requests.request("POST", url, headers=headers, data=payload)
        salida_llm = response.json()['choices'][0]['text']

        # El modelo tiene tendencia a seguir los ejemplos con alucinaciones. Diga lo que diga, intento aprovechar la primera salida (previa al primer \n)
        if (salida_llm.find("\\") != -1):
            salida_llm = salida_llm.split("\\", 1)[0].strip()


        # Comprobación de respuesta válida mediante REGEX con sintaxis ASP.
        if (re.search(ASP_REGEX, salida_llm) != None ):

            return([0, salida_llm])

        else: intentos = intentos + 1

    return([1, "Lo siento, no soy capaz de procesar esto. Por favor, reescribe tu puzzle explicando el estado de forma precisa o usando otras palabras."])


# Logs para debug
#print("[Context]  " + contexto)
#print("[Prompt]  " +  prompt)
#print("[Answer]  " + json_res['choices'][0]['text'])
