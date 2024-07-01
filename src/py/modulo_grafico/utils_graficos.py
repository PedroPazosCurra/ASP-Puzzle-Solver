from PIL import Image
from os import path

# Rutas a elementos estáticos de la BD
atom_imgs_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/atom_images"))
img_path = path.abspath(path.join(path.dirname(__file__), "..", "../../resources/img"))
imagen_silla = Image.open(img_path + '/silla.jpg')

# Escala una imagen a determinado tamaño y la devuelve
def escala_imagen(img, tamaño_escala):

    wpercent = (tamaño_escala / float(img.size[0]))
    hsize = round((float(img.size[1]) * float(wpercent)))
    img = img.resize((round(tamaño_escala), hsize), Image.Resampling.LANCZOS)
    return [img, hsize]


# Dibuja una silla en el fondo en determinados º rotación, tamaño y coordenadas xy
def dibuja_silla(fondo, xy, tamaño_silla, grados_rotacion):
        
        imagen_silla = Image.open(img_path + '/silla.jpg')
        silla_local = imagen_silla.copy().rotate(round(-grados_rotacion), expand=0, fillcolor='white')
        silla_local, _ = escala_imagen(silla_local, tamaño_silla)
        fondo.paste(silla_local, xy)


# Dibuja una mesa en el fondo con determinado tamaño
def dibuja_mesa(tamaño_mesa, tamaño_fondo, dibujo_solucion):
    
    coord_comienzo_mesa = tamaño_fondo/2 - tamaño_mesa/2
    coord_final_mesa = coord_comienzo_mesa + tamaño_mesa

    dibujo_solucion.ellipse(
        xy= (coord_comienzo_mesa, coord_comienzo_mesa, coord_final_mesa, coord_final_mesa), 
        fill = 'wheat', 
        outline ='tan',
        width=10)
    
# Función auxiliar que abstrae la búsqueda de una imagen dado un nombre. Primero, de forma estática. Después, busca URL.
def busca_imagen(nombre : str):

    nombre = nombre.replace(r'"', '')

    # jpg
    try:
        img = Image.open(atom_imgs_path + f'/{nombre}.jpg')
    except:

        # png
        try:
            img = Image.open(atom_imgs_path + f'/{nombre}.png').convert("RGB")
        except:

            # jpeg
            try:
                img = Image.open(atom_imgs_path + f'/{nombre}.jpeg')
            except:
                img = None

    # return
    finally:
        return img