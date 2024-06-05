# IMPORTS
from PIL import Image, ImageDraw, ImageFont
import requests
import numpy as np
from os import path
from io import BytesIO
from webcolors import name_to_rgb
from collections import defaultdict
import traceback
import math

######################################### Constantes y variables ##############################################
TAMAÑO_DEFAULT = 80
TAMAÑO_FONDO = 1200
DEBUG = False

# Crea nueva imagen importándola. La imagen es 2000x2000
img_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/img"))
tmp_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/tmp"))
atom_imgs_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/atom_images"))
font_path = path.abspath(path.join(path.dirname(__file__), "..", "../resources/fonts"))

fondo_estado_inicial = Image.open(img_path + '/fondo_imagen_generada.png')
fondo_solucion = Image.open(img_path + '/fondo_imagen_generada.png')

# Crea objeto Draw
dibujo_estado_inicial = ImageDraw.Draw(fondo_estado_inicial)
dibujo_solucion = ImageDraw.Draw(fondo_solucion)

## Función principal para representación gráfica de puzzle de Comensales.
# args -> [seated_atoms] -> [[john,1], [maria,2]]
def comensales_grafico(args):



    tamaño_circulo = 400
    num_asientos = len(args)
    angulo_asiento = 360 / num_asientos
    angulo_inicial = 90
    tamaño_asientos = TAMAÑO_DEFAULT * 0.2 *num_asientos
    tamaño_texto = TAMAÑO_DEFAULT / num_asientos + 0.4*TAMAÑO_DEFAULT

    # Ordena la lista de personas sentadas según número de asiento
    args = sorted(args, key=lambda d: d[1])

    # Coordenadas centradas
    coord_comienzo_circulo = TAMAÑO_FONDO/2 - tamaño_circulo/2
    coord_final_circulo = coord_comienzo_circulo + tamaño_circulo

    dibujo_estado_inicial.ellipse(
        xy= (coord_comienzo_circulo, coord_comienzo_circulo, coord_final_circulo, coord_final_circulo), 
        fill = 'wheat', 
        outline ='tan',
        width=10)
    
    fuente_texto = ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = tamaño_texto)
    
    
    for asiento in args:

        num_asiento = asiento[1]

        x_ponderado = math.cos(math.radians(angulo_inicial + num_asiento*angulo_asiento)) * tamaño_circulo + TAMAÑO_FONDO/2 - tamaño_texto
        y_ponderado = math.sin(math.radians(angulo_inicial + num_asiento*angulo_asiento)) * tamaño_circulo + TAMAÑO_FONDO/2 - tamaño_texto

        x_ponderado2 = math.cos(math.radians(angulo_inicial + num_asiento*angulo_asiento)) * tamaño_circulo/1.5 + TAMAÑO_FONDO/2 -(0.4*tamaño_texto)
        y_ponderado2 = math.sin(math.radians(angulo_inicial + num_asiento*angulo_asiento)) * tamaño_circulo/1.5 + TAMAÑO_FONDO/2  -(0.6*tamaño_texto)

        dibujo_estado_inicial.text(xy = (x_ponderado, y_ponderado),
                text = asiento[0],
                font= fuente_texto,
                stroke_width= round(TAMAÑO_DEFAULT * 0.05),
                stroke_fill='black'
                )
        
        dibujo_estado_inicial.text(xy = (x_ponderado2, y_ponderado2),
                text = str(asiento[1]),
                font= fuente_texto,
                stroke_width= round(TAMAÑO_DEFAULT * 0.05),
                stroke_fill='black'
                )



as_prueba = [['juan', 1], ['jose', 2]]
as_prueba2 = [['juan', 1], ['jose', 2], ['lucia', 3], ['alba', 4], ['chemita', 5]]
as_prueba3 = [['juan', 2], ['jose', 1], ['lucia', 3], ['alba', 4], ['chemita', 5], ['abraham', 6], ['moises', 7], ['camaño', 8]]

comensales_grafico(as_prueba3)
# Enseña las imgs por pantalla
fondo_estado_inicial.show()
#fondo_solucion.show()