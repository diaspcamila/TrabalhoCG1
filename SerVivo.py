from Energia import EnergiaStatus, StatusEnergia

class SerVivo:
    largura, altura = 1000, 1000
    escala = 20  # tamanho do passo
    energia_padrao = 300  # quantidade arbitrária para usar em alguns momentos, o suficiente para o ser viver por um bom tempo
    energia_reproducao = 500  # quantidade de energia necessária para o ser se reproduzir
    custo_energetico = 6  # custo energético por turno para se manter vivo

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energia = self.energia_padrao

    def gastarEnergia(self) -> StatusEnergia:
        if self.energia > self.energia_reproducao: #so reproduzir se tiver energia o suficiente
            self.energia = self.energia_padrao
            return StatusEnergia(EnergiaStatus.REPRODUZINDO)
        elif self.energia > 0: #gastar energia para se manter vivo
            self.energia -= type(self).custo_energetico #custo energético por turno para se manter vivo
            return StatusEnergia(EnergiaStatus.VIVO)
        else: #morrer
            return StatusEnergia(EnergiaStatus.MORTO)
