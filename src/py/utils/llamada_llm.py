import requests
import json
from dotenv import load_dotenv
import os

# Obtención de secretos (archivo .env)
load_dotenv()
secret_key = os.getenv('AWANLLM_API_KEY')
modelo = os.getenv('MODELO')
url = os.getenv('URL')

# Función para llamar al LLM con una petición JSON (el contrato de AWANLLM es prácticamente igual a OPENAI)
#
#   prompt : string, temperatura : float -> response : JSON
#
def llamada_llm(prompt : str, temperatura : float):

    # Creación de paquete JSON
    payload = json.dumps({ 
                        "model": modelo,
                        "messages": [{"role" : "user", "content" : prompt}],
                        "max_tokens": 1024,
                        "temperature": temperatura,
                        "stream": False
                        })   
    headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {secret_key}" }

    return requests.request("POST", url, headers=headers, data=payload).json()