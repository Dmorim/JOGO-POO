from Player import Player
from Game_Actions_Army_Actions import ArmyActions
from multipledispatch import dispatch


class Game_Action():
    def __init__(self):
        self.actions = ArmyActions()

    def action(self, player: Player, action: str):
        if action == "1":
            self.actions.army_action(player)
        elif action == "2":
            self.game.upgrade_province(player)
        elif action == "0":
            return
