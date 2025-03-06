from Player import Player
from Province import Province


class Province_Execution:
    def __init__(self, game):
        self.game = game

    def upgrade_province(self, player: Player, province: Province):
        player.action_upgrade_province(province)
        province.upgrade()
        self.game.mapmode = False
        print(f'{province.get_name()} foi melhorada com sucesso.')

