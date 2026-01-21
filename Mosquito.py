from Animal import Animal

class Mosquito(Animal):
    def predar(self, plantas, animais):
        if self.energia < 270: #verificar se está com fome
            for planta in list(plantas):
                if (abs(self.x - planta.x) <=self.passo) and (abs(self.y - planta.y) <=self.passo): #verificar se tem planta perto
                    plantas.remove(planta) #mata a planta
                    self.energia += 300 #ganha energia
                    break