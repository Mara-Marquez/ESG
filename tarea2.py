#imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal
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
    print("Menu de opciones:")
    print("1. Graficar fila específica")
    print("2. Graficar todas las filas")
    print("3. Proceso sin visualización y estadísticas")
    print("4. Salir")
    opcion = input("Selecciona una opción: ")
    
    if opcion == "1":
        print("Opción 1 seleccionada")
        # llamar funcion_graficar_fila()1

    elif opcion == "2":
        print("Opción 2 seleccionada")
        # llamar funcion_graficar_todas()

    elif opcion == "3":
        print("Opción 3 seleccionada")
        # llamar proceso_sin_visualizacion()

    elif opcion == "4":
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Por favor, selecciona una opción válida.")

#hacerlo de forma visual
#hacerlo en froma automatica de todo

#bucle para abrir todas las filas y q se cierre con un enter
    #imagen original
    #imagen con las marcas
    #imagen de porsentajes aciertos, y el número de descartados