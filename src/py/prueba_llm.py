# Imports
import sys
import requests
import json
from os import path
import re

# Constantes
from dotenv import load_dotenv
import os

# Obtención de secretos (archivo .env)
load_dotenv(dotenv_path= path.join(path.dirname(__file__), "utils\.env"))
secret_key = os.getenv('AWANLLM_API_KEY')
modelo = os.getenv('MODELO')
url = os.getenv('URL')


input_answer_set = "There are three houses. In them live a Spanish, an English and a chinese. There are three pets: a dog, a cat and a duck. There are 3 tobacco brands: Ducados, Camel and Blue Master. There are also three drinks: coffee, water and tea. The Spanish man house is painted red, while the Englishman house is tainted blue. The house of the chinese man is purple. The Spanish man keeps a dog. The chinese man loves to drink tea. The Spanish one, on the other hand, smokes Ducados."
puzzle_elegido = "Einstein"

# Contexto
contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/zero_einstein_to_ASP.txt"))
contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/einstein_to_ASP.txt"))

with open(contexto_zeroshot_path, 'r') as file: zeroshot = file.read()
with open(contexto_path, 'r') as file: fewshot = file.read()

contexto_fewshot = zeroshot + fewshot

# Zero-shot o Few-shot?
contexto = contexto_fewshot

# Construcción de prompt completo
prompt_w_context = zeroshot + input_answer_set +"\nOUTPUT: "

# Petición a la LLM
payload = json.dumps({  
                        "model": modelo,
                        "prompt": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are an expert logical code to natural language translator.<|eot_id|><|start_header_id|>user<|end_header_id|>{prompt_w_context}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                        "max_tokens": 1024,
                        "temperature": 0.7,
                        "repetition_penalty": 1.1,
                        "top_p": 0.9,
                        "top_k": 40,
                        "stream": False
                    })

try:
    headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {secret_key}" }
    response = requests.request("POST", url, headers=headers, data=payload)

except requests.exceptions.ConnectTimeout:
    print("Timeout por parte del servidor. Probablemente esté caído.")

try:
    #print(response.status_code)
    response = response.json()
    salida_llm = response['choices'][0]['text']
    print(response)
    print(salida_llm)
except KeyError:
    print("Error en el servidor del LLM: ")
except requests.exceptions.JSONDecodeError:
    print(f"Error en servidor: {response.status_code}")
except:
    print("Error no manejado en la comunicación con el LLM")

    

