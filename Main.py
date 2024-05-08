from Player import Player
from Terrain import Terrain
from Province import Province
from Game import Game


class Main:
    def __init__(self):
        ### Criação de jogadores ###
        player1 = Player("Jogador")
        player2 = Player("IA 1")
        player3 = Player("IA 2")
        player4 = Player("IA 3")

        ### Criação de Terrenos ###
        planice = Terrain("Planice", 1, 1, 1)
        floresta = Terrain("Floresta", 0.8, 1.25, 1.1)
        montanha = Terrain("Montanha", 0.6, 1.33, 1.5)
        tundra = Terrain("Tundra", 1.1, 0.8, 1.3)
        deserto = Terrain("Deserto", 1.2, 1, 0.7)

        ### Criação de Províncias ###
        # Províncias do Jogador
        viena = Province("Viena", player1, montanha)
        moscou = Province("Moscou", player1, tundra)
        berlim = Province("Berlim", player1, planice)
        skopje = Province("Skopje", player1, floresta)

        player1.add_province(viena)
        player1.add_province(moscou)
        player1.add_province(berlim)
        player1.add_province(skopje)

        # Províncias da IA 1
        tripoli = Province("Tripoli", player2, deserto)
        cairo = Province("Cairo", player2, deserto)
        cartum = Province("Cartum", player2, montanha)
        kinshasa = Province("Kinshasa", player2, floresta)

        player2.add_province(tripoli)
        player2.add_province(cairo)
        player2.add_province(cartum)
        player2.add_province(kinshasa)

        # Províncias da IA 2
        teera = Province("Teerã", player3, deserto)
        pequim = Province("Pequim", player3, planice)
        jacarta = Province("Jacarta", player3, montanha)
        toquio = Province("Tóquio", player3, montanha)

        player3.add_province(teera)
        player3.add_province(pequim)
        player3.add_province(jacarta)
        player3.add_province(toquio)

        # Províncias da IA 3
        cidade_do_mexico = Province("Cidade do México", player4, floresta)
        quito = Province("Quito", player4, montanha)
        lima = Province("Lima", player4, floresta)
        buenos_aires = Province("Buenos Aires", player4, planice)

        player4.add_province(cidade_do_mexico)
        player4.add_province(quito)
        player4.add_province(lima)
        player4.add_province(buenos_aires)

        # Create game
        game = Game()

        # Add players to game
        game.add_player(player1)
        game.add_player(player2)
        game.add_player(player3)
        game.add_player(player4)

        # Start game
        game.start()

        # Play game
        game.play()


if "__main__" == __name__:
    Main()


"""
Checklist:
Criação de Exércitos	Check
Criação de Províncias	Check
Criação de Jogadores	Check
Criação de Terrenos     Check
Geração de Exércitos	Check
Criação do Mapa         Check
Funçao para melhorar província	Check
Função para criar exercito em turno    Check

Função para movimentação de tropas
Função para atacar províncias(Dependente de movimentação de tropas)
Função para curar exércitos
Função para inserção dos dados do jogo antes de iniciar
Encapsulamento de classes em arquivos separados
Classe para armazenar funções de ação
Classe para armazenar as informações do jogo antes de começar
Implementação de AI
Definição de Mapa para o jogo


Organização de prioridades:
1- Encapsulamento de classes em arquivos separados                  Check
2- Classe para armazenar funções de ação ( Inviável )               Check
3- Classe para armazenar as informações do jogo antes de começar    Check
4- Definição de Mapa para o jogo                                    Check
5- Sistema de aglutinação de exércitos
6- Função para movimentação de tropas
7- Função para atacar províncias(Dependente de movimentação de tropas)
8- Função para curar exércitos
9- Implementação de AI
"""


"""
Sistema de Movimentação de Tropas:
- O jogador escolhe a província de origem e a província de destino
- Tropas terão uma quantiade de movimentos por turno
- Províncias terão um custo de movimentação multiplicado pelo terreno
- 
"""
