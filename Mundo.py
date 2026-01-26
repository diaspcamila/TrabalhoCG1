import pygame
import traceback
from Energia import EnergiaStatus
from Graficos import setPixel, setScanlineFill, setBordaRetangulo
from SerVivo import SerVivo
from Planta import Planta
from Animal import Animal
from Predador import Predador
from Transformacoes import aplica_transformacao
from Clipping import desenhar_poligono, desenhar_poligono_recortado, janela_viewport, desenhar_linha_recortada


class Mundo:
    def __init__(self, largura=1000, altura=800, escala=20):
        self.largura = largura
        self.altura = altura
        self.escala = escala

        SerVivo.largura, SerVivo.altura = largura, altura
        SerVivo.escala = escala

        self.plantas: list[Planta] = []
        self.animais: list[Animal] = []
        self.tela: pygame.Surface | None = None
        self.textura_fundo = None

    # Render
    def configurar_tela(self, titulo="EcoSim"):
        pygame.init()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(titulo)

    def desenhar(self):
        if self.tela is None:
            return
        if self.textura_fundo:
            self.tela.blit(self.textura_fundo, (0, 0))
        else:
            self.tela.fill((255, 255, 255))

        for p in self.plantas:
            p.desenhar(self.tela)
        for a in self.animais:
            a.desenhar(self.tela)

        # viewport a borda retangular
        largura_tela, altura_tela = self.tela.get_size()
        margem = 10
        largura_vp = int(largura_tela*0.3)
        altura_vp = int(altura_tela*0.25)

        vxmin, vymin = margem, margem
        vxmax, vymax = largura_vp + vxmin, altura_vp + vymin
        viewport = (vxmin, vymin, vxmax, vymax)

        # janela do mundo
        janela = (0, 0, self.largura, self.altura)

        # matriz que escala as coordenadas
        m = janela_viewport(janela, viewport)
        coords = [(vxmin, vymin), (vxmax, vymin), (vxmax, vymax), (vxmin,vymax)]
        #desenhando viewport
        w = vxmax - vxmin
        h = vymax - vymin
        setScanlineFill(self.tela, coords, (0, 0, 0))
        setBordaRetangulo(self.tela, vxmin, vymin, w, h, (255, 255, 255))

        try:
            for p in self.plantas:
                cor = (0, 255, 0)
                x, y = aplica_transformacao(m, [(p.x, p.y)])[0]
                if vxmin <= int(x) <= vxmax and vymin <= int(y) <= vymax:
                    setPixel(self.tela, int(x), int(y), cor)

            for a in self.animais:
                if isinstance(a, Predador):
                    cor = (0, 150, 250)
                else:
                    cor = (205, 150, 150)
                x, y = aplica_transformacao(m, [(a.x, a.y)])[0]
                if vxmin <= int(x) <= vxmax and vymin <= int(y) <= vymax:
                    setPixel(self.tela, int(x), int(y), cor)

        except Exception as e:
            traceback.print_exc()

        pygame.display.flip()

    def adicionar_planta(self, planta: Planta):
        self.plantas.append(planta)

    def adicionar_animal(self, animal: Animal):
        self.animais.append(animal)

    def spawn_filho(self, pai):
        filho = type(pai)(pai.x, pai.y)
        if hasattr(filho, 'fotossintese'):
            for i in range(2):
                filho.mover(self.plantas, self.animais)
        else:
            filho.mover(self.plantas, self.animais)
        return filho

    def tick(self):
        novas_plantas: list[Planta] = []
        plantas_mortas: list[Planta] = []
        for p in list(self.plantas):
            res = p.gastarEnergia()
            if res.status is EnergiaStatus.REPRODUZINDO:
                novas_plantas.append(self.spawn_filho(p))
            elif res.status is EnergiaStatus.MORTO:
                plantas_mortas.append(p)
            # fotossíntese depois do gasto energético
            p.fotossintese(self.plantas, self.animais)
        for p in plantas_mortas:
            if p in self.plantas:
                self.plantas.remove(p)
        self.plantas.extend(novas_plantas)


        novos_animais: list[Animal] = []
        animais_mortos: list[Animal] = []
        for a in list(self.animais):
            res = a.gastarEnergia()
            if res.status is EnergiaStatus.REPRODUZINDO:
                novos_animais.append(self.spawn_filho(a))
            elif res.status is EnergiaStatus.MORTO:
                animais_mortos.append(a)

            a.atualizar()
            a.mover(self.plantas, self.animais)
            a.predar(self.plantas, self.animais)

        for a in animais_mortos:
            if a in self.animais:
                self.animais.remove(a)
        self.animais.extend(novos_animais)