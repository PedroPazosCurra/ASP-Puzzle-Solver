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
contexto_zeroshot = "### I want to translate sentences to facts expressed as atomic logical predicates. Do not reply with a sentence, only with the logical atoms. Don't explain the result and don't say anything else than the result. Process only one iteration in each step. ###\n\
            Input: "

contexto_fewshot = contexto_zeroshot + "In my puzzle there is a Brit, a Norwegian, a German and a Dane.\n\
            Output: person(brittish; norwegian; german; dane).\n\
            Input: I have 3 people: a Swede, a Dane and a Norwegian.\n\
            Output: person(swede; dane; norwegian).\n\
            Input: There are 5 people: a German, an Italian; a Brittish, a Spaniard and a Chinese.\n\
            Output: person(german; italian; brittish; spaniard; chinese).\n\
            Input: In my puzzle there are only 2 people: one is a German, and the other one is from Sweden.\n\
            Output: person(german; swede).\n\
            Input: Hello! I have a puzzle to resolve: There are 3 man involved. One of them is from Germany, the other one is French and the last one is Nigerian.\n\
            Output: person(german; french; nigerian).\n\
            Input: A Brittish, a Japanese, an Albanese and a Norwegian.\n\
            Output: person(brit; japanese; albanese; norwegian).\n\
            Input: There are five house colours: red, white, blue, green and yellow.\n\
            Output: color(red; white; blue; green; yellow).\n\
            Input: This problem has a purple and a cyan house.\n\
            Output: color(purple; cyan).\n\
            Input: The houses come in 6 colours: white, beige, blue, red, green and orange.\n\
            Output: color(white; beige; blue; red; green; orange).\n\
            Input: The problem I'm working with has 4 houses. One house is red, other one is green, other is yellow and the last is black.\n\
            Output: house(1..4). color(red; green; yellow; black).\n\
            Input: Seven houses.\n\
            Output: house(1..7).\n\
            Input: There are three houses.\n\
            Output: house(1..3).\n\
            Input: There is a Swede, a Dane and a Norwegian. The puzzle has 3 houses.\n\
            Output: person(swede; dane; norwegian). house(1..3).\n\
            Input: The puzzle has two houses. An Italian and a Rumanian live there.\n\
            Output: house(1..2). person(italian; rumanian). \n\
            Input: There are three drinks: coffee, milk and beer.\n\
            Output: beverage(coffee; milk; beer).\n\
            Input: In this Einstein puzzle there are 4 different types of beverages: water, tea, soda and whiskey.\n\
            Output: beverage(water; tea; soda; whiskey).\n\
            Input: The following drinks are present in the puzzle: tea, wine, beer and juice.\n\
            Output: beverage(tea; wine; beer; juice).\n\
            Input: The puzzle has ten houses. The drinks are water, tea, whiskey, soda, juice, milk, coffee, horchata, gazpacho and beer. Houses are painted red, green, white, black, yellow, purple, grey, brown, blue or orange. \n\
            Output: house(1..10). beverage(water; tea; whisky; soda; juice; milk; coffee; horchata; gazpacho; beer). color(red; green; white; black; yellow; purple; grey; brown; blue; orange).\n\
            Input: The tobacco brands are Blends, Pall and Dunhill.\n\
            Output: tobaccobrand(blends; pall; dunhill).\n\
            Input: There are a Spanish person and a Chinese one. There are also two tobacco brands: Marlboro and Blends. In addition, coffee and wine are being drunk.\n\
            Output: person(spanish; chinese). tobaccobrand(blends; pall; dunhill). beverage(coffee; wine).\n\
            Input: The pets that live in the houses are a dog, a cat and a raccoon.\n\
            Output: pet(dog; cat; raccoon).\n\
            Input: In this exercise there are the following pets: a horse, a bird, a fish and a lizard.\n\
            Output: pet(horse; bird; fish; lizard).\n\
            Input: The drinks and the pets are the following: coffee, milk, dog and cat.\n\
            Output: beverage(coffee; milk). pet(dog; cat).\n\
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
