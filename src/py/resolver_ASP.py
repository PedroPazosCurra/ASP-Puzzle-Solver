import sys
import clingo
from os import path

def resolver_ASP(salida_llm, clingo_args = []):

    cc = clingo.Control(clingo_args)

    ruta_asp = path.abspath(path.join(path.dirname(__file__), "..", "../resources/txt/asp_einstein.txt"))
    cc.load(ruta_asp)

    cc.add('base', [], salida_llm)
    cc.ground([("base",[])])

    def onmodel(m):
        print(m)

    print(cc.solve(on_model=onmodel))

if __name__ == '__main__':
    resolver_ASP("hola(pedro). person(brit;swede;dane;german;norw). color(red;white;blue;green;yellow). beverage(water;tea;beer;milk;coffee). tobaccobrand(prince;pall;blends;dunhill;bluem). pet(fish;horse;dog;bird;cat). house(1..5).")
