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
ASP_REGEX = "^\s?([a-z\_]*\((([a-z\_]+(,\s?)?)+|([a-z\_]+(;\s?)?)*|([0-9]+\.\.[0-9]+))\)\.\s?)+$"
REINTENTOS_MAX = 1

def NL_to_ASP(prompt, puzzle):

    # Contexto sin ejemplos (Zero-Shot)
    contexto_zeroshot = "### You MUST parse natural language sentences to atomic logical predicates. Reply only with the logical atoms. You will be penalized if you write something different from the final logical predicates. Write only the last iteration. You are provided with examples. ###\n"

    # Leemos /resources/txt/ctx... para tener el contexto para few-shot learning
    match puzzle:
        case "Einstein":
            contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/ctx_einstein_to_ASP.txt"))
        case _:
            return([1, "En NL_to_ASP.py, se recibe un puzzle que no existe. Vigila que se pase bien."])
    
    # Construcción de prompt
    with open(contexto_path, 'r') as file: fewshot = file.read()
    contexto_fewshot = contexto_zeroshot + fewshot
    contexto = contexto_fewshot # Zero-shot o Few-shot?
    prompt_w_context = contexto + prompt +"\nOutput: "

    # Bucle para reintentar petición si salida incorrecta
    intentos = 0

    while (intentos <= REINTENTOS_MAX):

        # Petición a la LLM (Actualmente, modelo pequeño para probar)
        payload = json.dumps({ "model": modelo, "messages": [{"role" : "user", "content" : prompt_w_context}] })
        headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {AWANLLM_API_KEY}" }
        response = requests.request("POST", url, headers=headers, data=payload)
        salida_llm = response.json()['choices'][0]['message']['content']

        # El modelo tiene tendencia a seguir los ejemplos con alucinaciones. Diga lo que diga, intento aprovechar la primera salida (previa al primer '\n' o 'INPUT')
        if (salida_llm.find("\\") != -1):
            salida_llm = salida_llm.strip().split("\\", 1)[0]
        elif (salida_llm.find("Input") != -1):
            salida_llm = salida_llm.strip().split("INPUT", 1)[0]

        # A veces se olvida de poner el punto en el último predicado. Intento rescatarlo.
        if (salida_llm.strip()[-1] != "."):
            salida_llm += "."


        # Comprobación de respuesta válida mediante REGEX con sintaxis ASP.
        if (re.search(ASP_REGEX, salida_llm) != None ):
            return([0, salida_llm])
        
        else: intentos += 1

    return([1, "Lo siento, no soy capaz de procesar esto. Por favor, reescribe tu puzzle explicando el estado de forma precisa o usando otras palabras."])


# Logs para debug
#print("[Context]  " + contexto)
#print("[Prompt]  " +  prompt)
#print("[Answer]  " + json_res['choices'][0]['text'])
