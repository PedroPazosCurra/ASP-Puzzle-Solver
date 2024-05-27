# IMPORTS
from PIL import Image, ImageDraw, ImageFont
from webcolors import name_to_rgb
import requests
import numpy as np
from io import BytesIO
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
def dibuja_datos(fondo, dibujo:ImageDraw.ImageDraw, coordenadas:tuple, tamaño:float, array_datos:list, array_rutas_imagenes:list):

    #print(f"Coordenadas {coordenadas}, tamaño {tamaño}, array datos {array_datos}, array_rutas {array_rutas_imagenes}\n")
    
    a, b = coordenadas
    c = a + tamaño*2
    d = b + tamaño*1.5

    fuente_letras = ImageFont.truetype("..../resources/fonts/OpenSans-Regular.ttf", size = tamaño*0.5)

    for i, dato in enumerate(array_datos):

        ruta_especificada = False
        
        # Para este dato, ¿tenemos ruta de imagen?
        for ruta in array_rutas_imagenes:

            if(ruta[0] == dato):
                ruta_especificada = True
                ruta_imagen = ruta[1]

        if ruta_especificada:

            # Busca la imagen. Si no existe, texto.
            try:

                img = Image.open(f'..../resources/atom_images/{ruta_imagen}.jpg')

                # Escala la imagen según tamaños
                wpercent = (tamaño / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((int(tamaño), hsize), Image.Resampling.LANCZOS)

                # Coloca la imagen donde toque
                fondo.paste(
                            box= (int(a + (c-a)/2 - tamaño*1.1), int(d + (d-b)*(0.75*i + 0.5)),  int((a + (c-a)/2 - tamaño*1.1) + int(tamaño)), int(d + (d-b)*(0.75*i + 0.5)) + hsize),
                            im= img
                            )
                
            except:

                # Dibuja texto
                dibujo.text(xy = (a + (c-a)/2 - tamaño*1.1, d + (d-b)*(0.75*i + 0.5)),
                            text = dato.capitalize() if (isinstance(dato, str)) else dato,
                            font= fuente_letras,
                            stroke_width= int(tamaño * 0.06),
                            stroke_fill= 'black'
                            )
            
        else:
            # Dibuja texto
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
                text = numero,
                font= fuente_numero,
                stroke_width= int(tamaño * 0.1),
                stroke_fill='black'
                )


def representa_casa(fondo, coordenadas, elems, tamaño, color = 'white', numero = '', rutas_imagenes = []):

    # Dibuja la casa
    dibuja_casa(dibujo_solucion, coordenadas, tamaño, color, numero)

    # Escribe los datos debajo de la casa
    dibuja_datos(fondo, dibujo_solucion, coordenadas, tamaño, elems, rutas_imagenes)


def representa_estado_inicial(casas, rutas_imagenes = []):

    dict_datos = defaultdict(list)         # Aquí van a ir recopilados los datos sin asociar a casas ("num" : [1,2,3]...)
    num_casas = len(casas)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_casas = (1.1**(-num_casas)) * 80

    # Para cada casa con índice i de la entrada
    for i, casa in enumerate(casas):

        # División de los 1000px que le toca a cada casa según cuántas casas hay
        division_casas = (1000/(num_casas+1)) * (i + 1)

        numero = ""
        if "house" in casa:
            numero = str(casa["house"])

            # Dibuja la casa en blanco
            dibuja_casa(dibujo_estado_inicial, coordenadas= (division_casas - tamaño_casas, 1000 - 6* tamaño_casas), tamaño= tamaño_casas, numero= numero)

            #TODO: Coger imagen de casa si se indica.

        # Recoge todos los datos de las casas y los almaceno por clave
        for key, value in casa.items():
            dict_datos[key].append(str(value))
        
    # Ya tengo los datos filtrados por clave
    num_datos = len(dict_datos)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_datos = (1.1**(-num_datos)) * 80

    for i, par in enumerate(dict_datos.items()):

        clave, valor = par

        division_datos = (1000/(num_datos+ 1)) * (i + 1)

        # Se prepara el array [clave, [valores...]]
        valor.insert(0, clave)

        dibuja_datos(fondo = fondo_estado_inicial,
                    dibujo= dibujo_estado_inicial,
                    tamaño= tamaño_datos,
                    coordenadas= (division_datos- tamaño_datos,100),
                    array_datos= valor,
                    array_rutas_imagenes= rutas_imagenes)

    return fondo_estado_inicial


def representa_solucion(casas, rutas_imagenes = []):

    num_casas = len(casas)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_casas = (1.1**(-num_casas)) * 80

    for i, casa in enumerate(casas):

        color = "white" 
        numero = ""


        # División de los 1000px que le toca a cada casa según cuántas casas hay
        division = (1000/(num_casas+1)) * (i + 1)

        # Argumentos de representa_casa (los quitamos del array casa porque ya no los queremos)
        if("house" in casa):
            numero = str(casa["house"])
            del casa["house"]
        
        if("color" in casa):
            color = str(casa["color"])
            del casa["color"]


        # Dibuja la casa y escribe sus datos
        representa_casa(fondo = fondo_solucion,
                        coordenadas = (division - tamaño_casas, 400),
                        numero = numero,
                        color = color,
                        tamaño=tamaño_casas,
                        elems = casa.values(),
                        rutas_imagenes= rutas_imagenes
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



# einstein_grafico: Función de nivel superior que se encarga del proceso del módulo gráfico.
#
#   Ejemplo de uso:
#
#   einstein_grafico(   array_has       = [['pedro', 'house', 1], ['pedro', 'drink', 'water']], 
#                       rutas_imagenes  = [['coffee', '/img/cafe.png']]
#                   )
#
def einstein_grafico(array_has, rutas_imagenes = []):

    tipo = ""
    casas = np.array([])

    # Ya tenemos un array de arrays de tres elementos correspondientes a todos los predicados has. Iteramos
    for entrada in array_has:

        #[brittish, color, red]
        persona = entrada[0]
        tipo = entrada[1]
        valor = entrada[2]

        persona_creada = False

        # ¿Esta persona está asignada a una casa en el array de diccionarios "casas[]"?
        for casa in casas:

            # Ya existe la casa de esta persona: se gestiona el predicado
            if(casa["person"] == persona):

                casa[tipo] = valor
                persona_creada = True

        # No existe la persona -> nueva casa
        if(persona_creada == False):

            nueva_casa = dict(person = persona)
            nueva_casa[tipo] = valor

            casas = np.append(casas, nueva_casa)


    # Ya tenemos un array de diccionarios con todos los datos de las casas. Ordenamos por número de casa (si es posible) y representamos. Añadimos el array de urls de imágenes
    if(all("house" in casa for casa in casas)):
        casas = sorted(casas, key=lambda d: d['house'])
    representa_estado_inicial(casas, rutas_imagenes).save("resources/tmp/estado_inicial_einstein.png")
    representa_solucion(casas, rutas_imagenes).save("resources/tmp/solucion_einstein.png")



################################################  Debug   ##########################################################

#as_prueba = [['juan', 'house', 4], ['pedro', 'house', 1], ['pedro', 'inventado', 'inventado'], ['chema', 'house', 5], ['pedro', 'car', 'ford'], ['spanish','house', 1], ['spanish','color','red'], ['spanish','pet','dog'], ['spanish','tobacco','ducados'], ['spanish','beverage','agua'], ['english','house',2], ['english','color','blue'], ['english','pet','giraffe'], ['english','beverage','horchata']]
#einstein_grafico(as_prueba, [['dog', 'cocacola']])


casa1 = {
    "house": 1,
    "person": "brittish",
    "color": "red",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa2 = {
    "house": 2,
    "person": "norwegian",
    "color": "blue",
    "pet": "cat",
    "beverage": "coffee",
    "tobacco": "camel"
}
casa3 = {
    "house": 3,
    "person": "french",
    "color": "yellow",
    "pet": "horse",
    "beverage": "wine",
    "tobacco": "marlboro"
}
casa4 = {
    "house": 4,
    "person": "brittish",
    "color": "white",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa5 = {
    "house": 5,
    "person": "brittish",
    "color": "purple",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "winston"
}
casa6 = {
    "house": 6,
    "person": "brittish",
    "color": "pink",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "bluem"
}
casa7 = {
    "house": 7,
    "person": "brittish",
    "color": "beige",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa8 = {
    "house": 8,
    "person": "brittish",
    "color": "green",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa9 = {
    "house": 9,
    "person": "brittish",
    "color": "cyan",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa10 = {
    "house": 10,
    "person": "brittish",
    "color": "black",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
}

#casas = [casa1, casa2, casa3]
#casas = [casa1, casa2, casa3, casa4, casa5, casa6]
#casas = [casa1, casa2, casa3, casa4, casa5, casa6, casa7, casa8, casa9, casa10]

#representa_estado_inicial(casas)
#representa_solucion(casas)

# Enseña la imagen por pantalla
#fondo_estado_inicial.show()
#fondo_solucion.show()