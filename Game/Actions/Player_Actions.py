from Player import Player
from IA.IA import IA
from Game.Game_State import Game_State
from Game.Actions.Game_Actions import Game_Action
from Game.Map_Actions.Map_Actions import MapActions

from multipledispatch import dispatch


class Player_Action:
    def __init__(self, Game_State: Game_State, Game_Action: Game_Action, Map_Action: MapActions):
        self.game_state = Game_State
        self.game_action = Game_Action
        self.map_action = Map_Action

    @dispatch(Player)
    def action(self, player: Player):
        choice = self.map_action.map_actions()
        self.game_action.action(player, choice)

    @dispatch(IA)
    def action(self, IA: IA):
        act, var = IA.act_do()
        if act == "Move":
            province = var[0][0]
            army = var[0][1]
            self.moviment.army_make_movement(
                army, None, province)
            print(f"Exército movido para {
                province.get_name()}")
        elif act == "Up_Prov":
            prov = var[0]
            self.current_player.action_upgrade_province(prov)
            self.upgrade_province(self.current_player, prov)
            print(f"Província {prov.get_name()} melhorada")
        elif act == "Heal":
            heal_army = var[0]
            self.heal_army(heal_army)
        elif act == "Skip":
            pass
