# Imports
from os import path
import re
from utils.llamada_llm import llamada_llm

# Constantes
ASP_REGEX_LIGERO = r"(([a-z\_]+\(([a-z\_]+\,\s?[V])\)\s:-\s[a-z\_]+\([A-Z]\)\.?\s?)|(\s?[a-z\_]+\([0-9]+\.\.[0-9]+\)\.?\s?)|(\s?[a-z\_]+\((\s?[a-z\_]+\;?\s?)+\)\.?\s?)|(\s?[a-z\_]+\(([a-z\_0-9]+\s?\,?\s?)+\)\.?\s?))+"
ASP_REGEX_ESTRICTO_EINSTEIN = r"^((living_place\(([a-z\_]+\,\s?[V])\)\s:-\s[a-z\_]+\([V]\)\.?\s?)|(type\(([a-z\_]+\,\s?V)\)\s:-\s[a-z\_]+\(V\)\.?\s?)|(\s?[a-z\_]+\([0-9]+\.\.[0-9]+\)\.?\s?)|(\s?[a-z\_]+\((\s?[a-z\_]+\s?\;?\s?)+\)\.?\s?)|(\s?(living_place|image|left|right|next_to|same_place)\(([a-z\_0-9]+\s?\,?\s?)+\)\.?\s?))+$"

def NL_to_ASP(prompt : str = None, puzzle : str = None, llm_puro_flag : bool = False):
   
    ###  Preprocesado:
    # Sale con error si alguno de los args es nulo
    if ((prompt == None) or (puzzle == None)): return([1, "NL_to_ASP recibe una entrada con uno de los valores nulos."])

    # Flag de iteración con LLM Puro?
    if llm_puro_flag: 

        contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/einstein_puro.txt"))
        with open(contexto_zeroshot_path, 'r') as file: zeroshot = file.read()
        fewshot = "\nIN: "

    else:
        # Leemos /resources/ctx... para tener el contexto para few-shot learning
        match puzzle:
            case "Einstein":
                contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/zero_einstein_to_ASP.txt"))
                contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/einstein_to_ASP.txt"))
            case "Comensales":
                contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/comensales/zero_comensales_to_ASP.txt"))
                contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/comensales/comensales_to_ASP.txt"))
            case _:
                return([1, "En NL_to_ASP.py, se recibe un puzzle que no existe: "+ puzzle + ". Vigila que se pase bien."])
        
        # Construcción de prompt
        with open(contexto_zeroshot_path, 'r') as file: zeroshot = file.read()
        with open(contexto_path, 'r') as file: fewshot = file.read()

    contexto_fewshot = zeroshot + fewshot
    prompt_w_context = f"{contexto_fewshot} {prompt}\nOUT: "

    ###  Petición a la API del LLM
    estado_peticion, salida_llm = llamada_llm(prompt=prompt_w_context, temperatura= 0.7)

    # Caso de error de peticion API LLM
    if (estado_peticion == 1): return([1, salida_llm])


    ###  Postprocesado:

    # Sale sin postprocesado si flag de iteración pura
    if(llm_puro_flag): return[1, salida_llm]

    # Preprocesado de caracteres extraños que a veces el LLM mete por formato. También estructuras ilegales en el programa ASP, por mejorar resultados marginalmente.
    if (salida_llm.find("`") != -1):
        salida_llm = salida_llm.replace("`", "")
    if (salida_llm.find("),") != -1):
        salida_llm = salida_llm.replace("),", ").")
    if (salida_llm.find("type(person, V) :- person(V).") != -1):
        salida_llm = salida_llm.replace("type(person, V) :- person(V).", "")

    salida_llm = salida_llm.strip()    # A veces se olvida de poner el punto en el último predicado.
    if (salida_llm[-1] != "."):
        salida_llm += "."

    # Comprobación de respuesta válida mediante REGEX con sintaxis ASP. Nota: REGEX en dos niveles para filtrar preámbulos y coletillas en nivel ligero y filtrar comandos erróneos en nivel estricto.
    
    try:
        match_regex_ligero = re.search(ASP_REGEX_LIGERO, salida_llm, flags=0).group()
        
        if(puzzle == "Einstein"):
            match_regex_estricto_einstein = re.search(ASP_REGEX_ESTRICTO_EINSTEIN, match_regex_ligero, flags=0).group()
            if match_regex_estricto_einstein == match_regex_ligero: 
                return([0, match_regex_estricto_einstein])

        elif(puzzle == "Comensales" and match_regex_ligero):
            return([0, match_regex_ligero])
            
        else:
            return([1, "Lo siento, no soy capaz de procesar esto. Por favor, reescribe tu puzzle explicando el estado de forma precisa o usando otras palabras. " + salida_llm])
    except:
        return([1, "Lo siento, no soy capaz de procesar esto. Por favor, reescribe tu puzzle explicando el estado de forma precisa o usando otras palabras. " + salida_llm])

        
# Logs para debug
#print("[Context]  " + contexto)
#print("[Prompt]  " +  prompt)
#print("[Answer]  " + json_res['choices'][0]['text'])
