import requests
import json
from utils.carga_dotenv import carga_dotenv

# Función para llamar al LLM con una petición JSON (el contrato de AWANLLM es prácticamente igual a OPENAI)
#
#   prompt : string, temperatura : float -> [status: int, response : JSON]
#
def llamada_llm(prompt : str, temperatura : float):

    # Carga variables de entorno
    salida_env = carga_dotenv()
    if len(salida_env) == 2:
        raise RuntimeError(salida_env[1])
    
    _, _, secret_key, modelo, url = salida_env

    # Creación de paquete JSON
    payload = json.dumps({
                        "model": modelo,
                        "prompt": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are an expert logical code to natural language translator.<|eot_id|><|start_header_id|>user<|end_header_id|>{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                        "repetition_penalty": 1.1,
                        "max_tokens": 1024,
                        "temperature": temperatura,
                        "top_p": 0.9,
                        "top_k": 40,
                        "stream": False
                        })
    
    try:
        headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {secret_key}" }
        response = requests.request("POST", url, headers=headers, data=payload)

    except requests.exceptions.ConnectTimeout:
        return [1, "Timeout por parte del servidor. Probablemente servidor caído o saturado."]


    try:
        response = response.json()
        salida_llm = response['choices'][0]['text']
        return [0, salida_llm]
    
    except KeyError:
        return [1, "Error con la peticion a API del LLM. Respuesta recibida: " + str(response)]
    except requests.exceptions.JSONDecodeError:
        return [1, f"Error en servidor: {response.status_code}"]
    except:
        return [1, "Error no manejado en la comunicación con el LLM"]