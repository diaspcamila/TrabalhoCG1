import pygame
import random
from Formas import *
from Clipping import desenhar_linha_recortada, desenhar_poligono_recortado, scanlineGrad_poligono_recortado

#animais e plantas
def setPlanta(tela, x, y, viewport): # TODO adicionar clipping
    w, h = tela.get_size() #proporções da tela, para clipping
    tam_tela = (0, 0, w, h)

    verde_mais_escuro = (0, 60, 0)
    verde_escuro = (0, 140, 0)
    verde = (0, 180, 0)

    s = 1.3  # escala da planta

    def sx(dx): return int(dx * s)
    def sy(dy): return int(dy * s)

    # caule
    desenhar_linha_recortada(tela, x + sx(-2), y + sy(-15), x + sx(1),  y + sy(-25), tam_tela, viewport, verde_escuro)
    desenhar_linha_recortada(tela, x + sx(-1), y + sy(0),   x + sx(-3), y + sy(-15), tam_tela, viewport, verde_escuro)

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

def setMosca(tela, x, y, viewport, fase, s=0.6): #TODO adicionar clipping
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


def setSapo(tela, x, y, fase, viewport, lingua): #TODO adicionar clipping
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
def setPeixe(tela, x, y, viewport, fase): #TODO adicionar clipping
    azul = (80, 170, 220)
    azul_esc = (30, 90, 160)
    borda = (0, 40, 90)
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
    setFloodFill(tela, x + ond, y, azul, borda)

    # sombra inferior
    for dy in range(0, ry):
        for dx in range(-rx, rx):
            if (dx*dx)/(rx*rx) + (dy*dy)/(ry*ry) <= 1:
                setPixel(tela, x + ond + dx, y + dy, azul_esc)

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

    scanline_fill_gradiente(tela, cauda, [azul_esc, azul, azul])

    # ---------- OLHO (COM PISCAR) ----------
    olho_x = x + 6 + ond
    olho_y = y - 2

    if piscar:
        # olho fechado (linha)
        setBresenham(tela, olho_x - 3, olho_y, olho_x + 3, olho_y, borda)
    else:
        # olho aberto
        setCircle(tela, olho_x, olho_y, 3, borda)
        setFloodFill(tela, olho_x, olho_y, branco, borda)

        setCircle(tela, olho_x, olho_y, 1, (0,0,0))
        setFloodFill(tela, olho_x, olho_y, (0,0,0), borda)


    setCircle(tela, olho_x, olho_y, 3, borda)
    setFloodFill(tela, olho_x, olho_y, branco, borda)

    setCircle(tela, olho_x, olho_y, 1, (0,0,0))
    setFloodFill(tela, olho_x, olho_y, (0,0,0), borda)


def setTubarao(tela, x, y, fase, viewport, comendo=False): #TODO adicionar clipping
    cinza = (140, 140, 150)
    cinza_esc = (90, 90, 100)
    branco = (220, 220, 220)
    borda = (30, 30, 40)

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

    # ---------- OLHO ----------
    olho_x = x + 14
    olho_y = y - 4

    setCircle(tela, olho_x, olho_y, 3, borda)
    setFloodFill(tela, olho_x, olho_y, (0, 0, 0), borda)

    # ---------- BOCA (ABRE QUANDO COME) ----------
    boca_x1 = x + 10
    boca_x2 = x + 26
    boca_y = y + 6

    if comendo:
        abertura = 6
        # boca aberta (V)
        setBresenham(tela, boca_x1, boca_y, boca_x2, boca_y - abertura, borda)
        setBresenham(tela, boca_x1, boca_y, boca_x2, boca_y + abertura, borda)
    else:
        # boca fechada
        setBresenham(tela, boca_x1, boca_y, boca_x2, boca_y, borda)


def setAlga(tela, x, y, viewport, fase): #TODO adicionar clipping
    verde1 = (20, 120, 60)
    verde2 = (40, 170, 90)
    verde3 = (10, 90, 50)

    altura = 35
    hastes = 5

    for i in range(hastes):
        # espalha as hastes
        bx = x + i * 4 - 8
        by = y

        # fase diferente pra cada haste
        f = fase + i * 0.7

        px, py = bx, by

        for t in range(1, altura):
            # curva da alga (balanço)
            dx = int(4 * math.sin(f * 0.8 + t * 0.2))
            nx = bx + dx
            ny = by - t

            cor = random.choice([verde1, verde2, verde3])

            setBresenham(tela, px, py, nx, ny, cor)

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


