import random
import pygame
from Energia import EnergiaStatus
from Graficos import setMosquito
from SerVivo import SerVivo
from Planta import Planta
from Animal import Animal

class Mundo:
    #seed bom p debug
    def __init__(self, largura=1000, altura=800, escala=20, seed=None):
        self.largura = largura
        self.altura = altura
        self.escala = escala
        if seed is not None:
            random.seed(seed)
        # Sincroniza parâmetros de mundo com SerVivo para manter compatibilidade
        SerVivo.largura, SerVivo.altura = largura, altura
        SerVivo.escala = escala

        self.plantas: list[Planta] = []
        self.animais: list[Animal] = []
        self.tela: pygame.Surface | None = None

    # --- Setup/Render ---
    def configurar_tela(self, titulo="EcoSim"):
        pygame.init()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(titulo)

    def desenhar(self):
        if self.tela is None:
            return
        self.tela.fill((255, 255, 255))
        # plantas em verde
        for p in self.plantas:
            setMosquito(self.tela, p.x, p.y, (0, 230, 0))
        # animais em preto
        for a in self.animais:
            setMosquito(self.tela, a.x, a.y, (0, 0, 0))
        pygame.display.flip()

    def adicionar_planta(self, planta: Planta):
        self.plantas.append(planta)

    def adicionar_animal(self, animal: Animal):
        self.animais.append(animal)

    def entidades(self):
        return self.plantas + self.animais

    def esta_livre(self, x: int, y: int) -> bool:
        for e in self.entidades():
            if e.x == x and e.y == y:
                return False
        return True

    def _clamp(self, v: int, vmin: int, vmax: int) -> int:
        return max(vmin, min(vmax, v))

    def colocar_perto(self, x: int, y: int, max_dist_celulas: int = 2) -> tuple[int, int]:
        for d in range(1, max_dist_celulas + 1):
            for dx in range(-d, d + 1):
                for dy in range(-d, d + 1):
                    nx = self._clamp(x + dx * self.escala, self.escala, self.largura - self.escala)
                    ny = self._clamp(y + dy * self.escala, self.escala, self.altura - self.escala)
                    if self.esta_livre(nx, ny):
                        return nx, ny
        return x, y

    def _spawn_filho(self, pai):
        filho = type(pai)(pai.x, pai.y)
        # Se for um animal afaste um pouco para não sobrepor
        if hasattr(filho, 'mover'):
            for _ in range(15):
                filho.mover(self.plantas, self.animais)
        else:
            # para plantas posiciona em célula vizinha livre
            filho.x, filho.y = self.colocar_perto(pai.x, pai.y)
        return filho

    def tick(self):
        novas_plantas: list[Planta] = []
        plantas_mortas: list[Planta] = []
        for p in list(self.plantas):
            res = p.gastarEnergia()
            if res.status is EnergiaStatus.REPRODUZINDO:
                novas_plantas.append(self._spawn_filho(p))
            elif res.status is EnergiaStatus.MORTO:
                plantas_mortas.append(p)
            # fotossíntese depois do gasto energético
            p.fotossintese(self.plantas)
        for p in plantas_mortas:
            if p in self.plantas:
                self.plantas.remove(p)
        self.plantas.extend(novas_plantas)


        novos_animais: list[Animal] = []
        animais_mortos: list[Animal] = []
        for a in list(self.animais):
            res = a.gastarEnergia()
            if res.status is EnergiaStatus.REPRODUZINDO:
                novos_animais.append(self._spawn_filho(a))
            elif res.status is EnergiaStatus.MORTO:
                animais_mortos.append(a)

            a.mover(self.plantas, self.animais)
            a.predar(self.plantas, self.animais)

        for a in animais_mortos:
            if a in self.animais:
                self.animais.remove(a)
        self.animais.extend(novos_animais)