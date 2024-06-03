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

input_answer_set = "There are three boats. There are a Spanish, an English and a Chinese. There are three drinks: Tea, Milk and Soda. The Spanish man drinks Soda. Soda is represented with the next image: cocacola. There's a Dog, a Cat and a Horse. The Spanish keeps the Cat, while the English man has a Dog. The Horse is represented by the image called 'horse'. The Cat is represented by https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg The Spanish man has a red boat. The chinese man, on the other hand, lives in a Purple boat. Represent the boat with https://t3.ftcdn.net/jpg/00/41/60/94/360_F_41609453_X3A8NNRDWvihqMLoJUVNmrQyKQgwgvh4.jpg."
puzzle_elegido = "Einstein"

# Contexto sin ejemplos (Zero-Shot)
contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/zero_einstein_to_ASP.txt"))
contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein_to_ASP.txt"))

with open(contexto_path, 'r') as file: zeroshot = file.read()
with open(contexto_path, 'r') as file: fewshot = file.read()

contexto_fewshot = zeroshot + fewshot

# Zero-shot o Few-shot?
contexto = contexto_fewshot

# Construcción de prompt completo
prompt_w_context = contexto + input_answer_set +"\nOUTPUT: "

# Petición a la LLM (Actualmente, modelo pequeño para probar)
payload = json.dumps({  
                        "model": modelo,
                        "messages": [{"role" : "user", "content" : prompt_w_context}],
                        "max_tokens": 1024,
                        "temperature": 0.7 
                    })

headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {AWANLLM_API_KEY}" }
response = requests.request("POST", url, headers=headers, data=payload).json()


try:
    print(response)
    print(response['choices'][0]['message']['content'])
except KeyError:
    print("Error en el servidor del LLM: " + response['message'])
except:
    print("Error no manejado en la comunicación con el LLM")

    

