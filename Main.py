from Player import Player
from Terrain import Terrain
from Province import Province
from Game import Game
from IA import IA


class Main:
    def __init__(self):
        ### Criação de jogadores ###
        player1 = Player("Jogador")
        player2 = Player("IA 1")
        player3 = Player("IA 2")
        player4 = Player("IA 3")

        player2.set_ia(IA("IA 1", player2))
        player3.set_ia(IA("IA 2", player3))
        player4.set_ia(IA("IA 3", player4))

        ### Criação de Terrenos ###
        planice = Terrain("Planice", 1, 1, 1)
        floresta = Terrain("Floresta", 1.15, 1.20, 1.5)
        montanha = Terrain("Montanha", 1.8, 1.33, 1.8)
        tundra = Terrain("Tundra", 1.15, 0.8, 1.1)
        deserto = Terrain("Deserto", 1.2, 1, 1.2)

        ### Criação de Províncias ###
        # Províncias do Jogador
        def europe_add_provinces(player_m):
            self.viena = Province("Viena", player_m, montanha)
            self.moscou = Province("Moscou", player_m, tundra)
            self.berlim = Province("Berlim", player_m, planice)
            self.skopje = Province("Skopje", player_m, floresta)

            player_m.add_province(self.viena)
            player_m.add_province(self.moscou)
            player_m.add_province(self.berlim)
            player_m.add_province(self.skopje)

        # Províncias da IA 1
        def africa_add_provinces(player_m):
            self.tripoli = Province("Tripoli", player_m, deserto)
            self.cairo = Province("Cairo", player_m, deserto)
            self.cartum = Province("Cartum", player_m, montanha)
            self.kinshasa = Province("Kinshasa", player_m, floresta)

            player_m.add_province(self.tripoli)
            player_m.add_province(self.cairo)
            player_m.add_province(self.cartum)
            player_m.add_province(self.kinshasa)

        # Províncias da IA 2
        def asia_add_provinces(player_m):
            self.teera = Province("Teerã", player_m, deserto)
            self.pequim = Province("Pequim", player_m, planice)
            self.jacarta = Province("Jacarta", player_m, montanha)
            self.toquio = Province("Tóquio", player_m, montanha)

            player_m.add_province(self.teera)
            player_m.add_province(self.pequim)
            player_m.add_province(self.jacarta)
            player_m.add_province(self.toquio)

        # Províncias da IA 3
        def america_add_provinces(player_m):
            self.cidade_do_mexico = Province("Cidade do México", player_m, floresta)
            self.quito = Province("Quito", player_m, montanha)
            self.lima = Province("Lima", player_m, floresta)
            self.buenos_aires = Province("Buenos Aires", player_m, planice)

            player_m.add_province(self.cidade_do_mexico)
            player_m.add_province(self.quito)
            player_m.add_province(self.lima)
            player_m.add_province(self.buenos_aires)

        def add_neighbors():
            self.berlim.add_neighbor(self.viena, self.moscou, self.skopje, self.cartum)
            self.viena.add_neighbor(self.lima, self.skopje, self.berlim)
            self.moscou.add_neighbor(self.skopje, self.berlim, self.teera)
            self.skopje.add_neighbor(self.moscou, self.berlim, self.viena, self.cairo)
            self.lima.add_neighbor(
                self.viena,
                self.buenos_aires,
                self.cidade_do_mexico,
                self.quito,
                self.cairo,
            )
            self.cidade_do_mexico.add_neighbor(self.lima, self.buenos_aires, self.quito)
            self.quito.add_neighbor(self.lima, self.cidade_do_mexico, self.buenos_aires)
            self.buenos_aires.add_neighbor(
                self.lima, self.cidade_do_mexico, self.quito, self.toquio
            )
            self.tripoli.add_neighbor(self.cairo, self.cartum, self.kinshasa)
            self.cairo.add_neighbor(
                self.skopje,
                self.tripoli,
                self.cartum,
                self.kinshasa,
                self.lima,
                self.teera,
            )
            self.cartum.add_neighbor(
                self.berlim, self.tripoli, self.cairo, self.kinshasa
            )
            self.kinshasa.add_neighbor(self.cairo, self.tripoli, self.cartum)
            self.teera.add_neighbor(
                self.moscou, self.pequim, self.jacarta, self.toquio, self.cairo
            )
            self.pequim.add_neighbor(self.teera, self.jacarta, self.toquio)
            self.jacarta.add_neighbor(self.teera, self.pequim, self.toquio)
            self.toquio.add_neighbor(
                self.teera, self.pequim, self.jacarta, self.buenos_aires
            )

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

        add_neighbors()
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

Função para movimentação de tropas  Check
Função para atacar províncias(Dependente de movimentação de tropas)
Função para curar exércitos
Função para inserção dos dados do jogo antes de iniciar
Encapsulamento de classes em arquivos separados
Classe para armazenar funções de ação
Classe para armazenar as informações do jogo antes de começar
Implementação de AI
Definição de Mapa para o jogo


Organização de prioridades:
1- Encapsulamento de classes em arquivos separados                      Check
2- Classe para armazenar funções de ação ( Inviável )                   Check
3- Classe para armazenar as informações do jogo antes de começar        Check
4- Definição de Mapa para o jogo                                        Check
5- Sistema de aglutinação de exércitos                                  Check
6- Função para movimentação de tropas                                   Check
7- Função para atacar províncias(Dependente de movimentação de tropas)
8- Função para curar exércitos
9- Implementação de AI
"""


"""
Sistema de Movimentação de Tropas:
- O jogador escolhe a província de origem e a província de destino  Check
- Tropas terão uma quantiade de movimentos por turno    Check
- Províncias terão um custo de movimentação multiplicado pelo terreno   Check
- A quantidade de pontos de movimentos necessários para concluír a movimentação será a soma do custo de movimentação da provincia atual para a provincia alvo.  Check
- Movimentação será permitida entre províncias vizinhas Check
- Um exército em movimentação não pode ser unificado com outro  Check
- Mapa deverá exibir: "Nacionalidade" das tropas, Tropas em movimento, e Provincias vizinhas    Check
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
}   Check
- Haverá um contador exibindo a quantidade de turnos para concluir a movimentação   Check
- O jogador poderá cancelar a movimentação a qualquer momento de seu turno  Check
- A pontuação de movimentação de tropas reiniará a cada turno   Check
"""

"""
Sistema de Ataque de Províncias:
- Sistema com base em turnos    Check
- Um exército marcado como atacante e outro como defensor   Check
- Fatores que irão influenciar na batalha:  Check
    - Valor de ataque do exército ofensor   Check
    - Valor de defesa do exército defensor  Check
    - Terreno da província  Check
    - Quanto menor a vida da tropa, menor será sua pontuação de ataque e defesa     Check
    - A pontuação de ataque e defesa terá um multiplicador randômico. O multiplicador terá um intervalo maior para o ataque e menor para a defesa no exército ofensor e vice-versa para o defensor  Check
    - A quantidade de dano infligida será baseada na diferença entre a pontuação de ataque e defesa dos exércitos  Check
    - O exército defensor causará dano de retaliação    Check
    - Uma vez travado em batalha, nenhum dos exércitos poderá tomar outra ação até o fim dela.  Check
    - Reforços poderão ser enviados para a batalha de ambas as partes   Check
    - A batalha acabará quando a vida de um dos exércitos chegar a 0. O exército perdedor será eliminado    Check
    - O exército vencedor terá sua vida reduzida pela quantidade de dano sofrida    Check
- Ao final da batlha, o exército vencedor poderá ocupar a província     Check
- A provincia ocupada ficará sem produzir unidades por 3 turnos após a conquista    Check
- A cura do exército impossibilitará o movimento até o exército estar com a vida cheia ou ser cancelado pelo usuário
- Batalhas que durarem mais de 10 turnos serão consideradas batalhas épicas e terão seus multiplicadores randômicos potencializados.    Check
- Avançar em uma provincia não pertencente ao jogador será considerado um ataque    Check

"""

"""
Sistema de Cura de Exércitos:
- Cura modificada pela provincia
- Cura será feita em turnos
- Cura será limitada pelo total de vida do exército
- Um exército em movimento não poderá ser curado
- Um exército em batalha não poderá ser curado
- Um exército se curando não poderá realizar outra ação até o fim da cura ou ela ser cancelada
- Haverá um contador exibindo quantos turnos faltam para terminar a cura
- A cura não poderar executar mais de uma vez por turno
- A cura não poderá exceder 50% da vida atual do exército
- Exércitos em cura serão exibidos no mapa com a simbologia de cura

"""
