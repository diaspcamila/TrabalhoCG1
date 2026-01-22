import pygame
import sys
import Main
from Graficos import *
from Fonte import *

pygame.init()
largura, altura = 900, 650
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("EcoSim - Menu")

FUNDO = (80, 120, 200)
BORDA = (255, 255, 255)
BOTAO = (21, 0, 76)
BOTAO_HOVER = (41, 14, 113)

# ---------------- ESTADOS ----------------
bioma = 0              # 0 floresta | 1 mar
qtd_bichos = 5

# ---------------- BOTÕES ----------------
btn_start = (275, 220, 350, 70)
btn_bioma  = (275, 320, 350, 70)
btn_qtd    = (275, 420, 350, 70)
btn_sair   = (275, 520, 350, 70)

# ---------------- FUNÇÕES ----------------
def dentro(mx, my, botao):
    x, y, w, h = botao
    return x <= mx <= x+w and y <= my <= y+h

def desenhar_botao(botao, cor):
    x, y, w, h = botao
    setBordaRetangulo(tela, x, y, w, h, BORDA)
    setFloodFill(tela, x+3, y+3, cor, BORDA)

def desenhar_tela():
    # fundo
    setPixel(tela, 0, 0, (0, 0, 0))
    setFloodFill(tela, 0, 0, FUNDO, BORDA)

    # botões
    desenhar_botao(btn_start, BOTAO)
    desenhar_botao(btn_bioma, BOTAO)
    desenhar_botao(btn_qtd, BOTAO)
    desenhar_botao(btn_sair, BOTAO)

    # textos fixos
    draw_text(tela, 247, 80, "ECO SIM", (21,0,76), escala=9, setPixel=setPixel)
    draw_text(tela, 390, 248, "INICIO", (255,255,255), escala=3, setPixel=setPixel)
    draw_text(tela, 300, 348, "BIOMA", (255,255,255), escala=3, setPixel=setPixel)
    draw_text(tela, 300, 448, "ANIMAIS", (255,255,255), escala=3, setPixel=setPixel)
    draw_text(tela, 410, 548, "SAIR", (255,255,255), escala=3, setPixel=setPixel)

    # textos variáveis
    if bioma == 0:
        draw_text(tela, 490, 348, "FLORESTA", (200, 200, 200), 2, setPixel=setPixel)
    else:
        draw_text(tela, 490, 348, "MAR", (200, 200, 200), 2, setPixel=setPixel)

    draw_text(tela, 560, 448, str(qtd_bichos), (200, 200, 200), 3, setPixel=setPixel)
    pygame.display.flip()

# ---------------- DESENHO INICIAL ----------------
desenhar_tela()

# ---------------- LOOP ----------------
clock = pygame.time.Clock()
rodando = True

while rodando:
    mx, my = pygame.mouse.get_pos()

    if (dentro(mx, my, btn_start) or
        dentro(mx, my, btn_bioma) or
        dentro(mx, my, btn_qtd) or 
        dentro(mx, my, btn_sair)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # ---------- DESENHA TELA COM HOVER ----------
    setPixel(tela, 0, 0, (0, 0, 0))
    setFloodFill(tela, 0, 0, FUNDO, BORDA)

    if dentro(mx, my, btn_start):
        desenhar_botao(btn_start, BOTAO_HOVER)
    else:
        desenhar_botao(btn_start, BOTAO)

    if dentro(mx, my, btn_bioma):
        desenhar_botao(btn_bioma, BOTAO_HOVER)
    else:
        desenhar_botao(btn_bioma, BOTAO)

    if dentro(mx, my, btn_qtd):
        desenhar_botao(btn_qtd, BOTAO_HOVER)
    else:
        desenhar_botao(btn_qtd, BOTAO)

    if dentro(mx, my, btn_sair):
        desenhar_botao(btn_sair, BOTAO_HOVER)
    else:
        desenhar_botao(btn_sair, BOTAO)

    # textos
    draw_text(tela, 247, 80, "ECO SIM", (0,0,0), escala=9, setPixel=setPixel)
    draw_text(tela, 390, 248, "INICIO", (255,255,255), escala=3, setPixel=setPixel)
    draw_text(tela, 300, 348, "BIOMA", (255,255,255), escala=3, setPixel=setPixel)
    draw_text(tela, 300, 448, "ANIMAIS", (255,255,255), escala=3, setPixel=setPixel)
    draw_text(tela, 410, 548, "SAIR", (255,255,255), escala=3, setPixel=setPixel)

    if bioma == 0:
        draw_text(tela, 490, 348, "FLORESTA", (200,200,200), 2, setPixel=setPixel)
    else:
        draw_text(tela, 490, 348, "MAR", (200,200,200), 2, setPixel=setPixel)

    draw_text(tela, 560, 448, str(qtd_bichos), (200,200,200), 3, setPixel=setPixel)

    pygame.display.flip()


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos

            if dentro(mx, my, btn_start):
                pygame.quit()
                Main.main()  # depois adapta a main

            elif dentro(mx, my, btn_bioma):
                bioma = 1 - bioma
                desenhar_tela()

            elif dentro(mx, my, btn_qtd):
                if qtd_bichos == 5:
                    qtd_bichos = 10
                elif qtd_bichos == 10:
                    qtd_bichos = 20
                else:
                    qtd_bichos = 5
                desenhar_tela()

            elif dentro(mx, my, btn_sair):
                pygame.quit()
                sys.exit()

    clock.tick(60)
