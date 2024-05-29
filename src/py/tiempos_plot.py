from matplotlib import pyplot as plt
import numpy as np

# Saca los porcentajes para colocarlos luego
def calcula_porcentaje(pct, tiempos):
    absolute = pct / 100.*np.sum(tiempos)
    return "{:.3f} s\n({:.1f} %)".format( absolute, pct)


# Función exportada: Dada una lista de tiempos (con los tiempos en segundos de cada fase del proceso), saca una gráfica tipo Pie.
def tiempos_plot(tiempos : list):
    num_fases = len(tiempos)
    fases_all = ["1.- NL_to_ASP", "2.- resolver_ASP", "3.- AS_to_NL", "4.- Módulo gráfico"]
    fases  = fases_all[ : num_fases]

    tiempo_total = 12.01

    fig, ax = plt.subplots(figsize =(6, 3), 
                        subplot_kw = dict(aspect ="equal"))



    # Tarta
    wedges, texts, autotexts = ax.pie(  tiempos,
                                        labels = fases,
                                        wedgeprops={'linewidth' : 3.0, 'edgecolor' : 'white'},
                                        textprops= dict(color = "w"),
                                        autopct= lambda pct: calcula_porcentaje(pct, tiempos))
    
    for i, patch in enumerate(wedges):
        texts[i].set_color(patch.get_facecolor())
        plt.setp(texts, fontweight = 600)

    plt.title(f"Tiempo total = {tiempo_total} s")
    plt.setp(autotexts, size = 8, weight ="bold")
    ax.set_title("Tiempo de ejecución por fase del proceso", )
    plt.show()
