from Player import Player
from Game.Executions.Move_Execution import Movement
from Game.Executions.Army_Execution import Army_Execution


class ArmyActions:
    def __init__(self, game):
        self.game = game
        self.army_movement = Movement(self.game)
        self.army_execution = Army_Execution(self.game)

    def __print_available_armys(self, player: Player):
        for number, army in enumerate(player.no_battle_armies()):
            print(f'{number + 1}. {army.army_situation()}')
        print('0. Voltar')

    def __selected_army_verification(self, player: Player) -> int:
        army = None
        while True:
            self.__print_available_armys(player)
            try:
                army = int(input('Selecione o exército pelo número: '))
                if army in range(1, len(player.no_battle_armies()) + 1) or army == 0:
                    return army
                else:
                    print("Valor inválido. Tente novamente.")
            except ValueError:
                print("Valor inválido. Tente novamente.")

    def __show_neighbors(self, selected_army) -> str:
        return f"Província atual: {selected_army.get_province().get_name()}, Vizinhos: {', '.join(neighbor.get_name() for neighbor in selected_army.get_province().get_neighbors())}"

    def __army_actions_verification(self, army) -> int:
        HEALING_ACTIONS = ["1", "0"]
        MOVE_ACTIONS = ["1", "2", "0"]
        DEFAULT_ACTIONS = ["1", "2", "3", "0"]

        if army.get_in_healing():
            valid_answers = HEALING_ACTIONS
        elif army.get_in_move():
            valid_answers = MOVE_ACTIONS
        else:
            valid_answers = DEFAULT_ACTIONS

        while True:
            army_actions = input('Escolha uma ação: ')
            if army_actions in valid_answers:
                return army_actions
            else:
                print("Valor inválido. Tente novamente. Ações válidas são: ",
                      ", ".join(valid_answers))

    def __show_neighbors_to_choose(self, army):
        for number, province in enumerate(army.get_province().get_neighbors()):
            print(
                f'{number + 1}. {province.get_name()} - {province.get_terrain().get_terrain_name()}')

    def __province_choose(self, army) -> int:
        self.__show_neighbors_to_choose(army)
        choose_province = None
        while True:
            try:
                choose_province = int(input('Escolha a província: '))
                if choose_province in range(1, len(army.get_province().get_neighbors()) + 1):
                    return choose_province
                else:
                    print("Valor inválido. Tente novamente.")
            except ValueError:
                print("Valor inválido. Tente novamente.")

    def __dynamic_actions_available(self, army) -> str:
        if army.get_in_healing():
            return "Ações Disponíveis: \n1 - Cancelar Cura\n0 - Voltar"
        elif army.get_in_move():
            return "Ações Disponíveis: \n1 - Cancelar Movimento\n2- Marcha Forçada\n0 - Voltar"
        else:
            return "Ações Disponíveis: \n1 - Mover Exército\n2 - Dividir Exército\n3 - Curar Exército\n0 - Voltar"

    def __elect_player_choice(self, action: str, army, player):
        if army.get_in_healing():
            match action:
                case "1": self.__army.set_in_healing()
                case "0": False
        elif army.get_in_move():
            match action:
                case "1": self.army_movement.cancel_army_movement(army)
                case "2": self.army_movement.forced_march()
                case "0": False
        else:
            match action:
                case "1": self.__army_move(army),
                case "2": self.army_execution.army_division(player, army),
                case "3": self.__attack_province
                case "0": self.army_action(player)

    def __army_move(self, army):
        choosen_province = army.get_province().get_neighbors()[
            self.__province_choose(army) - 1]
        self.army_movement.army_make_movement(army, choosen_province)

    def army_action(self, player):
        if player.no_battle_armies() == []:
            print("Não há exércitos disponíveis.")
            return False

        print("Exércitos disponíveis: ")

        selected_army_index = self.__selected_army_verification(player)
        if selected_army_index == 0:
            self.game.mapmode = False
            return False
        selected_army = player.armys[selected_army_index - 1]
        print(self.__show_neighbors(selected_army))

        print(
            self.__dynamic_actions_available(selected_army)
        )
        self.__elect_player_choice(
            self.__army_actions_verification(selected_army), selected_army, player)
