import sys
from Mundo import Mundo
from Planta import Planta
from Presa import Presa
from Predador import Predador
from Graficos import *

def main(qtd_entidades, bioma):
    pygame.init()

    # Configurações do mundo
    largura, altura, escala = 1000, 800, 20
    mundo = Mundo(largura=largura, altura=altura, escala=escala, bioma=bioma)
    mundo.configurar_tela("EcoSim")

    # População inicial | x,2x,4x
    max_cx = (largura // escala) - 1
    max_cy = (altura // escala) - 1

    textura_fundo = pygame.Surface((largura, altura))
    print("surface criada")

    if bioma == 0:
        textura_floresta(textura_fundo)
    else:
        textura_mar(textura_fundo)

    print("textura gerada")

    mundo.textura_fundo = textura_fundo
    print("textura atribuída ao mundo")

    for _ in range((qtd_entidades//7)*4):
        x = random.randint(1, max_cx) * escala
        y = random.randint(1, max_cy) * escala
        mundo.adicionar_planta(Planta(x, y))

    for _ in range((qtd_entidades//7)*2):
        x = random.randint(1, max_cx) * escala
        y = random.randint(1, max_cy) * escala
        mundo.adicionar_animal(Presa(x, y))

    for _ in range(qtd_entidades//7):
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
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mundo.click_zoom(evento.pos)

        mundo.tick()
        mundo.desenhar()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()