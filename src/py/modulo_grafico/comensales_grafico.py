############ Imports ############
from PIL import Image, ImageDraw, ImageFont
import requests
import numpy as np
from os import path
from io import BytesIO
from webcolors import name_to_rgb
from collections import defaultdict
import traceback
import math
from modulo_grafico.utils_graficos import escala_imagen, dibuja_silla, dibuja_mesa


######################################### Constantes y variables ##############################################

TAMAÑO_DEFAULT = 80
TAMAÑO_FONDO = 1200
DEBUG = False

# Crea nueva imagen importándola. La imagen es 2000x2000
img_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/img"))
tmp_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/tmp"))
atom_imgs_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/atom_images"))
font_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/fonts"))


######################################### Funciones ##############################################

# Estado Inicial
def representa_estado_inicial(array_seated, array_speaks):

    fondo_estado_inicial = Image.open(img_path + '/fondo_imagen_generada.png')
    dibujo_estado_inicial = ImageDraw.Draw(fondo_estado_inicial)

    num_asientos = len(array_seated)
    division_fondo = TAMAÑO_FONDO / (num_asientos + 1)

    tamaño_texto = TAMAÑO_DEFAULT / num_asientos + 0.1*TAMAÑO_DEFAULT
    fuente_texto = ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = tamaño_texto)

    for i, asiento in enumerate(array_seated):

        [nombre_persona, num_asiento] = asiento

        texto_persona = nombre_persona

        x_local = round(division_fondo * (i + 1) - tamaño_texto)

        # Buscamos si habla idioma
        for atomo_speaks in array_speaks: # [[pedro, spanish], [maria, italian]]

            [nombre_speaks, idioma_speaks] = atomo_speaks

            if nombre_speaks == nombre_persona:
                texto_persona = f"{nombre_persona}\n({idioma_speaks})"
        
        # Nombre de persona
        dibujo_estado_inicial.text(xy = (x_local, 500),
                text = texto_persona,
                font= fuente_texto,
                stroke_width= round( (0.15 * TAMAÑO_DEFAULT )/ num_asientos),
                stroke_fill='black'
                )

        # Silla
        tamaño_silla = (2*TAMAÑO_DEFAULT / num_asientos) + 50
        dibuja_silla(fondo_estado_inicial, (x_local, 300), tamaño_silla, 0)

    return fondo_estado_inicial


# Estado Final
def representa_solucion(args):

    fondo_solucion = Image.open(img_path + '/fondo_imagen_generada.png')
    dibujo_solucion = ImageDraw.Draw(fondo_solucion)

    tamaño_mesa = 400
    num_asientos = len(args)
    angulo_asiento = 360 / num_asientos
    angulo_inicial = 270
    tamaño_texto = TAMAÑO_DEFAULT / num_asientos + 0.3*TAMAÑO_DEFAULT
    nombre_persona = ""

    fuente_texto = ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = tamaño_texto)
    
    for asiento in args: # -> ['nombre', 1] , ['nombre2', 2], ...

        [nombre_persona, num_asiento] = asiento
        grados_rotacion = (num_asiento - 1) *angulo_asiento
        radianes_angulo_local = math.radians(angulo_inicial + grados_rotacion)
        
        # Calcula las coordenadas alrededor de la mesa en 3 alturas
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
                text = nombre_persona,
                font= fuente_texto,
                stroke_width= round(TAMAÑO_DEFAULT * 0.05),
                stroke_fill='black'
                )
        
        # Número
        dibujo_solucion.text(xy = (x_ponderado_nums + round(tamaño_texto/3), y_ponderado_nums),
                text = str(num_asiento),
                font= fuente_texto,
                stroke_width= round(TAMAÑO_DEFAULT * 0.05),
                stroke_fill='black'
                )
        
    # Mesa
    dibuja_mesa(tamaño_mesa, TAMAÑO_FONDO, dibujo_solucion)

    return fondo_solucion

## Función principal para representación gráfica de puzzle de Comensales.
# args -> [seated_atoms] -> [[john,1], [maria,2]]
def comensales_grafico(args):

    try:

        [array_seated, array_speaks] = args

        tamaño_mesa = 400
        num_asientos = len(array_seated)
        angulo_asiento = 360 / num_asientos
        angulo_inicial = 270
        tamaño_texto = TAMAÑO_DEFAULT / num_asientos + 0.3*TAMAÑO_DEFAULT

        # Ordena la lista de personas sentadas según número de asiento
        array_seated = sorted(array_seated, key=lambda d: d[1])

        # Dibuja las salidas
        estado_inicial = representa_estado_inicial(array_seated, array_speaks)
        solucion = representa_solucion(array_seated)

        # Listo, OK
        #estado_inicial.show()
        #solucion.show()

        estado_inicial.save(tmp_path + "/estado_inicial.png")
        solucion.save(tmp_path + "/solucion.png")

        return [0, "OK"]

    # Caso de excepcion en el proceso
    except Exception as exc:
        return[1, traceback.format_exception(exc)]
        
if DEBUG:
    as_prueba = [[['juan', 1], ['jose', 2]], [['juan', 'catalan'], ['jose', 'gallego']]]
    as_prueba2 = [[['juan', 1], ['jose', 2], ['lucia', 3], ['alba', 4], ['chemita', 5]], [['juan', 'catalan'], ['jose', 'gallego']]]
    as_prueba3 = [[['juan', 2], ['jose', 1], ['lucia', 3], ['alba', 4], ['chemita', 5], ['abraham', 6], ['moises', 7], ['camaño', 8]], [['juan', 'catalan'], ['jose', 'gallego']]]

    comensales_grafico(as_prueba3)