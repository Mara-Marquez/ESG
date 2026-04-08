#tratar de detectar ondas QRS

#imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import neurokit2 as nk
from scipy.signal import find_peaks as fp
from peakutils import indexes

from scipy.signal import butter, lfilter

def bandpass(signal,lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    #nyquist para q no se distorcione
    low = lowcut / nyq
    high = highcut / nyq#noemaliza el valor q tendra 
    b, a =butter(order,[low,high],btype ="band")
    y=lfilter(b,a,signal)
    return y
def Error(medido, real):
    if real == 0:
        return 0
    return abs(medido - real) / real * 100


def graficar_fila(fila, n):
    fila_num = pd.to_numeric(fila, errors='coerce').dropna()
    if fila_num.empty:
        print(f"La fila {n} no tiene valores numéricos para graficar.")
        return
    x = np.arange(len(fila_num))
    y = fila_num.values
    plt.figure(figsize=(10, 4))
    plt.plot(x, y, marker="o", linewidth=1)
    plt.title(f"Electrocardiograma de la fila {n}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, alpha=0.3)
    step = 20
    xticks = np.arange(0, len(x), step)
    if xticks[-1] != len(x) - 1:
        xticks = np.append(xticks, len(x) - 1)
    plt.xticks(xticks, rotation=0)
    plt.tight_layout()
    plt.show()

def graficar_QRS(fila, n):
    global contadorFilas
    fila_num = pd.to_numeric(fila, errors='coerce').dropna()
    if fila_num.empty:
        print(f"La fila {n} no tiene valores numéricos para graficar.")
        return
    x = np.arange(len(fila_num))
   
    y = fila_num.values

    
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
 
    # Gráfica original
    axs[0].plot(x, y, linewidth=1)
    axs[0].set_title(f"Electrocardiograma original fila {n}")
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("y")
    axs[0].grid(True, alpha=0.3)
    step = 20
    xticks = np.arange(0, len(x), step)
    if xticks[-1] != len(x) - 1:
        xticks = np.append(xticks, len(x) - 1)
    axs[0].set_xticks(xticks)
    # Gráfica con marcas (aquí solo se repite la original, puedes agregar marcas QRS después)
    fila = df.iloc[n]
       #filtro
    lowcut=0.1
    highcut=60.0
    sampling=1000

    senal_filtrada=bandpass(fila.values,lowcut,highcut,sampling)

    #indexes
    # mdist=4
    # thres_=.07
    # pl=indexes(fila.values,
    #             min_dist=mdist,
    #                 thres=thres_)
        
    # print('pico',pl)

 # Gráfica con marcas fp (aquí solo se repite la original, puedes agregar marcas QRS después)
 #find_peaks
    h=.4
    prom=.03
    dist=2
    p2, _ =fp(
        x=senal_filtrada,
        height=h,
        threshold=prom,
        distance=dist
    )


    axs[1].plot(x, senal_filtrada, linewidth=1)
    # axs[1].scatter(pl, y[pl], color='red', marker='o', label='QRS') #indexes
    # axs[1].scatter(p2, senal_filtrada[p2], color='red', marker='o', label='QRS fp')#find_peaks
    # for idx in p2:
    #     axs[1].text(idx + 2, senal_filtrada[idx], 'R', fontsize=10, color='red', va='center')

    # Marcar el punto más alto R de la señal filtrada
    max_idx = np.argmax(senal_filtrada)
    axs[1].scatter([max_idx], [senal_filtrada[max_idx]], color='red', marker='o', label='R')
    axs[1].text(max_idx, senal_filtrada[max_idx], 'R', fontsize=10, color='red', va='bottom')



    axs[1].set_title(f"Electrocardiograma con QRS  y filtro {n}")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("y")
    axs[1].grid(True, alpha=0.3)
    axs[1].set_xticks(xticks)
    plt.tight_layout(rect=[0, 0.12, 1, 1])  # deja espacio abajo
    contadorFilas += 1
    # --- Labels debajo ---
    parametros = {
        "QRS detectados": contadorFilas,
        "% acierto": "-",
        "Descartados": "-"
    }
    texto = "    ".join([f"{k}: {v}" for k, v in parametros.items()])
    fig.text(0.5, 0.04, texto, ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))
    plt.show()
    
    
    

def mostrar_todas_las_filas():
    print(leng)
    for n in range(leng):
        print(f"Mostrando fila {n}...")
        fila = df.iloc[n]
        graficar_QRS(fila, n)
    pass
    

def proceso_sin_visualizacion():
    # proceso de detección de QRS sin mostrar gráficos
    # calcular porcentaje de aciertos y número de descartados
    pass
#ruta y si puede abrir el archivo
ruta = r'C:/Users/v84394/Downloads/train1000.csv'  # Ajusta la ruta según tu archivo

# Verificar que el archivo se puede abrir
try:
    open(ruta, 'r')
except FileNotFoundError:
    print(f"No se encontró el archivo en: {ruta}")
    exit()
df = pd.read_csv(ruta)
# Longitud de filas
leng = len(df)
print(f"Archivo cargado con {leng} filas (índices válidos: 0 a {leng-1}).")


global contadorFilas 

contadorFilas =0
contadorR=0
contadorQ=0
contadorS=0

#menu de opciones
while True:
    #bucle para abrir todas las filas y q se cierre con un enter
    #imagen original
    #imagen con las marcas
    #imagen de porsentajes aciertos, y el número de descartados
    print("Menu de opciones:")
    print("1. Graficar fila específica")
    print("2. Graficar todas las filas con marcas QRS")
    print("3. Proceso sin visualización y estadísticas")
    print("4. Salir")
    opcion = input("Selecciona una opción: ")
    
    if opcion == "1":
        print("1. Graficar fila específica")
        # llamar funcion_graficar_fila()11
        print("Escribe el número de fila a graficar:")
        variable = input("> ")
        try:
            numero = int(variable)
        except ValueError:
            print("No es un número entero. Intenta de nuevo.")
            continue
        if numero < 0 or numero >= leng:
            print(f"El número debe estar en el rango 0 a {leng-1}.")
            continue
        fila = df.iloc[numero]
        mdist=1
        thres_=.03
        pl=indexes(fila.values,
                    min_dist=mdist,
                        thres=thres_)
            
        print('pico',pl)
        graficar_fila(fila, numero)

       

    elif opcion == "2":
        print("2. Graficar todas las filas con marcas QRS")
        mostrar_todas_las_filas()
        # llamar funcion_graficar_todas()

    elif opcion == "3":
        print("3. Proceso sin visualización y estadísticas")
        # llamar proceso_sin_visualizacion()
    

        #hacerlo en froma automatica de todos los archivos y que se cierre con un enter
    elif opcion == "4":
        print("4. Saliendo...")
        break
    else:
        print("Opción no válida. Por favor, selecciona una opción válida.")



