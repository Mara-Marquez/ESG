#final
import pygame
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# ---------- INIT
#Inicializa todos los módulos de Pygame. Es obligatorio antes de usar cualquier función de Pygame.
pygame.init()
# Define el ancho y alto de la ventana principal en píxeles.
WIDTH, HEIGHT = 1600,800
#Crea la ventana principal con las dimensiones especificadas.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Establece el título de la ventana.
pygame.display.set_caption("ECG monitor")
#Crea un objeto para controlar la velocidad de actualización del bucle principal.
clock = pygame.time.Clock()
# Crea un objeto de fuente para renderizar texto en la pantalla. El primer argumento es el nombre de la fuente (None para la fuente predeterminada) y el segundo es el tamaño de la fuente.
font = pygame.font.SysFont(None, 24)

#Diccionario con los intervalos de tiempo (en segundos) para las ondas T y P del ECG.
VENTANAS = {
    "T": (-0.20, -0.08),
    "P": ( -0.08,  0),
}
#Crea un rectángulo en la parte superior de la ventana para mostrar información.
INFO_RECT = pygame.Rect(0, 0, WIDTH, 36)
#Listas vacías para guardar los intervalos de las áreas P y T detectadas en la señal.
areas_P = []
areas_T = []
#Frecuencia de muestreo de la señal ECG (360 Hz).
Fs=360
# ---------- AREA ECG 
#Define la posición y tamaño del área donde se dibuja el ECG.
ECG_X = 60
ECG_Y = 40
ECG_WIDTH = 880
ECG_HEIGHT = 300

#Crea un rectángulo para el área del ECG.
ECG_RECT = pygame.Rect(ECG_X, ECG_Y, ECG_WIDTH, ECG_HEIGHT)
#Índice de la fila actual del archivo CSV.
numero=0
#Rutas de los archivos CSV con los datos del ECG.
ruta1 = r'C:/Users/v84394/Downloads/train1000.csv'
ruta2 = r'C:/Users/v84394/Downloads/muestras tipo 1 (1).csv'
#Indica cuál archivo está activo (1 o 2).
archivo_actual = 1  
#Funciones para obtener la ruta y el nombre del archivo actualmente seleccionado.
def get_ruta_actual():
    return ruta1 if archivo_actual == 1 else ruta2
def get_nombre_actual():
    return 'Archivo 1' if archivo_actual == 1 else 'Archivo 2'
#Carga el archivo CSV activo en un DataFrame de pandas.
df = pd.read_csv(get_ruta_actual())
#Define el tamaño y la posición base de los botones de navegación.
BTN_WIDTH = 180
BTN_HEIGHT = 44
BTN_X = (WIDTH - BTN_WIDTH) // 2
BTN_Y = HEIGHT - BTN_HEIGHT - 20
NEXT_BTN_RECT = pygame.Rect(BTN_X, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
PREV_BTN_RECT = pygame.Rect(BTN_X - BTN_WIDTH - 20, BTN_Y, BTN_WIDTH, BTN_HEIGHT)

BTN_FILE1_RECT = pygame.Rect(BTN_X + BTN_WIDTH + 40, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
BTN_FILE2_RECT = pygame.Rect(BTN_X + 2*BTN_WIDTH + 60, BTN_Y, BTN_WIDTH, BTN_HEIGHT)

def cargar_fila(indice):
    #Declara variables globales que serán modificadas dentro de la función.
    global numero, y, x, p2, q_points, s_points
    global areas_P, areas_T, ecg_points
    global eventos_r, eventos_s, eventos_t_3_4, eventos_t_fin
    global estado_valvulas, cursor
#Calcula el número de fila a cargar usando el índice dado y el número total de filas en el DataFrame.
    numero = indice % len(df)
    #Obtiene la fila correspondiente del DataFrame.
    fila = df.iloc[numero]
    #Convierte los valores de la fila a números, elimina los que no son válidos y los guarda como un array.
    y = pd.to_numeric(fila, errors='coerce').dropna().values
    #Crea un array con los índices de los datos de la señal.
    x = np.arange(len(y))
#Reinicia las listas de áreas P y T para la nueva fila.
    areas_P = []
    areas_T = []
#etecta los picos (ondas R) en la señal ECG.
    p2, _ = find_peaks(y, height=0.8, distance=1)
    q_points, s_points = [], []
    window = int(0.06 * len(y))
#por cada r en p2 
    for r in p2:
        if r <= 0:
            continue
        #Busca el punto Q (mínimo antes de R) y lo agrega si la diferencia de amplitud es suficiente.
        q_region = y[max(0, r-window):r]
        q_idx = np.argmin(q_region) + max(0, r-window)
        if abs(y[r] - y[q_idx]) >= 0.3:
            q_points.append(q_idx)
#Busca el punto S (mínimo después de R) y lo agrega si la diferencia de amplitud es suficiente.
        s_region = y[r:r+window]
        s_idx = np.argmin(s_region) + r
        if abs(y[r] - y[s_idx]) >= 0.3:
            s_points.append(s_idx)
#Calcula el inicio y fin del área P alrededor de cada R y lo guarda. 
        p_ini = max(0, int(r + VENTANAS["P"][0] * Fs))
        p_fin = min(len(y)-1, int(r + VENTANAS["P"][1] * Fs))
        areas_P.append((p_ini, p_fin))
#Calcula el inicio y fin del área t alrededor de cada R y lo guarda. 
        t_ini = max(0, int(r + VENTANAS["T"][0] * Fs))
        t_fin = min(len(y)-1, int(r + VENTANAS["T"][1] * Fs))
        areas_T.append((t_ini, t_fin))
#ESTA ES LA SENAL Convierte los puntos de la señal a coordenadas de pantalla. SENAL
    ecg_points = [escalar(i, y[i]) for i in range(len(y))]

#Crea conjuntos para los eventos de interés (R, S, 3/4 de T, fin de T).
    eventos_r = set(int(r) for r in p2)
    eventos_s = set(int(s) for s in s_points)
    eventos_t_3_4 = set()
    eventos_t_fin = set()
#Calcula los puntos de cierre (3/4 y fin) del área T y los guarda.
    for ini, fin in areas_T:
        ini_idx, fin_idx = sorted((int(ini), int(fin)))
        duracion = max(0, fin_idx - ini_idx)
        t_3_4 = ini_idx + int(0.75 * duracion)
        eventos_t_3_4.add(t_3_4)
        eventos_t_fin.add(fin_idx)
#Reinicia el cursor al inicio de la señal.
    cursor = 0
    #Inicializa el estado de las válvulas cardíacas.
    estado_valvulas = {
        'tricuspide': 'abierta',
        'mitral': 'abierta',
        'pulmonar': 'cerrada',
        'aortica': 'cerrada'
    }

# ---------- ESCALA 
#que convierte un punto de la señal ECG (índice y valor) a coordenadas de pantalla.
def escalar(i, valor):
    #Calcula la coordenada X en pantalla para el punto i, escalando el índice al ancho del área ECG
    sx = ECG_X + int(i * ECG_WIDTH / len(y))
    #Calcula la coordenada Y en pantalla para el valor, centrando en la mitad del área ECG y escalando el valor.
    sy = ECG_Y + ECG_HEIGHT // 2 - int(valor * 120)
    return sx, sy
# ----------no se usa Define la función que crea un rectángulo semitransparente para resaltar una ventana de interés en el ECG.  NO SE  USA EN EL CODIGO FINAL, SE DEJO COMO REFERENCIA PARA FUTURAS MEJORAS
def ventana_a_rect(r_idx, ventana_sec, color, alpha=80):
    #Define la frecuencia de muestreo (360 Hz).
    Fs=360
    #Calcula los índices de inicio y fin de la ventana, desplazados desde r_idx según los segundos definidos en ventana_sec.
    inicio_idx = int(r_idx + ventana_sec[0] * Fs)
    fin_idx    = int(r_idx + ventana_sec[1] * Fs)
#Asegura que los índices estén dentro del rango válido de la señal.
    inicio_idx = max(0, inicio_idx)
    fin_idx    = min(len(y)-1, fin_idx)
#Convierte los índices de inicio y fin a coordenadas X en pantalla.
    x1, _ = escalar(inicio_idx, 0)
    x2, _ = escalar(fin_idx, 0)
#Calcula el ancho del rectángulo y, si no es positivo, no dibuja nada.
    ancho = x2 - x1
    if ancho <= 0:
        return None
#Calcula el ancho del rectángulo y, si no es positivo, no dibuja nada
    surf = pygame.Surface((ancho, ECG_HEIGHT), pygame.SRCALPHA)
    #Rellena la superficie con el color y el nivel de transparencia (alpha).
    surf.fill((*color, alpha))
    #Devuelve la superficie y la posición donde debe dibujarse en la pantalla.
    return surf, (x1, ECG_Y)


# ---------- CUADRICULA 
#Define la función para dibujar la cuadrícula del área ECG.
def dibujar_cuadricula_ecg():
    #Define los colores para las líneas finas y gruesas de la cuadrícula.
    color_fino = (30, 30, 30)
    color_grueso = (70, 70, 70)
#Dibuja líneas verticales finas cada 20 píxeles en el área ECG.
    for x in range(ECG_X, ECG_X + ECG_WIDTH, 20):
        pygame.draw.line(screen, color_fino, (x, ECG_Y), (x, ECG_Y + ECG_HEIGHT))
#DDibuja líneas horizontales finas cada 20 píxeles en el área ECG.
    for y in range(ECG_Y, ECG_Y + ECG_HEIGHT, 20):
        pygame.draw.line(screen, color_fino, (ECG_X, y), (ECG_X + ECG_WIDTH, y))
#Dibuja líneas verticales gruesas cada 100 píxeles en el área ECG.
    for x in range(ECG_X, ECG_X + ECG_WIDTH, 100):
        pygame.draw.line(screen, color_grueso, (x, ECG_Y), (x, ECG_Y + ECG_HEIGHT))
        #Dibuja líneas horizontales gruesas cada 100 píxeles en el área ECG.
    for y in range(ECG_Y, ECG_Y + ECG_HEIGHT, 100):
        pygame.draw.line(screen, color_grueso, (ECG_X, y), (ECG_X + ECG_WIDTH, y))
        #Dibuja el borde del área ECG con un rectángulo gris claro.
    pygame.draw.rect(screen, (150, 150, 150), ECG_RECT, 2)
#Define la función para dibujar el eje X (horizontal) debajo del ECG.
def dibujar_eje_x():
    #Define el número de divisiones del eje X.
    pasos = 10
    #Para cada división, calcula la posición y el valor correspondiente, renderiza el texto y lo dibuja debajo del área ECG.


    for i in range(pasos + 1):
        x = ECG_X + i * (ECG_WIDTH // pasos)
        valor = int(i * len(y) / pasos)
        txt = font.render(str(valor), True, (200, 200, 200))
        screen.blit(txt, (x - 10, ECG_Y + ECG_HEIGHT + 5))
#Define la función para dibujar el eje Y (vertical) a la izquierda del ECG.
def dibujar_eje_y():
    #Define el número de divisiones hacia arriba y abajo desde el centro.
    pasos = 4
    #Para cada división, calcula la posición vertical y el valor (en voltaje), renderiza el texto y lo dibuja a la izquierda del área ECG.
    for i in range(-pasos, pasos + 1):
        y_pos = ECG_Y + ECG_HEIGHT // 2 - i * (ECG_HEIGHT // (2 * pasos))
        txt = font.render(f"{i/2:.1f}", True, (200, 200, 200))
        screen.blit(txt, (ECG_X - 45, y_pos - 8))
# Define una función para dibujar válvulas como círculos, recibiendo el color, el estado (abierta/cerrada) y el nombre de la válvula.
def dibujar_valvulas_circulos(color, estatus,nombre):
    if color == 'azul':
        door_color = (0, 100, 255)
    elif color == 'rojo':
        door_color = (199, 39, 33)
        #Define el grosor de la línea para el círculo (cuando está abierta).
    door_width = 2
    #altura
    y=250
    #Define el tamaño (diámetro) del círculo.
    largo = 25
    #Define la separación entre válvulas. no se usa
    separacion = 10
    #dependiendo del nombre de la válvula, asigna una posición horizontal específica para cada una.
    if nombre =='tricuspide':
     x=1100
    if nombre =='pulmonar':
        x=1200
    if nombre =='aortica':
        x=1300
    if nombre =='mitral':
        x=1400
        #Si la válvula está cerrada, dibuja un círculo sólido.
    if estatus == 'cerrada':
        pygame.draw.circle(screen, door_color, (x + largo//2, y), largo//2)
        #Si la válvula está abierta, dibuja un círculo con solo el borde (no relleno).
    elif estatus == 'abierta':
         pygame.draw.circle(screen, door_color, (x + largo//2, y), largo//2, door_width)
#no se usa en el codigo final, se dejo como referencia para futuras mejoras, dibuja válvulas como líneas, recibiendo el color, el estado (abierta/cerrada) y el nombre de la válvula.
def dibujar_valvulas(color, estatus, nombre):
    if color == 'azul':
        door_color = (0, 100, 255)
    elif color == 'rojo':
        door_color = (199, 39, 33)
    door_width = 2
    y=250
    largo = 25
    separacion = 10
    if nombre =='tricuspide':
     x=1100
    if nombre =='pulmonar':
     x=1170

    if nombre =='aortica':
        x=1240
    if nombre =='mitral':
        x=1310

    if estatus == 'cerrada':
        x1 = x
        x2 = x + largo
        x3 = x2 + separacion
        x4 = x3 + largo
        pygame.draw.line(screen, door_color, (x1, y), (x2, y), door_width)
        pygame.draw.line(screen, door_color, (x3, y), (x4, y), door_width)

    elif estatus == 'abierta':
        y1 = y
        x1=  x
        y2 = y - largo
        x2= x+largo+largo+separacion
        y3 = y2 + separacion
        y4 = y3 + largo

        pygame.draw.line(screen, door_color, (x1, y1), (x1, y2), door_width)
        pygame.draw.line(screen, door_color, (x2, y1), (x2, y2), door_width)

#Define la función para dibujar áreas resaltadas en el ECG.
def dibujar_areas():
    #Itera sobre cada tupla (inicio, fin) de las áreas P detectadas.
    for ini, fin in areas_P:
        #Ordena los índices para asegurarse de que ini_idx ≤ fin_idx.
        ini_idx, fin_idx = sorted((ini, fin))
        #Convierte el índice inicial a coordenada X en pantalla.
        x1, _ = escalar(ini_idx, 0)
        #Convierte el índice final a coordenada X en pantalla.
        x2, _ = escalar(fin_idx, 0)
        #Calcula el ancho del área a resaltar.
        ancho = x2 - x1
        #Si el ancho no es positivo, salta a la siguiente área.
        if ancho <= 0:
            continue
        #Crea una superficie transparente del tamaño del área a resaltar.
        surf = pygame.Surface((ancho, ECG_HEIGHT), pygame.SRCALPHA)
        #Rellena la superficie con un color morado semitransparente.
        surf.fill((160, 80, 200, 70))
        #Dibuja la superficie sobre la pantalla en la posición correspondiente.
        screen.blit(surf, (x1, ECG_Y))
#Repite el mismo proceso para las áreas T detectadas.
    for ini, fin in areas_T:
        ini_idx, fin_idx = sorted((ini, fin))
        x1, _ = escalar(ini_idx, 0)
        x2, _ = escalar(fin_idx, 0)
        ancho = x2 - x1
        if ancho <= 0:
            continue
        surf = pygame.Surface((ancho, ECG_HEIGHT), pygame.SRCALPHA)
        surf.fill((255, 140, 0, 70))
        screen.blit(surf, (x1, ECG_Y))
#Define la función para mostrar información en la parte superior de la pantalla.
def dibujar_panel_info():
    #Dibuja un rectángulo oscuro como fondo del panel de información.
    pygame.draw.rect(screen, (20, 20, 20), INFO_RECT)
    #Si hay áreas P, crea un texto con los índices de la primera área P.
    if areas_P:
        p_txt = f"P: {areas_P[0][0]} → {areas_P[0][1]}"
        screen.blit(font.render(p_txt, True, (180, 120, 230)), (220, 8))
        #Si hay áreas t, crea un texto con los índices de la primera área P.
    if areas_T:
        t_txt = f"T: {areas_T[0][0]} → {areas_T[0][1]}"
        screen.blit(font.render(t_txt, True, (255, 170, 80)), (22, 8))

#Define la función para dibujar los botones de navegación y mostrar información relevante.
def dibujar_botones_navegacion():
    #Obtiene la posición actual del mouse.
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #Verifica si el mouse está sobre el botón "Atras".
    hover_prev = PREV_BTN_RECT.collidepoint(mouse_x, mouse_y)
    #Verifica si el mouse está sobre el botón "Siguiente".
    hover_next = NEXT_BTN_RECT.collidepoint(mouse_x, mouse_y)
    #Verifica si el mouse está sobre el botón "archivo1".
    hover_file1 = BTN_FILE1_RECT.collidepoint(mouse_x, mouse_y)
    #Verifica si el mouse está sobre el botón "Archivo2".
    hover_file2 = BTN_FILE2_RECT.collidepoint(mouse_x, mouse_y)
#Si el mouse está sobre "Atras", usa un azul claro; si no, un azul oscuro. cambia el color del botón para dar feedback visual al usuario.
    prev_color = (80, 130, 255) if hover_prev else (50, 90, 200)
    next_color = (80, 130, 255) if hover_next else (50, 90, 200)
    file1_color = (80, 200, 130) if hover_file1 else (50, 120, 90)
    file2_color = (200, 130, 80) if hover_file2 else (120, 90, 50)

#dibuja boton y el borde para "Atras", "Siguiente", "Archivo 1" y "Archivo 2" usando los colores definidos. El borde es un rectángulo con un color gris claro para resaltar el botón.
    pygame.draw.rect(screen, prev_color, PREV_BTN_RECT, border_radius=8)
    pygame.draw.rect(screen, (230, 230, 230), PREV_BTN_RECT, 2, border_radius=8)#borde

    pygame.draw.rect(screen, next_color, NEXT_BTN_RECT, border_radius=8)
    pygame.draw.rect(screen, (230, 230, 230), NEXT_BTN_RECT, 2, border_radius=8)

    pygame.draw.rect(screen, file1_color, BTN_FILE1_RECT, border_radius=8)
    pygame.draw.rect(screen, (230, 230, 230), BTN_FILE1_RECT, 2, border_radius=8)

    pygame.draw.rect(screen, file2_color, BTN_FILE2_RECT, border_radius=8)
    pygame.draw.rect(screen, (230, 230, 230), BTN_FILE2_RECT, 2, border_radius=8)
#texto para cada boton, renderizado en blanco y centrado dentro de cada botón.
    txt_prev = font.render("Atras", True, (255, 255, 255))
    txt_prev_rect = txt_prev.get_rect(center=PREV_BTN_RECT.center)
    screen.blit(txt_prev, txt_prev_rect)

    txt = font.render("Siguiente", True, (255, 255, 255))
    txt_rect = txt.get_rect(center=NEXT_BTN_RECT.center)
    screen.blit(txt, txt_rect)

    txt_file1 = font.render("Archivo 1", True, (255, 255, 255))
    txt_file1_rect = txt_file1.get_rect(center=BTN_FILE1_RECT.center)
    screen.blit(txt_file1, txt_file1_rect)

    txt_file2 = font.render("Archivo 2", True, (255, 255, 255))
    txt_file2_rect = txt_file2.get_rect(center=BTN_FILE2_RECT.center)
    screen.blit(txt_file2, txt_file2_rect)
#saber cual es la fila 
    fila_txt = font.render(f"Fila {numero + 1}/{len(df)}", True, (230, 230, 230))
    fila_rect = fila_txt.get_rect(midbottom=(NEXT_BTN_RECT.centerx, NEXT_BTN_RECT.top - 6))
    screen.blit(fila_txt, fila_rect)

    # Mostrar archivo actual
    archivo_txt = font.render(f"Actual: {get_nombre_actual()}", True, (255, 255, 0))
    archivo_rect = archivo_txt.get_rect(midbottom=(BTN_FILE2_RECT.centerx, BTN_FILE2_RECT.top - 6))
    screen.blit(archivo_txt, archivo_rect)

cargar_fila(numero)

# ---------- LOOP principal
#Inicializa el cursor (índice de la muestra actual del ECG) en cero.
cursor = 0
#Variable de control para mantener el bucle principal activo.
running = True
#Diccionario que guarda el estado inicial de las válvulas cardíacas.
estado_valvulas = {
        'tricuspide': 'abierta',
        'mitral': 'abierta',
        'pulmonar': 'cerrada',
        'aortica': 'cerrada'
    }
#Inicia el bucle principal del programa (se ejecuta mientras running sea True).
while running:
    #imita la velocidad del bucle a 15 cuadros por segundo.
    clock.tick(15)
#Procesa todos los eventos de Pygame (teclado, mouse, cerrar ventana, etc).
    for event in pygame.event.get():
        #Si el usuario cierra la ventana, termina el bucle.
        if event.type == pygame.QUIT:
            running = False
            #Si se presiona el botón izquierdo del mouse:
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #botones de navegación
            if PREV_BTN_RECT.collidepoint(event.pos):
                cargar_fila(numero - 1)
            if NEXT_BTN_RECT.collidepoint(event.pos):
                cargar_fila(numero + 1)
                #cargar los archivos
            if BTN_FILE1_RECT.collidepoint(event.pos):
                if archivo_actual != 1:
                    archivo_actual = 1
                    df = pd.read_csv(ruta1)
                    cargar_fila(0)
            if BTN_FILE2_RECT.collidepoint(event.pos):
                if archivo_actual != 2:
                    archivo_actual = 2
                    df = pd.read_csv(ruta2)
                    cargar_fila(0)
#Limpia la pantalla con color negro.
    screen.fill((0, 0, 0))
      

    # ---- GRID 
    #Dibuja el panel superior con información de áreas P y T.
    dibujar_panel_info()
#Dibuja la cuadrícula del área ECG.
    dibujar_cuadricula_ecg()
#Dibuja el eje X (horizontal) debajo del ECG.
    dibujar_eje_x()
#Dibuja el eje y (vertical) debajo del ECG.
    dibujar_eje_y()
#Dibuja las áreas P y T resaltadas en el ECG.
    dibujar_areas()
    #Dibuja la señal ECG en verde.
    pygame.draw.lines(screen, (0, 255, 0), False, ecg_points, 2)
    # ---- ECG COMPLETO 
    #no se por q sale 2 veces
    pygame.draw.lines(screen, (0, 255, 0), False, ecg_points, 2)
#Define las ventanas de tiempo para T y P (no se usan aquí directamente).
    VENTANA_T = (-0.20, -0.08)
    VENTANA_P = ( -0.08,  0)
    #
    # ---- QRS 
#dibuja puntos de r q s
    for r in p2:
        # Dibuja un círculo rojo en cada pico R.
        pygame.draw.circle(screen, (255, 0, 0), escalar(r, y[r]), 4)

        for q in q_points:
            pygame.draw.circle(screen, (0, 0, 255), escalar(q, y[q]), 3)
        for s in s_points:
            pygame.draw.circle(screen, (0, 0, 255), escalar(s, y[s]), 3)

    # ---- dibujar valvulas 

    # cierre de mitral y tricuspide en R
    if cursor in eventos_r:
        estado_valvulas['tricuspide'] = 'cerrada'
        estado_valvulas['mitral'] = 'cerrada'

    # apertura de aortica y pulmonar en S
    if cursor in eventos_s:
        estado_valvulas['pulmonar'] = 'abierta'
        estado_valvulas['aortica'] = 'abierta'

    # cierre de pulmonar y aortica a los 3/4 del area T
    if cursor in eventos_t_3_4:
        estado_valvulas['pulmonar'] = 'cerrada'
        estado_valvulas['aortica'] = 'cerrada'

    # apertura de mitral y tricuspide al final del area T
    if cursor in eventos_t_fin:
        estado_valvulas['tricuspide'] = 'abierta'
        estado_valvulas['mitral'] = 'abierta'
#dibuja las válvulas usando círculos, pasando el color, el estado actual y el nombre de cada válvula. Se comenta la función de líneas para dejar solo la versión de círculos.
    dibujar_valvulas_circulos('azul', estado_valvulas['tricuspide'], 'tricuspide')
    #dibujar_valvulas('rojo', estado_valvulas['mitral'], 'mitral')


    dibujar_valvulas_circulos('rojo', estado_valvulas['mitral'], 'mitral')
    #dibujar_valvulas('rojo', estado_valvulas['mitral'], 'mitral')

    dibujar_valvulas_circulos('azul', estado_valvulas['pulmonar'], 'pulmonar')
    #dibujar_valvulas('azul', estado_valvulas['pulmonar'], 'pulmonar')

    dibujar_valvulas_circulos('rojo', estado_valvulas['aortica'], 'aortica')
    #dibujar_valvulas('rojo', estado_valvulas['aortica'], 'aortica')
#Dibuja un rectángulo oscuro detrás de los nombres de las válvulas para mejorar la legibilidad del texto.
    pygame.draw.rect(screen, (15, 15, 15), (1050, 360, 450, 50))
#Renderiza los textos de los nombres de las válvulas.
    texto_tricuspide = font.render("Tricúspide", True, (255, 255, 255))
    texto_pulmonar   = font.render("Pulmonar",   True, (255, 255, 255))
    texto_aortica    = font.render("Aórtica",    True, (255, 255, 255))
    texto_mitral     = font.render("Mitral",     True, (255, 255, 255))

    screen.blit(texto_tricuspide, (1085, 370))
    screen.blit(texto_pulmonar,   (1185, 370))
    screen.blit(texto_aortica,    (1285, 370))
    screen.blit(texto_mitral,     (1385, 370))

    # ---- CURSOR 
    #Dibuja una línea roja vertical en la posición actual del cursor.
    cx, _ = escalar(cursor, y[cursor])
    pygame.draw.line(
        screen,
        (255, 0, 0),
        (cx, ECG_Y),
        (cx, ECG_Y + ECG_HEIGHT),
        2
    )
    #Muestra el valor actual del cursor y el voltaje correspondiente.
    texto = font.render(
        f"X {cursor} | Voltaje = {y[cursor]:.3f}",
        True, (255, 255, 255)
    )
    screen.blit(texto, (700, 20))
    #Dibuja los botones de navegación.
    dibujar_botones_navegacion()
    # Avanza el cursor. Si llega al final de la señal, vuelve al inicio.
    cursor += 1
    if cursor >= len(y):
        cursor = 0
#Actualiza la pantalla con todo lo dibujado.
    pygame.display.flip()
#Sale de Pygame y cierra la ventana al terminar el bucle.
pygame.quit()