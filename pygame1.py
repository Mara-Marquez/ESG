import pygame
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# ---------- INIT ----------
pygame.init()
WIDTH, HEIGHT = 2000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ECG monitor")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ---------- AREA ECG ----------
ECG_X = 60
ECG_Y = 40
ECG_WIDTH = 880     # más grande
ECG_HEIGHT = 300    # más alto

ECG_RECT = pygame.Rect(ECG_X, ECG_Y, ECG_WIDTH, ECG_HEIGHT)



# ---------- CARGAR ECG ----------
numero=4
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

# ---------- ESCALA ----------

def escalar(i, valor):
    sx = ECG_X + int(i * ECG_WIDTH / len(y))
    sy = ECG_Y + ECG_HEIGHT // 2 - int(valor * 120)
    return sx, sy


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


# ---------- ECG PRECALCULADO ----------
ecg_points = [escalar(i, y[i]) for i in range(len(y))]

# ---------- LOOP ----------
cursor = 0
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # ---- GRID ----
   
    dibujar_cuadricula_ecg()
    dibujar_eje_x()
    dibujar_eje_y()

    pygame.draw.lines(screen, (0, 255, 0), False, ecg_points, 2)


    # ---- ECG COMPLETO ----
    pygame.draw.lines(screen, (0, 255, 0), False, ecg_points, 2)

    # ---- QRS ----
    for r in p2:
        pygame.draw.circle(screen, (255, 0, 0), escalar(r, y[r]), 4)
    for q in q_points:
        pygame.draw.circle(screen, (0, 255, 0), escalar(q, y[q]), 3)
    for s in s_points:
        pygame.draw.circle(screen, (0, 0, 255), escalar(s, y[s]), 3)

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