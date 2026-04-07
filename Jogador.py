import random
import time
from Utilities import ITENS_DB

class Jogador:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.inventario = {"Poção Menor": 2}  # Começa com 2 poções menores
        
        # Configuração de Atributos baseados na Classe
        if classe == "Guerreiro":
            self.hp_max = 120
            self.forca = 12
            self.inteligencia = 3
            self.velocidade = 5
            self.defesa_base = 15 # Ganha 15 de escudo todo começo de luta
        elif classe == "Mago":
            self.hp_max = 80
            self.forca = 2
            self.inteligencia = 15
            self.velocidade = 8
            self.defesa_base = 5  # Ganha 5 de escudo todo começo de luta
            
        self.hp = self.hp_max
        self.escudo_temp = 0 # Defesa temporária durante o combate

    def esta_vivo(self):
        return self.hp > 0

    def mostrar_status(self):
        print("\n" + "="*30)
        print(f"Nome: {self.nome} | Classe: {self.classe}")
        print(f"HP: {self.hp}/{self.hp_max} | Escudo Atual: {self.escudo_temp}")
        print(f"FOR: {self.forca} | INT: {self.inteligencia} | VEL: {self.velocidade} | DEF Base: {self.defesa_base}")
        print("="*30 + "\n")

    def gerenciar_inventario(self, em_combate=False, inimigo=None):
        if not self.inventario:
            print("Seu inventário está vazio!")
            time.sleep(1.5)
            return False

        print("\n--- INVENTÁRIO ---")
        itens_lista = list(self.inventario.keys())
        for i, item in enumerate(itens_lista):
            qtd = self.inventario[item]
            desc = ITENS_DB[item]["desc"]
            print(f"[{i+1}] {item} (x{qtd}) - {desc}")
        print(f"[{len(itens_lista)+1}] Voltar")

        escolha = input("Escolha um item para usar: ")
        try:
            escolha = int(escolha) - 1
            if escolha == len(itens_lista):
                return False # Voltou
            
            if 0 <= escolha < len(itens_lista):
                item_escolhido = itens_lista[escolha]
                efeito = ITENS_DB[item_escolhido]
                
                # Consumir Item
                self.inventario[item_escolhido] -= 1
                if self.inventario[item_escolhido] <= 0:
                    del self.inventario[item_escolhido]

                # Aplicar Efeito
                print(f"\nVocê usou {item_escolhido}!")
                if efeito["tipo"] == "cura":
                    cura = efeito["valor"]
                    self.hp = min(self.hp + cura, self.hp_max)
                    print(f"Você recuperou {cura} de HP. Seu HP agora é {self.hp}/{self.hp_max}.")
                
                elif efeito["tipo"] == "escudo":
                    if em_combate:
                        self.escudo_temp += efeito["valor"]
                        print(f"Seu escudo aumentou para {self.escudo_temp}!")
                    else:
                        print("Você desperdiçou o cristal! Escudos só funcionam em combate.")
                
                elif efeito["tipo"] == "dano":
                    if em_combate and inimigo:
                        dano = efeito["valor"]
                        inimigo.tomar_dano(dano)
                        print(f"A bomba explodiu causando {dano} de dano no {inimigo.nome}!")
                    else:
                        print("Você jogou a bomba no chão... Não havia inimigos. Que desperdício.")
                
                time.sleep(2)
                return True # Item usado com sucesso
            else:
                print("Opção inválida.")
                return False
        except ValueError:
            print("Entrada inválida.")
            return False

    def atacar(self, inimigo):
        # Dano variável (rolagem de 1 a 6) + Modificador (Força ou Inteligência)
        rolagem = random.randint(1, 6)
        if self.classe == "Guerreiro":
            dano_total = rolagem + self.forca
            tipo_ataque = "Golpe de Espada"
        else:
            dano_total = rolagem + self.inteligencia
            tipo_ataque = "Raio Mágico"
            
        print(f"\nVocê usou {tipo_ataque}! (Rolagem: {rolagem} + Modificador)")
        time.sleep(1)
        inimigo.tomar_dano(dano_total)

    def tomar_dano(self, dano):
        # A defesa atua como vida temporária que absorve o dano primeiro
        if self.escudo_temp > 0:
            if self.escudo_temp >= dano:
                self.escudo_temp -= dano
                print(f"Seu escudo absorveu todo o dano! (Escudo restante: {self.escudo_temp})")
                return
            else:
                dano_restante = dano - self.escudo_temp
                print(f"Seu escudo foi quebrado! Ele absorveu {self.escudo_temp} de dano.")
                self.escudo_temp = 0
                dano = dano_restante
        
        self.hp -= dano
        print(f"Você perdeu {dano} de HP! (HP atual: {max(0, self.hp)}/{self.hp_max})")