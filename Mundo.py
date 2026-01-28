import pygame
import traceback
from Energia import EnergiaStatus
from Fonte import draw_text
from Graficos import setPixel, setScanlineFill, setBordaRetangulo, setPixelGrosso
from SerVivo import SerVivo
from Planta import Planta
from Animal import Animal
from Predador import Predador
from Transformacoes import aplica_transformacao, dentro
from Clipping import janela_viewport

class Mundo:
    def __init__(self, bioma, largura=1000, altura=800, escala=20):
        self.largura = largura
        self.altura = altura
        self.escala = escala
        self.bioma = bioma

        SerVivo.largura, SerVivo.altura = largura, altura
        SerVivo.escala = escala

        self.plantas: list[Planta] = []
        self.animais: list[Animal] = []
        self.tela: pygame.Surface | None = None
        self.textura_fundo = None

        #botoes zoom
        self.zoom, self.zoom_min, self.zoom_max, self.zoom_passo = 1.0, 1.0, 3.0, 1.25

        self.btn_tam, self.btn_margem = 26, 6

    # Render
    def configurar_tela(self, titulo="EcoSim"):
        pygame.init()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(titulo)

    def desenhar_viewport(self):
        if self.tela is None:
            return (0, 0, 0, 0)
        largura_tela, altura_tela = self.tela.get_size()
        margem = 10
        largura_vp = int(largura_tela * 0.3)
        altura_vp = int(altura_tela * 0.25)

        vxmin, vymin = margem, margem
        vxmax, vymax = largura_vp + vxmin, altura_vp + vymin
        return vxmin, vymin, vxmax, vymax

    def desenhar_zoom(self, viewport):
        if self.tela is None:
            return None, None

        vxmin, vymin, vxmax, vymax = viewport
        t, mg = self.btn_tam, self.btn_margem

        bx = vxmax - t - mg
        by_mais = vymin + mg
        by_menos = by_mais + t + mg

        btn_mais = (bx, by_mais, t, t)
        btn_menos = (bx, by_menos, t, t)

        BORDA, FUNDO, TEXTO = (255, 255, 255), (0, 0, 0), (255, 255, 255)
        x, y, w, h = btn_mais
        setBordaRetangulo(self.tela, x, y, w, h, BORDA)
        setScanlineFill(self.tela, [(x, y), (x+w, y), (x+w, y+h), (x, y+h)], FUNDO)
        draw_text(self.tela, x+8, y+6, "+", TEXTO, escala=3, setPixel=setPixel)

        x,y,w,h = btn_menos
        setBordaRetangulo(self.tela, x, y, w, h, BORDA)
        setScanlineFill(self.tela, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], FUNDO)
        draw_text(self.tela, x + 8, y + 6, "-", TEXTO, escala=3, setPixel=setPixel)

        return btn_mais, btn_menos

    def click_zoom(self, pos):
        if self.tela is None:
            return

        mx, my = pos
        viewport = self.desenhar_viewport()
        btn_plus, btn_minus = self.desenhar_zoom(viewport)

        if btn_plus and dentro(mx, my, btn_plus):
            self.zoom *= self.zoom_passo
            if self.zoom > self.zoom_max:
                self.zoom = self.zoom_max
        elif btn_minus and dentro(mx, my, btn_minus):
            self.zoom /= self.zoom_passo
            if self.zoom < self.zoom_min:
                self.zoom = self.zoom_min


    def desenhar(self):
        if self.tela is None:
            return

        #janela do mundo zoom
        w = int(self.largura / self.zoom)
        h = int(self.altura / self.zoom)
        x0 = (self.largura - w) // 2
        y0 = (self.altura - h) // 2
        janela_zoom = (x0, y0, x0 + w, y0 + h)
        janela_inteira = (0, 0, self.largura, self.altura)

        mundo = janela_viewport(janela_zoom, janela_inteira)

        viewport = self.desenhar_viewport()
        minimap = janela_viewport(janela_inteira, viewport)

        if self.textura_fundo:
            self.tela.blit(self.textura_fundo, (0, 0))
        else:
            self.tela.fill((255, 255, 255))

        # viewport a borda retangular
        largura_tela, altura_tela = self.tela.get_size()
        margem = 10
        largura_vp = int(largura_tela*0.3)
        altura_vp = int(altura_tela*0.25)

        #entidades no mundo
        try:
            for p in self.plantas:
                (sx, sy) = aplica_transformacao(mundo, [(p.x, p.y)])[0]
                ox, oy = p.x, p.y
                p.x, p.y = sx, sy
                p.desenhar(self.tela, self.bioma, viewport)
                p.x, p.y = ox, oy
            for a in self.animais:
                (sx, sy) = aplica_transformacao(mundo, [(a.x, a.y)])[0]
                ox, oy = a.x, a.y
                a.x, a.y = sx, sy
                a.desenhar(self.tela, self.bioma, viewport)
                a.x, a.y = ox, oy

        except Exception:
            traceback.print_exc()

        # desenhando viewport
        vxmin, vymin, vxmax, vymax = viewport
        w = vxmax - vxmin
        h = vymax - vymin
        coords = [(vxmin, vymin), (vxmax, vymin), (vxmax, vymax), (vxmin, vymax)]
        if self.bioma == 0:
            setScanlineFill(self.tela, coords, (155, 255, 155))
            setBordaRetangulo(self.tela, vxmin, vymin, w, h, (0, 140, 0))
        else:
            setScanlineFill(self.tela, coords, (100, 200, 255))
            setBordaRetangulo(self.tela, vxmin, vymin, w, h, (50, 60, 85))

        self.desenhar_zoom(viewport)
        #entidades no viewport
        try:
            for p in self.plantas:
                x, y = aplica_transformacao(minimap, [(p.x, p.y)])[0]
                setPixelGrosso(self.tela, int(x), int(y), (0, 180, 0))
            for a in self.animais:
                if isinstance(a, Predador) and self.bioma == 0:
                    cor = (0, 170, 200)
                elif isinstance(a, Predador) and self.bioma == 1:
                    cor = (120, 120, 130)
                elif not isinstance(a, Predador) and self.bioma == 0:
                    cor = (50, 50, 50)
                else:
                    cor = (250, 100, 80)

                x, y = aplica_transformacao(minimap, [(a.x, a.y)])[0]
                if vxmin <= int(x) <= vxmax and vymin <= int(y) <= vymax:
                    setPixelGrosso(self.tela, int(x), int(y), cor)

        except Exception:
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
            p.atualizar()
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