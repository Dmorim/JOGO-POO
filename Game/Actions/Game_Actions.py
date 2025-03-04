from Player import Player
from Game.Actions.Game_Actions_Army_Actions import ArmyActions


class Game_Action:
    def __init__(self, game):
        self.game = game
        self.army_actions = ArmyActions(self.game)

    def action(self, player: Player, action: str):
        if action == "1":
            self.army_actions.army_action(player)
        elif action == "2":
            self.game.upgrade_province(player)
        elif action == "0":
            self.game.player_skip = True
