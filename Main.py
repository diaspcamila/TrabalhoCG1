import sys
import random
import pygame
from Mundo import Mundo
from Planta import Planta
from Presa import Presa
from Predador import Predador

def main():
    pygame.init()

    # Configurações do mundo
    largura, altura, escala = 1000, 800, 20
    mundo = Mundo(largura=largura, altura=altura, escala=escala)
    mundo.configurar_tela("EcoSim")

    # População inicial
    max_cx = (largura // escala) - 1
    max_cy = (altura // escala) - 1

    for _ in range(25):
        x = random.randint(1, max_cx) * escala
        y = random.randint(1, max_cy) * escala
        mundo.adicionar_planta(Planta(x, y))

    for _ in range(12):
        x = random.randint(1, max_cx) * escala
        y = random.randint(1, max_cy) * escala
        mundo.adicionar_animal(Presa(x, y))

    for _ in range(5):
        x = random.randint(1, max_cx) * escala
        y = random.randint(1, max_cy) * escala
        mundo.adicionar_animal(Predador(x, y))

    # Loop
    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False



        mundo.tick()
        mundo.desenhar()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()