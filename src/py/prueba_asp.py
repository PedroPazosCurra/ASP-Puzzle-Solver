# Nota: Este programa se borrará así avance el proyecto. Tiene un valor puramente ejemplar.

# Imports
import sys
import clingo
from os import path

reglas_einstein = path.abspath(path.join(path.dirname(__file__), "..", "../resources/asp/asp_einstein.lp"))

cc = clingo.Control(["--warn=none"])

try:
    cc.add('base', [], "house(1..3). person(congolese; chinese; irish).")
    cc.ground([("base",[])])
except:
    print("Ha habido un problema en el grounding")
    

solve_handle = cc.solve(yield_= True)

for model in solve_handle:
    print(model)
