from Player import Player
from Game.Actions.Game_Actions_Army_Actions import ArmyActions
from Game.Actions.Game_Actions_Upgrade_Province import Upgrade_Province


class Game_Action:
    def __init__(self, game):
        self.game = game
        self.army_actions = ArmyActions(self.game)
        self.upgrade_province = Upgrade_Province(self.game)

    def action(self, player: Player, action: str):
        if action == "1":
            self.army_actions.army_action(player)
        elif action == "2":
            self.upgrade_province.upgrade_province(player)
        elif action == "0":
            self.game.player_skip = True
