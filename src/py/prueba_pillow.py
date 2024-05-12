# IMPORTS
from PIL import Image, ImageDraw, ImageFont
from webcolors import name_to_rgb


# CONSTANTES
SIZE = 70

# Crea nueva imagen importándola. La imagen es 1000x1000
fondo = Image.open('..../resources/img/fondo_imagen_generada.png')

# Crea elemento fuente
fuente = ImageFont.truetype("..../resources/fonts/OpenSans-Regular.ttf", size = SIZE*0.5)

# Crea objeto Draw
dibujo = ImageDraw.Draw(fondo)

def haz_casita(coordenadas, numero, color):

    color_casa = name_to_rgb(color)

    a, b = coordenadas
    c = a + SIZE*2
    d = b + SIZE*1.5


    dibujo.rectangle(xy = (a, b, c, d),
                    fill = color_casa,
                    outline = 'black')

    dibujo.polygon([(a - SIZE*0.2, b), (c + SIZE*0.2, b), ((c + a)/2, b - SIZE*1.3)], fill = color_casa, outline = 'black')

    
    dibujo.text(xy = (a + (c-a)/2 - SIZE*0.2, b + (d-b)/4),
                text = str(numero),
                font= fuente,
                stroke_width=2,
                stroke_fill='black'
                )

def haz_casitas(casas):

    num_casas = len(casas)

    for i, casa in enumerate(casas):

        haz_casita(((1000/num_casas+1) * i, 300), casa["num"], casa["color"])

casa1 = {
    "num": 1,
    "person": "brittish",
    "color": "red",
    "beverage": "milk",
    "tobacco": "ducados"
}
casa2 = {
    "num": 2,
    "person": "brittish",
    "color": "blue",
    "beverage": "milk",
    "tobacco": "ducados"
}

casas = [casa1, casa2]
haz_casitas(casas)

# Enseña la imagen por pantalla
fondo.show()