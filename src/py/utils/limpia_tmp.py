from os import path, remove, listdir
from pathlib import Path
from glob import glob

# Vacía la carpeta de salidas temporales del módulo de imagen usadas previamente
try:
    tmp_path = Path(__file__).parents[2].joinpath('resources/tmp')

    for img in listdir(tmp_path):
        img_path = path.join(tmp_path, img)
        remove(img_path)

except:
    pass # Es una petición delete, no vale la pena coger la vuelta.

# Listo