from Player import Player


class ArmyActions:
    def __init__(self):
        pass
    
    def __print_available_armys(self, player: Player):
        for number, army in enumerate(player.get_available_army()):
            print(f'{number + 1}. {army.army_situation()}')

    def __selected_army_verification(self, player: Player) -> int:
        army = None
        while army not in range(1, len(player.get_available_army()) + 1):
            self.__print_available_armys(player)
            try:
                army = int(input('Selecione o exército pelo número: '))
                if army not in range(1, len(player.get_available_army()) + 1):
                    print("Valor inválido. Tente novamente.")
            except ValueError:
                print("Valor inválido. Tente novamente.")
        return army

    def __show_neighbors(self, selected_army) -> str:
        return f"Província atual: {selected_army.get_province().get_name()}, Vizinhos: {', '.join(neighbor.get_name() for neighbor in selected_army.get_province().get_neighbors())}"

    def __army_actions_verification(self, valid_answers: list = ["1", "2", "3", "0"]) -> str:
        army_actions = input('Escollha uma ação: ')
        while army_actions not in valid_answers:
            print("Valor inválido. Tente novamente.")
            army_actions = input('Escollha uma ação: ')
        return army_actions

    def __elect_player_choice(self, action: str):
        match action:
            case "1": return self._army_action,
            case "2": return self.__upgrade_province,
            case "3": return self.__attack_province
            case "0": return False

    def army_action(self, player):
        if player.get_available_army() == []:
            print("Não há exércitos disponíveis.")
            self.game.mapmode = False
            return

        print("Exércitos disponíveis: ")

        selected_army_index = self.__selected_army_verification(player)
        selected_army = player.armys[selected_army_index - 1]
        print(self.__show_neighbors(selected_army))
        print(
            "Ações disponíveis:\n1 - Mover Exército\n2 - Dividir Exército\n3 - Curar Exército\n0 - Voltar"
        )
        army_actions = self.__army_actions_verification()
        self.__elect_player_choice(army_actions)
