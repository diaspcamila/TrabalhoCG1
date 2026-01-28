import pygame
import math
import random

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

def desenhar_asa(tela, x, y, lado, ang, cor, s):
    # ponto onde a asa gruda na cabeça
    px = x + int(lado * 4 * s)
    py = y - int(6 * s)

    # centro da elipse antes da rotação
    cx = px + int(lado * 12 * s)
    cy = py

    draw_ellipse_pivot(
        tela,
        px, py,
        cx, cy,
        rx=int(12 * s),
        ry=int(4 * s),
        ang=ang * lado,
        cor=cor
    )

#animais e plantas
def setPlanta(tela, x, y):
    verde_mais_escuro = (0, 60, 0)
    verde_escuro = (0, 140, 0)
    verde = (0, 180, 0)

    s = 1.3  # escala da planta

    def sx(dx): return int(dx * s)
    def sy(dy): return int(dy * s)

    # caule
    setBresenham(tela, x + sx(-2), y + sy(-15), x + sx(1),  y + sy(-25), verde_escuro)
    setBresenham(tela, x + sx(-1), y + sy(0),   x + sx(-3), y + sy(-15), verde_escuro)

    cores_folha = [
        verde,
        verde,
        verde_mais_escuro,
        verde_mais_escuro
    ]

    # ---------- folha esquerda ----------
    folha_esq = [
        (x + sx(-10), y + sy(-20)),
        (x + sx(-2),  y + sy(-15)),
        (x + sx(-10), y + sy(-10)),
        (x + sx(-18), y + sy(-15))
    ]

    for i in range(4):
        x0, y0 = folha_esq[i]
        x1, y1 = folha_esq[(i+1) % 4]
        setBresenham(tela, x0, y0, x1, y1, verde_escuro)

    scanline_fill_gradiente(tela, folha_esq, cores_folha)

    # ---------- folha direita ----------
    folha_dir = [
        (x + sx(7),  y + sy(-25)),
        (x + sx(15), y + sy(-20)),
        (x + sx(7),  y + sy(-15)),
        (x + sx(1),  y + sy(-20))
    ]

    for i in range(4):
        x0, y0 = folha_dir[i]
        x1, y1 = folha_dir[(i+1) % 4]
        setBresenham(tela, x0, y0, x1, y1, verde_escuro)

    scanline_fill_gradiente(tela, folha_dir, cores_folha)


def setMosca(tela, x, y, fase, s=0.6):
    preto = (0, 0, 0)
    cinza = (120, 120, 120)
    branco = (230, 230, 230)

    max_ang = math.radians(70)
    ang = max_ang * (abs(math.sin(fase)))

    # asas
    desenhar_asa(tela, x, y, -1, ang, branco, s)
    desenhar_asa(tela, x, y,  1, ang, branco, s)

    # cabeça
    setCircle(tela, x, y - int(6*s), int(5*s), preto)
    setFloodFill(tela, x, y - int(6*s), cinza, preto)


def setSapo(tela, x, y, fase, lingua):
    azul = (0,200,230)
    azul_esc = (30, 50, 100)
    borda = (0,20,80)
    vermelho = (255, 0, 0)

    # ---------- CORPO ----------
    corpo = trapezio_pequeno(x, y-14, topo=26, base=40, h=20)

    for i in range(len(corpo)):
        x0, y0 = corpo[i]
        x1, y1 = corpo[(i+1) % len(corpo)]
        setBresenham(tela, x0, y0, x1, y1, borda)

    cores_corpo = [
        azul,
        azul,
        azul_esc,
        azul_esc
    ]
    scanline_fill_gradiente(tela, corpo, cores_corpo)

    # ---------- CABEÇA ----------
    cabeca = hexagono_largo(x, y-30, w=50, h=16)
    cores_cabeca = [
        azul,
        azul,
        azul,
        azul,
        azul_esc,
        azul_esc
    ]

    for i in range(len(cabeca)):
        x0, y0 = cabeca[i]
        x1, y1 = cabeca[(i+1) % len(cabeca)]
        setBresenham(tela, x0, y0, x1, y1, borda)

    scanline_fill_gradiente(tela, cabeca, cores_cabeca)

    olho_y = y - 47
    dx = 12

    # cores
    branco = (255,255,255)

    piscar = (int(fase) % 8 == 0)

    for lado in (-1, 1):
        cx = x + lado * dx

        setCircle(tela, cx, olho_y, 5, azul)
        setFloodFill(tela, cx, olho_y, azul, borda)


        if piscar:
            # olho fechado
            setBresenham(tela, cx - 4, olho_y, cx + 4, olho_y, borda)
        else:

            # branco do olho
            setCircle(tela, cx, olho_y, 5, borda)
            setFloodFill(tela, cx, olho_y, branco, borda)

            # pupila
            setCircle(tela, cx, olho_y, 2, (0,0,0))
            setFloodFill(tela, cx, olho_y, (0,0,0), borda)


    # ---------- PATAS ----------
    chao = y + 7
    altura = 12
    sep = 14
    cores_patas = [
        azul_esc,
        azul_esc,
        azul
    ]

    # -------- pata esquerda --------
    pata_esq = [
        (x - (14 + sep), chao),
        (x - (2  + sep), chao),
        (x - (8  + sep), chao - altura)
    ]

    for i in range(3):
        x0, y0 = pata_esq[i]
        x1, y1 = pata_esq[(i+1) % 3]
        setBresenham(tela, x0, y0, x1, y1, borda)

    scanline_fill_gradiente(tela, pata_esq, cores_patas)

    # -------- pata direita --------
    pata_dir = [
        (x + (2  + sep), chao),
        (x + (14 + sep), chao),
        (x + (8  + sep), chao - altura)
    ]

    for i in range(3):
        x0, y0 = pata_dir[i]
        x1, y1 = pata_dir[(i+1) % 3]
        setBresenham(tela, x0, y0, x1, y1, borda)

    scanline_fill_gradiente(tela, pata_dir, cores_patas)

    # ---------- BOCA (LINHAS) ----------
    frente_y = y - 22
    dist = 10          

    setBresenham(tela, x - dist, frente_y, x - dist - 10, frente_y - 8, borda)
    setBresenham(tela, x + dist, frente_y, x + dist + 10, frente_y - 8, borda)
    setBresenham(tela, x - dist, frente_y, x + dist, frente_y, borda)

    # ---------- BRAÇO (LINHAS) ----------
    frente_y = y
    dist = 4

    # braço esquerdo
    x1, y1 = x - dist, frente_y
    x2, y2 = x - dist - 8, frente_y - 10
    setBresenham(tela, x1, y1+4, x2+1, y2, borda)

    setBresenham(tela, x2, y2+12, x2 + 4, y2 + 6, borda)

    # braço direito
    x3, y3 = x + dist, frente_y
    x4, y4 = x + dist + 8, frente_y - 10
    setBresenham(tela, x3, y3+4, x4-1, y4, borda)

    setBresenham(tela, x4, y4+12, x4 - 4, y4 + 6, borda)

    if lingua > 0:
        setBresenham(tela, x-1, frente_y, x, frente_y - 20, vermelho)
        setBresenham(tela, x, frente_y, x, frente_y - 20, vermelho)
        setBresenham(tela, x + 1, frente_y, x, frente_y - 20, vermelho)

#bioma mar
def setPeixe(tela, x, y, fase):
    laranja = (255, 140, 100)
    laranja_esc = (250, 100, 80)
    borda = (255, 40, 90)
    branco = (255, 255, 255)

    piscar = (int(fase) % 25 == 0)

    # ---------- ANIMAÇÃO ----------
    ond = int(4 * math.sin(fase * 0.3))   # balanço lateral
    cauda_ang = math.sin(fase * 0.5) * 0.6

    # ---------- CORPO (ELIPSE) ----------
    rx = 16
    ry = 9

    # borda
    setEllipse(tela, x + ond, y, rx, ry, borda)

    # preenchimento simples (flood)
    setFloodFill(tela, x + ond, y, laranja, borda)

    # sombra inferior
    for dy in range(0, ry):
        for dx in range(-rx, rx):
            if (dx*dx)/(rx*rx) + (dy*dy)/(ry*ry) <= 1:
                setPixel(tela, x + ond + dx, y + dy, laranja_esc)

    # ---------- CAUDA (TRIÂNGULO BALANÇANDO) ----------
    base_x = x - rx + ond
    base_y = y

    dx = int(10 * math.cos(cauda_ang))
    dy = int(10 * math.sin(cauda_ang))

    cauda = [
        (base_x, base_y),
        (base_x - 12 + dy, base_y - 8 - dx),
        (base_x - 12 - dy, base_y + 8 + dx)
    ]

    for i in range(3):
        x0, y0 = cauda[i]
        x1, y1 = cauda[(i+1) % 3]
        setBresenham(tela, x0, y0, x1, y1, borda)

    scanline_fill_gradiente(tela, cauda, [laranja_esc, laranja, laranja])

    # ---------- OLHO (COM PISCAR) ----------
    olho_x = x + 6 + ond
    olho_y = y - 2

    if piscar:
        # olho fechado (linha)
        setBresenham(tela, olho_x - 3, olho_y, olho_x + 3, olho_y, (0,0,0))
    else:
        # olho aberto
        setCircle(tela, olho_x, olho_y, 3, (0,0,0))
        setFloodFill(tela, olho_x, olho_y, branco, (0,0,0))

        setCircle(tela, olho_x, olho_y, 1, (0,0,0))
        setFloodFill(tela, olho_x, olho_y, (0,0,0), (0,0,0))


    setCircle(tela, olho_x, olho_y, 3, (0,0,0))
    setFloodFill(tela, olho_x, olho_y, branco, (0,0,0))

    setCircle(tela, olho_x, olho_y, 1, (0,0,0))
    setFloodFill(tela, olho_x, olho_y, (0,0,0), (0,0,0))


def setTubarao(tela, x, y, fase, comendo=False):
    cinza = (140, 140, 150)
    cinza_esc = (90, 90, 100)
    branco = (220, 220, 220)
    borda = (30, 30, 40)

    piscar = (int(fase) % 25 == 0)

    # ---------- CORPO (ELIPSE) ----------
    rx = 38
    ry = 14

    # borda da elipse
    setEllipse(tela, x, y, rx, ry, borda)

    # preenchimento (flood fill)
    setFloodFill(tela, x, y, cinza, borda)

    # sombra barriga
    setEllipse(tela, x, y + 4, rx - 6, ry - 6, branco)
    setFloodFill(tela, x, y + 4, branco, borda)

    # ---------- BARBATANA SUPERIOR ----------
    barbatana = [
        (x - 5, y - ry - 10),
        (x + 6, y - ry + 2),
        (x - 18, y - ry + 2)
    ]

    for i in range(3):
        x0, y0 = barbatana[i]
        x1, y1 = barbatana[(i + 1) % 3]
        setBresenham(tela, x0, y0, x1, y1, borda)

    scanline_fill_gradiente(tela, barbatana, [cinza_esc]*3)

    # ---------- CAUDA (BALANÇANDO) ----------
    swing = int(8 * math.sin(fase))

    cauda = [
        (x - rx + 2, y),
        (x - rx - 20 + swing, y - 14),
        (x - rx - 20 + swing, y + 14)
    ]

    for i in range(3):
        x0, y0 = cauda[i]
        x1, y1 = cauda[(i + 1) % 3]
        setBresenham(tela, x0, y0, x1, y1, borda)

    scanline_fill_gradiente(tela, cauda, [cinza_esc]*3)

     # ---------- OLHO (COM PISCAR) ----------
    olho_x = x + 14
    olho_y = y - 4

    if piscar:
        # olho fechado (linha)
        setBresenham(tela, olho_x - 3, olho_y, olho_x + 3, olho_y, borda)
    else:
        # olho aberto
        setCircle(tela, olho_x, olho_y, 3, borda)
        setFloodFill(tela, olho_x, olho_y, (255, 255, 255), borda)

        setCircle(tela, olho_x, olho_y, 1, (0,0,0))
        setFloodFill(tela, olho_x, olho_y, (0,0,0), borda)

    # ---------- BOCA (ABRE QUANDO COME) ----------
    boca_x1 = x + 16
    boca_x2 = x + 32
    boca_y = y + 6

    if comendo:
        abertura = 6
        # boca aberta (V)
        setBresenham(tela, boca_x1-6, boca_y, boca_x2-6, boca_y - abertura, borda)
        setBresenham(tela, boca_x1-6, boca_y, boca_x2-6, boca_y + abertura, borda)
    else:
        # boca fechada
        setBresenham(tela, boca_x1, boca_y, boca_x2, boca_y, borda)


def setAlga(tela, x, y, fase):
    verde1 = (0, 160, 0)
    verde2 = (0, 180, 0)

    ramos = [
        {"dx": -8, "altura": 22, "amp": 2.0, "invert": False},  # esquerda
        {"dx":  0, "altura": 32, "amp": 3.5, "invert": True},   # meio (S invertido)
        {"dx":  8, "altura": 22, "amp": 2.0, "invert": False},  # direita
    ]

    for i, r in enumerate(ramos):
        bx = x + r["dx"]
        by = y

        px, py = bx, by

        for t in range(1, r["altura"]):
            direcao = -1 if r["invert"] else 1

            curva = math.sin((t * 0.25) + fase * 0.6) * r["amp"] * direcao
            nx = int(bx + curva)
            ny = by - t

            cor = verde1 if (t % 2 == 0) else verde2

            # --------- ESPESSURA ---------
            # mais grosso na base, fino no topo
            if t < r["altura"] * 0.3:
                esp = 2
            elif t < r["altura"] * 0.6:
                esp = 1
            else:
                esp = 0

            # desenha várias linhas lado a lado
            for e in range(-esp, esp + 1):
                setBresenham(tela, px + e, py, nx + e, ny, cor)

            px, py = nx, ny


# textura floresta
def fundo_grama(superficie, passo=3):
    w, h = superficie.get_width(), superficie.get_height()
    superficie.lock()

    for y in range(0, h, passo):
        for x in range(0, w, passo):
            g = random.randint(200, 225)
            r = random.randint(0, 90)

            for dy in range(passo):
                for dx in range(passo):
                    setPixel(superficie, x + dx, y + dy, (r, g, r))

    superficie.unlock()

def ruido_grama(superficie, qtd=15000):
    w = superficie.get_width()
    h = superficie.get_height()

    superficie.lock()
    for _ in range(qtd):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)

        g = random.randint(140, 180)
        r = random.randint(30, 50)

        setPixel(superficie, x, y, (r, g, r))
    superficie.unlock()

def fiapos_grama(superficie, qtd=4000):
    w = superficie.get_width()
    h = superficie.get_height()

    superficie.lock()
    for _ in range(qtd):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)

        hastes = random.randint(2, 5)  # quantas folhas no tufo

        for _ in range(hastes):
            tam = random.randint(5, 10)
            dx = random.choice([-1, 0, 1])

            cor = random.choice([
                (40, 130, 40),
                (90, 220, 90),
                (60, 160, 60)
            ])

            setBresenham(superficie, x, y, x + dx, y - tam, cor)
    superficie.unlock()

def textura_floresta(superficie):
    fundo_grama(superficie)
    ruido_grama(superficie, 8000)
    fiapos_grama(superficie, 3500)

#textura mar
def fundo_mar(superficie, passo=2):
    w, h = superficie.get_width(), superficie.get_height()
    superficie.lock()

    for y in range(0, h, passo):
        t = y / h

        # gradiente: mais claro em cima, mais escuro embaixo
        r = int(20 + 20 * t)
        g = int(120 + 60 * t)
        b = int(200 + 30 * t)

        for x in range(0, w, passo):
            for dy in range(passo):
                for dx in range(passo):
                    setPixel(superficie, x + dx, y + dy, (r, g, b))

    superficie.unlock()

def ruido_mar(superficie, qtd=10000):
    w, h = superficie.get_width(), superficie.get_height()
    superficie.lock()

    for _ in range(qtd):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)

        cor = random.choice([
            (30, 150, 210),
            (20, 130, 190),
            (40, 170, 230)
        ])

        setPixel(superficie, x, y, cor)

    superficie.unlock()

def ondas_mar(superficie, qtd=3000):
    w, h = superficie.get_width(), superficie.get_height()
    superficie.lock()

    for _ in range(qtd):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)

        tam = random.randint(4, 10)

        cor = random.choice([
            (180, 220, 255),
            (160, 210, 240)
        ])

        setBresenham(superficie, x, y, x + tam, y + random.choice([-1, 0, 1]), cor)

    superficie.unlock()

def textura_mar(superficie):
    fundo_mar(superficie)
    ruido_mar(superficie, 12000)
    ondas_mar(superficie, 2500)


