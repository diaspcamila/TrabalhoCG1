from Animal import Animal
from Graficos import setSapo, setTubarao

class Predador(Animal):
    custo_energetico = 2# custo energético por turno para se manter vivo
    #deve ser menor para predador para ele sobreviver longos períodos sem presas

    energia_fome = 1000

    lingua = 0

    def predar(self, plantas, animais):
        if self.energia < self.energia_fome: #verificar se está com fome
            for animal in list(animais):
                if type(animal) != type(self):
                    if (abs(self.x - animal.x) <= self.escala) and (abs(self.y - animal.y) <= self.escala):  # verificar se tem presa perto
                        self.lingua = 4
                        animais.remove(animal)  # mata a presa
                        self.energia += 120  # ganha energia
                        break
    
    def desenhar(self, tela, bioma, viewport):
        if bioma == 0:
            setSapo(tela, self.x, self.y, self.fase, viewport, self.lingua)
        else:
            setTubarao(tela, self.x, self.y, self.fase, viewport, self.lingua > 0)

    def atualizar(self):
        self.fase += 0.5
        if self.lingua > 0:
            self.lingua -= 1