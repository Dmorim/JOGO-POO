from Game.Game import Game
from Player import Player
from Army import Army_Group


class Game_Action():
    def __init__(self, game: Game):
        self.game = game

    def __print_available_armys(self, player: Player):
        for number, army in enumerate(player.get_available_army()):
            print(f'{number + 1}. {army.army_situation()}')

    def __selected_army_verification(self, player: Player) -> int:
        army = 0
        while army in range(len(player.get_available_army())):
            self.__print_available_armys(player)
            army = int(input())

        return army

    def __army_action(self, player: Player):
        if player.get_available_army() == []:
            print("Não há exércitos disponíveis.")
            self.game.mapmode = False
            return

        print("Exércitos disponíveis: ")
        self.__print_available_armys(player)

        selected_army = input()
        if int(selected_army) <= len(player.get_available_army()) + 1:
            selected_army = player.armys[int(selected_army) - 1]
            print(
                f"Província atual: {selected_army.get_province().get_name()}, Vizinhos: {
                    [neighbor.get_name() for neighbor in selected_army.get_province().get_neighbors()]}"
            )

            print(
                "Ações disponíveis:\n1 - Mover Exército\n2 - Dividir Exército\n3 - Curar Exército\n0 - Voltar"
            )
            army_actions = input()
            if army_actions == "1":
                self.moviment.army_movement(player, selected_army)
            elif army_actions == "2":
                self.army_split(player, selected_army)
            elif army_actions == "3":
                self.heal_army(selected_army)
            elif army_actions == "0":
                pass

    def action(self, player: Player):
        pass
