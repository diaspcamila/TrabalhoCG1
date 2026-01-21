import random
from SerVivo import SerVivo

class Animal(SerVivo):
    passo = SerVivo.escala
    largura, altura, custo_energetico = SerVivo.largura, SerVivo.altura, SerVivo.custo_energetico

    def mover(self, plantas, animais):  # TODO fazer a borda impassável
        movimentos = ['N', 'S', 'E', 'W']  # direcões possíveis de andar

        seres = plantas + animais
        vizinhos = []
        for ser in seres:  # faz uma lista de vizinhos
            if self != ser:
                if (abs(self.x - ser.x) <= self.passo) and (abs(self.y - ser.y) <= self.passo):
                    vizinhos.append(ser)

        direcao = random.choice(movimentos)
        tentativas = 0
        while True:  # tenta a direção aleatória, se não der certo
            tentativas += 1
            if tentativas > 4:
                if self in plantas:
                    plantas.remove(self)
                if self in animais:
                    animais.remove(self)
                break

            match direcao:  # escolhe uma direção aleatória, se não funcionar, tenta outra 3 vezes
                case 'N':
                    for vizinho in vizinhos:
                        if self.y - vizinho.y >= 0 or self.y < self.passo * 2:  # se a direção é impossível, tente de novo
                            direcao = 'S'
                            continue
                    self.y += self.passo
                case 'S':
                    for vizinho in vizinhos:
                        if self.y - vizinho.y <= 0 or self.y > self.altura - self.passo * 2:
                            direcao = 'E'
                            continue
                    self.y += -self.passo
                case 'E':
                    for vizinho in vizinhos:
                        if self.x - vizinho.x <= 0 or self.x > self.largura - self.passo * 2:
                            direcao = 'W'
                            continue
                    self.x += -self.passo
                case 'W':
                    for vizinho in vizinhos:
                        if self.x - vizinho.x >= 0 or self.x < self.passo * 2:
                            direcao = 'N'
                            continue
                    self.x += self.passo
            break

    def predar(self, plantas, animais):
        return