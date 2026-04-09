from typing import *
import random
import time
from Jogador import Jogador
from Utilities import gerar_inimigo_aleatorio, iniciar_combate, limpar_tela
from Save import carregar_jogo, salvar_jogo #importando as funções de salvamento e carregamento.

def jogo_principal() -> None:
    limpar_tela()
    DIVISOR: Final[str] = "=" * 40

    print(DIVISOR)
    print(" " * 8 + "AVENTURA ÉPICA RPG")
    print(DIVISOR)
    print("Escolha um Slot de Save:")
    num_slot = input("\n1.\n2.\n3.\n>")
    slot_selecionado = "save_slot" + num_slot
    jogo_salvo = carregar_jogo(slot_selecionado) #variável que recebe os valores retornados do carregar_jogo().

    if jogo_salvo == None: #testando se foi encontrado arquivo de save com a variável.
        
        nome_input: str = input("\nDigite o nome do seu Herói: ")
        nome: str = nome_input if nome_input.strip() else "Herói Anônimo"

        classe_valida: bool = False
        while not classe_valida:
            print("\nEscolha sua Classe:")
            print("[1] Guerreiro (Alto HP, Alta Força, Começa com muito Escudo)")
            print("[2] Mago (Alta Inteligência, Muito Rápido, Ataques Mágicos)")
            escolha_classe: str = input("-> ")
            
            if escolha_classe == '1':
                jogador = Jogador(nome, "Guerreiro")
                classe_valida = True
            elif escolha_classe == '2':
                jogador = Jogador(nome, "Mago")
                classe_valida = True
            else:
                print("Classe inválida! Tente novamente.")
        batalhas_vencidas: int = 0
    else:
        limpar_tela()
        print(DIVISOR)
        print(" " * 8 + "AVENTURA ÉPICA RPG")
        print(DIVISOR)
        jogador, batalhas_vencidas = jogo_salvo # cada variável recebe um dos valores retornados.
        print("save carregado!")
        time.sleep(1)
        limpar_tela()
    
    if jogador is None:
        return

    print(f"\nBem-vindo, {jogador.classe} {jogador.nome}!")
    time.sleep(2)
    

    while jogador.esta_vivo():
        limpar_tela()
        print(DIVISOR)
        print("MENU PRINCIPAL - FLORESTA ESCURA")
        print(f"Batalhas Vencidas: {batalhas_vencidas}")
        print(DIVISOR)
        print("[1] Explorar (Procurar Inimigos)")
        print("[2] Status e Inventário")
        print("[3] Descansar (Recupera um pouco de HP, risco de emboscada)")
        print("[4] Salvar e sair")
        print("[5] Desistir da Aventura")

        escolha: str = input("\nO que deseja fazer? ")

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
                cura: int = int(jogador.hp_max * 0.3)
                jogador.hp = min(jogador.hp + cura, jogador.hp_max)
                print(f"Descanso tranquilo. Você recuperou {cura} de HP!")
                time.sleep(2)

        elif escolha == '4':
            salvar_jogo(jogador, batalhas_vencidas, slot_selecionado) #cria o arquivo json para salvar as informações do jogador.
            print("jogo salvo!")
            break

        elif escolha == '5':
            print(f"\nVocê decidiu voltar para casa. Batalhas vencidas: {batalhas_vencidas}. Até logo!")
            break
        else:
            print("\nComando inválido!")
            time.sleep(1)

    if not jogador.esta_vivo():
        limpar_tela()
        print(DIVISOR)
        print(" " * 12 + "GAME OVER")
        print(DIVISOR)
        print(f"{jogador.nome} caiu em batalha.")
        print(f"Monstros derrotados: {batalhas_vencidas}")
        print(DIVISOR)
        jogo_salvo[slot_selecionado] = None

if __name__ == "__main__":
    jogo_principal()
