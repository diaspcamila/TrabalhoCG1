from SerVivo import SerVivo

class Animal(SerVivo):
    largura, altura, custo_energetico = SerVivo.largura, SerVivo.altura, SerVivo.custo_energetico

    def predar(self, plantas, animais):
        return
