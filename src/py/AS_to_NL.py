# Imports
from os import path
from utils.llamada_llm import llamada_llm

def AS_to_NL(input_answer_set = None, puzzle_elegido = None):
    
    # Sale con error si alguno de los args es nulo
    if ((input_answer_set == None) or (puzzle_elegido == None)): return([1, "AS_to_NL recibe una entrada con uno de los valores nulos."])
    
    # Leemos /resources/txt/ctx... para tener el contexto para few-shot learning
    match puzzle_elegido:
        case "Einstein":
            contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/zero_einstein_to_NL.txt"))
            contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/einstein/einstein_to_NL.txt"))
        case "Comensales":
            contexto_zeroshot_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/comensales/zero_comensales_to_NL.txt"))
            contexto_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/ctx/comensales/comensales_to_NL.txt"))
        case _:
            return([1, "En AS_to_NL.py, se recibe un puzzle que no existe: " + puzzle_elegido + ". Vigila que se pase bien."])
    
    # Construcción de prompt
    with open(contexto_zeroshot_path, 'r') as file_zero: zeroshot = file_zero.read()
    with open(contexto_path, 'r') as file_few: fewshot = file_few.read()

    contexto_fewshot = zeroshot + fewshot

    # Zero-shot o Few-shot?
    contexto = contexto_fewshot
    
    # Construcción de prompt completo
    prompt_w_context = contexto + input_answer_set +"\nOUT: "

    ###  Petición a la API del LLM
    estado_peticion, salida_llm = llamada_llm(prompt=prompt_w_context, temperatura= 0.7)

    # Caso de error de peticion API LLM
    if (estado_peticion == 1): return([1, salida_llm])

    if (salida_llm == ""):
        return([1, "El puzzle tiene una solucion y la he encontrado, pero no soy capaz de explicarla en lenguaje natural. El Answer Set encontrado, de todas formas, es: " + input_answer_set])
    else:
        return([0, salida_llm])
