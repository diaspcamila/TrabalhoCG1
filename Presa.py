from Animal import Animal

class Presa(Animal):
    def predar(self, plantas, animais):
        if self.energia < self.energia_fome: #verificar se está com fome
            for planta in list(plantas):
                if (abs(self.x - planta.x) <=self.escala) and (abs(self.y - planta.y) <=self.escala): #verificar se tem planta perto
                    plantas.remove(planta) #mata a planta
                    self.energia += 300 #ganha energia
                    break