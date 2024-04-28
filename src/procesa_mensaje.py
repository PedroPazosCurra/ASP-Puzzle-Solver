import sys
import requests
import json

AWANLLM_API_KEY = "cee74e0e-35c6-46b0-b4d5-071396a48e32"
url = "https://api.awanllm.com/v1/completions"
prompt = "You're a Natural Language to Answer Set Programming translator. Input: John is hungry. / Output: hungry(john) / Input: Mary is drinking ale / Output: drinking(mary,ale) / Input: Albert lives in a red house / Output: "
modelo = "Meta-Llama-3-8B-Instruct-Dolfin-v0.1"

def procesa_mensaje(msg):

    print("Llega al programa python con mensaje: " + msg)

    # Petición a la LLM (Actualmente, modelo pequeño para probar)
    payload = json.dumps({ "model": modelo, "prompt": prompt })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {AWANLLM_API_KEY}"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_res = response.json()
    
    # Comprobación de respuesta, verificación y posible reenvío hasta resultado satisfactorio

    # Envío al solver ASP
    print(json_res[""])
    return "Placeholder para respuesta final"

if __name__ == "__main__":

    message = sys.stdin.readline().strip()
    response = procesa_mensaje(message)
    sys.stdout.write(response)