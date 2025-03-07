from Player import Player
from Game.Game_State import Game_State
from Game.Executions.Province_Execution import Province_Execution


class Upgrade_Province:
    def __init__(self):
        self.game_state = Game_State()
        self.province_execution = Province_Execution()

    def __show_available_province(self, player: Player):
        for number, province in enumerate(player.province_available_to_upgrade()):
            print(
                f'{number + 1}. {province.get_name()} - {province.get_terrain().get_terrain_name()} - Custo: {player.get_upgrade_cost(province)}')
        print('0. Voltar')

    def __selected_province_verification(self, player: Player) -> int:
        while True:
            self.__show_available_province(player)
            try:
                province = int(input('Selecione a província pelo número: '))
                if province in range(1, len(player.province_available_to_upgrade()) + 1) or province == 0:
                    return province
                else:
                    print("Valor inválido. Tente novamente.")
            except ValueError:
                print("Valor inválido. Tente novamente.")

    def upgrade_province(self, player: Player):
        print('Províncias disponíveis para melhoria:')
        province_index = self.__selected_province_verification(player)
        if province_index == 0:
            self.game_state.mapmode = False
            return
        self.province_execution.upgrade_province(
            player, player.province_available_to_upgrade()[province_index - 1])
