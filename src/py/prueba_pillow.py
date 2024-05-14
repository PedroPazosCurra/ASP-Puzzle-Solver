# IMPORTS
from PIL import Image, ImageDraw, ImageFont
from webcolors import name_to_rgb


# CONSTANTES
tamaño = 70

# Crea nueva imagen importándola. La imagen es 1000x1000
fondo = Image.open('..../resources/img/fondo_imagen_generada.png')

# Crea objeto Draw
dibujo = ImageDraw.Draw(fondo)

def haz_casita(coordenadas, numero, persona, bebida, mascota, tabaco, color, tamaño):

    # En base al nombre del color, una librería pasa un rgb. Si no puede, gris.
    try:
        color_casa = name_to_rgb(color)
    except ValueError:
        color_casa = (105,105,105)

    a, b = coordenadas
    c = a + tamaño*2
    d = b + tamaño*1.5

    # Dibuja la casa
    dibujo.rectangle(xy = (a, b, c, d),
                    fill = color_casa,
                    outline = 'black')

    dibujo.polygon([(a - tamaño*0.2, b), (c + tamaño*0.2, b), ((c + a)/2, b - tamaño*1.3)], fill = color_casa, outline = 'black')

    # Crea elemento fuente
    fuente = ImageFont.truetype("..../resources/fonts/OpenSans-Regular.ttf", size = tamaño*0.55)
    
    # Dibuja el número de la casa
    dibujo.text(xy = (a + (c-a)/2 - tamaño*0.2, b + (d-b)/4),
                text = str(numero),
                font= fuente,
                stroke_width=2,
                stroke_fill='black'
                )
    
    # Escribe la persona
    dibujo.text(xy = (a + (c-a)/2 - tamaño, d + (d-b)*0.5),
                text = persona,
                font= fuente,
                stroke_width=2,
                stroke_fill='black'
                )
    
    # Escribe la mascota
    dibujo.text(xy = (a + (c-a)/2 - tamaño, d + (d-b)),
                text = mascota,
                font= fuente,
                stroke_width=2,
                stroke_fill='black'
                )
    
    # Escribe la bebida
    dibujo.text(xy = (a + (c-a)/2 - tamaño, d + (d-b)*1.5),
                text = bebida,
                font= fuente,
                stroke_width=2,
                stroke_fill='black'
                )
    
    # Escribe el tabaco
    dibujo.text(xy = (a + (c-a)/2 - tamaño, d + (d-b)*2),
                text = tabaco,
                font= fuente,
                stroke_width=2,
                stroke_fill='black'
                )

def haz_casitas(casas):

    num_casas = len(casas)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_casas = (1.1**(-num_casas)) * 80

    for i, casa in enumerate(casas):

        haz_casita(coordenadas= ((1000/(num_casas+1)) * (i + 1) - tamaño, 400),
                    numero= casa["num"],
                    persona=casa["person"],
                    bebida=casa["beverage"],
                    mascota=casa["pet"],
                    tabaco=casa["tobacco"],
                    color= casa["color"],
                    tamaño= tamaño_casas)

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
    "tobacco": "ducados"
}
casa6 = {
    "num": 6,
    "person": "brittish",
    "color": "pink",
    "pet": "dog",
    "beverage": "milk",
    "tobacco": "ducados"
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

casas = [casa1, casa2, casa3]
#casas = [casa1, casa2, casa3, casa4, casa5, casa6]
#casas = [casa1, casa2, casa3, casa4, casa5, casa6, casa7, casa8, casa9, casa10]
haz_casitas(casas)

# Enseña la imagen por pantalla
fondo.show()