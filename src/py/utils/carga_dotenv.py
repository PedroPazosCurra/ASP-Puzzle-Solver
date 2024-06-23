from dotenv import load_dotenv
import os

# Función para obtener las variables de entorno (archivo .env)
def carga_dotenv():

    if not load_dotenv():
        with open(".env", "w") as f:
            f.write(r"AWANLLM_API_KEY=\"YOUR_API_KEY_HERE\"\nMODELO=\"Meta-Llama-3-8B-Instruct\"\nURL=\"https://api.awanllm.com/v1/chat/completions\"")
        return [1, "Este sistema no tiene la clave de la API del LLM. Ve a /src/py/utils/.env a ponerla."]

    secret_key = os.getenv('AWANLLM_API_KEY')
    modelo = os.getenv('MODELO')
    url = os.getenv('URL')

    if secret_key == "YOUR_API_KEY_HERE" or secret_key == None:
        return [1, "Este sistema no tiene puesta la clave de la API del LLM. Ve a /src/py/utils/.env a ponerla.", None, None, None]
    else:
        return [0, "OK", secret_key, modelo, url]
