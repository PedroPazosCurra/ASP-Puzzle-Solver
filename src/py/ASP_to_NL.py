# Imports
import sys
import requests
import json
from os import path

# Constantes
AWANLLM_API_KEY = "cee74e0e-35c6-46b0-b4d5-071396a48e32"
modelo = "Meta-Llama-3-8B-Instruct-Dolfin-v0.1"
url = "https://api.awanllm.com/v1/completions"

# Prompt y puzzle recibidos por argumento
input_answer_set = sys.argv[1]
puzzle_elegido = sys.argv[2]


# Cadenas de contexto
contexto_zeroshot = "### I want to translate atomic logical predicates to natural language sentences. Reply only with the result sentence, don't explain the result and don't say anything else than the result. Process only one iteration in each step. ###\n\
            Input: "

# Leemos /resources/txt/contexto_einstein.txt para tener el contexto few-shot
contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/ctx_einstein_to_NL.txt"))

with open(contexto_path, 'r') as file:
    fewshot = file.read()

contexto_fewshot = contexto_zeroshot + fewshot

# Variables usadas?
answer_set = input_answer_set
contexto = contexto_fewshot

# Construcción de prompt completo
prompt_w_context = contexto + answer_set +"\nOutput: "

# Petición a la LLM (Actualmente, modelo pequeño para probar)
payload = json.dumps({ "model": modelo, "prompt": prompt_w_context })
headers = {
'Content-Type': 'application/json',
'Authorization': f"Bearer {AWANLLM_API_KEY}"
}

response = requests.request("POST", url, headers=headers, data=payload)
json_res = response.json()
salida_llm = json_res['choices'][0]['text']

# Comprobación de respuesta, verificación y posible reenvío hasta resultado satisfactorio
#

# Logs para debug
#print("[Context]  " + contexto)
#print("[Prompt]  " +  prompt)
#print("[Answer]  " + json_res['choices'][0]['text'])

print(salida_llm)
