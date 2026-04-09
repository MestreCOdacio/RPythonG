from __future__ import annotations
from typing import TYPE_CHECKING, Any
import random
import time
import os
from Inimigo import Inimigo

if TYPE_CHECKING:
    from Jogador import Jogador

# Função para limpar a tela do terminal
def limpar_tela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

# Dicionário de itens e seus efeitos
ITENS_DB: dict[str, dict[str, Any]] = {
    "Poção de Vida": {"tipo": "cura", "valor": 40, "desc": "Restaura 40 de HP."},
    "Poção Menor": {"tipo": "cura", "valor": 20, "desc": "Restaura 20 de HP."},
    "Cristal de Barreira": {"tipo": "escudo", "valor": 30, "desc": "Adiciona 30 de Defesa (Vida Temporária) na luta."},
    "Bomba de Fogo": {"tipo": "dano", "valor": 35, "desc": "Causa 35 de dano direto no inimigo."},
    "Poção de Força": {"tipo": "forca", "desc": "Aumenta sua Força total em +1"},
    "Poção de Inteligência": {"tipo": "inteligencia", "desc": "Aumenta sua Inteligência total em +1"},
    "Poção de Velocidade": {"tipo": "velocidade", "desc": "Aumenta sua Velocidade total em +1"}
}

def gerar_inimigo_aleatorio() -> Inimigo:
    inimigos: list[dict[str, Any]] = [
        {"nome": "Goblin Ladrão", "hp": 40, "vel": 6, "dmin": 4, "dmax": 8},
        {"nome": "Orc Brutal", "hp": 75, "vel": 3, "dmin": 8, "dmax": 15},
        {"nome": "Lobo Selvagem", "hp": 35, "vel": 9, "dmin": 5, "dmax": 10},
        {"nome": "Esqueleto Arqueiro", "hp": 45, "vel": 7, "dmin": 6, "dmax": 12},
        {"nome": "Troll da Caverna", "hp": 100, "vel": 2, "dmin": 10, "dmax": 20}
    ]
    escolhido: dict[str, Any] = random.choice(inimigos)
    return Inimigo(escolhido["nome"], escolhido["hp"], escolhido["vel"], escolhido["dmin"], escolhido["dmax"])

def dar_recompensa(jogador: Jogador) -> None:
    chance: float = random.random()
    if chance < 0.3: # 60% chance de dropar item
        item_ganho = random.choice(list(ITENS_DB.keys()))
        if item_ganho in jogador.inventario:
            jogador.inventario[item_ganho] += 1
        else:
            jogador.inventario[item_ganho] = 1
        print(f"\n[!] Vitória! O inimigo deixou cair: {item_ganho}!")
    else:
        print("\n[!] Vitória! Mas o inimigo não deixou nada.")
    time.sleep(2)

def iniciar_combate(jogador: Jogador, inimigo: Inimigo) -> None:
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
        
        acao: str = input("\nO que você faz? ")
        
        turno_jogador_concluido: bool = False
        fugiu: bool = False

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
            chance: float = (jogador.velocidade / (jogador.velocidade + inimigo.velocidade)) * 100
            sorte: int = random.randint(1, 100)
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
