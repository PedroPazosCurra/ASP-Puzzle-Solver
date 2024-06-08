import requests
import json

AWANLLM_API_KEY = "4b8749be-38d2-4f66-9417-e05debfce1c6"
modelo = "Meta-Llama-3-8B-Instruct"
url = "https://api.awanllm.com/v1/chat/completions"

def llamada_llm(prompt : str, temperatura : float):

    ###  Petición al LLM
    payload = json.dumps({ 
                        "model": modelo, 
                        "messages": [{"role" : "user", "content" : prompt}],
                        "max_tokens": 1024,
                        "temperature": temperatura,
                        "stream": False
                        })   
    headers = { 'Content-Type': 'application/json', 'Authorization': f"Bearer {AWANLLM_API_KEY}" }

    return requests.request("POST", url, headers=headers, data=payload).json()