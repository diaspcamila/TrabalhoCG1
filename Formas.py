import math
import pygame

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

def hexagono_largo(cx, cy, w, h):
    return [
        (cx - w//2, cy),
        (cx - w//4, cy - h),
        (cx + w//4, cy - h),
        (cx + w//2, cy),
        (cx + w//4, cy + h),
        (cx - w//4, cy + h),
    ]

def trapezio_pequeno(cx, cy, topo, base, h):
    return [
        (cx - topo//2, cy),
        (cx + topo//2, cy),
        (cx + base//2, cy + h),
        (cx - base//2, cy + h),
    ]

def losango(cx, cy, w, h):
    return [
        (cx,     cy - h),  # cima
        (cx + w, cy),      # direita
        (cx,     cy + h),  # baixo
        (cx - w, cy)       # esquerda
    ]

def setPixelGrosso(tela, x, y, cor, tamanho=2):
    for dx in range(-tamanho//2, tamanho//2 + 1):
        for dy in range(-tamanho//2, tamanho//2 + 1):
            setPixel(tela, x + dx, y + dy, cor)

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
    # Encontra Y mínimo e máximo4

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


def interpola_cor(c1, c2, t): #função auxiliar
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)

    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))

    return r, g, b

def scanline_fill_gradiente(superficie, pontos, cores):
    ys = [p[1] for p in pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(pontos)

    for y in range(y_min, y_max):
        intersecoes = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            c0 = cores[i]
            c1 = cores[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                c0, c1 = c1, c0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)
            cor_y = interpola_cor(c0, c1, t)

            intersecoes.append((x, cor_y))

        intersecoes.sort(key=lambda i: i[0])

        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                x_ini, cor_ini = intersecoes[i]
                x_fim, cor_fim = intersecoes[i + 1]

                if x_fim == x_ini:
                    continue

                for x in range(int(x_ini), int(x_fim) + 1):
                    t = (x - x_ini) / (x_fim - x_ini)
                    cor = interpola_cor(cor_ini, cor_fim, t)
                    setPixel(superficie, x, y, cor)

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