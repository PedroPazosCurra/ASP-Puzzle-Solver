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
from utils_graficos import escala_imagen, dibuja_silla, dibuja_mesa

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

    tamaño_mesa = 400
    num_asientos = len(args)
    angulo_asiento = 360 / num_asientos
    angulo_inicial = 270
    tamaño_texto = TAMAÑO_DEFAULT / num_asientos + 0.3*TAMAÑO_DEFAULT

    # Ordena la lista de personas sentadas según número de asiento
    args = sorted(args, key=lambda d: d[1])

    fuente_texto = ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = tamaño_texto)
    
    for asiento in args:

        num_asiento = asiento[1]
        grados_rotacion = (num_asiento - 1) *angulo_asiento
        radianes_angulo_local = math.radians(angulo_inicial + grados_rotacion)
        
        x_ponderado_nombres = round(math.cos(radianes_angulo_local) * 1.2*tamaño_mesa + TAMAÑO_FONDO/2 - 0.7*tamaño_texto)
        y_ponderado_nombres = round(math.sin(radianes_angulo_local) * 1.2*tamaño_mesa + TAMAÑO_FONDO/2 - 0.7*tamaño_texto)

        x_ponderado_nums = round(math.cos(radianes_angulo_local) * tamaño_mesa/2.6 + TAMAÑO_FONDO/2 -(0.6*tamaño_texto))
        y_ponderado_nums = round(math.sin(radianes_angulo_local) * tamaño_mesa/2.6 + TAMAÑO_FONDO/2  -(0.6*tamaño_texto))

        x_ponderado_sillas = round(math.cos(radianes_angulo_local) * tamaño_mesa/1.6 + TAMAÑO_FONDO/2 -(0.8*tamaño_texto))
        y_ponderado_sillas = round(math.sin(radianes_angulo_local) * tamaño_mesa/1.6 + TAMAÑO_FONDO/2  -(1.2*tamaño_texto))

        # Silla
        tamaño_silla = (2*TAMAÑO_DEFAULT / num_asientos) + 50
        dibuja_silla(fondo_solucion, (x_ponderado_sillas, y_ponderado_sillas), tamaño_silla, grados_rotacion)

        # Nombre de persona
        dibujo_solucion.text(xy = (x_ponderado_nombres, y_ponderado_nombres),
                text = asiento[0],
                font= fuente_texto,
                stroke_width= round(TAMAÑO_DEFAULT * 0.05),
                stroke_fill='black'
                )
        
        # Número
        dibujo_solucion.text(xy = (x_ponderado_nums + round(tamaño_texto/3), y_ponderado_nums),
                text = str(asiento[1]),
                font= fuente_texto,
                stroke_width= round(TAMAÑO_DEFAULT * 0.05),
                stroke_fill='black'
                )
        
    # Mesa
    dibuja_mesa(tamaño_mesa, TAMAÑO_FONDO, dibujo_solucion)
        

as_prueba = [['juan', 1], ['jose', 2]]
as_prueba2 = [['juan', 1], ['jose', 2], ['lucia', 3], ['alba', 4], ['chemita', 5]]
as_prueba3 = [['juan', 2], ['jose', 1], ['lucia', 3], ['alba', 4], ['chemita', 5], ['abraham', 6], ['moises', 7], ['camaño', 8]]

comensales_grafico(as_prueba)
# Enseña las imgs por pantalla
fondo_solucion.show()
#fondo_solucion.show()