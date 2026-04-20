import pygame
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# ---------- INIT ----------
pygame.init()
WIDTH, HEIGHT = 1600,900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ECG monitor")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

VENTANAS = {
    "T": (-0.20, -0.08),   # PR
    "P": ( -0.08,  0),   # QT
}
INFO_RECT = pygame.Rect(0, 0, WIDTH, 36)

areas_P = []   # [(inicio, fin), ...]
areas_T = []
Fs=360
# ---------- AREA ECG ----------
ECG_X = 60
ECG_Y = 40
ECG_WIDTH = 880     # más grande
ECG_HEIGHT = 300    # más alto

ECG_RECT = pygame.Rect(ECG_X, ECG_Y, ECG_WIDTH, ECG_HEIGHT)



# ---------- CARGAR ECG ----------
numero=1
ruta = r'C:/Users/v84394/Downloads/train1000.csv'
df = pd.read_csv(ruta)
fila = df.iloc[numero]
y = pd.to_numeric(fila, errors='coerce').dropna().values
x = np.arange(len(y))

# ---------- QRS ----------
p2, _ = find_peaks(y, height=0.8, distance=1)

q_points, s_points = [], []
window = int(0.06 * len(y))
for r in p2:
    if r > 0:
        q_region = y[max(0, r-window):r]
        q_idx = np.argmin(q_region) + max(0, r-window)
        if abs(y[r] - y[q_idx]) >= 0.3:
            q_points.append(q_idx)

        s_region = y[r:r+window]
        s_idx = np.argmin(s_region) + r
        if abs(y[r] - y[s_idx]) >= 0.3:
            s_points.append(s_idx)
    #arreglos de
        p_ini = max(0, int(r + VENTANAS["P"][0] * Fs))
        p_fin = min(len(y)-1, int(r + VENTANAS["P"][1] * Fs))
        areas_P.append((p_ini, p_fin))

        t_ini = max(0, int(r + VENTANAS["T"][0] * Fs))
        t_fin = min(len(y)-1, int(r + VENTANAS["T"][1] * Fs))
        areas_T.append((t_ini, t_fin))

#
# ---------- ESCALA ----------

def escalar(i, valor):
    sx = ECG_X + int(i * ECG_WIDTH / len(y))
    sy = ECG_Y + ECG_HEIGHT // 2 - int(valor * 120)
    return sx, sy
# ---------- area ----------
def ventana_a_rect(r_idx, ventana_sec, color, alpha=80):
    """
    r_idx: índice de R
    ventana_sec: (inicio, fin) en segundos respecto a R
    color: (R, G, B)
    alpha: transparencia 0–255
    """
    Fs=360
    inicio_idx = int(r_idx + ventana_sec[0] * Fs)
    fin_idx    = int(r_idx + ventana_sec[1] * Fs)

    inicio_idx = max(0, inicio_idx)
    fin_idx    = min(len(y)-1, fin_idx)

    x1, _ = escalar(inicio_idx, 0)
    x2, _ = escalar(fin_idx, 0)

    ancho = x2 - x1
    if ancho <= 0:
        return None

    surf = pygame.Surface((ancho, ECG_HEIGHT), pygame.SRCALPHA)
    surf.fill((*color, alpha))

    return surf, (x1, ECG_Y)


# ---------- CUADRICULA ----------

def dibujar_cuadricula_ecg():
    color_fino = (30, 30, 30)
    color_grueso = (70, 70, 70)

    # Líneas finas
    for x in range(ECG_X, ECG_X + ECG_WIDTH, 20):
        pygame.draw.line(screen, color_fino, (x, ECG_Y), (x, ECG_Y + ECG_HEIGHT))
    for y in range(ECG_Y, ECG_Y + ECG_HEIGHT, 20):
        pygame.draw.line(screen, color_fino, (ECG_X, y), (ECG_X + ECG_WIDTH, y))

    # Líneas gruesas
    for x in range(ECG_X, ECG_X + ECG_WIDTH, 100):
        pygame.draw.line(screen, color_grueso, (x, ECG_Y), (x, ECG_Y + ECG_HEIGHT))
    for y in range(ECG_Y, ECG_Y + ECG_HEIGHT, 100):
        pygame.draw.line(screen, color_grueso, (ECG_X, y), (ECG_X + ECG_WIDTH, y))

    # Borde del ECG
    pygame.draw.rect(screen, (150, 150, 150), ECG_RECT, 2)


def dibujar_eje_x():
    pasos = 10
    for i in range(pasos + 1):
        x = ECG_X + i * (ECG_WIDTH // pasos)
        valor = int(i * len(y) / pasos)
        txt = font.render(str(valor), True, (200, 200, 200))
        screen.blit(txt, (x - 10, ECG_Y + ECG_HEIGHT + 5))


def dibujar_eje_y():
    pasos = 4
    for i in range(-pasos, pasos + 1):
        y_pos = ECG_Y + ECG_HEIGHT // 2 - i * (ECG_HEIGHT // (2 * pasos))
        txt = font.render(f"{i/2:.1f}", True, (200, 200, 200))
        screen.blit(txt, (ECG_X - 45, y_pos - 8))


def dibujar_valvulas(color, x, y, estatus):
    if color == 'azul':
        door_color = (0, 100, 255)
    elif color == 'rojo':
        door_color = (199, 39, 33)

    door_width = 2

    # Longitudes
    largo = 50
    separacion = 10

    if estatus == 'cerrada':
        # Líneas horizontales
        x1 = x
        x2 = x + largo
        x3 = x2 + separacion
        x4 = x3 + largo

        pygame.draw.line(screen, door_color, (x1, y), (x2, y), door_width)
        pygame.draw.line(screen, door_color, (x3, y), (x4, y), door_width)

    elif estatus == 'abierta':
        # Líneas verticales
        y1 = y
        x1=  x
        y2 = y - largo
        x2= x+largo+largo+separacion
        y3 = y2 + separacion
        y4 = y3 + largo

        pygame.draw.line(screen, door_color, (x1, y1), (x1, y2), door_width)
        pygame.draw.line(screen, door_color, (x2, y1), (x2, y2), door_width)


def dibujar_areas():
    for ini, fin in areas_P:
        x1, _ = escalar(ini, 0)
        x2, _ = escalar(fin, 0)
        surf = pygame.Surface((x2-x1, ECG_HEIGHT), pygame.SRCALPHA)
        surf.fill((160, 80, 200, 70))
        screen.blit(surf, (x1, ECG_Y))

    for ini, fin in areas_T:
        x1, _ = escalar(ini, 0)
        x2, _ = escalar(fin, 0)
        surf = pygame.Surface((x2-x1, ECG_HEIGHT), pygame.SRCALPHA)
        surf.fill((255, 140, 0, 70))
        screen.blit(surf, (x1, ECG_Y))

def dibujar_panel_info():
    pygame.draw.rect(screen, (20, 20, 20), INFO_RECT)
    if areas_P:
        p_txt = f"P: {areas_P[0][0]} → {areas_P[0][1]}"
        screen.blit(font.render(p_txt, True, (180, 120, 230)), (220, 8))
    if areas_T:
        t_txt = f"T: {areas_T[0][0]} → {areas_T[0][1]}"
        screen.blit(font.render(t_txt, True, (255, 170, 80)), (22, 8))

# ---------- ECG PRECALCULADO ----------
ecg_points = [escalar(i, y[i]) for i in range(len(y))]

# ---------- LOOP ----------
cursor = 0
running = True

while running:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # ---- GRID ----
    dibujar_panel_info()

    dibujar_cuadricula_ecg()
    dibujar_eje_x()
    dibujar_eje_y()

    dibujar_areas()

    pygame.draw.lines(screen, (0, 255, 0), False, ecg_points, 2)


    # ---- ECG COMPLETO ----
    pygame.draw.lines(screen, (0, 255, 0), False, ecg_points, 2)

    VENTANA_T = (-0.20, -0.08)   # PR
    VENTANA_P = ( -0.08,  0)   # QT




    # ---- QRS ----
    for r in p2:
        pygame.draw.circle(screen, (255, 0, 0), escalar(r, y[r]), 4)

        for q in q_points:
            pygame.draw.circle(screen, (0, 0, 255), escalar(q, y[q]), 3)
        for s in s_points:
            pygame.draw.circle(screen, (0, 0, 255), escalar(s, y[s]), 3)

    # ---- dibujar valvulas ---- 
    dibujar_valvulas('rojo',1100,100,'abierta') 
    dibujar_valvulas('azul',1300,100,'abierta')

    dibujar_valvulas('azul',1100,200,'cerrada')
    dibujar_valvulas('rojo',1300,200,'cerrada')
    #dibujar_valvulas('azul',1200,200,abierta,cerrada)

    #escribir titulo 

    # ---- CURSOR VERTICAL ----

    cx, _ = escalar(cursor, y[cursor])
    pygame.draw.line(
        screen,
        (255, 0, 0),
        (cx, ECG_Y),
        (cx, ECG_Y + ECG_HEIGHT),
        2
    )


    texto = font.render(
        f"X {cursor} | Voltaje = {y[cursor]:.3f}",
        True, (255, 255, 255)
    )
    screen.blit(texto, (700, 20))

    cursor += 1
    if cursor >= len(y):
        cursor = 0

    pygame.display.flip()

pygame.quit()