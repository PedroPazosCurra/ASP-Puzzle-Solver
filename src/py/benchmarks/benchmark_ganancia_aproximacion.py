# Test de ganancia de la aproximación neurosimbólica
# Objetivo: Medir la ventaja del sistema neurosimbólico frente a la solución del modelo de lenguaje puro.
#

# Imports
import os
import sys
from os import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from NL_to_ASP import NL_to_ASP
from resolver_ASP import resolver_ASP
from AS_to_NL import AS_to_NL


# Pruebas (en este caso, hay que ejecutarlas de forma manual)
prueba_1 = "Einstein | There are two houses, and two people: a German and a English. One house is painted Red and the other one is colored Purple. The German lives in the Red house."
prueba_2 = "Einstein | There are three houses. In them live a Spanish, an English and a Chinese. The houses are painted Red, Blue and Purple. There are three pets: a Dog, a Cat and a Duck. There are 3 tobacco brands: Ducados, Camel and Blue Master. There are also three drinks: Coffee, Water and Tea. The Spanish man house is painted Red, while the English man house is tainted Blue. The house of the Chinese man is Purple. The Spanish man keeps a Dog. The Chinese man loves to drink Tea. The Spanish one, on the other hand, smokes Ducados."
prueba_3 = "Einstein |  There are three houses. In them live a Spanish, an English and a Chinese. There are three pets: a Dog, a Cat and a Duck. The houses are painted Red, Blue and Purple. There are 3 tobacco brands: Ducados, Camel and Blue Master. There are also three drinks: Coffee, Water and Tea. The Spanish man house is painted Red, while the English house is tainted Blue. The Chinese man loves to drink Tea. The owner of the Purple house has a Duck pet. "
prueba_4 = "Einstein | There are three boats: one is Red, other is Purple and the other one is Green. There are a Spanish, an English and a Chinese. There are three drinks: Tea, Milk and Soda. The Spanish man drinks Soda. There's a Dog, a Cat and a Horse. The Spanish keeps the Cat, while the English man has a Dog. The Spanish man has a Red boat. The Chinese man, on the other hand, lives in a Purple boat."
prueba_5 = "Einstein | There are five houses: one is Yellow, other is Green, other is White, other is Red and the other is Blue. There's an British, a Danish, a German, a Norwegian and a Swedish. There are five pets: a Dog, a Fish, a Bird, a Horse and a Cat. The drinks are Beer, Coffee, Tea, Milk and Water. The tobacco brands are Blends, Blue Master, Dunhill, Pall Mall and Prince. The British lives in the Red house. The Swedish has a Dog. The Danish drinks Tea. The Green house is to the left of the White house. The owner of the Green house drinks Coffee. The person who smokes Pall Mall keeps a Bird. The owner of the Yellow house smokes Dunhill. The man living in the house number 3 drinks Milk. The Norwegian lives in the first house. The man who smokes Blends is neighbor of the one who keeps a Cat. The man who keeps a Horse lives next to the man who smokes Dunhill. The man who smokes Blue Master drinks Beer. The German smokes Prince. The Norwegian lives next to the Blue house. The man who smokes Blends has a neighbor who drinks Water."
prueba_6 = "Einstein | There are five houses: one is Gold, other is Olive, other is Ivory, other is Crimson and the other is Indigo. There's an Irish, a Welsh, a Scottish, a Belgian and a Moroccan. There are five pets: a Dragon, a Gryphon, a Wyvern, a Chimera and a Wyrm. The drinks present are Wine, Whiskey, Gin, Vodka and Vermut. The tobacco brands are Ducados, Camel, Winston, Pueblo and Lucky Strike. The Irish lives in the Crimson house. The Moroccan has a Dragon. The Welsh drinks Gin. The Olive house is to the left of the Ivory house. The owner of the Olive house drinks Whiskey. The person who smokes Pueblo keeps the Wyvern. The owner of the Gold house smokes Winston. The man living in the house number 3 drinks Vodka. The Belgian lives in the first house. The man who smokes Ducados is neighbor of the one who keeps a Wyrm. The man who keeps a Chimera lives next to the man who smokes Winston. The man who smokes Camel drinks Wine. The Scottish smokes Lucky Strike. The Belgian lives next to the Indigo house. The man who smokes Ducados has a neighbor who drinks Vermut."
prueba_7 = "Einstein | There are five houses whose colours are Gold, Olive, Ivory, Crimson and Indigo. In these houses live an Irish, a Welsh, a Scottish, a Belgian and a Moroccan. Five pets are kept: a Dragon, a Gryphon, a Wyvern, a Chimera and a Wyrm. Five drinks are drunk: Wine, Whiskey, Gin, Vodka and Vermut. The following brands are smoked: Ducados, Camel, Winston, Pueblo and Lucky Strike. The Crimson house is the home of the Irish. The Dragon is kept by the Moroccan. The Welsh's drink is Gin. The Ivory house is to the right of the Olive house. Whiskey is drunk in the Olive house. The Wyvern is kept in the house of the Pueblo smoker. The Winston smoker lives in the Gold house. Vodka is drunk in the third house. The Belgian lives in the house number 1. The Ducados smoker lives next to the one who keeps a Wyrm. The Chimera owner is neighbor of the Winston smoker. The Wine drinker is also a Camel smoker. The Scottish is a Lucky Strike smoker. The Indigo house is next to the house of the Belgian. The Ducados smoker has a neighbor who is a Vermut drinker."
prueba_8 = "Einstein | There are 20 houses. They are painted of the colors: Black, Blue, Purple, Magenta, Navy, Yellow, Ocre, White, Maroon, Ivory, Lime, Cyan, Rose, Pink, Grey, Green, Brown, Violet, Olive and Mustard. The people are a Dominican man, a Nicaraguan, a British, a Irish, a Norwegian, a Spanish, a Portuguese, a Chilean, a Peruvian, a Ecuatorian, an Italian, a German, a Belgian, a Swedish, a Swiss, a Greek, a Russian, an Ukranian, a Palestinian and a French."
prueba_9 = "Comensales | In this table there are 4 people sitting: Jose, Martina, Claudia and Pedro. The languages spoken in the table are German, Spanish and Arabic. Pedro and Jose speak Arabic. Claudia speaks Spanish and Martina speaks German."
prueba_10 = "Comensales | There are 3 people about to sit in a table: Juan, who speaks Spanish, Maria and Sofia. Both Maria and Sofia want to sit next to someone who speaks Spanish."
prueba_11 = "Comensales | In this table there are 4 people sitting: Jose, Martina, Claudia and Pedro. The languages spoken in the table are German, Spanish and Arabic. Pedro and Jose speak Arabic. Claudia speaks Spanish and Martina speaks German. Claudia refuses to sit next to Pedro. Pedro, on the other hand, wants to sit next to someone who speaks Arabic. Martina wants Jose to be on the opposite side of the table."
prueba_12 = "Comensales | In this table there are 10 people sitting: Alberto, Carlos, Carolina, Paco, Lucia, Isabel, Jose, Martina, Claudia and Pedro. The languages spoken in the table are German, Spanish, Galician, Catalan, Basque, French, English and Arabic. Pedro and Jose speak Arabic. Claudia speaks Spanish and Martina speaks German. Claudia refuses to sit next to Pedro. Pedro, on the other hand, wants to sit next to someone who speaks Arabic. Martina wants Jose to be on the opposite side of the table. Alberto only agrees to sit if Carolina is on the opposite side of the table. Isabel speaks French and wants to sit next to Pedro. Paco wants Lucía sitting on the opposite end of the table. Claudia wants to sit next to Carlos. Carolina speaks Basque and needs to sit next to someone who speaks French."
prueba_13 = "Comensales | In this table there are 25 people: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X and Y. The languages that are spoken are Spanish, Italian, German, Esperanto, Galician, English, Brazilian, Portuguese and French. A, D and C speak Brazilian. B, T and S are Spanish speakers."

pruebas = [prueba_9, prueba_10, prueba_11, prueba_12, prueba_13]

# Proceso
for i, prueba in enumerate(pruebas):

    puzzle, prompt = prueba.split("|")
    puzzle = puzzle.strip()
    prompt = prompt.strip()

    log = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/txt/benchmark_ganancia_aproximacion.txt")), "a")
    log.write(f"\n\n##################   Prueba {i}   ##################\n[# Entrada] - {prompt}\n")
    log.close()


    # LLM Puro
    try:
        [estado, salida_llm_puro] = NL_to_ASP(prompt, puzzle, True)

        print(f"[# Salida Puro] - {salida_llm_puro}\n")
        log = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/txt/benchmark_ganancia_aproximacion.txt")), "a")
        log.write(f"[# Salida Puro] - {salida_llm_puro} \n") 
        log.close()

    except Exception as e:
        log = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/txt/benchmark_ganancia_aproximacion.txt")), "a")
        log.write(f"[# Salida Puro] - FALLO {e}\n")
        log.close()


    # Sistema neurosimbólico
    estado = 0
    try:
        [estado, salida_llm] = NL_to_ASP(prompt, puzzle, False)
        if estado != 0: raise Exception(salida_llm)

        [estado, salida_solver, _] = resolver_ASP(salida_llm, puzzle)
        if estado != 0: raise Exception(salida_solver + "\n" + salida_llm)

        [estado, salida_llm_2] = AS_to_NL(salida_solver, puzzle)
        if estado != 0: raise Exception(salida_llm_2 + "\n" + salida_solver)

        print(f"[# Salida Sis. Neurosim.] - {salida_llm_2}\n")
        log = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/txt/benchmark_ganancia_aproximacion.txt")), "a")
        log.write(f"[# Salida Sis. Neurosim. [1]] - {salida_llm} \n") 
        log.write(f"[# Salida Sis. Neurosim. [2]] - {salida_solver} \n") 
        log.write(f"[# Salida Sis. Neurosim. [3]] - {salida_llm_2} \n") 
        log.close()

    except Exception as e:
        log = open(path.abspath(path.join(path.dirname(__file__), "..", "../../resources/txt/benchmark_ganancia_aproximacion.txt")), "a")
        log.write(f"[# Salida Sis. Neurosim.] - FALLO {e} \n")
        log.close()