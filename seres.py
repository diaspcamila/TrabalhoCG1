import random
import copy

class SerVivo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energia = 100 #energia padrão

    def mover(self):
        movimentos = ['N', 'S', 'L', 'W'] #direões possíveis de andar
        passo = 10 #tamanho do passo

        direcao = random.choice(movimentos)
        match direcao:
            case 'N':
                self.x += 0
                self.y += -passo
                if self.y < 0:
                    self.y += passo
            case 'S':
                self.x += 0
                self.y += passo
                if self.y > 800:
                    self.y += -passo
            case 'L':
                self.x += passo
                self.y += 0
                if self.x > 800:
                    self.x += -passo
            case 'W':
                self.x += -passo
                self.y += 0
                if self.x < 0:
                    self.x += passo

    def gastarEnergia(self):
        if self.energia > 500: #gasta energia para reproduzir
            self.energia = 100 #energia padrão
            filho = copy.deepcopy(self)
            filho.mover()
            return filho
        elif self.energia > 0: #gasta energia para se manter vivo
            self.energia -= 1 #custo energético por turno para se manter vivo
            return 0
        else: #morre
            return -1



class Planta(SerVivo):
    def fotossintese(self):
        self.energia += 5

class Animal(SerVivo):
    def test():
        return
