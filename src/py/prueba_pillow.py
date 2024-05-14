# IMPORTS
from PIL import Image, ImageDraw, ImageFont
from webcolors import name_to_rgb


# CONSTANTES
tamaño = 70

# Crea nueva imagen importándola. La imagen es 1000x1000
fondo = Image.open('..../resources/img/fondo_imagen_generada.png')

# Crea objeto Draw
dibujo = ImageDraw.Draw(fondo)

def dibuja_datos(coordenadas, tamaño, fuente, array_datos):

    a, b = coordenadas
    c = a + tamaño*2
    d = b + tamaño*1.5

    for i, dato in enumerate(array_datos):

        # Escribe
        dibujo.text(xy = (a + (c-a)/2 - tamaño*1.1, d + (d-b)*(0.75*i + 0.5)),
                    text = dato.capitalize(),
                    font= fuente,
                    stroke_width= int(tamaño * 0.06),
                    stroke_fill= 'black'
                    )


def representa_casa(coordenadas, numero, persona, bebida, mascota, tabaco, color, tamaño):

    # En base al nombre del color, una librería pasa un rgb. Si no puede, gris.
    try:
        color_casa = name_to_rgb(color)
    except ValueError:
        color_casa = (105,105,105)

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
    

    fuente_letras = ImageFont.truetype("..../resources/fonts/OpenSans-Regular.ttf", size = tamaño*0.5)

    # Escribe los datos debajo de la casa
    dibuja_datos(coordenadas, tamaño, fuente_letras, [persona, bebida, mascota, tabaco])


def representa_solucion(casas):

    num_casas = len(casas)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_casas = (1.1**(-num_casas)) * 80

    for i, casa in enumerate(casas):

        # División de los 1000px que le toca a cada casa según cuántas casas hay
        division = (1000/(num_casas+1)) * (i + 1)

        # Dibuja la casa y escribe sus datos
        representa_casa(coordenadas= (division - tamaño_casas, 400),
                    numero= casa["num"],
                    persona=casa["person"],
                    bebida=casa["beverage"],
                    mascota=casa["pet"],
                    tabaco=casa["tobacco"],
                    color= casa["color"],
                    tamaño= tamaño_casas)
        
        # Dibuja separador
        dibujo.line(xy= [(division - tamaño_casas*1.25 - 1.068**tamaño_casas, 420), (division - tamaño_casas*1.25 - 1.068**tamaño_casas, 340 + 8*tamaño_casas)],
                width= int(1.03**tamaño_casas),
                fill= 'gray')
        
    # Dibuja último separador
    dibujo.line(xy= [(((1000/(num_casas+1)) * (num_casas + 1)) - tamaño_casas*1.25 - 1.068**tamaño_casas, 420), (((1000/(num_casas+1)) * (num_casas + 1)) - tamaño_casas*1.25 - 1.068**tamaño_casas, 340 + 8*tamaño_casas)],
            width= int(1.03**tamaño_casas),
            fill= 'gray')

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

casas = [casa1, casa2, casa3]
casas = [casa1, casa2, casa3, casa4, casa5, casa6]
casas = [casa1, casa2, casa3, casa4, casa5, casa6, casa7, casa8, casa9, casa10]
representa_solucion(casas)

# Enseña la imagen por pantalla
fondo.show()