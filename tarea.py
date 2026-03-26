import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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


# 3) Bucle de interacción
print(f"Archivo cargado con {leng} filas (índices válidos: 0 a {leng-1}).")


while True:
    print("Escribe el número de fila a graficar o 's' para salir.")
    variable = input("> ")

    if variable.lower() == "s":
        print("Saliendo...")
        break

    # Validación: entero
    try:
        numero = int(variable)
    except ValueError:
        print("No es un número entero. Intenta de nuevo.")
        continue

    # Validación: rango (¡hazla ANTES de acceder a df.iloc[numero]!)
    if numero < 0 or numero >= leng:
        print(f"El número debe estar en el rango 0 a {leng-1}.")
        continue

 
  
      #extraccion de la fila seleccionada permite acceder a filas por su posición 
    fila=df.iloc[numero]
    n=numero
      # Nos quedamos solo con valores numericos en la fila y otros en NAN y se eliminan
    fila_num = pd.to_numeric(fila, errors='coerce').dropna()
#si esta vacia
    if fila_num.empty:
        print("La fila no tiene valores numéricos para graficar.")
        continue

    #  crea un arreglo de 0 hasta la cantidad de elementos en la fila -1 
    #x indice de cada valor
# y los valores numericos
    x = np.arange(len(fila_num))
    y = fila_num.values
#tamaño de la ventana 
    plt.figure(figsize=(10, 4))
    #dibuja con los indices x y valores y  marker o es para el punto y el ancho de linea
    plt.plot(x, y, marker="o", linewidth=1)

    plt.title(f"Electrocardiograma de la fila {n}")
    plt.xlabel("x")
    plt.ylabel("y")
     #activa cuadricula 30% opacidad
    plt.grid(True, alpha=0.3)

        # tik cada 20 
    # Marcadores de 0 a len(y)-1, con paso 20
    step = 20
    #crea el arreglo  0 20,40,60 hasta final
    xticks = np.arange(0, len(x), step)
    if xticks[-1] != len(x) - 1:
        #  añade el ultimo punto si no cae exacto
        xticks = np.append(xticks, len(x) - 1)
#anade el tick sin rotacion
    plt.xticks(xticks, rotation=0)
#ajusta diseno y muestra
    plt.tight_layout()
    plt.show()
    