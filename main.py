import pygame
import sys
import time
import random
from seres import *
from graficos import *

pygame.init()
largura, altura = 1000, 1000
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("EcoSim")

#listas de animais e plantas
animais = []
plantas = []

#inicializando alguns animais e plantas para teste
for i in range(10):
    planta = Planta(random.randint(1, 39)*20, random.randint(1, 39)*20)
    plantas.append(planta)
for i in range(5):
    animal = Mosquito(random.randint(1, 39)*20, random.randint(1, 39)*20)
    animais.append(animal)

#loop de simulação
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((255, 255, 255))
    time.sleep(0.1) #tempo entre "turnos"

    #simula as ações de cada planta
    for planta in plantas:
        setMosquito(tela, planta.x, planta.y, (0, 230, 0)) #chamar função para representar graficamente

        filho = planta.gastarEnergia(plantas, animais) #gasta energia disponível para se manter vivo ou reproduzir
        if filho == -1:
            plantas.remove(planta)
        elif filho != 0:
            plantas.append(filho)

        planta.fotossintese(plantas) #faz fotossintese

    #simular as acões de cada animal
    for animal in animais:
        setMosquito(tela, animal.x, animal.y, (0, 0, 0)) #chamar função para representar graficamente

        filho = animal.gastarEnergia(plantas, animais) #gasta energia disponível para se manter vivo ou reproduzir
        if filho == -1:
            animais.remove(animal)
        elif filho != 0:
            animais.append(filho)

        animal.mover(plantas, animais)
        animal.predar(plantas, animais)

    pygame.display.flip()

pygame.quit()
sys.exit()


