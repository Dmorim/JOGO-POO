from Player import Player
from Game.Game_State import Game_State
from Game.Actions.Game_Actions_Army_Actions import ArmyActions
from Game.Actions.Game_Actions_Upgrade_Province import Upgrade_Province
from Game.Map_Actions.Map_Error import MapError


class Game_Action:
    def __init__(self):
        self.game_state = Game_State()
        self.army_actions = ArmyActions()
        self.upgrade_province = Upgrade_Province()

    def action(self, player: Player, action: str):
        try:
            if action == "1":
                self.army_actions.army_action(player)
            elif action == "2":
                self.upgrade_province.upgrade_province(player)
            elif action == "0":
                self.game_state.player_skip = True

        except MapError:
            pass
