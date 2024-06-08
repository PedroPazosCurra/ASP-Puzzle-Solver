# Imports
import sys
import requests
import json
from os import path
import re

# Constantes
AWANLLM_API_KEY = "4b8749be-38d2-4f66-9417-e05debfce1c6"
modelo = "Meta-Llama-3-8B-Instruct"
url = "https://api.awanllm.com/v1/chat/completions"

input_answer_set = "There are three houses. In them live a Spanish, an nglish and a chinese. There are three pets: a dog, a cat and a duck. There are 3 tobacco brands: Ducados, Camel and Blue Master. There are also three drinks: coffee, water and tea. The Spanish man house is painted red, while the Englishman house is tainted blue. The house of the chinese man is purple. The Spanish man keeps a dog. The chinese man loves to drink tea. The Spanish one, on the other hand, smokes Ducados."
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

# Petición a la LLM (Actualmente, modelo pequeño para probar)
payload = json.dumps({  
                        "model": modelo,
                        "messages": [{"role" : "user", "content" : input_answer_set}],
                        "max_tokens": 1024,
                        "temperature": 0.7,
                        "stream": False
                    })

headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {AWANLLM_API_KEY}" }
response = requests.request("POST", url, headers=headers, data=payload).json()


try:
    #print(response)
    print(response['choices'][0]['message']['content'])
except KeyError:
    print("Error en el servidor del LLM: " + response)
except:
    print("Error no manejado en la comunicación con el LLM")

    

