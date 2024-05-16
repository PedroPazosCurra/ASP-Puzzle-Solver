# Imports
import sys
import requests
import json
from os import path
import re

# Constantes
AWANLLM_API_KEY = "59053288-c83e-4da7-bb4e-d0c0c1c885f9"
modelo = "Awanllm-Llama-3-8B-Dolfin"
url = "https://api.awanllm.com/v1/chat/completions"

input_answer_set = "There are three houses. In them live a spanish, an english and a chinese. There are three pets: a dog, a cat and a duck. There are 3 tobacco brands: Ducados, Camel and Bluem. There are also three drinks: coffee, water and tea. The spanish man house is painted red, while the englishman house is tainted blue. The house of the chinese is purple. The spanish keeps a dog. The chinese loves to drink tea. The spanish, on the other hand, smokes Ducados."
puzzle_elegido = "Einstein"

# Contexto sin ejemplos (Zero-Shot)
contexto_zeroshot = "### You MUST parse natural language sentences to atomic logical predicates. Reply only with the logical atoms. You will be penalized if you write something different from the final logical predicates. Write only the last iteration. You are provided with examples. ###\n"

contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/ctx_einstein_to_ASP.txt"))

with open(contexto_path, 'r') as file: fewshot = file.read()

contexto_fewshot = contexto_zeroshot + fewshot

# Zero-shot o Few-shot?
contexto = contexto_fewshot

# Construcción de prompt completo
prompt_w_context = contexto + input_answer_set +"\nOUTPUT: "

# Petición a la LLM (Actualmente, modelo pequeño para probar)
payload = json.dumps({ "model": modelo, "messages": [{"role" : "user", "content" : prompt_w_context}] })
headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {AWANLLM_API_KEY}" }
response = requests.request("POST", url, headers=headers, data=payload)
print(response.json()['choices'][0]['message']['content'])

