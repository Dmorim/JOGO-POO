from Player import Player
from Army import Army_Group
from Game.Battle_Control import Battle_Control


class ArmyChecks:
    def __init__(self):
        self.battle_control = Battle_Control()
        self.constant_army_move_points = 5

    def __army_creation(self, player):
        for province in player.get_player_province():
            province.produce_army()

    def __create_groups_of_armys(self, player):
        for province in player.get_player_province():
            if province.get_available_armys() > 1:
                armies = province.get_available_armys()
                army_group = self.__find_or_create_army_group(province, armies)
                self.__add_armies_to_group(army_group, armies)

    def __add_armies_to_group(self, army_group: Army_Group, armies: list):
        for army in armies:
            if not isinstance(army, Army_Group):
                army_group.add_army(army)
                army.get_owner().remove_army(army)

    def __find_or_create_army_group(self, province, armies):
        for army in armies:
            if isinstance(army, Army_Group):
                return army
        return Army_Group(province, armies[0].get_owner())

    def __turn_healing(self, player):
        for army in player.get_army_in_healing():
            army.heal_army_action()

    def update_movement_turns(self, player_m):
        for army in player_m.get_army_in_move():
            if self.verify_battle(army):
                army.turns_to_move -= 1
                if army.turns_to_move == 0:
                    self.army_into_province(army)

    def __update_domination_turns(self, player):
        for province in player.obtain_dominated_provinces:
            province.update_dom_turns()

    def __cancel_moviment_to_battle(self, player):
        for army in player.get_army_in_move():
            if army.get_province().get_in_battle():
                self.__check_battle_owner(army)

    def __check_battle_owner(self, army):
        battle = self.battle_control.get_ongoing_battle(
            army.get_destination_province())
        if battle.get_off_army_owner() != army.get_owner() and battle.get_def_army_owner() != army.get_owner():
            army.cancel_movement()

    def army_into_province(self, selected_army):
        selected_army.in_move = False
        selected_army.current_province = selected_army.dest_province
        if selected_army.dest_province.get_in_battle():
            self.game.check_battles(selected_army)
        elif selected_army.dest_province.get_owner() != selected_army.get_owner():
            self.game.check_battles(selected_army)
        selected_army.dest_province = None
        selected_army.turns_to_move = None

    def army_checks(self, player: Player):
        self.__army_creation(player)
        self.__create_groups_of_armys(player)
        self.__turn_healing(player)
        self.__cancel_moviment_to_battle(player)
        self.__update_domination_turns(player)
