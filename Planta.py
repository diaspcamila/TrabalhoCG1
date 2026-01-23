from SerVivo import *
from Graficos import setPlanta

class Planta(SerVivo):
    alcance_vizinhos = SerVivo.escala * 2
    custo_energetico = 3

    def fotossintese(self, plantas):
        vizinhos = 0
        for planta in plantas:
            if planta is self:
                continue
            if ((abs(self.x - planta.x) <=self.alcance_vizinhos)
                    and (abs(self.y - planta.y) <=self.alcance_vizinhos)):
                vizinhos += 1
        if vizinhos < 4:
            self.energia += 20

    def desenhar(self, tela):
        setPlanta(tela, self.x, self.y)
