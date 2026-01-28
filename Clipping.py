from Transformacoes import multiplicar_matrizes, escala, identidade, translacao
from Formas import *

INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

def codigo_regiao(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= TOP  # y cresce para baixo
    elif y > ymax:
        code |= BOTTOM
    return code


def cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    c0 = codigo_regiao(x0, y0, xmin, ymin, xmax, ymax)
    c1 = codigo_regiao(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if not (c0 | c1):
            return True, x0, y0, x1, y1  # totalmente visível

        if c0 & c1:
            return False, None, None, None, None  # totalmente fora

        c_out = c0 if c0 else c1

        x, y = x0, y0

        if c_out & TOP:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin
        elif c_out & BOTTOM:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax
        elif c_out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax
        elif c_out & LEFT:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin

        if c_out == c0:
            x0, y0 = x, y
            c0 = codigo_regiao(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            c1 = codigo_regiao(x1, y1, xmin, ymin, xmax, ymax)

#janela p  viewport
def janela_viewport(janela, viewport):
    Wxmin, Wymin, Wxmax, Wymax = janela
    Vxmin, Vymin, Vxmax, Vymax = viewport

    sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
    sy = (Vymax - Vymin) / (Wymax - Wymin)  # Y para baixo (sem inversão)

    m = identidade()
    m = multiplicar_matrizes(translacao(-Wxmin, -Wymin), m)
    m = multiplicar_matrizes(escala(sx, sy), m)
    m = multiplicar_matrizes(translacao(Vxmin, Vymin), m)
    return m

#sutherland hodgman
def dentroClip(ponto, aresta, janela):
    x, y = ponto
    xmin, ymin, xmax, ymax = janela

    if aresta == 'LEFT':
        return x >= xmin
    elif aresta == 'RIGHT':
        return x <= xmax
    elif aresta == 'BOTTOM':
        return y <= ymax
    elif aresta == 'TOP':
        return y >= ymin
    return True

def intersecao(p1, p2, aresta, janela):
    x1, y1, = p1
    x2, y2 = p2
    xmin, ymin, xmax, ymax = janela

    dx = x2-x1
    dy = y2-y1

    if aresta == 'LEFT':
        x = xmin
        if dx == 0:
            return x1, y1
        t = (xmin - x1)/dx
        y = y1 + t*dy
        return x,y
    if aresta == 'RIGHT':
        x = xmax
        if dx == 0:
            return x1, y1
        t = (xmax - x1)/dx
        y = y1 + t*dy
        return x,y
    if aresta == 'BOTTOM':
        y = ymax
        if dy == 0:
            return x1, y1
        t = (ymax - y1)/dy
        x = x1 + t*dx
        return x,y
    if aresta == 'TOP':
        y = ymin
        if dy == 0:
            return x1, y1
        t = (ymin - y1)/dy
        x = x1 + t*dx
        return x,y
    return x1, y1

def sutherlandhodgman(pontos, janela):
    if not pontos:
        return []

    saida = pontos[:]
    for aresta in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP']:
        entrada = saida
        saida = []
        if not entrada:
            break

        s = entrada[-1]

        for e in entrada:
            e_dentro = dentroClip(e, aresta, janela)
            s_dentro = dentroClip(s, aresta, janela)

            if e_dentro:
                if not s_dentro:
                    saida.append(intersecao(s, e, aresta, janela))
                saida.append(e)
            else:
                if s_dentro:
                    saida.append(intersecao(s, e, aresta, janela))
            s = e
    return saida

#desenhos:
def desenhar_poligono(superficie, pontos, cor):
    n = len(pontos)
    for i in range(n):
        x0, y0 = pontos[i]
        x1, y1 = pontos[(i + 1) % n]
        setBresenham(superficie, int(x0), int(y0), int(x1), int(y1), cor)

def desenhar_linha_recortada(superficie, x0, y0, x1, y1, janela, viewport, cor):
    xmin, ymin, xmax, ymax = janela
    visivel, cx0, cy0, cx1, cy1 = cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
    if not visivel:
        return

    m = janela_viewport(janela, viewport)

    setBresenham(superficie, int(cx0), int(cy0), int(cx1), int(cy1), cor)

def desenhar_poligono_recortado(superficie, pontos, janela, viewport, cor):
    pontos_clip = sutherlandhodgman(pontos, janela)
    if len(pontos_clip) < 2:
        return

    for i in range(len(pontos_clip)):
        x, y = pontos_clip[i]
        pontos_clip[i] = int(x), int(y)

    desenhar_poligono(superficie, pontos_clip, cor)

def scanlineGrad_poligono_recortado(superficie, pontos, janela, viewport, cores):
    pontos_clip = sutherlandhodgman(pontos, janela)
    if len(pontos_clip) < 2:
        return

    if len(pontos_clip) > len(cores):
        for i in range(len(pontos_clip)-len(cores)):
            cores.append(cores[0])

    for i in range(len(pontos_clip)):
        x, y = pontos_clip[i]
        pontos_clip[i] = int(x), int(y)

    scanline_fill_gradiente(superficie, pontos_clip, cores)