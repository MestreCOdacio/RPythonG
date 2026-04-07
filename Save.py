import json #importando a biblioteca nativa para manipular json
from Jogador import Jogador

def salvar_jogo(jogador : type, batalhas_vencidas : int): # definindo a tipagem do parâmetro pra poder pegar o objeto junto com o inteiro
    save_jogador = (vars(jogador)) # salva os chave-valores do objeto e não a coordenada.
    save_jogador['batalhas_vencidas'] = batalhas_vencidas #coloca uma chave no objeto com o valor do segundo parâmetro
    with open("save.json", "w") as f: #utiliza a estrutura with, para que não aja necessidade de fechar o arquivo manualmente caso dê errado.
        json.dump(save_jogador, f, indent=2) #manipulando json para salvar o jogador e as batalhas vencidas
    
def carregar_jogo():
    try:
        with open("save.json", "r") as f:
            save = json.load(f)#manipulando para carregar as informações arquivadas.
            
            carregar_save = input(f"Foi encontrado um save com o nome {save['nome']}, deseja carregar?[s/n]").lower()
            if carregar_save == 's':
                jogador_carregado = Jogador(save['nome'], save['classe']) # criando um objeto com o construtor
                jogador_carregado.inventario = save['inventario']
                jogador_carregado.hp_max = save['hp_max']
                jogador_carregado.forca = save['forca']
                jogador_carregado.inteligencia = save['inteligencia'] #definindo as propriedades do construtor com as info arquivadas.
                jogador_carregado.velocidade = save['velocidade']
                jogador_carregado.defesa_base = save['defesa_base']
                jogador_carregado.hp = save['hp']
                jogador_carregado.escudo_temp = save['escudo_temp']
                return jogador_carregado, save['batalhas_vencidas'] #retornando dois valores, objeto e o inteiro.
            elif carregar_save == 'n':
                return None
    except FileNotFoundError: 
        return None
    
    
