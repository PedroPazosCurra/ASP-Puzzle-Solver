# En este documento se lleva a cabo la tarea central de procesar el mensaje en lenguaje natural recibido del front-end

# Imports
import sys
import requests
import json
from os import path
import re
import clingo
from NL_to_ASP import NL_to_ASP
from ASP_to_NL import ASP_to_NL
from resolver_ASP import resolver_ASP

# Pasa el NL a ASP
# NL_to_ASP(...)

# Pasa el ASP a Answer Set (resuelve ASP)
# resolver_ASP(...)

# Pasa Answer Set a NL
# ASP_to_NL(...)

# Devuelve al front-end
#return(...)