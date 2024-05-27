# Imports
import requests
import json
from os import path

# Constantes
AWANLLM_API_KEY = "59053288-c83e-4da7-bb4e-d0c0c1c885f9"
modelo = "Meta-Llama-3-8B-Instruct"
url = "https://api.awanllm.com/v1/chat/completions"

def AS_to_NL(input_answer_set = None, puzzle_elegido = None):

    # Contexto sin ejemplos (Zero-Shot)
    contexto_zeroshot = "### I want to translate atomic logical predicates to natural language sentences. Reply only with the result sentence, don't explain the result and don't say anything else than the result. Process only one iteration in each step. ###\n"
    
    # Sale con error si alguno de los args es nulo
    if ((input_answer_set == None) or (puzzle_elegido == None)): return([1, "AS_to_NL recibe una entrada con uno de los valores nulos."])
    
    # Leemos /resources/txt/ctx... para tener el contexto para few-shot learning
    match puzzle_elegido:
        case "Einstein":
                contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/ctx_einstein_to_NL.txt"))
        case _:
            return([1, "En AS_to_NL.py, se recibe un puzzle que no existe: " + puzzle_elegido + ". Vigila que se pase bien."])
    

    with open(contexto_path, 'r') as file: fewshot = file.read()

    contexto_fewshot = contexto_zeroshot + fewshot

    # Zero-shot o Few-shot?
    contexto = contexto_fewshot

    # Construcción de prompt completo
    prompt_w_context = contexto + input_answer_set +"\nOutput: "

    # Petición a la LLM (Actualmente, modelo pequeño para probar)
    payload = json.dumps({ "model": modelo, "messages": [{"role" : "user", "content" : prompt_w_context}] })
    headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {AWANLLM_API_KEY}" }
    response = requests.request("POST", url, headers=headers, data=payload).json()

    # Maneja la respuesta por si trae algún error por parte de servidor.
    try:
        salida_llm = response['choices'][0]['message']['content']
    except KeyError:
        return([1, "Error en el servidor del LLM: " + response['message']])
    except:
        return([1, "Error no manejado en la comunicación con el LLM"])

    if (salida_llm == ""):
        return([1, "El puzzle tiene una solucion y la he encontrado, pero no soy capaz de explicarla en lenguaje natural. El Answer Set encontrado, de todas formas, es: " + input_answer_set])
    else:
        return([0, salida_llm])


    # Logs para debug
    #print("[Context]  " + contexto)
    #print("[Prompt]  " +  prompt)
    #print("[Answer]  " + json_res['choices'][0]['text'])
