# IMPORTS
from PIL import Image, ImageDraw, ImageFont
from webcolors import name_to_rgb
import re
import numpy as np
from collections import defaultdict


######################################### Constantes y variables ##############################################
TAMAÑO_DEFAULT = 70

# Crea nueva imagen importándola. La imagen es 1000x1000
fondo_estado_inicial = Image.open('..../resources/img/fondo_imagen_generada.png')
fondo_solucion = Image.open('..../resources/img/fondo_imagen_generada.png')

# Crea objeto Draw
dibujo_estado_inicial = ImageDraw.Draw(fondo_estado_inicial)
dibujo_solucion = ImageDraw.Draw(fondo_solucion)


######################################### Funciones ##############################################

# Función auxiliar que dibuja un array de texto en determinadas coordenadas y tamaño. 
def dibuja_datos(dibujo, coordenadas, tamaño, array_datos):

    a, b = coordenadas
    c = a + tamaño*2
    d = b + tamaño*1.5

    fuente_letras = ImageFont.truetype("..../resources/fonts/OpenSans-Regular.ttf", size = tamaño*0.5)

    for i, dato in enumerate(array_datos):

        # Escribe
        dibujo.text(xy = (a + (c-a)/2 - tamaño*1.1, d + (d-b)*(0.75*i + 0.5)),
                    text = dato.capitalize() if (isinstance(dato, str)) else dato,
                    font= fuente_letras,
                    stroke_width= int(tamaño * 0.06),
                    stroke_fill= 'black'
                    )

# Función auxiliar que dibuja una casa en determinadas coordenadas, tamaño, color y número. 
def dibuja_casa(dibujo, coordenadas, tamaño, color = 'white', numero = ''):

    # En base al nombre del color, una librería pasa un rgb. Si no puede, gris.
    try:
        color_casa = name_to_rgb(color)
    except ValueError:
        color_casa = (255,255,255)

    a, b = coordenadas
    c = a + tamaño*2
    d = b + tamaño*1.15

    # Dibuja la casa
    dibujo.polygon([(a - tamaño*0.3, b), (a,b), (a,d), (c,d), (c,b), (c + tamaño*0.3, b), ((c + a)/2, b - tamaño*1.3)],
                    fill = color_casa,
                    outline = 'black',
                    width= int(tamaño * 0.1))

    # Crea elemento fuente
    fuente_numero = ImageFont.truetype("..../resources/fonts/OpenSans-Regular.ttf", size = tamaño*0.8)
    
    # Dibuja el número de la casa
    dibujo.text(xy = (a + (c-a)/2 - tamaño*0.25, b - tamaño*0.2 ),
                text = str(numero),
                font= fuente_numero,
                stroke_width= int(tamaño * 0.1),
                stroke_fill='black'
                )
    

def representa_casa(coordenadas, persona, bebida, mascota, tabaco, tamaño, color = 'white', numero = ''):

    # Dibuja la casa
    dibuja_casa(dibujo_solucion, coordenadas, tamaño, color, numero)

    # Escribe los datos debajo de la casa
    dibuja_datos(dibujo_solucion, coordenadas, tamaño, [persona, bebida, mascota, tabaco])


def representa_estado_inicial(casas):

    dict_datos = defaultdict(list)         # Aquí van a ir recopilados los datos sin asociar a casas ("num" : [1,2,3]...)
    num_casas = len(casas)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_casas = (1.1**(-num_casas)) * 80

    # Para cada casa con índice i de la entrada
    for i, casa in enumerate(casas):

        # División de los 1000px que le toca a cada casa según cuántas casas hay
        division_casas = (1000/(num_casas+1)) * (i + 1)
        
        # Dibuja la casa en blanco
        dibuja_casa(dibujo_estado_inicial, coordenadas= (division_casas - tamaño_casas, 1000 - 6* tamaño_casas), tamaño= tamaño_casas, numero= casa["num"])

        # Recoge todos los datos de las casas y los almaceno por clave
        for key, value in casa.items():
            dict_datos[key].append(str(value))
        
    # Ya tengo los datos filtrados por clave
    num_datos = len(dict_datos)


    tamaño_datos = (1.1**(-num_datos)) * 80

    for i, par in enumerate(dict_datos.items()):

        clave, valor = par
        print(clave)
        print(valor)

        division_datos = (1000/(num_datos+ 1)) * (i + 1)

        # Se prepara el array [clave, [valores...]]
        valor.insert(0, clave)

        dibuja_datos(dibujo= dibujo_estado_inicial,
                    tamaño= tamaño_datos,
                    coordenadas= (division_datos- tamaño_datos,100),
                    array_datos= valor)

    return fondo_estado_inicial


def representa_solucion(casas):

    num_casas = len(casas)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_casas = (1.1**(-num_casas)) * 80

    for i, casa in enumerate(casas):

        # División de los 1000px que le toca a cada casa según cuántas casas hay
        division = (1000/(num_casas+1)) * (i + 1)

        # Dibuja la casa y escribe sus datos
        representa_casa(coordenadas= (division - tamaño_casas, 400),
                    numero = casa["num"] if ("num" in casa) else '',
                    persona = casa["person"] if ("person" in casa) else "",
                    bebida= casa["beverage"] if ("beverage" in casa) else "",
                    mascota = casa["pet"] if ("pet" in casa) else "",
                    tabaco = casa["tobacco"] if ("tobacco" in casa) else "",
                    color = casa["color"] if ("color" in casa) else "white",
                    tamaño = tamaño_casas       
                    )
        
        # Dibuja separador
        dibujo_solucion.line(xy= [(division - tamaño_casas*1.25 - 1.068**tamaño_casas, 420), (division - tamaño_casas*1.25 - 1.068**tamaño_casas, 340 + 8*tamaño_casas)],
                width= int(1.03**tamaño_casas),
                fill= 'gray')
        
    # Dibuja último separador
    dibujo_solucion.line(xy= [(((1000/(num_casas+1)) * (num_casas + 1)) - tamaño_casas*1.25 - 1.068**tamaño_casas, 420), (((1000/(num_casas+1)) * (num_casas + 1)) - tamaño_casas*1.25 - 1.068**tamaño_casas, 340 + 8*tamaño_casas)],
            width= int(1.03**tamaño_casas),
            fill= 'gray')
    
    return fondo_solucion


def einstein_grafico(answer_set):

    regex = r"\(([^)]+)\)"
    array_has = []
    casas = np.array([])

    # Extraer las palabras usando el patrón 
    matches_regex = re.findall(regex, answer_set)

    for matched in matches_regex:
        array_has.append(matched.split(","))

    # Ya tenemos un array de arrays de tres elementos correspondientes a todos los predicados has. Iteramos
    for entrada in array_has:

        #
        #np.where(casas["person"] == entrada[0])

        persona_creada = False

        # ¿Esta persona está asignada a una casa en el array de diccionarios "casas[]"?
        for casa in casas:

            # Ya existe la casa de esta persona: se gestiona el predicado
            if(casa["person"] == entrada[0]):

                match entrada[1]:
                    case "house":    casa["num"]      =   entrada[2]
                    case "color":    casa["color"]    =   entrada[2]
                    case "pet":      casa["pet"]      =   entrada[2]
                    case "beverage": casa["beverage"] =   entrada[2]
                    case "tobacco":  casa["tobacco"]  =   entrada[2]

                persona_creada = True

        # No existe la persona -> nueva casa
        if(persona_creada == False):

            nueva_casa = dict(person = entrada[0])

            match entrada[1]:
                case "house":    nueva_casa["num"]      =   entrada[2]
                case "color":    nueva_casa["color"]    =   entrada[2]
                case "pet":      nueva_casa["pet"]      =   entrada[2]
                case "beverage": nueva_casa["beverage"] =   entrada[2]
                case "tobacco":  nueva_casa["tobacco"]  =   entrada[2]

            casas = np.append(casas, nueva_casa)



    # Ya tenemos un array de diccionarios con todos los datos de las casas. Ordenamos por número y representamos.
    casas = sorted(casas, key=lambda d: d['num'])
    representa_estado_inicial(casas).save("resources/tmp/estado_inicial_einstein.png")
    representa_solucion(casas).save("resources/tmp/solucion_einstein.png")



################################################  Debug   ##########################################################

casa1 = {
    "num": 1,
    "person": "brittish",
    "color": "red",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa2 = {
    "num": 2,
    "person": "norwegian",
    "color": "blue",
    "pet": "cat",
    "beverage": "coffee",
    "tobacco": "camel"
}
casa3 = {
    "num": 3,
    "person": "french",
    "color": "yellow",
    "pet": "horse",
    "beverage": "wine",
    "tobacco": "marlboro"
}
casa4 = {
    "num": 4,
    "person": "brittish",
    "color": "white",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa5 = {
    "num": 5,
    "person": "brittish",
    "color": "purple",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "winston"
}
casa6 = {
    "num": 6,
    "person": "brittish",
    "color": "pink",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "bluem"
}
casa7 = {
    "num": 7,
    "person": "brittish",
    "color": "beige",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa8 = {
    "num": 8,
    "person": "brittish",
    "color": "green",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa9 = {
    "num": 9,
    "person": "brittish",
    "color": "cyan",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa10 = {
    "num": 10,
    "person": "brittish",
    "color": "black",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}

#casas = [casa1, casa2, casa3]
#casas = [casa1, casa2, casa3, casa4, casa5, casa6]
#casas = [casa1, casa2, casa3, casa4, casa5, casa6, casa7, casa8, casa9, casa10]

as_prueba = "has(spanish,house,3). has(spanish,color,red). has(spanish,pet,dog). has(spanish,tobacco,ducados). has(spanish,beverage,agua). has(english,house,2). has(english,color,blue). has(english,pet,giraffe). has(english,beverage,horchata)."
einstein_grafico(as_prueba)

#representa_estado_inicial(casas)
#representa_solucion(casas)

# Enseña la imagen por pantalla
#fondo_estado_inicial.show()
#fondo_solucion.show()