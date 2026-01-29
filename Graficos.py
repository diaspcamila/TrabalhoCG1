import pygame
import random
from Formas import *
from Clipping import desenhar_linha_recortada, desenhar_poligono_recortado, scanlineGrad_poligono_recortado

#animais e plantas
def setPlanta(tela, x, y, viewport, zoom=1.0):
    w, h = tela.get_size() #proporções da tela, para clipping
    tam_tela = (0, 0, w, h)

    verde_mais_escuro = (0, 60, 0)
    verde_escuro = (0, 140, 0)
    verde = (0, 180, 0)

    s = 1.3 * zoom # escala da planta

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
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, verde_escuro)

    scanlineGrad_poligono_recortado(tela, folha_esq, tam_tela, viewport, cores_folha)

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
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, verde_escuro)

    scanlineGrad_poligono_recortado(tela, folha_dir, tam_tela, viewport, cores_folha)

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

def setMosca(tela, x, y, viewport, fase, s=0.6):
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


def setSapo(tela, x, y, fase, viewport, lingua, zoom=1.0):
    w, h = tela.get_size()  # proporções da tela, para clipping
    tam_tela = (0, 0, w, h)

    azul = (0,200,230)
    azul_esc = (30, 50, 100)
    borda = (0,20,80)
    vermelho = (255, 0, 0)

    z = zoom

    # ---------- CORPO ----------
    corpo = trapezio_pequeno(x, y-int(14*z), topo=int(26*z), base=int(40*z), h=int(20*z))

    for i in range(len(corpo)):
        x0, y0 = corpo[i]
        x1, y1 = corpo[(i+1) % len(corpo)]
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, borda)

    cores_corpo = [
        azul,
        azul,
        azul_esc,
        azul_esc
    ]
    scanlineGrad_poligono_recortado(tela, corpo, tam_tela, viewport, cores_corpo)

    # ---------- CABEÇA ----------
    cabeca = hexagono_largo(x, y - int(30*z), w=int(50*z), h=int(16*z))
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
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, borda)

    scanlineGrad_poligono_recortado(tela, cabeca, tam_tela, viewport, cores_cabeca)

    olho_y = y - int(47 * z)
    dx = int(12 * z)

    # cores
    branco = (255,255,255)

    piscar = (int(fase) % 8 == 0)

    for lado in (-1, 1):
        cx = x + lado * dx

        setCircle(tela, cx, olho_y, int(5*z), azul)
        setFloodFill(tela, cx, olho_y, azul, borda)


        if piscar:
            # olho fechado
            desenhar_linha_recortada(tela, cx - int(4*z), olho_y, cx + int(4*z), olho_y, tam_tela, viewport, borda)
        else:

            # branco do olho
            setCircle(tela, cx, olho_y, int(5*z), borda)
            setFloodFill(tela, cx, olho_y, branco, borda)

            # pupila
            setCircle(tela, cx, olho_y, int(2*z), (0,0,0))
            setFloodFill(tela, cx, olho_y, (0,0,0), borda)


    # ---------- PATAS ----------
    chao = y + int(7 * z)
    altura = int(12 * z)
    sep = int(14 * z)
    cores_patas = [
        azul_esc,
        azul_esc,
        azul
    ]

    # -------- pata esquerda --------
    pata_esq = [
        (x - ((14*z) + sep), chao),
        (x - ((2*z)  + sep), chao),
        (x - ((8*z)  + sep), chao - altura)
    ]

    for i in range(3):
        x0, y0 = pata_esq[i]
        x1, y1 = pata_esq[(i+1) % 3]
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, borda)

    scanlineGrad_poligono_recortado(tela, pata_esq, tam_tela, viewport, cores_patas)

    # -------- pata direita --------
    pata_dir = [
        (x + ((2*z)   + sep), chao),
        (x + ((14*z) + sep), chao),
        (x + ((8*z)  + sep), chao - altura)
    ]

    for i in range(3):
        x0, y0 = pata_dir[i]
        x1, y1 = pata_dir[(i+1) % 3]
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, borda)

    scanlineGrad_poligono_recortado(tela, pata_dir, tam_tela, viewport, cores_patas)

    # ---------- BOCA (LINHAS) ----------
    frente_y = y - 22
    dist = 10          

    desenhar_linha_recortada(tela, x - dist, frente_y, x - dist - 10, frente_y - 8, tam_tela, viewport, borda)
    desenhar_linha_recortada(tela, x + dist, frente_y, x + dist + 10, frente_y - 8, tam_tela, viewport, borda)
    desenhar_linha_recortada(tela, x - dist, frente_y, x + dist, frente_y, tam_tela, viewport, borda)

    # ---------- BRAÇO (LINHAS) ----------
    frente_y = y
    dist = 4

    # braço esquerdo
    x1, y1 = x - dist, frente_y
    x2, y2 = x - dist - 8, frente_y - 10
    desenhar_linha_recortada(tela, x1, y1+4, x2+1, y2, tam_tela, viewport, borda)

    desenhar_linha_recortada(tela, x2, y2+12, x2 + 4, y2 + 6, tam_tela, viewport, borda)

    # braço direito
    x3, y3 = x + dist, frente_y
    x4, y4 = x + dist + 8, frente_y - 10
    desenhar_linha_recortada(tela, x3, y3+4, x4-1, y4, tam_tela, viewport, borda)

    desenhar_linha_recortada(tela, x4, y4+12, x4 - 4, y4 + 6, tam_tela, viewport, borda)

    if lingua > 0:
        desenhar_linha_recortada(tela, x-1, frente_y, x, frente_y - 20, tam_tela, viewport, vermelho)
        desenhar_linha_recortada(tela, x, frente_y, x, frente_y - 20, tam_tela, viewport, vermelho)
        desenhar_linha_recortada(tela, x + 1, frente_y, x, frente_y - 20, tam_tela, viewport, vermelho)

#bioma mar
def setPeixe(tela, x, y, viewport, fase, zoom=1.0):
    w, h = tela.get_size()  # proporções da tela, para clipping
    tam_tela = (0, 0, w, h)

    azul = (80, 170, 220)
    azul_esc = (30, 90, 160)
    borda = (255, 40, 90)
    laranja = (255, 140, 100)
    laranja_esc = (250, 100, 80)
    branco = (255, 255, 255)

    z = max(0.01, float(zoom))

    piscar = (int(fase) % 25 == 0)

    ond = int(4 * z * math.sin(fase * 0.3))
    cauda_ang = math.sin(fase * 0.5) * 0.6

    # ---------- CORPO (ELIPSE) ----------
    rx = max(2, int(16 * z))
    ry = max(2, int(9 * z))

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

    dx = int(10 * z * math.cos(cauda_ang))
    dy = int(10 * z * math.sin(cauda_ang))

    cauda = [
        (base_x, base_y),
        (base_x - int(12 * z) + dy, base_y - int(8 * z) - dx),
        (base_x - int(12 * z) - dy, base_y + int(8 * z) + dx),
    ]

    for i in range(3):
        x0, y0 = cauda[i]
        x1, y1 = cauda[(i+1) % 3]
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, borda)

    scanlineGrad_poligono_recortado(tela, cauda, tam_tela, viewport, [azul_esc, azul, azul])

    # ---------- OLHO ----------
    olho_x = x + int(6 * z) + ond
    olho_y = y - int(2 * z)

    if piscar:
        desenhar_linha_recortada(tela, olho_x - int(3 * z), olho_y, olho_x + int(3 * z), olho_y, tam_tela, viewport, borda)
    else:
        setCircle(tela, olho_x, olho_y, max(1, int(3 * z)), (0, 0, 0))
        setFloodFill(tela, olho_x, olho_y, branco, (0, 0, 0))
        setCircle(tela, olho_x, olho_y, max(1, int(1 * z)), (0, 0, 0))
        setFloodFill(tela, olho_x, olho_y, (0, 0, 0), (0, 0, 0))


    #setCircle(tela, olho_x, olho_y, 3, (0,0,0))
    #setFloodFill(tela, olho_x, olho_y, branco, (0,0,0))

    #setCircle(tela, olho_x, olho_y, 1, (0,0,0))
    #setFloodFill(tela, olho_x, olho_y, (0,0,0), (0,0,0))


def setTubarao(tela, x, y, fase, viewport, comendo=False, zoom=1.0):
    w, h = tela.get_size()  # proporções da tela, para clipping
    tam_tela = (0, 0, w, h)

    cinza = (140, 140, 150)
    cinza_esc = (90, 90, 100)
    branco = (220, 220, 220)

    borda = (30, 30, 40)

    z = max(0.01, float(zoom))

    piscar = (int(fase) % 25 == 0)

    # ---------- CORPO (ELIPSE) ----------
    rx = max(2, int(38 * z))
    ry = max(2, int(14 * z))

    # borda da elipse
    setEllipse(tela, x, y, rx, ry, borda)

    # preenchimento (flood fill)
    setFloodFill(tela, x, y, cinza, borda)

    # sombra barriga
    setEllipse(tela, x, y + int(4 * z), max(2, rx - int(6 * z)), max(2, ry - int(6 * z)), branco)
    setFloodFill(tela, x, y + int(4 * z), branco, borda)

    # ---------- BARBATANA SUPERIOR ----------
    barbatana = [
        (x - int(5 * z), y - ry - int(10 * z)),
        (x + int(6 * z), y - ry + int(2 * z)),
        (x - int(18 * z), y - ry + int(2 * z)),
    ]

    for i in range(3):
        x0, y0 = barbatana[i]
        x1, y1 = barbatana[(i + 1) % 3]
        setBresenham(tela, x0, y0, x1, y1, borda)
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, borda)

    scanlineGrad_poligono_recortado(tela, barbatana, tam_tela, viewport, [cinza_esc]*3)

    # ---------- CAUDA (BALANÇANDO) ----------
    swing = int(8 * z * math.sin(fase))

    cauda = [
        (x - rx + int(2 * z), y),
        (x - rx - int(20 * z) + swing, y - int(14 * z)),
        (x - rx - int(20 * z) + swing, y + int(14 * z)),
    ]

    for i in range(3):
        x0, y0 = cauda[i]
        x1, y1 = cauda[(i + 1) % 3]
        setBresenham(tela, x0, y0, x1, y1, borda)
        desenhar_linha_recortada(tela, x0, y0, x1, y1, tam_tela, viewport, borda)

    scanlineGrad_poligono_recortado(tela, cauda, tam_tela, viewport, [cinza_esc]*3)

    # ---------- OLHO (COM PISCAR) ----------
    olho_x = x + int(14 * z)
    olho_y = y - int(4 * z)

    if piscar:
        # olho fechado (linha)
        setBresenham(tela, olho_x - int(3 * z), olho_y, olho_x + int(3 * z), olho_y, borda)
    else:
        # olho aberto
        setCircle(tela, olho_x, olho_y, max(1, int(3 * z)), borda)
        setFloodFill(tela, olho_x, olho_y, (255, 255, 255), borda)

        setCircle(tela, olho_x, olho_y, max(1, int(1 * z)), (0, 0, 0))
        setFloodFill(tela, olho_x, olho_y, (0, 0, 0), borda)

    # ---------- BOCA (ABRE QUANDO COME) ----------
    boca_x1 = x + int(16 * z)
    boca_x2 = x + int(32 * z)
    boca_y = y + int(6 * z)

    if comendo:
        abertura = int(6 * z)
        # boca aberta (V)
        desenhar_linha_recortada(tela, boca_x1, boca_y, boca_x2, boca_y - abertura, tam_tela, viewport, borda)
        desenhar_linha_recortada(tela, boca_x1, boca_y, boca_x2, boca_y + abertura, tam_tela, viewport, borda)
    else:
        # boca fechada
        desenhar_linha_recortada(tela, boca_x1, boca_y, boca_x2, boca_y, tam_tela, viewport, borda)


def setAlga(tela, x, y, viewport, fase, zoom=1.0):
    w, h = tela.get_size()  # proporções da tela, para clipping
    tam_tela = (0, 0, w, h)

    verde1 = (20, 120, 60)
    verde2 = (40, 170, 90)
    verde3 = (10, 90, 50)

    z = max(0.01, float(zoom))

    ramos = [
        {"dx": int(-8 * z), "altura": int(22 * z), "amp": 2.0 * z, "invert": False},  # esquerda
        {"dx": int(0 * z), "altura": int(32 * z), "amp": 3.5 * z, "invert": True},  # meio (S invertido)
        {"dx": int(8 * z), "altura": int(22 * z), "amp": 2.0 * z, "invert": False},  # direita
    ]

    for i, r in enumerate(ramos):
        bx = x + r["dx"]
        by = y

        px, py = bx, by

        for t in range(1, max(2, r["altura"])):
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
                desenhar_linha_recortada(tela, px + e, py, nx + e, ny, tam_tela, viewport, cor)

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

#textura titulo
def scanline_texture(superficie, pontos, uvs, textura):
    tex_w = textura.get_width()
    tex_h = textura.get_height()
    n = len(pontos)

    ys = [p[1] for p in pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    for y in range(y_min, y_max):
        inter = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            u0, v0 = uvs[i]
            u1, v1 = uvs[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                u0, v0, u1, v1 = u1, v1, u0, v0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)

            x = x0 + t * (x1 - x0)
            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)

            inter.append((x, u, v))

        inter.sort(key=lambda i: i[0])

        for i in range(0, len(inter), 2):
            if i + 1 >= len(inter):
                continue

            x_start, u_start, v_start = inter[i]
            x_end,   u_end,   v_end   = inter[i + 1]

            if x_start == x_end:
                continue

            for x in range(int(x_start), int(x_end) + 1):
                t = (x - x_start) / (x_end - x_start)

                u = u_start + t * (u_end - u_start)
                v = v_start + t * (v_end - v_start)

                tx = int(u * (tex_w - 1))
                ty = int(v * (tex_h - 1))

                cor = textura.get_at((tx, ty))

                if cor.a > 0:   # só desenha se NÃO for transparente
                    setPixel(superficie, x, y, cor)
