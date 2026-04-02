#imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks as fp
from peakutils import indexes

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
    #indexes
    # mdist=4
    # thres_=.07
    # pl=indexes(fila.values,
    #             min_dist=mdist,
    #                 thres=thres_)
        
    # print('pico',pl)

 # Gráfica con marcas fp (aquí solo se repite la original, puedes agregar marcas QRS después)
 #find_peaks
    h=.5
    prom=None
    dist=4
    p2, _ =fp(
        x=fila.values,
        height=h,
        threshold=prom,
        distance=dist
    )

    axs[1].plot(x, y, linewidth=1)
    
    # axs[1].scatter(pl, y[pl], color='red', marker='o', label='QRS') #indexes
    axs[1].scatter(p2, y[p2], color='red', marker='o', label='QRS fp')#find_peaks

    axs[1].set_title(f"Electrocardiograma con QRS {n}")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("y")
    axs[1].grid(True, alpha=0.3)
    axs[1].set_xticks(xticks)
    plt.tight_layout(rect=[0, 0.12, 1, 1])  # deja espacio abajo
    # --- Labels debajo ---
    parametros = {
        "QRS detectados": "-",
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



