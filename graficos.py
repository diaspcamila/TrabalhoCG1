import pygame

def setPixel(superficie, x, y, cor):
    superficie.set_at((x, y), cor)

def setMosquito(superficie, x, y, cor): #cria um quadrado simples
    for i in range (x-2, x+3):
        for j in range(y-2, y+3):
            setPixel(superficie, i, j, cor)
