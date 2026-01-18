import pygame
import sys
import time
from seres import *
from graficos import *

pygame.init()
largura, altura = 800, 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("EcoSim")

#listas de animais e plantas
animais = []
plantas = []

#inicializando alguns animais para teste
for i in range(5):
    animal = Animal(largura//2, altura//2)
    animais.append(animal)

#loop de simulação
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((255, 255, 255))
    time.sleep(0.1)

    #simula as ações de cada planta
    for planta in plantas:
        print("ainda não tem plantas")
    #simular as acões de cada animal
    for animal in animais:
        setMosquito(tela, animal.x, animal.y, (0, 0, 0))
        animal.mover()

    pygame.display.flip()

pygame.quit()
sys.exit()
