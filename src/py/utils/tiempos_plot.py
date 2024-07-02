from matplotlib import pyplot as plt
import numpy as np

# Saca los porcentajes para colocarlos luego
def calcula_porcentaje(pct, tiempos):
    absolute = pct / 100.*np.sum(tiempos)
    return "{:.3f} s\n({:.1f} %)".format( absolute, pct)


# Función exportada: tiempos_plot
#  Dada una lista de tiempos (con los tiempos en segundos de cada fase del proceso), saca una gráfica tipo barra horizontal.
#   list, int, int -> void
#   
def tiempos_plot(tiempos : list, tiempo_total : int, intentos : int, representaciones : list = ["show_graphic", "show_description"]):

    num_fases = len(tiempos)
    fases_nombres = ["1.- NL_to_ASP", "2.- resolver_ASP", "3.- AS_to_NL", "4.- Módulo gráfico"]
    fases_actuales  = fases_nombres[ : num_fases]

    if num_fases <= 0 or num_fases > 4: exit()
    elif num_fases == 3 and len(representaciones) == 1: 

        if representaciones[0] == "show_graphic":
            fases_actuales[2] = "3.- Módulo gráfico"
        elif representaciones[0] == "show_description":
            fases_actuales[2] = "3.- AS_to_NL"
        
        else: exit()

    colores_barra = ['#8d02ff', '#ff00c8', '#ff001e', '#ff7300']
    colores_texto = ['#490163', '#61003e', '#660000', '#663d00']

    fig, ax = plt.subplots(figsize =(10, 3), 
                        subplot_kw = dict(aspect ="equal"))

    left_count = 0
    left_sum = [0]
    
    for i, tiempo in enumerate(tiempos):
        ax.barh(
                y= " ",
                width= tiempo,
                left= left_count,
                label= fases_actuales[i],
                color= colores_barra[i],
                edgecolor= colores_texto[i],
                linewidth= 1
                )

        texto_x = left_count + tiempo / 2
        texto_y =  0.5
        ax.text(texto_x, texto_y, fases_actuales[i], ha='center', va='bottom', fontsize=8, color=colores_texto[i])

        left_count += tiempo
        left_sum.append(round(left_count, 2))

    ax.text(0, -3.5, f"Tiempo total iteración: {tiempo_total:.2f} s", ha='left', va='bottom', fontsize=12)
    ax.text(0, -5, f"Iteraciones previas: {intentos}", ha='left', va='bottom', fontsize=12)

    ax.set_xticks(left_sum, labels=left_sum, rotation=-25)      # Marcas de tiempo en separaciones
    ax.get_yaxis().set_visible(False)                           # Borra etiquetas en Y
    ax.set_xlim(right=left_count)                               # Ajusta el límite

    ax.set_title(f"Tiempo de ejecución por fase (s.)", loc='center', y=2.8)
    
    plt.show(block = True)

# Debug
# tiempos_plot([23.123, 2.3, 15.4], 150, 3, ["show_graphic", "show_description"])
