import pygame
import traceback
from Energia import EnergiaStatus
from Graficos import setPixel
from SerVivo import SerVivo
from Planta import Planta
from Animal import Animal
from Transformacoes import janela_viewport, aplica_transformacao

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

    # Render
    def configurar_tela(self, titulo="EcoSim"):
        pygame.init()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(titulo)

    def desenhar(self):
        if self.tela is None:
            return
        self.tela.fill((255, 255, 255))
        for p in self.plantas:
            p.desenhar(self.tela)
        for a in self.animais:
            a.desenhar(self.tela)

        # viewport
        try:
            L, A = self.tela.get_size()
            margem = 10
            vm_w, vm_h = int(0.30 * L), int(0.25 * A)
            Vxmin, Vymin = margem, margem
            Vxmax, Vymax = Vxmin + vm_w, Vymin + vm_h
            viewport = (Vxmin, Vymin, Vxmax, Vymax)


            janela = (0, 0, self.largura, self.altura)
            M = janela_viewport(janela, viewport)

            # Fundo da viewport para impedir que a cena principal apareça por baixo
            rect = pygame.Rect(Vxmin, Vymin, vm_w, vm_h)
            pygame.draw.rect(self.tela, (245, 245, 245), rect)

            # Limita o desenho dos marcadores à área da viewport
            old_clip = self.tela.get_clip()
            try:
                self.tela.set_clip(rect)

                # Plantas (verde)
                for p in self.plantas:
                    (px, py), = aplica_transformacao(M, [(p.x, p.y)])
                    for dx in (0, 1):
                        for dy in (0, 1):
                            setPixel(self.tela, px + dx, py + dy, (0, 160, 0))

                # Animais (preto)
                for a in self.animais:
                    (px, py), = aplica_transformacao(M, [(a.x, a.y)])
                    for dx in (0, 1):
                        for dy in (0, 1):
                            setPixel(self.tela, px + dx, py + dy, (0, 0, 0))
            finally:
                # Restaura o clip e desenha a borda por cima
                self.tela.set_clip(old_clip)
                pygame.draw.rect(self.tela, (0, 0, 0), rect, 1)
        except Exception as e:
            print(f"[Mundo.desenhar] Erro ao renderizar viewport: {e}")
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