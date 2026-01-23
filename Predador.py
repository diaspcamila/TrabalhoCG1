from Animal import Animal
from Graficos import setSapo

class Predador(Animal):
    custo_energetico = 2# custo energético por turno para se manter vivo
    #deve ser menor para predador para ele sobreviver longos períodos sem presas

    energia_fome = 1000

    def predar(self, plantas, animais):
        if self.energia < self.energia_fome: #verificar se está com fome
            for animal in list(animais):
                if type(animal) != type(self):
                    if (abs(self.x - animal.x) <= self.escala) and (abs(self.y - animal.y) <= self.escala):  # verificar se tem presa perto
                        animais.remove(animal)  # mata a presa
                        self.energia += 120  # ganha energia
                        break
    
    def desenhar(self, tela):
        setSapo(tela, self.x, self.y)