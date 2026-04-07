from __future__ import annotations
from typing import TYPE_CHECKING
import random
import time

if TYPE_CHECKING:
    from Jogador import Jogador

class Inimigo:
    def __init__(self, nome: str, hp: int, velocidade: int, dano_min: int, dano_max: int) -> None:
        self.nome: str = nome
        self.hp: int = hp
        self.velocidade: int = velocidade
        self.dano_min: int = dano_min
        self.dano_max: int = dano_max

    def esta_vivo(self) -> bool:
        return self.hp > 0

    def atacar(self, jogador: Jogador) -> None:
        dano = random.randint(self.dano_min, self.dano_max)
        print(f"\nO {self.nome} ataca você!")
        time.sleep(1)
        jogador.tomar_dano(dano)

    def tomar_dano(self, dano: int) -> None:
        self.hp -= dano
        print(f"O {self.nome} sofreu {dano} de dano! (HP do Inimigo: {max(0, self.hp)})")