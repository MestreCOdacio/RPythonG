import random
import time
import os

# Função segura para ler input que evita crash em ambientes sem terminal interativo
def safe_input(prompt, default="1"):
    try:
        return input(prompt)
    except EOFError:
        print(f"{default} [Auto-selecionado pelo sistema]")
        time.sleep(0.5)
        return default

# Função para limpar a tela do terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Dicionário de itens e seus efeitos
ITENS_DB = {
    "Poção de Vida": {"tipo": "cura", "valor": 40, "desc": "Restaura 40 de HP."},
    "Poção Menor": {"tipo": "cura", "valor": 20, "desc": "Restaura 20 de HP."},
    "Cristal de Barreira": {"tipo": "escudo", "valor": 30, "desc": "Adiciona 30 de Defesa (Vida Temporária) na luta."},
    "Bomba de Fogo": {"tipo": "dano", "valor": 35, "desc": "Causa 35 de dano direto no inimigo."}
}

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

        escolha = safe_input("Escolha um item para usar: ")
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


def gerar_inimigo_aleatorio():
    inimigos = [
        {"nome": "Goblin Ladrão", "hp": 40, "vel": 6, "dmin": 4, "dmax": 8},
        {"nome": "Orc Brutal", "hp": 75, "vel": 3, "dmin": 8, "dmax": 15},
        {"nome": "Lobo Selvagem", "hp": 35, "vel": 9, "dmin": 5, "dmax": 10},
        {"nome": "Esqueleto Arqueiro", "hp": 45, "vel": 7, "dmin": 6, "dmax": 12},
        {"nome": "Troll da Caverna", "hp": 100, "vel": 2, "dmin": 10, "dmax": 20}
    ]
    escolhido = random.choice(inimigos)
    return Inimigo(escolhido["nome"], escolhido["hp"], escolhido["vel"], escolhido["dmin"], escolhido["dmax"])

def dar_recompensa(jogador):
    chance = random.random()
    if chance < 0.6: # 60% chance de dropar item
        item_ganho = random.choice(list(ITENS_DB.keys()))
        if item_ganho in jogador.inventario:
            jogador.inventario[item_ganho] += 1
        else:
            jogador.inventario[item_ganho] = 1
        print(f"\n[!] Vitória! O inimigo deixou cair: {item_ganho}!")
    else:
        print("\n[!] Vitória! Mas o inimigo não deixou nada.")
    time.sleep(2)

def iniciar_combate(jogador, inimigo):
    limpar_tela()
    print(f"⚔️ UM {inimigo.nome.upper()} APARECEU! ⚔️")
    time.sleep(1.5)
    
    # Preparar escudo para o combate
    jogador.escudo_temp = jogador.defesa_base
    print(f"\nSua Defesa Base concedeu {jogador.escudo_temp} de Escudo (Vida Temporária) para esta luta!")
    time.sleep(1.5)

    while jogador.esta_vivo() and inimigo.esta_vivo():
        limpar_tela()
        print("="*40)
        print(f"{jogador.nome} (HP: {jogador.hp}/{jogador.hp_max} | Escudo: {jogador.escudo_temp})")
        print(f"INIMIGO: {inimigo.nome} (HP: {inimigo.hp})")
        print("="*40)
        
        print("\nSeu Turno:")
        print("[1] Atacar")
        print("[2] Usar Item")
        print("[3] Tentar Fugir")
        
        acao = safe_input("\nO que você faz? ")
        
        turno_jogador_concluido = False
        fugiu = False

        if acao == '1':
            # Checagem de velocidade para ver quem ataca primeiro
            if jogador.velocidade >= inimigo.velocidade:
                jogador.atacar(inimigo)
                if inimigo.esta_vivo():
                    inimigo.atacar(jogador)
            else:
                print(f"\nO {inimigo.nome} é mais rápido e ataca primeiro!")
                time.sleep(1)
                inimigo.atacar(jogador)
                if jogador.esta_vivo():
                    jogador.atacar(inimigo)
            turno_jogador_concluido = True

        elif acao == '2':
            usou = jogador.gerenciar_inventario(em_combate=True, inimigo=inimigo)
            if usou:
                # Inimigo ataca após usar o item
                if inimigo.esta_vivo():
                    inimigo.atacar(jogador)
                turno_jogador_concluido = True

        elif acao == '3':
            # Chance de fuga baseada na velocidade
            chance = (jogador.velocidade / (jogador.velocidade + inimigo.velocidade)) * 100
            sorte = random.randint(1, 100)
            if sorte <= chance + 20: # +20% base chance
                print("\nVocê conseguiu fugir com sucesso!")
                time.sleep(2)
                fugiu = True
                break
            else:
                print("\nVocê tentou fugir, mas tropeçou!")
                time.sleep(1)
                inimigo.atacar(jogador)
                turno_jogador_concluido = True
        else:
            print("Ação inválida!")
            time.sleep(1)

        if turno_jogador_concluido:
            time.sleep(2)

    # Fim de combate
    jogador.escudo_temp = 0 # Escudo some após o combate
    if not jogador.esta_vivo():
        print(f"\nVocê foi derrotado pelo {inimigo.nome}...")
        time.sleep(2)
    elif not fugiu:
        dar_recompensa(jogador)

def jogo_principal():
    limpar_tela()
    print("="*40)
    print(" " * 8 + "AVENTURA ÉPICA RPG")
    print("="*40)
    
    nome = safe_input("\nDigite o nome do seu Herói: ", "Herói Anônimo")
    
    classe_valida = False
    while not classe_valida:
        print("\nEscolha sua Classe:")
        print("[1] Guerreiro (Alto HP, Alta Força, Começa com muito Escudo)")
        print("[2] Mago (Alta Inteligência, Muito Rápido, Ataques Mágicos)")
        escolha_classe = safe_input("-> ")
        
        if escolha_classe == '1':
            jogador = Jogador(nome, "Guerreiro")
            classe_valida = True
        elif escolha_classe == '2':
            jogador = Jogador(nome, "Mago")
            classe_valida = True
        else:
            print("Classe inválida! Tente novamente.")

    print(f"\nBem-vindo, {jogador.classe} {jogador.nome}!")
    time.sleep(2)

    batalhas_vencidas = 0

    while jogador.esta_vivo():
        limpar_tela()
        print("="*40)
        print("MENU PRINCIPAL - FLORESTA ESCURA")
        print(f"Batalhas Vencidas: {batalhas_vencidas}")
        print("="*40)
        print("[1] Explorar (Procurar Inimigos)")
        print("[2] Status e Inventário")
        print("[3] Descansar (Recupera um pouco de HP, risco de emboscada)")
        print("[4] Desistir da Aventura")

        escolha = safe_input("\nO que deseja fazer? ")

        if escolha == '1':
            print("\nVocê caminha pela floresta escura...")
            time.sleep(1.5)
            inimigo = gerar_inimigo_aleatorio()
            iniciar_combate(jogador, inimigo)
            if jogador.esta_vivo():
                batalhas_vencidas += 1

        elif escolha == '2':
            jogador.mostrar_status()
            jogador.gerenciar_inventario(em_combate=False)

        elif escolha == '3':
            print("\nVocê monta um pequeno acampamento para descansar...")
            time.sleep(2)
            if random.random() < 0.3: # 30% chance de emboscada
                print("CUIDADO! Você foi emboscado enquanto descansava!")
                time.sleep(1.5)
                inimigo = gerar_inimigo_aleatorio()
                iniciar_combate(jogador, inimigo)
                if jogador.esta_vivo():
                    batalhas_vencidas += 1
            else:
                cura = int(jogador.hp_max * 0.3)
                jogador.hp = min(jogador.hp + cura, jogador.hp_max)
                print(f"Descanso tranquilo. Você recuperou {cura} de HP!")
                time.sleep(2)

        elif escolha == '4':
            print(f"\nVocê decidiu voltar para casa. Batalhas vencidas: {batalhas_vencidas}. Até logo!")
            break
        else:
            print("\nComando inválido!")
            time.sleep(1)

    if not jogador.esta_vivo():
        limpar_tela()
        print("="*40)
        print(" " * 12 + "GAME OVER")
        print("="*40)
        print(f"{jogador.nome} caiu em batalha.")
        print(f"Monstros derrotados: {batalhas_vencidas}")
        print("="*40)

if __name__ == "__main__":
    jogo_principal()
