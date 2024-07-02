############ Imports ############
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from os import path
from webcolors import name_to_rgb
from collections import defaultdict
import traceback
import os
from modulo_grafico.utils_graficos import busca_imagen, escala_imagen

######################################### Constantes y variables ##############################################
TAMAÑO_DEFAULT = 80
TAMAÑO_FONDO = 1200
DEBUG = False


img_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/img"))
tmp_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/tmp"))
font_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/fonts"))

# Si no existe /tmp, lo crea.
try:
    os.mkdir(tmp_path)
except FileExistsError:
    pass
except:
    pass

# Crea imágenes temporales con las que trabajar. Cada imagen es 2000x2000
inicial_save_path = path.join(tmp_path,"estado_inicial.png")
solucion_save_path = path.join(tmp_path,"solucion.png")


# Recoge los fondos de las imgs
fondo_estado_inicial = Image.open(img_path + '/fondo_imagen_generada.png')
fondo_solucion = Image.open(img_path + '/fondo_imagen_generada.png')

# Crea objeto Draw
dibujo_estado_inicial = ImageDraw.Draw(fondo_estado_inicial)
dibujo_solucion = ImageDraw.Draw(fondo_solucion)


######################################### Funciones ##############################################


# Función auxiliar que dibuja un array de texto en determinadas coordenadas y tamaño. 
def dibuja_datos(fondo, dibujo:ImageDraw.ImageDraw, coordenadas:tuple, tamaño:float, array_datos:list):

    #print(f"Coordenadas {coordenadas}, tamaño {tamaño}, array datos {array_datos}, array_rutas {array_rutas_imagenes}\n")
    
    a, b = coordenadas
    c = a + tamaño*2
    d = b + tamaño*1.5

    fuente_letras = ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = round(tamaño*0.5))

    for i, dato in enumerate(array_datos):

        # Primer elemento con texto más grande
        if (i==0): fuente_letras = ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = round(tamaño*0.65))
        
        # Busca la imagen. Si no existe, texto.
        img = busca_imagen(dato)

        if img != None:

            try:
                # Escala la imagen según tamaños
                img, hsize = escala_imagen(img, round(tamaño))

                # Coloca la imagen donde toque
                fondo.paste(
                            box= (round(a + (c-a)/2 - tamaño*1.1), round(d + (d-b)*(0.75*i + 0.5)),  round((a + (c-a)/2 - tamaño*1.1) + round(tamaño)), round(d + (d-b)*(0.75*i + 0.5)) + hsize),
                            im= img
                            )
                
            except:

                # Dibuja texto
                dibujo.text(xy = (a + (c-a)/2 - tamaño*1.1, d + (d-b)*(0.75*i + 0.5)),
                            text = dato.capitalize() if (isinstance(dato, str)) else dato,
                            font= fuente_letras,
                            stroke_width= round(tamaño * 0.06),
                            stroke_fill= 'black'
                            )
            
        else:
            # Dibuja texto
            dibujo.text(xy = (round(a + (c-a)/2 - tamaño*1.1), round(d + (d-b)*(0.75*i + 0.5))),
                        text = dato.capitalize() if (isinstance(dato, str)) else dato,
                        font= fuente_letras,
                        stroke_width= round(tamaño * 0.06),
                        stroke_fill= 'black'
                        )


# Función auxiliar que dibuja un elemento en determinadas coordenadas, tamaño, color y número. 
def dibuja_elemento(fondo, elemento, dibujo, coordenadas, tamaño, color = 'white', numero = ''):

    a, b = coordenadas
    c = a + tamaño*2
    d = b + tamaño*1.15

    # En base al nombre del color, una librería pasa un rgb. Si no puede, gris.
    try:
        color_elem = name_to_rgb(color.strip())
    except ValueError:
        color_elem = ("grey")

    # Si es casa, dibuja una casa del color indicado
    if (elemento in ["house", "casa", "home", "residence", "homestead", "domicile"]):

        dibujo.polygon([(a - tamaño*0.3, b), (a,b), (a,d), (c,d), (c,b), (c + tamaño*0.3, b), ((c + a)/2, b - tamaño*1.3)],
                        fill = color_elem,
                        outline = 'black',
                        width= round(tamaño * 0.1))
        
        # Dibuja el número del elemento
        fuente_numero = ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = tamaño*0.8)
        dibujo.text(xy = (a + (c-a)/2 - tamaño*0.25, b - tamaño*0.2 ),
                    text = numero,
                    font= fuente_numero,
                    stroke_width= round(tamaño * 0.1),
                    stroke_fill='black'
                    )
    
    # Si no es una casa, ponemos la imagen del elemento y indicamos el color en un círculo de color.
    else:
        try:
            img = busca_imagen(elemento)

            # Escala la imagen según tamaños
            tamaño_escala = round(2*tamaño)
            img, hsize = escala_imagen(img, tamaño_escala)

            # Coloca la imagen donde toque
            fondo.paste(
                        box= (round(a - tamaño*0.3), round(b), round(a - tamaño*0.3 + tamaño_escala), round(b) + hsize),
                        im= img
                        )
        
        except:
            # No consigo la imagen: pongo el nombre del elemento en su lugar.
            fuente= ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = tamaño)
            dibujo.text(xy = (a, b),
                text = elemento.capitalize(),
                font= fuente,
                stroke_width= round(tamaño * 0.1),
                stroke_fill='black'
                )
            
        finally:

            # Círculo indicando color arriba a la derecha
            dibujo.ellipse(xy=(c, b, c + 0.6*tamaño, b + 0.6*tamaño),
                        fill= color_elem,
                        outline = 'black',
                        width= round(tamaño * 0.05))
        
        # Dibuja el número del elemento
        fuente_numero = ImageFont.truetype(font_path + "/OpenSans-Regular.ttf", size = 0.6*tamaño)
        dibujo.text(xy = (c, d),
                    text = numero,
                    font= fuente_numero,
                    stroke_width= round(tamaño * 0.05),
                    stroke_fill='black'
                    )


def representa_elemento(fondo, elemento, coordenadas, elems, tamaño, color = 'white', numero = ''):

    # Dibuja la casa
    dibuja_elemento(fondo, elemento, dibujo_solucion, coordenadas, tamaño, color, numero)

    # Escribe los datos debajo de la casa
    dibuja_datos(fondo, dibujo_solucion, coordenadas, tamaño, elems)


def representa_estado_inicial(elemento_central, grupos):

    dict_datos = defaultdict(list)         # Aquí van a ir recopilados los datos sin asociar a elementos centrales ("num" : [1,2,3]...)
    num_grupos = len(grupos)

    # Función exponencial para ajustar el tamaño de los elementos centrales para que quepan en el fondo 
    tamaño_elem_central = (1.1**(-num_grupos)) * TAMAÑO_DEFAULT

    # Para cada grupo con índice i de la entrada
    for i, grupo in enumerate(grupos):

        # División de los 2000px que le toca a cada casa según cuántas casas hay
        division_elems_centrales = (TAMAÑO_FONDO/(num_grupos+1)) * (i + 1)

        numero = str(grupo[elemento_central])

        # Dibuja el elemento en blanco
        dibuja_elemento(fondo_estado_inicial, elemento_central, dibujo_estado_inicial, coordenadas= (division_elems_centrales - tamaño_elem_central, TAMAÑO_FONDO - 6* tamaño_elem_central), tamaño= tamaño_elem_central, numero= numero)
        
        # Recoge todos los datos de las casas y los almaceno por clave
        for key, value in grupo.items():
            dict_datos[key].append(str(value))
        
    # Ya tengo los datos filtrados por clave
    num_datos = len(dict_datos)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_datos = (1.1**(-num_grupos)) * TAMAÑO_DEFAULT

    for i, par in enumerate(dict_datos.items()):

        clave, valor = par

        division_datos = (TAMAÑO_FONDO/(num_datos+ 1)) * (i + 1)

        # Se prepara el array [clave, [valores...]]
        valor.insert(0, clave)

        dibuja_datos(fondo = fondo_estado_inicial,
                    dibujo= dibujo_estado_inicial,
                    tamaño= tamaño_datos,
                    coordenadas= (division_datos- tamaño_datos,100),
                    array_datos= valor)

    return fondo_estado_inicial


def representa_solucion(elemento_central, grupos):

    num_elems = len(grupos)

    # Función exponencial para ajustar el tamaño de las casas para que quepan en el fondo 
    tamaño_elems = (1.1**(-num_elems)) * TAMAÑO_DEFAULT

    for i, grupo in enumerate(grupos):

        color = "gray" 
        numero = ""
        numero = str(grupo.get(elemento_central, []))

        # División de los 2000px que le toca a cada elemento central según cuántos haya
        division = (TAMAÑO_FONDO/(num_elems+1)) * (i + 1)

        # Argumentos de representa_elemento (los quitamos del array casa porque ya no los queremos)
        if(elemento_central in grupo):
            del grupo[elemento_central]

        for elem in list(grupo):
            if("color" in elem):
                color = grupo[elem]
                del grupo[elem]

        # Dibuja el elemento central y escribe sus datos
        representa_elemento(fondo       = fondo_solucion,
                        elemento        = elemento_central,
                        coordenadas     = (division - tamaño_elems, 400),
                        numero          = numero,
                        color           = color,
                        tamaño          = tamaño_elems,
                        elems           = grupo.values()
                        )
        
        # Dibuja separador
        dibujo_solucion.line(xy= [(division - tamaño_elems*1.25 - 1.068**tamaño_elems, 420), (division - tamaño_elems*1.25 - 1.068**tamaño_elems, 340 + 8*tamaño_elems)],
                width= round(1.03**tamaño_elems),
                fill= 'gray')
        
    # Dibuja último separador
    dibujo_solucion.line(xy= [(((TAMAÑO_FONDO/(num_elems+1)) * (num_elems + 1)) - tamaño_elems*1.25 - 1.068**tamaño_elems, 420), (((TAMAÑO_FONDO/(num_elems+1)) * (num_elems + 1)) - tamaño_elems*1.25 - 1.068**tamaño_elems, 340 + 8*tamaño_elems)],
            width= round(1.03**tamaño_elems),
            fill= 'gray')
    
    return fondo_solucion



# einstein_grafico: Función de nivel superior que se encarga del proceso del módulo gráfico.
#
#   Ejemplo de uso:
#
#   einstein_grafico(   array_has       = [['pedro', 'house', 1], ['pedro', 'drink', 'water']], 
#                   )
#
def einstein(argumentos):

    tipo = ""
    elemento_central = "house"
    grupos = np.array([])
    [_, array_has] = argumentos

    try:

        # Ya tenemos un array de arrays de tres elementos correspondientes a todos los predicados has. Iteramos
        for entrada in array_has:

            #[brittish, color, red]
            persona = entrada[0]
            tipo = entrada[1]
            valor = entrada[2]

            persona_creada = False

            # ¿Esta persona está asignada a una casa en el array de diccionarios "grupos[]"?
            for elem in grupos:

                # Ya existe el grupo de esta persona: se gestiona el predicado
                if(elem["person"] == persona):
                    elem[tipo] = valor
                    persona_creada = True

            # No existe la persona -> nueva casa
            if(persona_creada == False):

                nuevo_elem = dict(person = persona)
                nuevo_elem[tipo] = valor

                grupos = np.append(grupos, nuevo_elem)


        # Elemento central es aquel con valor int
        for elem in grupos:
            
            for k,v in elem.items():
                if isinstance(v, int):
                    elemento_central = k
                    break

        # Ya tenemos un array de diccionarios con todos los datos de las casas. Ordenamos por número de elemento central y representamos.
        if(all(elemento_central in grupo for grupo in grupos)):
            grupos = sorted(grupos, key=lambda d: d[elemento_central])

            representa_estado_inicial(elemento_central, grupos).save(inicial_save_path)
            representa_solucion(elemento_central, grupos).save(solucion_save_path)

            return [0, "OK"]
        
        else: return[1, f"El script einstein_grafico no tiene todos los elementos centrales presentes en el array de elementos: Grupos: {grupos} Array_has: {array_has}"]

    # Caso de excepcion en el proceso
    except Exception as exc:
        return[1, traceback.format_exception(exc)]



################################################  Debug   ##########################################################

if DEBUG:

    # Falla, 'pedro' no tiene 'house'
    as_prueba_falla = [['juan', 'house', 4], ['chema', 'house', 5], ['pedro', 'car', 'ford'], ['spanish','house', 1], ['spanish','color','red'], ['spanish','pet','dog'], ['spanish','tobacco','ducados'], ['spanish','beverage','agua'], ['english','house',2], ['english','color','blue'], ['english','pet','giraffe'], ['english','beverage','horchata']]
    
    # 3 coches, ejemplo con mucha foto.
    as_prueba2 = [['pedro', 'car', 1], ['isabel', 'car', 2], ['josito', 'car', 3], ['pedro', 'bebida', 'cocacola'], ['isabel', 'bebida', 'agua'], ['josito', 'bebida', 'leche'], ['pedro','color','red'], ['isabel','color','blue'], ['josito','color','green']]
    
    # 7 casas, elementos heterogéneamente definidos.
    as_prueba3 = [['juan', 'house', 4], ['pedro', 'house', 1], ['ramon', 'house', 6], ['luis', 'house', 7], ['pedro', 'inventado', 'inventado'], ['chema', 'house', 5], ['pedro', 'car', 'ford'], ['spanish','house', 3], ['spanish','color','red'], ['spanish','pet','dog'], ['spanish','tobacco','ducados'], ['spanish','beverage','agua'], ['english','house',2], ['english','color','blue'], ['english','pet','giraffe'], ['english','beverage','horchata']]
    
    # 2 Casas, muchos elemetos
    as_prueba4 = [['a', 'house', 1], ['b', 'house', 2], ['a', 'pet', 'perro'], ['b', 'pet', 'gato'], ['a', 'drink', 'cocacola'], ['b', 'drink', 'water'], ['a', 'food', 'arroz'], ['b', 'food', 'macarrones'], ['a', 'car', 'ford'], ['b', 'car', 'mitshubishi']]

    # 15 casas
    as_prueba5 = [['a', 'house', 1], ['a', 'pet', 'cat'], ['a', 'drink', 'cocacola'], ['b', 'house', 2],  ['c', 'house', 3],  ['d', 'house', 4],  ['e', 'house', 5],  ['f', 'house', 6],  ['g', 'house', 7],  ['h', 'house', 8],  ['i', 'house', 9],  ['j', 'house', 10],  ['k', 'house', 11],  ['l', 'house', 12],  ['m', 'house', 13],  ['n', 'house', 14],  ['o', 'house', 15],  ['p', 'house', 16], ['q', 'house', 17], ['r', 'house', 18], ['s', 'house', 19], ['t', 'house', 20]]

    print(einstein([["show_graphic", "show_description"], as_prueba2]))

    # Enseña las imgs por pantalla
    fondo_estado_inicial.show()
    fondo_solucion.show()