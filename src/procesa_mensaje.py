# Imports
import sys
import requests
import json

# Constantes
AWANLLM_API_KEY = "cee74e0e-35c6-46b0-b4d5-071396a48e32"
modelo = "Meta-Llama-3-8B-Instruct-Dolfin-v0.1"
url = "https://api.awanllm.com/v1/completions"

# Prompts de prueba
prompt_debug_1 = "The bird is a pet"
prompt_debug_2 = "This house is purple"
prompt_debug_3 = "Blends tobacco is smoked at the fourth house."

# Prompt y puzzle recibidos por argumento
prompt_usuario = sys.argv[1]
puzzle_elegido = sys.argv[2]



# Cadenas de contexto
contexto_zeroshot = "I want to translate sentences to facts expressed as atomic logical predicates. Do not reply with a sentence, only with the logical atoms. Don't explain the result and don't say anything else than the result.\n\
            Input: "

contexto_fewshot = "I want to translate sentences to facts expressed as atomic logical predicates. Do not reply with a sentence, only with the logical atoms. Don't explain the result and don't say anything else than the result.\n \
            Input: The house is blue.\n\
            Output: color(blue, house).\n\
            Input: The cat is a pet.\n\
            Output: pet(cat).\n\
            Input: Prince cigarettes are smoked in the fifth house.\n\
            Output: at(tobacco, prince, 5).\n\
            Input: The norwegian lives at the first house.\n\
            Output: at(person, norw, 1).\n\
            Input: The brit lives at the third house.\n\
            Output: at(person, brit, 3).\n\
            Input: The first house has a dog pet.\n\
            Output: at(pet, dog, 1) \n\
            Input: The german is living at the green house.\n\
            Output: :- at(person, german, X), not at(color, green, X)\n\
            Input: In the purple house, they smoke Dunhill cigarettes.\n\
            Output: :- at(color, purple, X), not at(smoke, dunhill, X).\n\
            Input: Coffee is drunk at the red house.\n\
            Output: :- at(color, red, X), not at(drink, coffee, X).\n\
            Input: It can't be that coffee is not being drunk at the red house.\n\
            Output: :- at(color, red, X), not at(drink, coffee, X).\n\
            Input: "

# Variables usadas?
prompt = prompt_usuario
contexto = contexto_fewshot

# Construcción de prompt completo
prompt_w_context = contexto + prompt +"\nOutput: "

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

# Envío al solver ASP
#

# Logs para debug
#print("[Context]  " + contexto)
#print("[Prompt]  " +  prompt)
#print("[Answer]  " + json_res['choices'][0]['text'])


print(salida_llm)
