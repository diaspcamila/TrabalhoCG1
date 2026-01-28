from SerVivo import *
from Graficos import setPlanta, setAlga


class Planta(SerVivo):
    alcance_vizinhos = SerVivo.escala * 2
    custo_energetico = 3

    def fotossintese(self, plantas, animais):
        vizinhos = 0
        for planta in plantas:
            if planta is self:
                continue
            if ((abs(self.x - planta.x) <=self.alcance_vizinhos)
                    and (abs(self.y - planta.y) <=self.alcance_vizinhos)):
                vizinhos += 1

        #se uma planta tem muitos vizinhos, ela não pega sol direito
        if vizinhos < 4:
            #se tem poucos animais no mundo, as plantas são pouco fertilizadas/polinizadas
            if len(animais) > 5:
                self.energia += 20
            else:
                self.energia += 5

    def desenhar(self, tela, bioma, viewport):
        if bioma == 0:
            setPlanta(tela, self.x, self.y, viewport)
        else:
            setAlga(tela, self.x, self.y, viewport, self.fase)
