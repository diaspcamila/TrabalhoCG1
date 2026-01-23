import pygame
import math

#set_pixel
def setPixel(superficie, x, y, cor):
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((x, y), cor)

#primitivas
def setBresenham(superficie, x0, y0, x1, y1, cor):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)
    ystep = 1 if y0 < y1 else -1

    d = 2 * dy - dx
    y = y0

    for x in range(x0, x1 + 1):
        if steep:
            setPixel(superficie, y, x, cor)
        else:
            setPixel(superficie, x, y, cor)

        if d > 0:
            y += ystep
            d -= 2 * dx
        d += 2 * dy

def setCircle(tela, xc, yc, r, cor):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        pontos = [
            ( xc+x, yc+y), ( xc-x, yc+y),
            ( xc+x, yc-y), ( xc-x, yc-y),
            ( xc+y, yc+x), ( xc-y, yc+x),
            ( xc+y, yc-x), ( xc-y, yc-x)
        ]
        for px, py in pontos:
            setPixel(tela, px, py, cor)

        if d < 0:
            d += 2*x + 3
        else:
            d += 2*(x - y) + 5
            y -= 1
        x += 1

def setEllipse(tela, xc, yc, rx, ry, cor):
    x = 0
    y = ry

    rx2 = rx*rx
    ry2 = ry*ry
    d1 = ry2 - rx2*ry + 0.25*rx2

    dx = 2*ry2*x
    dy = 2*rx2*y

    # Região 1
    while dx < dy:
        plot_ellipse_points(tela, xc, yc, x, y, cor)
        if d1 < 0:
            x += 1
            dx += 2*ry2
            d1 += dx + ry2
        else:
            x += 1
            y -= 1
            dx += 2*ry2
            dy -= 2*rx2
            d1 += dx - dy + ry2

    # Região 2
    d2 = (ry2*(x+0.5)**2) + (rx2*(y-1)**2) - rx2*ry2
    while y >= 0:
        plot_ellipse_points(tela, xc, yc, x, y, cor)
        if d2 > 0:
            y -= 1
            dy -= 2*rx2
            d2 += rx2 - dy
        else:
            y -= 1
            x += 1
            dx += 2*ry2
            dy -= 2*rx2
            d2 += dx - dy + rx2

def plot_ellipse_points(tela, xc, yc, x, y, cor):
    setPixel(tela, xc+x, yc+y, cor)
    setPixel(tela, xc-x, yc+y, cor)
    setPixel(tela, xc+x, yc-y, cor)
    setPixel(tela, xc-x, yc-y, cor)

def setBordaRetangulo(superficie, x, y, w, h, cor):
    setBresenham(superficie, x, y, x+w, y, cor)
    setBresenham(superficie, x+w, y, x+w, y+h, cor)
    setBresenham(superficie, x+w, y+h, x, y+h, cor)
    setBresenham(superficie, x, y+h, x, y, cor)

#preenchimento
def setFloodFill(superficie, x, y, cor_preenchimento, cor_borda):
    largura = superficie.get_width()
    altura = superficie.get_height()

    pilha = [(x, y)]
    contador = 0

    while pilha:
        px, py = pilha.pop()

        if not (0 <= px < largura and 0 <= py < altura):
            continue

        cor_atual = superficie.get_at((px, py))[:3]

        if cor_atual == cor_borda or cor_atual == cor_preenchimento:
            continue

        setPixel(superficie, px, py, cor_preenchimento)

        pilha.append((px + 1, py))
        pilha.append((px - 1, py))
        pilha.append((px, py + 1))
        pilha.append((px, py - 1))

        contador += 1
        if contador % 5000 == 0:
            pygame.display.flip()

def setScanlineFill(superficie, pontos, cor_preenchimento):
    # Encontra Y mínimo e máximo
    ys = [p[1] for p in pontos]
    y_min = min(ys)
    y_max = max(ys)

    n = len(pontos)

    for y in range(y_min, y_max):
        intersecoes_x = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            # Ignora arestas horizontais
            if y0 == y1:
                continue

            # Garante y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            # Regra Ymin ≤ y < Ymax
            if y < y0 or y >= y1:
                continue

            # Calcula interseção
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersecoes_x.append(x)

        # Ordena interseções
        intersecoes_x.sort()

        # Preenche entre pares
        for i in range(0, len(intersecoes_x), 2):
            if i + 1 < len(intersecoes_x):
                x_inicio = int(round(intersecoes_x[i]))
                x_fim = int(round(intersecoes_x[i + 1]))

                for x in range(x_inicio, x_fim + 1):
                    setPixel(superficie, x, y, cor_preenchimento)

#transformações geométricas
def draw_ellipse_pivot(tela, px, py, cx, cy, rx, ry, ang, cor):
    passos = 80

    cos_a = math.cos(ang)
    sin_a = math.sin(ang)

    for i in range(passos):
        t = 2 * math.pi * i / passos

        x = cx + rx * math.cos(t)
        y = cy + ry * math.sin(t)

        # rotação em torno do pivô (px, py)
        xr = px + cos_a*(x - px) - sin_a*(y - py)
        yr = py - sin_a*(x - px) + cos_a*(y - py)

        setPixel(tela, int(xr), int(yr), cor)

def desenhar_asa(tela, x, y, lado, ang, cor):
    # ponto onde a asa gruda na cabeça
    px = x + lado * 4
    py = y - 6

    # centro da elipse ANTES da rotação (asa aberta)
    cx = px + lado * 12
    cy = py

    draw_ellipse_pivot(
        tela,
        px, py,        # pivô (grudado)
        cx, cy,        # centro da elipse
        rx=12, ry=4,
        ang=ang * lado,
        cor=cor
    )

#animais e plantas
def setPlanta(tela, x, y):
    verde_escuro = (0, 140, 0)
    verde = (0, 180, 0)

    setBresenham(tela, x, y, x, y-30, verde_escuro)

    setEllipse(tela, x-10, y-15, 10, 5, verde_escuro)
    setFloodFill(tela, x-10, y-15, verde, verde_escuro)

    setEllipse(tela, x+10, y-20, 10, 5, verde_escuro)
    setFloodFill(tela, x+10, y-20, verde, verde_escuro)

def setMosca(tela, x, y, fase):
    preto = (0, 0, 0)
    cinza = (120, 120, 120)
    branco = (230, 230, 230)

    max_ang = math.radians(70)
    ang = max_ang * (abs(math.sin(fase)))

    desenhar_asa(tela, x, y, -1, ang, branco)
    desenhar_asa(tela, x, y,  1, ang, branco)

    setCircle(tela, x, y-6, 5, preto)
    setFloodFill(tela, x, y-6, cinza, preto)

def setSapo(tela, x, y):
    azul = (0,200,230)
    borda = (0,20,80)
    branco = (255,255,255)

    # Corpo (elipse)
    setEllipse(tela, x, y+10, 25, 18, borda)
    setFloodFill(tela, x, y+10, azul, borda)

    # Cabeça (círculo)
    setCircle(tela, x, y-5, 14, borda)
    setFloodFill(tela, x, y-5, azul, borda)
    # Olhos
    setCircle(tela, x-6, y-10, 3, branco)
    setCircle(tela, x+6, y-10, 3, branco)