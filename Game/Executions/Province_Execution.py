from Player import Player
from Game.Game_State import Game_State
from Province import Province


class Province_Execution:
    def __init__(self):
        self.game_state = Game_State()

    def upgrade_province(self, player: Player, province: Province):
        player.action_upgrade_province(province)
        province.upgrade()
        self.game_state.mapmode = False
        print(f'{province.get_name()} foi melhorada com sucesso.')
