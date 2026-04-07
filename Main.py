import random
import time
import Jogador
import Utilities
import Save #importando o modulo de salvamento.

def jogo_principal():
    Utilities.limpar_tela()
    print("="*40)
    print(" " * 8 + "AVENTURA ÉPICA RPG")
    print("="*40)
    jogo_salvo = Save.carregar_jogo() #variável que recebe os valores retornados do carregar_jogo().

    if jogo_salvo == None: #testando se foi encontrado arquivo de save com a variável,

        """nome = input("\nDigite o nome do seu Herói: ", "Herói Anônimo") 
        correction: tava dando erro ao executar, pois o imput só aceita um argumento."""
        nome = input("\nDigite o nome do seu Herói: ")
        if nome == "":
            nome = "Herói Anônimo"
        
        classe_valida = False
        while not classe_valida:
            print("\nEscolha sua Classe:")
            print("[1] Guerreiro (Alto HP, Alta Força, Começa com muito Escudo)")
            print("[2] Mago (Alta Inteligência, Muito Rápido, Ataques Mágicos)")
            escolha_classe = input("-> ")
            
            if escolha_classe == '1':
                jogador = Jogador.Jogador(nome, "Guerreiro")
                classe_valida = True
            elif escolha_classe == '2':
                """jogador = Jogador(nome, "Mago")
                correction: estava mencionando apenas o module, vc queria pegar a classe que ta dentro do module,
                fiz a mesma correção no do guerreiro."""
                jogador = Jogador.Jogador(nome, "Mago")
                classe_valida = True
            else:
                print("Classe inválida! Tente novamente.")
        batalhas_vencidas = 0

    else:
        Utilities.limpar_tela()
        print("="*40)
        print(" " * 8 + "AVENTURA ÉPICA RPG")
        print("="*40)
        jogador, batalhas_vencidas = jogo_salvo # cada variável recebe um dos valores retornados.
        print("save carregado!")
        time.sleep(1)
        Utilities.limpar_tela()
        


    print(f"\nBem-vindo, {jogador.classe} {jogador.nome}!")
    time.sleep(2)

    

    while jogador.esta_vivo():
       # Utilities.limpar_tela()
        print("="*40)
        print("MENU PRINCIPAL - FLORESTA ESCURA")
        print(f"Batalhas Vencidas: {batalhas_vencidas}")
        print("="*40)
        print("[1] Explorar (Procurar Inimigos)")
        print("[2] Status e Inventário")
        print("[3] Descansar (Recupera um pouco de HP, risco de emboscada)")
        print("[4] Salvar e sair")
        print("[5] Desistir da Aventura")

        escolha = input("\nO que deseja fazer? ")

        if escolha == '1':
            print("\nVocê caminha pela floresta escura...")
            time.sleep(1.5)
            inimigo = Utilities.gerar_inimigo_aleatorio()
            Utilities.iniciar_combate(jogador, inimigo)
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
                inimigo = Utilities.gerar_inimigo_aleatorio()
                Utilities.iniciar_combate(jogador, inimigo)
                if jogador.esta_vivo():
                    batalhas_vencidas += 1
            else:
                cura = int(jogador.hp_max * 0.3)
                jogador.hp = min(jogador.hp + cura, jogador.hp_max)
                print(f"Descanso tranquilo. Você recuperou {cura} de HP!")
                time.sleep(2)

        elif escolha == '4':
            Save.salvar_jogo(jogador, batalhas_vencidas) #cria o arquivo json para salvar as info do jogador.
            print("jogo salvo!")
            break

        elif escolha == '5':
            print(f"\nVocê decidiu voltar para casa. Batalhas vencidas: {batalhas_vencidas}. Até logo!")
            break
        else:
            print("\nComando inválido!")
            time.sleep(1)

    if not jogador.esta_vivo():
        Utilities.limpar_tela()
        print("="*40)
        print(" " * 12 + "GAME OVER")
        print("="*40)
        print(f"{jogador.nome} caiu em batalha.")
        print(f"Monstros derrotados: {batalhas_vencidas}")
        print("="*40)

if __name__ == "__main__":
    jogo_principal()
