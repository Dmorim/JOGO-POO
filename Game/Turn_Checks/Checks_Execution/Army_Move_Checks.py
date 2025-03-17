from Player import Player
from Game.Battle_Control import Battle_Control


class ArmyMoveChecks:
    def __init__(self):
        self.battle_control = Battle_Control()

    def __update_movement_turns(self, player):
        for army in player.get_army_in_move():
            army.update_turns_to_move()
            if army.turns_to_move == 0:
                self.__army_into_province(army)

    def __army_into_province(self, army):
        army.finish_movement()
        if army.get_province().get_owner() != army.get_owner():
            self.battle_control.handle_battle(army.get_province(), army)

    def __cancel_moviment_to_battle(self, player):
        for army in player.get_army_in_move():
            if army.get_province().get_in_battle():
                self.__check_battle_owner(army)

    def __check_battle_owner(self, army):
        battle = self.battle_control.get_ongoing_battle(
            army.get_destination_province())
        if battle is not None:
            if (battle.get_off_army_owner() != army.get_owner() and battle.get_def_army_owner() != army.get_owner()):
                army.cancel_movement()
                print(
                    f"Movimento cancelado, devido a batalha em {army.get_destination_province().get_name()}, exército retornou para {army.get_province().get_name()}")

    def __turn_healing(self, player):
        for army in player.get_army_in_healing():
            army.heal_army_action()

    def move_checks(self, player: Player):
        self.__cancel_moviment_to_battle(player)
        self.__update_movement_turns(player)
        self.__turn_healing(player)
