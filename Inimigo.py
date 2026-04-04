import random
import time

class Inimigo:
    def __init__(self, nome, hp, velocidade, dano_min, dano_max):
        self.nome = nome
        self.hp = hp
        self.velocidade = velocidade
        self.dano_min = dano_min
        self.dano_max = dano_max

    def esta_vivo(self):
        return self.hp > 0

    def atacar(self, jogador):
        dano = random.randint(self.dano_min, self.dano_max)
        print(f"\nO {self.nome} ataca você!")
        time.sleep(1)
        jogador.tomar_dano(dano)

    def tomar_dano(self, dano):
        self.hp -= dano
        print(f"O {self.nome} sofreu {dano} de dano! (HP do Inimigo: {max(0, self.hp)})")