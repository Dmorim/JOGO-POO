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
        floresta = Terrain("Floresta", 1.15, 1.20, 1.1)
        montanha = Terrain("Montanha", 1.8, 1.33, 1.5)
        tundra = Terrain("Tundra", 1.15, 0.8, 1.1)
        deserto = Terrain("Deserto", 1.2, 1, 1.2)

        ### Criação de Províncias ###
        # Províncias do Jogador
        def europe_add_provinces(player_m):
            viena = Province("Viena", player_m, montanha)
            moscou = Province("Moscou", player_m, tundra)
            berlim = Province("Berlim", player_m, planice)
            skopje = Province("Skopje", player_m, floresta)

            player_m.add_province(viena)
            player_m.add_province(moscou)
            player_m.add_province(berlim)
            player_m.add_province(skopje)

        # Províncias da IA 1
        def africa_add_provinces(player_m):
            tripoli = Province("Tripoli", player_m, deserto)
            cairo = Province("Cairo", player_m, deserto)
            cartum = Province("Cartum", player_m, montanha)
            kinshasa = Province("Kinshasa", player_m, floresta)

            player_m.add_province(tripoli)
            player_m.add_province(cairo)
            player_m.add_province(cartum)
            player_m.add_province(kinshasa)

        # Províncias da IA 2
        def asia_add_provinces(player_m):
            teera = Province("Teerã", player_m, deserto)
            pequim = Province("Pequim", player_m, planice)
            jacarta = Province("Jacarta", player_m, montanha)
            toquio = Province("Tóquio", player_m, montanha)

            player_m.add_province(teera)
            player_m.add_province(pequim)
            player_m.add_province(jacarta)
            player_m.add_province(toquio)

        # Províncias da IA 3
        def america_add_provinces(player_m):
            cidade_do_mexico = Province("Cidade do México", player_m, floresta)
            quito = Province("Quito", player_m, montanha)
            lima = Province("Lima", player_m, floresta)
            buenos_aires = Province("Buenos Aires", player_m, planice)

            player_m.add_province(cidade_do_mexico)
            player_m.add_province(quito)
            player_m.add_province(lima)
            player_m.add_province(buenos_aires)

        # Create game
        game = Game()

        # Add players to game
        game.add_player(player1)
        game.add_player(player2)
        game.add_player(player3)
        game.add_player(player4)

        for player in game.players:
            if player.name == "Jogador":
                europe_add_provinces(player)
            elif player.name == "IA 1":
                africa_add_provinces(player)
            elif player.name == "IA 2":
                asia_add_provinces(player)
            elif player.name == "IA 3":
                america_add_provinces(player)

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
5- Sistema de aglutinação de exércitos                              Check
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
- A quantidade de pontos de movimentos necessários para concluír a movimentação será a soma do custo de movimentação da provincia atual para a provincia alvo.
- Movimentação será permitida entre províncias vizinhas
- Um exército em movimentação não pode ser unificado com outro
- Mapa deverá exibir: "Nacionalidade" das tropas, Tropas em movimento, e Provincias vizinhas
- As provincias se organizarão da seguinte forma (Provincia - Vizinhos): {
    Berlim - Viena, Moscou, Skopje, Cartum
    Viena - Skopje, Berlim, Lima
    Moscou - Skopje, Berlim, Teera
    Skopje - Moscou, Berlim, Viena, Cairo
    
    Cairo - Skopje, Tripoli, Cartum, Kinshasa
    Tripoli - Cairo, Cartum, Kinshasa
    Kinshasa - Cairo, Tripoli, Cartum
    Cartum - Berlim, Tripoli, Cairo, Kinshasa
    
    Teerã - Moscou, Pequim, Jacarta, Tóquio
    Pequim - Teerã, Jacarta, Tóquio
    Jacarta - Teerã, Pequim, Tóquio
    Tóquio - Teerã, Pequim, Jacarta, Buenos Aires
    
    Lima - Viena, Buenos Aires, Cidade do México, Quito
    Cidade do México - Lima, Buenos Aires, Quito
    Quito - Lima, Cidade do México, Buenos Aires
    Buenos Aires - Lima, Cidade do México, Quito, Tóquio
}
- Haverá um contador exibindo a quantidade de turnos para concluir a movimentação
- O jogador poderá cancelar a movimentação a qualquer momento de seu turno
- A pontuação de movimentação de tropas reiniará a cada turno
"""
