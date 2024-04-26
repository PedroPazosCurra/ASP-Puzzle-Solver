import sys

def procesa_mensaje(msg):

    print("Llega al programa python con mensaje: " + msg)

    # Llamada a la API del LLM
    
    # Comprobación de respuesta, verificación y posible reenvío hasta resultado satisfactorio

    # Envío al solver ASP

    return msg

if __name__ == "__main__":

    message = sys.stdin.readline().strip()
    response = procesa_mensaje(message)
    sys.stdout.write(response)