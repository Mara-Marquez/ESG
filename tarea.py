
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal
# 1) Leer CSV local
# Cambia la ruta por la ubicación de tu archivo en tu PC
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

def mostrar_todas_las_filas():
    print(leng)
    for n in range(leng):
        print(f"Mostrando fila {n}...")
        fila = df.iloc[n]
        graficar_fila(fila, n)
        # Espera a que el usuario cierre la ventana para continuar



# --- Menú principal ---
while True:
    print("\nOpciones:")
    print("1. Graficar una fila específica")
    print("2. Mostrar todas las filas una tras otra")
    print("s. Salir")
    opcion = input("> ")
    if opcion == "1":
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
        graficar_fila(fila, numero)
    elif opcion == "2":
        mostrar_todas_las_filas()
    elif opcion.lower() == "s":
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Intenta de nuevo.")

#    Debe identificar los segmentos QRS del dataset
#  MITBH. Puede descartar algunos ECG,
#  proporcionando una lista de los descartados.
#  Debe mostrar simultaneamente dos imagenes, 
# la original y la imagen con marcas verticales y 
# letras, ambas en color rojo. Se debe ejecutar como 
# un ciclo, a partir del primero, consecutivamente
# .Debe ir mostrando en cada ECG el porcentaje 
# de aciertos, excluyendo descartados. 
# El porcentaje de aciertos debe ser de al menos 90%.


# También se debe ejecutar en carrera libre,
#  para analizar los 1000 ECG, y mostrar al final 
# el porcentaje de aciertos, y el número de descartados.
# entregar un reporte con portada, código, 
# fallas en la identificación de los tres segmentos,
#  indicar  el porcentaje al finalizar el análisis de 
# los 1000 ECG.  

