import random
from Energia import EnergiaStatus, StatusEnergia

class SerVivo:
    largura, altura = 1000, 1000
    escala = 20  # tamanho do passo
    energia_padrao = 300  # quantidade arbitrária para usar em alguns momentos, o suficiente para o ser viver por um bom tempo
    energia_reproducao = 500  # quantidade de energia necessária para o ser se reproduzir
    custo_energetico = 7  # custo energético por turno para se manter vivo
    energia_fome = 230 # energia abaixo da qual o ser come
    direcao = 'E' #última direção na qual se moveu

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energia = self.energia_padrao
        self.fase = 0

    def atualizar(self):
        self.fase += 0.5

    def gastarEnergia(self) -> StatusEnergia:
        if self.energia > self.energia_reproducao: #so reproduzir se tiver energia o suficiente
            self.energia -= self.energia_padrao
            return StatusEnergia(EnergiaStatus.REPRODUZINDO)
        elif self.energia > 0: #gastar energia para se manter vivo
            self.energia -= type(self).custo_energetico #custo energético por turno para se manter vivo
            return StatusEnergia(EnergiaStatus.VIVO)
        else: #morrer
            return StatusEnergia(EnergiaStatus.MORTO)

    def mover(self, plantas, animais):
        seres = [s for s in plantas + animais if s != self]

        movimentos = ['N', 'S', 'E', 'W']
        random.shuffle(movimentos)

        moveu = False

        for aponta in movimentos:
            #calcula uma coordenada para andar
            tx, ty = self.x, self.y
            match aponta:
                case 'N':
                    ty -= self.escala
                case 'S':
                    ty += self.escala
                case 'E':
                    tx += self.escala
                case 'W':
                    tx -= self.escala

            #verifica a borda do mundo
            if not (0 <= tx <= self.largura and 0 <= ty <= self.altura):
                continue  #se bateu na borda, repete o loop

            #verificar colisão com plantas e animais
            colisao = False
            for ser in seres:
                #if abs(tx - ser.x) < self.escala and abs(ty - ser.y) < self.escala:
                if tx == ser.x and ty == ser.y: #tá durando mais?
                    colisao = True
                    break
            if colisao:
                continue

            #anda!
            self.x = tx
            self.y = ty
            self.direcao = aponta #salva o sentido em que se moveu
            moveu = True
            break

        #se tentou as 4 direções e não moveu, morre
        if not moveu:
            if self in plantas:
                plantas.remove(self)
            elif self in animais:
                animais.remove(self)