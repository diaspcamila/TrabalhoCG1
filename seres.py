import random

class SerVivo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Animal(SerVivo):
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
